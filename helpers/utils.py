from django.core.cache import cache


def delete_substring_from_redis(key, substring):
    lua_script = """
    local value = redis.call('GET', KEYS[1])
    if value then
        value = string.gsub(value, ARGV[1], "")
        redis.call('SET', KEYS[1], value)
    end
    """

    cache.eval(lua_script, 1, key, substring)
