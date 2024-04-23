import casbin
import casbin_redis_adapter.adapter

from configs import REDIS_HOST, REDIS_PASSWORD, REDIS_PORT, REDIS_USERNAME

adapter = casbin_redis_adapter.adapter.Adapter(
    host=REDIS_HOST, port=REDIS_PORT, username=REDIS_USERNAME, password=REDIS_PASSWORD)

abac_enforcer = casbin.Enforcer('./configs/abac.conf', adapter)
abac_enforcer.enable_auto_save(True)

abac_enforcer.add_policy('True', '/user/me', 'read')
abac_enforcer.add_policy('True', '/user/me', 'write')
