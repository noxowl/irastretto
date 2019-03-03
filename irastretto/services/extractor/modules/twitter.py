""":mod:'irastretto.services.extractor.modules.twitter'

"""
import re
from lxml import etree

from quart import g

from . import Extractor, ExtractorReceipt, ExtractData

# https://twitter.com/HistoryToLearn/status/1098772996372672512


class Twitter(Extractor):
    _identity = "(https?:\/\/(.+?\.)?{0}(\/[A-Za-z0-9\-\._~:\/\?#\[\]@!$&'\(\)\*\+,;\=]*)?)" \
                .format('twitter.com')

    def __init__(self):
        print('init twitter module')
        self.source = {}
        self.receipt = None

    def init(self, source):
        self.source = source

    def awake(self):
        self.prepare(self.source['source'])

    def start(self):
        if self.receipt:
            self.extract()

    def prepare(self, source_url: str) -> None:
        """Prepare receipt.

        :param source_url: URL for extract
        :return: None
        """
        if self._is_twitter(source_url):
            target_url = self.protocol_cutoff(source_url)
            if self._is_desktop_url(source_url):
                target_url = self._convert_to_mobile_url(target_url)
            print(target_url)
            self.receipt = ExtractorReceipt(
                task_id='',
                target_url=target_url,
                request_from='anon_user'
            )

    def _is_twitter(self, source_url: str) -> bool:
        return True if 'twitter.com' in source_url else False

    def _is_desktop_url(self, source_url: str) -> bool:
        return True if not re.match(
            "^(mobile\.|m\.)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$",
            source_url) else False

    def _convert_to_mobile_url(self, target_url: str) -> str:
        return 'mobile.' + target_url

    def extract(self) -> None:
        """Extract media and metadata from target url.

        :return:
        """
        if self.receipt:
            self._extract(self.receipt.target_url)

    def _extract(self, target_url: str):
        _raw = self.get_raw_content('https://' + target_url,
                                    verbose=True,
                                    )
        ext = self._parser(_raw)
        print(ext.__dict__)
        for path in ext.get('content_path'):
            ext.add('content',
                    self.__get_twitter_original_image(path))

    def _parser(self, raw_tweet) -> ExtractData:
        """Parse legacy twitter mobile web(NoJS).
        It extract only 1 image per parse.

        :param raw_tweet: a raw tweet page.
        :return:
        """
        ext = ExtractData()
        if raw_tweet:
            try:
                parser = etree.HTMLParser(encoding='utf-8')
                tree = etree.fromstring(raw_tweet, parser=parser)
                root = tree.xpath("/html/body"
                                  "/div[@id='container']"
                                  "/div[@id='main_content']"
                                  "/div[@id='main-content']"
                                  "/div[@class='main-tweet-container']"
                                  "/table[@class='main-tweet']")
                ext.add('username', self.__get_username(root[0][0][1]))
                ext.add('data_id', self.__get_data_id(root[0][1][0]))
                ext.add('alt', self.__get_alt(root[0][1][0]))
                ext.add('content_path', self.__get_media_path(root[0][1][0]))
            except Exception as e:
                print(e)
        return ext

    def __get_ext_from_iterator(self, root: etree._Element, ext: ExtractData) -> ExtractData:
        """Get a extract data with etree elements loop.
        Discontinued method.

        :param etree._Element root: etree element root
                                    (Twitter nojs mobile page <table>).
        :param ExtractData ext: extract data object.
        :return: extract data.
        """
        for row in root[0].getchildren():
            for c in row:
                if c.attrib['class'] == 'user-info':
                    ext.add('username', self.__get_username(c))
                elif c.attrib['class'] == 'tweet-content':
                    ext.add('data_id', self.__get_data_id(c))
                    ext.add('alt', self.__get_alt(c))
                    ext.add('content_path', self.__get_media_path(c))
                    if ext.get('username'):
                        break
        return ext

    def __get_username(self, element: etree._Element) -> str:
        username = element.xpath("./a/span/text()")[1].replace('\n', '')
        username = re.sub(r"\s+$", "", username, flags=re.UNICODE)
        return username

    def __get_data_id(self, element: etree._Element) -> str:
        data_id = element.xpath("./div[@class='tweet-text']")[0] \
                         .attrib['data-id']
        return data_id

    def __get_alt(self, element: etree._Element) -> str:
        alt = element.xpath("./div[@class='tweet-text']"
                            "/div[@class='dir-ltr']"
                            "/text()")[0]
        alt = re.sub("^\s+|\s+$", "", alt, flags=re.UNICODE)
        return alt

    def __get_media_path(self, element: etree._Element) -> str:
        return self.__get_media_image_path(element)

    def __get_media_image_path(self, element: etree._Element) -> str:
        image_path = element.xpath("./div[@class='card-photo']"
                                   "/div[@class='media']"
                                   "/img/@src")[0]
        image_path = re.sub(r"(?<=:)\w+", "orig", image_path)
        return image_path

    def __get_twitter_original_image(self, image_path):
        data = self.get_raw_content(image_path,
                                    verbose=True)
        return data
