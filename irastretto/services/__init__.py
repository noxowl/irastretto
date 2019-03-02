""":mod:'irastretto.services'

"""
from quart import g


def info() -> dict:
    """Return current status.

    :return: status data
    """
    service_info = {
        'version': 'v1',  # g.config.version
        'queue_health': 'good',  # RabbitMQ status
        'disk_health': 'good',  # Media space capability or availability
        'network_health': 'good'  # Network status
    }
    return service_info
