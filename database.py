import sqlite3
import hashlib
import os
from datetime import datetime

DATABASE_FILE = 'users.db'

def get_db_connection():
    """获取数据库连接"""
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    """初始化数据库和表结构"""
    conn = get_db_connection()
    
    # 创建用户表
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def hash_password(password):
    """对密码进行哈希加密"""
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(email, password):
    """创建新用户"""
    conn = get_db_connection()
    password_hash = hash_password(password)
    
    try:
        conn.execute(
            'INSERT INTO users (email, password_hash) VALUES (?, ?)',
            (email, password_hash)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False  # 邮箱已存在
    finally:
        conn.close()

def verify_user(email, password):
    """验证用户登录"""
    conn = get_db_connection()
    password_hash = hash_password(password)
    
    user = conn.execute(
        'SELECT * FROM users WHERE email = ? AND password_hash = ?',
        (email, password_hash)
    ).fetchone()
    
    if user:
        # 更新最后登录时间
        conn.execute(
            'UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?',
            (user['id'],)
        )
        conn.commit()
    
    conn.close()
    return user is not None

def get_user_by_email(email):
    """根据邮箱获取用户信息"""
    conn = get_db_connection()
    user = conn.execute(
        'SELECT id, email, created_at, last_login FROM users WHERE email = ?',
        (email,)
    ).fetchone()
    conn.close()
    return user

def init_default_user():
    """初始化默认用户"""
    default_email = 'v530026236@mail.uic.edu.cn'
    default_password = '123456'
    
    # 检查默认用户是否已存在
    if not get_user_by_email(default_email):
        create_user(default_email, default_password)
        print(f"默认用户已创建: {default_email}")
    else:
        print(f"默认用户已存在: {default_email}")

if __name__ == '__main__':
    # 初始化数据库
    init_database()
    init_default_user()
    print("数据库初始化完成！")