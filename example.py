#
# example.py
# @author Sidharth Mishra
# @website sidmishraw.github.io
# @description An example usage of schema-to-example.
# @created 2019-05-27T20:03:51.102Z-07:00
# @last-modified 2019-05-27T20:05:53.053Z-07:00
#


from app import generate_example
from json import loads, dumps

with open("test-1.schema.json", 'r') as f:
    s = f.read()
    ss = loads(s)
    a = generate_example(ss)
    with open("test-1.json", 'w') as w:
        w.write(dumps(a.value))

with open("test-2.schema.json", 'r') as f:
    s = f.read()
    ss = loads(s)
    a = generate_example(ss)
    with open("test-2.json", 'w') as w:
        w.write(dumps(a.value))
