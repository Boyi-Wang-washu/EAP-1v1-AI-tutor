import os
import json
import uuid
import time
from datetime import datetime
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_cors import CORS
from cozepy import Coze, TokenAuth, Message, ChatEventType, COZE_CN_BASE_URL
from functools import wraps
from database import init_database, init_default_user, verify_user, get_user_by_email

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'your-secret-key-change-this')  # 从环境变量读取

# 启用 CORS - 允许 Next.js 前端调用
CORS(app, 
     resources={r"/api/*": {"origins": [
         "http://localhost:3000",
         "http://127.0.0.1:3000",
         "https://cansolve-eap-agent-web.vercel.app"
     ]}},
     supports_credentials=True,
     allow_headers=["Content-Type", "X-User-ID"],
     methods=["GET", "POST", "OPTIONS"]
)

# 配置 - 支持从环境变量读取（生产环境）
COZE_API_TOKEN = os.getenv('COZE_API_TOKEN', "sat_G9soTeMGzMr6oOmfwSdx80P1mGNCPJ3c7pFOLIyqPvajlvJyOFp5UyBedtgzXQ7s")
BOT_ID = os.getenv('BOT_ID', "7565215004040527912")

# 初始化 Coze 客户端
coze = Coze(auth=TokenAuth(COZE_API_TOKEN), base_url=COZE_CN_BASE_URL)

# 登录验证装饰器
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_email' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# 聊天记录存储文件
CHAT_HISTORY_FILE = 'chat_history.json'

def load_chat_history():
    """加载聊天记录"""
    if os.path.exists(CHAT_HISTORY_FILE):
        try:
            with open(CHAT_HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}
    return {}

