# 下面两个枚举 请勿删除
class SQL_INJECT_TYPE:
  # 时间盲注
  SLEEP_INJECT              = 'SQL_BOOLEAN_INJECT'
  # 布尔注入
  BOOLEAN_INJECT            = 'SQL_SLEEP_INJECT'
  # 布尔注入（无列名注入版本）
  BOOLEAN_INJECT_NOT_COLUMN = 'SQL_BOOLEAN_INJECT_NOT_COLUMN'

class SQL_TYPE:
  GET_SCHEMATA_LEN_SQL      = 'GET_SCHEMATA_LEN_SQL'
  GET_SCHEMATA_VALUE_SQL    = 'GET_SCHEMATA_VALUE_SQL'
  GET_TABLES_LEN_SQL        = 'GET_TABLES_LEN_SQL'
  GET_TABLES_VALUE_SQL      = 'GET_TABLES_VALUE_SQL'
  GET_COLUMNS_LEN_SQL       = 'GET_COLUMNS_LEN_SQL'
  GET_COLUMNS_VALUE_SQL     = 'GET_COLUMNS_VALUE_SQL'
  GET_DATA_LEN_SQL          = 'GET_DATA_LEN_SQL'
  GET_DATA_VALUE_SQL        = 'GET_DATA_VALUE_SQL'

