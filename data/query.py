import sqlite3
import json
from pathlib import Path

# 数据库配置
DATABASE_PATHS = {
    "chinook": "data/Chinook.db"
}


def dict_factory(cursor, row):
    """将查询结果转换为字典格式"""
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}


def get_db_connection(database, use_dict_factory=True):
    """获取数据库连接
    Args:
        database: 数据库名称
        use_dict_factory: 是否使用dict_factory作为row_factory
    """
    if database not in DATABASE_PATHS:
        raise ValueError(f"未知数据库: {database}")

    db_path = Path(DATABASE_PATHS[database])
    if not db_path.exists():
        raise FileNotFoundError(f"数据库文件不存在: {db_path}")

    conn = sqlite3.connect(str(db_path))
    if use_dict_factory:
        conn.row_factory = dict_factory
    return conn


def execute_query(query, database="chinook"):
    """执行SQL查询
    Args:
        query: SQL查询语句
        database: 数据库名称，默认为chinook
    Returns:
        查询结果的JSON字符串
    """
    try:
        with get_db_connection(database) as conn:
            # 添加LIMIT子句以防止返回过多数据
            if 'limit' not in query.lower() and 'select' in query.lower():
                query = f"{query} LIMIT 100"

            cursor = conn.execute(query)
            results = cursor.fetchall()

            # 转换为JSON字符串
            result_str = json.dumps(results, ensure_ascii=False, default=str)

            # 添加查询统计信息
            stats = f"\n--- 查询返回 {len(results)} 条记录 ---"
            return result_str + stats

    except Exception as e:
        return f"SQL查询出错: {str(e)}"


def get_table_names(conn):
    """Return a list of table names."""
    tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
    return [table['name'] for table in tables.fetchall()]


def get_column_names(conn, table_name):
    """Return a list of column names."""
    columns = conn.execute(f"PRAGMA table_info('{table_name}');")
    return [col['name'] for col in columns.fetchall()]


def get_database_info(conn):
    """Return a list of dicts containing the table name and columns for each table in the database."""
    table_dicts = []
    for table_name in get_table_names(conn):
        columns_names = get_column_names(conn, table_name)
        table_dicts.append(
            {"table_name": table_name, "column_names": columns_names})
    return table_dicts


def get_database_schema_string(database="chinook"):
    """获取数据库schema的字符串描述"""
    with get_db_connection(database) as conn:
        database_schema_dict = get_database_info(conn)
        return "\n".join(
            [
                f"Table: {table['table_name']}\nColumns: {', '.join(table['column_names'])}"
                for table in database_schema_dict
            ]
        )
