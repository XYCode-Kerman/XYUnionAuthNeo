import casbin
import casbin_redis_adapter.adapter
from casbin_redis_watcher import WatcherOptions, new_watcher

from configs import REDIS_HOST, REDIS_PASSWORD, REDIS_PORT, REDIS_USERNAME

adapter = casbin_redis_adapter.adapter.Adapter(
    host=REDIS_HOST, port=REDIS_PORT, username=REDIS_USERNAME, password=REDIS_PASSWORD)

abac_enforcer = casbin.Enforcer('./configs/abac.conf', adapter)


def set_watcher():
    def callback(event):
        abac_enforcer.load_policy()

    options = WatcherOptions()
    options.host = REDIS_HOST
    options.port = REDIS_PORT
    options.username = REDIS_USERNAME
    options.password = REDIS_PASSWORD

    watcher = new_watcher(options)
    watcher.set_update_callback(callback)
    abac_enforcer.set_watcher(watcher)


set_watcher()

abac_enforcer.enable_auto_save(True)

abac_enforcer.add_policy('True', '/user/me', 'read')
abac_enforcer.add_policy('True', '/user/me', 'write')
