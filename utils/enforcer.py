import casbin
import casbin_redis_adapter.adapter

from config import REDIS_HOST, REDIS_PASSWORD, REDIS_PORT

adapter = casbin_redis_adapter.adapter.Adapter(
    host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)
enforcer = casbin.Enforcer('config/casbin.conf', adapter, True)
