"""工具:查询组织数据库(Text-to-SQL)"""
import json
import sqlite3

from langchain_core.tools import tool

from app.org_db import get_connection

@tool
def query_org_db(sql:str) -> str:
    """查询公司组织信息数据库(员工,部门)

    数据库结构:
    - departments 部门表:id(部门ID)、name(部门名称)
    - employees 员工表:id(员工ID)、name(姓名)、department_id(所属部门ID,关联 departments.id)、
      title(职级,如 P5~P9)、manager_id(直接上级员工ID,关联 employees.id)、skills(技能,逗号分隔,如 "Python,SQL")

    请先把用户问题翻译成 SQLite 的 SELECT 语句,再调用本工具。
    入参 sql:合法的 SQLite SELECT 查询语句(只读,禁止 INSERT/UPDATE/DELETE)。
    """

    if not sql.strip().upper().startswith("SELECT"):
        return "只允许执行SELECT语句"

    conn = get_connection()
    try:
        rows = conn.execute(sql).fetchall()
        return json.dumps([dict(row) for row in rows], ensure_ascii=False)
    except sqlite3.Error as e:
        return f"SQL 执行出错:{e}。请检查 SQL 语句后重试。"
    finally:
        conn.close()