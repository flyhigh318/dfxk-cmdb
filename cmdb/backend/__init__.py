import logging
class _NullHandler(logging.Handler):
    def emit(self, record):
        pass

# LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
# logging.basicConfig(filename='celery_backend.log', level=logging.DEBUG, format=LOG_FORMAT)


logger = logging.getLogger(__name__).addHandler(_NullHandler())



from .saltstack.salt_master import *
from .saltstack.saltstackapi import *
from .zabbix.base_class import *
from .zabbix.api import *
from .zabbix.graph import *
from .zabbix.triggers import *
from .zabbix.hosts import *

