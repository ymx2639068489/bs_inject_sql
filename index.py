import get_tables
import sys
from config import set_url, set_inject_type
from myEnum import SQL_INJECT_TYPE
def get_argv():
  list = sys.argv
  for i in range(1, len(list), 2):
    if list[i] == '-u':
      # print(list[i + 1])
      set_url(list[i + 1])
    if list[i] == '-t':
      # print(list[i + 1])
      if list[i + 1] == 'b' or list[i + 1] == 'B':
        set_inject_type(SQL_INJECT_TYPE.BOOLEAN_INJECT)
      if list[i + 1] == 's' or list[i + 1] == 'S':
        set_inject_type(SQL_INJECT_TYPE.SLEEP_INJECT)
      if list[i + 1] == 'bnc' or list[i + 1] == 'BNC':
        set_inject_type(SQL_INJECT_TYPE.BOOLEAN_INJECT_NOT_COLUMN)
    if list[i] == '-h':
      print("""
1. -u, set url
2. -t, set inject type
  b   -> boolean inject
  bnc -> boolean inject(not columns)
  s   -> sleep inject""")
      return
  
  
  

if __name__ == '__main__':
  get_argv()
  get_tables.run()
