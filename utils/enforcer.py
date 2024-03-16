import casbin
import casbin_redis_adapter.adapter

from config import REDIS_HOST, REDIS_PASSWORD, REDIS_PORT

adapter = casbin_redis_adapter.adapter.Adapter(
    host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)
enforcer = casbin.Enforcer('config/casbin.conf', adapter, True)
enforcer.enable_auto_save(True)

# 自动配置初始权限
if adapter.client.get('policy_init') is None:
    enforcer.add_policies(
        [
            ['r.sub.user.role == "application"',
                "xyunionauth.application.token", "read"],
            ['r.sub.user.role == "application"',
                "xyunionauth.application", "read"],
        ]
    )

    enforcer.save_policy()

    adapter.client.set('policy_init', 1)
