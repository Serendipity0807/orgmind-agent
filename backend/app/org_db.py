"""组织数据库:建表、灌示例数据、提供连接"""
import sqlite3

from app.config import ORG_DB


def get_connection():
    """打开数据库连接(查询结果可用列名取值)"""
    conn = sqlite3.connect(ORG_DB)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """建表 + 灌示例数据(可重复执行:先删后建)"""
    conn = get_connection()
    cur = conn.cursor()
    cur.executescript(
        """
        DROP TABLE IF EXISTS employees;
        DROP TABLE IF EXISTS departments;

        CREATE TABLE departments (
            id   INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        );

        CREATE TABLE employees (
            id            INTEGER PRIMARY KEY,
            name          TEXT NOT NULL,
            department_id INTEGER NOT NULL REFERENCES departments(id),
            title         TEXT NOT NULL,
            manager_id    INTEGER REFERENCES employees(id),
            skills        TEXT
        );
        """
    )

    departments = [
        (1, "技术部"),
        (2, "产品部"),
        (3, "市场部"),
        (4, "人事部"),
        (5, "财务部"),
    ]

    employees = [
        # (id, 姓名, 部门, 职级, 上级, 技能)
        (1, "王建国", 1, "P9", None, "管理,架构"),
        (2, "李娜",   1, "P8", 1, "Python,后端"),
        (3, "张三",   1, "P7", 2, "Python,SQL"),
        (4, "刘洋",   1, "P6", 2, "前端,Vue"),
        (5, "陈静",   1, "P6", 3, "Python,测试"),
        (6, "杨帆",   1, "P5", 3, "Python"),
        (7, "赵敏",   2, "P8", 1, "产品设计,用户研究"),
        (8, "孙磊",   2, "P6", 7, "数据分析,SQL"),
        (9, "周杰",   3, "P7", 1, "市场推广,文案"),
        (10, "吴倩",  3, "P6", 9, "新媒体,视频剪辑"),
        (11, "郑洁",  4, "P7", 1, "招聘,HR"),
        (12, "冯涛",  5, "P7", 1, "会计,财务分析"),
    ]

    cur.executemany("INSERT INTO departments VALUES (?, ?)", departments)
    cur.executemany("INSERT INTO employees VALUES (?, ?, ?, ?, ?, ?)", employees)
    conn.commit()
    conn.close()
    print(f"组织数据库初始化完成:{ORG_DB}")


if __name__ == "__main__":
    init_db()
