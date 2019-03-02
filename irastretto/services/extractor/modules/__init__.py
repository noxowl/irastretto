""":mod:'irastretto.services.extractor.modules'

"""
import re
import requests


def __load_submodules():
    # TODO: auto import
    from .twitter import Twitter


class ExtractorReceipt(object):
    def __init__(self, task_id, target_url, request_from):
        self.task_id = task_id
        self.target_url = target_url
        self.request_from = request_from


class ExtractData(object):
    def __init__(self):
        self.username = None
        self.content = None
        self.content_path = None
        self.alt = None
        self.data_id = None

    def add(self, key: str, value):
        setattr(self, key, value)

    def get(self, key):
        if hasattr(self, key):
            return getattr(self, key)
        return None


class Extractor:
    plugins = []
    _identity = ''

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.plugins.append(cls())

    def init(self, source: dict):
        """Init module data.

        :param dict source:
        :return: None
        """
        pass

    def awake(self):
        """Prepare Module. It must be set self.receipt.

        :return: None
        """
        pass

    def start(self):
        """Run extract task. It will load from service queue.

        :return: None
        """
        pass

    @property
    def regex(self):
        return re.compile(self._identity)

    @staticmethod
    def _is_duplicated(data_id: str):
        """Check is request duplicated.

        :param data_id:
        :return: It duplicated or not
        """
        return False

    @staticmethod
    def protocol_cutoff(source_url: str) -> str:
        """Cutoff url protocol.

        :param str source_url:
        :return: url string
        """
        return re.sub(r"https?://(www\.)?", "", source_url)

    @staticmethod
    def get_raw_content(target_url: str, manual: bool=False, verbose: bool=False, **kwargs):
        """Get bytes from target url.

        :param target_url:
        :param bool manual: using requests.Session()
        :param bool verbose: show detail of request and response
        :return: response bytes
        """
        try:
            if manual:
                s = requests.Session()
                req = requests.Request('GET', target_url)
                prepped = req.prepare()
                if 'headers' in kwargs:
                    req.headers.update(kwargs['headers'])
                r = s.send(prepped)
            else:
                r = requests.get(target_url)
            if verbose:
                print('request to: {0}'.format(target_url))
                print('request headers:\n{0}'.format(r.request.headers))
                print('response headers:\n{0}'.format(r.headers))
                print('response size: {0}kb'.format(round(len(r.text.encode('utf-8')) / 1000)))
            return r.content
        except requests.exceptions.BaseHTTPError:
            pass


__load_submodules()
