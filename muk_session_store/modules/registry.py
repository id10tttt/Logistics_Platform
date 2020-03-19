#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from odoo.tools import lazy_property
import logging
import odoo
from ..tools.redis_cache import RedisLRU
import redis
from odoo.modules.registry import Registry

REDIS_URL = 'redis://@localhost:6379/1'
_logger = logging.getLogger(__name__)


# class Registry_inherit(Mapping):
#
@lazy_property
def cache(self):
    try:
        r = redis.StrictRedis.from_url(odoo.tools.config['ormcache_redis_url'])
    except Exception as e:
        r = redis.StrictRedis.from_url(REDIS_URL)
    db_name = self.db_name
    return RedisLRU(r, db_name)


Registry.cache = cache
