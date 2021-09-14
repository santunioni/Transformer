import ujson


def ujson_dumps(data, default, **dumps_kwargs):
    return ujson.dumps(data, ensure_ascii=False)