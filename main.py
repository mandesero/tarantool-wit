from tarantool.imports import box, msgpack
import json
from typing import Any

def encode(obj: Any):
    return msgpack.encode(json.dumps(obj).encode('utf-8'))

def decode(data: bytes):
    decoded_json_string = msgpack.decode(data).decode('utf-8')
    return json.loads(decoded_json_string)

space: box.Space = box.Space.find("test_space")
index: box.Index = space.index("primary")

tup: box.BoxTuple = box.BoxTuple(encode([1, "Alice", 25]))
space.insert(tup.to_vec())

key: bytes = encode([1])
ops: bytes = encode([["=", 2, 26]])
tup = index.update(key, ops)
print(f"Updated tuple {decode(tup.to_vec())}")
