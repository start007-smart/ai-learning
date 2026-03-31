"""
MySQL 数据库查询示例
演示如何连接本地 MySQL 数据库，查询 wukong.wk_admin_menu 表的数据
"""

import mysql.connector
from mysql.connector import Error


# ============================================================
# 数据库连接配置
# ============================================================
DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "database": "wukong",
    "user": "root",
    "password": "",          # 无密码，保持空字符串
    "charset": "utf8mb4",
    "use_unicode": True,
}


def get_connection():
    """创建并返回数据库连接"""
    conn = mysql.connector.connect(**DB_CONFIG)
    return conn


def query_menu_list():
    """查询 wk_admin_menu 表中所有数据"""
    sql = "SELECT * FROM wk_admin_menu ORDER BY menu_id ASC"

    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)   # dictionary=True 结果以字典形式返回
        cursor.execute(sql)
        rows = cursor.fetchall()
        return rows
    except Error as e:
        print(f"❌ 查询失败：{e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def print_menu_tree(menus: list, parent_id: int = 0, indent: int = 0):
    """
    递归打印菜单树形结构
    :param menus:     所有菜单列表
    :param parent_id: 当前父级 ID
    :param indent:    缩进层级
    """
    prefix = "  " * indent + ("└─ " if indent > 0 else "")
    for m in menus:
        pid = m.get("parent_id") or 0
        if pid == parent_id:
            name = m.get("menu_name") or "-"
            mid  = m.get("menu_id", "?")
            path = m.get("realm") or m.get("realm_url") or ""
            print(f"{prefix}[{mid}] {name}  {path}")
            print_menu_tree(menus, mid, indent + 1)


def main():
    print("=" * 60)
    print("  MySQL 查询示例 · wukong.wk_admin_menu")
    print("=" * 60)

    # 1. 查询数据
    menus = query_menu_list()

    if not menus:
        print("⚠️  未查询到任何菜单数据，请确认表中是否有记录。")
        return

    total = len(menus)
    print(f"\n✅ 共查询到 {total} 条菜单记录\n")

    # 2. 打印原始字段（以第一条为参考，展示所有列名）
    print("【字段列表】")
    print("  " + " | ".join(menus[0].keys()))
    print()

    # 3. 打印前 5 条明细（格式化输出）
    print("【前 5 条数据明细】")
    print("-" * 60)
    for row in menus[:5]:
        for key, val in row.items():
            print(f"  {key:<20}: {val}")
        print("-" * 60)

    # 4. 尝试以树形结构展示菜单层级
    print("\n【菜单树形结构】")
    print_menu_tree(menus)

    print("\n✔  查询完毕")


if __name__ == "__main__":
    main()
