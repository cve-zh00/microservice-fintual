from blacksheep.settings.json import json_settings
import orjson

def serialize(value) -> str:
    return orjson.dumps(value).decode("utf8")

json_settings.use(
    loads=orjson.loads,
    dumps=serialize,
)
