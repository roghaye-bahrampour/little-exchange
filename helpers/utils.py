import redis
from django.conf import settings

redis_client = redis.Redis(host=settings.REDIS_HOST, port=6379, db=settings.REDIS_PORT)


def delete_substring_from_redis(key, substring):
    # TODO: this script needs to be fixed
    lua_script = """
    local value = redis.call('GET', KEYS[1])
    if value then
        value = string.gsub(value, ARGV[1], "")
        redis.call('SET', KEYS[1], value)
    end
    """

    redis_client.eval(lua_script, 1, key, substring)