def save_chat_history(history):
    """保存聊天记录"""
    with open(CHAT_HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def get_user_id():
    """获取或创建用户ID - 支持从 Next.js 传来的用户ID"""
    # 优先从请求头获取用户 ID（Next.js 调用时使用）
    user_id_from_header = request.headers.get('X-User-ID')
    if user_id_from_header:
        return user_id_from_header
    
    # 兼容原有的 session 方式（直接访问 Flask 页面时使用）
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
    return session['user_id']

def create_conversation(user_id):
    """通过Coze API创建新的对话"""
    try:
        # 使用Coze API创建对话
        response = coze.conversations.create(
            bot_id=BOT_ID,
            user_id=user_id
        )
        return response.id
    except Exception as e:
        print(f"创建对话失败: {e}")
        return None

def get_conversation_id():
    """获取当前会话的对话ID"""
    return session.get('conversation_id')

# 登录页面
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            flash('请输入邮箱和密码', 'error')
            return render_template('login.html')
        
        if verify_user(email, password):
            session['user_email'] = email
            flash('登录成功！', 'success')
            return redirect(url_for('index'))
        else:
            flash('邮箱或密码错误', 'error')
            return render_template('login.html')
    
    # 如果已经登录，直接跳转到主页
    if 'user_email' in session:
        return redirect(url_for('index'))
    
    return render_template('login.html')

# 退出登录
@app.route('/logout')
def logout():
    session.pop('user_email', None)
    flash('已退出登录', 'info')
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    """主页面"""
    user_email = session.get('user_email')
    user_info = get_user_by_email(user_email)
    user_id = get_user_id()
    chat_history = load_chat_history()
    user_messages = chat_history.get(user_id, [])
    return render_template('index.html', messages=user_messages, user_info=user_info)

@app.route('/chat', methods=['POST'])
@login_required
def chat():
    """处理聊天请求"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': '消息不能为空'}), 400
        
        user_id = get_user_id()
        
        # 加载聊天历史
        chat_history = load_chat_history()
        if user_id not in chat_history:
            chat_history[user_id] = []
        
        # 保存用户消息
        user_msg_record = {
            'id': str(uuid.uuid4()),
            'type': 'user',
            'content': user_message,
            'timestamp': datetime.now().isoformat()
        }
        chat_history[user_id].append(user_msg_record)
        
        # 调用Coze API获取回复
        bot_response = ""
        token_usage = 0
        conversation_id = get_conversation_id()
        
        # 如果没有conversation_id，先创建一个新的对话
        if not conversation_id:
            conversation_id = create_conversation(user_id)
            if conversation_id:
                session['conversation_id'] = conversation_id
        
        try:
            # 构建API调用参数
            chat_params = {
                'bot_id': BOT_ID,
                'user_id': user_id,
                'additional_messages': [
                    Message.build_user_question_text(user_message),
                ]
            }
            
            # 如果有conversation_id，添加到参数中
            if conversation_id:
                chat_params['conversation_id'] = conversation_id
            
            for event in coze.chat.stream(**chat_params):
                if event.event == ChatEventType.CONVERSATION_MESSAGE_DELTA:
                    bot_response += event.message.content
                
                if event.event == ChatEventType.CONVERSATION_CHAT_COMPLETED:
                    if hasattr(event.chat, 'usage') and hasattr(event.chat.usage, 'token_count'):
                        token_usage = event.chat.usage.token_count
                    # 如果之前没有conversation_id，保存API返回的conversation_id
                    if not session.get('conversation_id') and hasattr(event.chat, 'conversation_id'):
                        session['conversation_id'] = event.chat.conversation_id
        
        except Exception as e:
            error_msg = str(e)
            # 如果是conversation_id不存在的错误，清除无效的conversation_id并重试
            if "conversation_id" in error_msg and "does not exist" in error_msg:
                if 'conversation_id' in session:
                    del session['conversation_id']
                
                # 重新尝试不带conversation_id的请求
                try:
                    chat_params = {
                        'bot_id': BOT_ID,
                        'user_id': user_id,
                        'additional_messages': [
                            Message.build_user_question_text(user_message),
                        ]
                    }
                    
                    for event in coze.chat.stream(**chat_params):
                        if event.event == ChatEventType.CONVERSATION_MESSAGE_DELTA:
                            bot_response += event.message.content
                        
                        if event.event == ChatEventType.CONVERSATION_CHAT_COMPLETED:
                            if hasattr(event.chat, 'usage') and hasattr(event.chat.usage, 'token_count'):
                                token_usage = event.chat.usage.token_count
                            # 保存新的conversation_id
                            if hasattr(event.chat, 'id'):
                                session['conversation_id'] = str(event.chat.id)
                
                except Exception as retry_e:
                    bot_response = f"抱歉，我遇到了一些问题：{str(retry_e)}"
            else:
                bot_response = f"抱歉，我遇到了一些问题：{error_msg}"
        
        # 保存机器人回复
        bot_msg_record = {
            'id': str(uuid.uuid4()),
            'type': 'bot',
            'content': bot_response,
            'timestamp': datetime.now().isoformat(),
            'token_usage': token_usage
        }
        chat_history[user_id].append(bot_msg_record)
        
        # 保存到文件
        save_chat_history(chat_history)
        
        return jsonify({
            'success': True,
            'response': bot_response,
            'token_usage': token_usage,
            'message_id': bot_msg_record['id']
        })
        
    except Exception as e:
        return jsonify({'error': f'服务器错误：{str(e)}'}), 500

@app.route('/history')
def get_history():
    """获取聊天历史"""
    user_id = get_user_id()
    chat_history = load_chat_history()
    user_messages = chat_history.get(user_id, [])
    return jsonify({'messages': user_messages})

@app.route('/clear_history', methods=['POST'])
@login_required
def clear_history():
    """清除聊天历史"""
    try:
        user_id = get_user_id()
        chat_history = load_chat_history()
        if user_id in chat_history:
            chat_history[user_id] = []
            save_chat_history(chat_history)
        
        # 清除对话ID，开始新的对话
        if 'conversation_id' in session:
            del session['conversation_id']
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': f'清除历史失败：{str(e)}'}), 500

# ==================== API 端点 for Next.js ====================

@app.route('/api/health', methods=['GET'])
def api_health():
    """健康检查"""
    return jsonify({
        'status': 'ok',
        'message': 'EAP Teaching Assistant API is running'
    })

@app.route('/api/chat', methods=['POST', 'OPTIONS'])
def api_chat():
    """API: 发送消息并获取回复（供 Next.js 调用）"""
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': '消息不能为空'}), 400
        
        user_id = get_user_id()
        
        # 加载聊天历史
        chat_history = load_chat_history()
        if user_id not in chat_history:
            chat_history[user_id] = []
        
        # 保存用户消息
        user_msg_record = {
            'id': str(uuid.uuid4()),
            'type': 'user',
            'content': user_message,
            'timestamp': datetime.now().isoformat()
        }
        chat_history[user_id].append(user_msg_record)
        
        # 调用Coze API获取回复
        bot_response = ""
        token_usage = 0
        conversation_id = session.get('conversation_id')
        
        # 如果没有conversation_id，先创建一个新的对话
        if not conversation_id:
            conversation_id = create_conversation(user_id)
            if conversation_id:
                session['conversation_id'] = conversation_id
        
        try:
            # 构建API调用参数
            chat_params = {
                'bot_id': BOT_ID,
                'user_id': user_id,
                'additional_messages': [
                    Message.build_user_question_text(user_message),
                ]
            }
            
            # 如果有conversation_id，添加到参数中
            if conversation_id:
                chat_params['conversation_id'] = conversation_id
            
            for event in coze.chat.stream(**chat_params):
                if event.event == ChatEventType.CONVERSATION_MESSAGE_DELTA:
                    bot_response += event.message.content
                
                if event.event == ChatEventType.CONVERSATION_CHAT_COMPLETED:
                    if hasattr(event.chat, 'usage') and hasattr(event.chat.usage, 'token_count'):
                        token_usage = event.chat.usage.token_count
                    if not session.get('conversation_id') and hasattr(event.chat, 'conversation_id'):
                        session['conversation_id'] = event.chat.conversation_id
        
        except Exception as e:
            error_msg = str(e)
            if "conversation_id" in error_msg and "does not exist" in error_msg:
                if 'conversation_id' in session:
                    del session['conversation_id']
                
                # 重新尝试不带conversation_id的请求
                try:
                    chat_params = {
                        'bot_id': BOT_ID,
                        'user_id': user_id,
                        'additional_messages': [
                            Message.build_user_question_text(user_message),
                        ]
                    }
                    
                    for event in coze.chat.stream(**chat_params):
                        if event.event == ChatEventType.CONVERSATION_MESSAGE_DELTA:
                            bot_response += event.message.content
                        
                        if event.event == ChatEventType.CONVERSATION_CHAT_COMPLETED:
                            if hasattr(event.chat, 'usage') and hasattr(event.chat.usage, 'token_count'):
                                token_usage = event.chat.usage.token_count
                            if hasattr(event.chat, 'id'):
                                session['conversation_id'] = str(event.chat.id)
                
                except Exception as retry_e:
                    bot_response = f"抱歉，我遇到了一些问题：{str(retry_e)}"
            else:
                bot_response = f"抱歉，我遇到了一些问题：{error_msg}"
        
        # 保存机器人回复
        bot_msg_record = {
            'id': str(uuid.uuid4()),
            'type': 'bot',
            'content': bot_response,
            'timestamp': datetime.now().isoformat(),
            'token_usage': token_usage
        }
        chat_history[user_id].append(bot_msg_record)
        
        # 保存到文件
        save_chat_history(chat_history)
        
        return jsonify({
            'success': True,
            'response': bot_response,
            'token_usage': token_usage,
            'message_id': bot_msg_record['id']
        })
        
    except Exception as e:
        return jsonify({'error': f'服务器错误：{str(e)}'}), 500

@app.route('/api/history', methods=['GET', 'OPTIONS'])
def api_history():
    """API: 获取聊天历史（供 Next.js 调用）"""
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        user_id = get_user_id()
        chat_history = load_chat_history()
        user_messages = chat_history.get(user_id, [])
        return jsonify({
            'success': True,
            'messages': user_messages
        })
    except Exception as e:
        return jsonify({'error': f'获取历史失败：{str(e)}'}), 500

@app.route('/api/clear', methods=['POST', 'OPTIONS'])
def api_clear():
    """API: 清除聊天历史（供 Next.js 调用）"""
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        user_id = get_user_id()
        chat_history = load_chat_history()
        if user_id in chat_history:
            chat_history[user_id] = []
            save_chat_history(chat_history)
        
        # 清除对话ID
        if 'conversation_id' in session:
            del session['conversation_id']
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': f'清除历史失败：{str(e)}'}), 500

if __name__ == '__main__':
    # 初始化数据库
    init_database()
    init_default_user()
    
    app.run(debug=True, host='0.0.0.0', port=5000)