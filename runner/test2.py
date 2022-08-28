import RestrictedPython

source_code = """
from os import path
import base64
import sys

print(path.curdir)
print(base64.encode(''))
print(sys.path)
print('hello world!')
"""

loc = {}
# result = RestrictedPython.compile_restricted(source_code, '<inline>', 'exec')
# exec(result, RestrictedPython.safe_globals, loc)
result = RestrictedPython.compile_restricted_exec(source_code, '<inline>')
print(result)
# print(RestrictedPython.safe_globals)
