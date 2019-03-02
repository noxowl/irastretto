""":mod:'irastretto.services.extractor'

"""
from quart import g, abort
from marshmallow import Schema, fields

# from irastretto.celery import app as celery_app
from .modules import Extractor, ExtractorReceipt


class ExtractorCustomerReceipt(Schema):
    __schema_name__ = 'extractor_customer_receipt'

    request_from = fields.Str()


def extract(resource: dict) -> dict:
    """Request extract.

    :param dict resource:
    :return: customer receipt for request result.
    """
    worker = None
    for plugin in Extractor.plugins:
        if plugin.regex.match(resource['source']):
            worker = plugin
            break
    if not worker:
        abort(400)
    worker.init(resource)
    worker.awake()
    if not worker.receipt:
        abort(400)
    _extract(worker)
    return after_extract(worker.receipt)


# @celery_app.task
def _extract(worker) -> None:
    """Add task to celery queue.

    :param worker:
    :return: None
    """
    worker.start()


def after_extract(receipt: ExtractorReceipt) -> dict:
    """Make customer receipt for request result.

    :param ExtractorReceipt receipt:
    :return: a customer receipt.
    """
    _schema = ExtractorCustomerReceipt()
    dump, error = _schema.dump(receipt)
    if error:
        print(error)
    return dump
