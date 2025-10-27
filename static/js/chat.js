// 聊天功能JavaScript代码

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    scrollToBottom();
    document.getElementById('messageInput').focus();
});

// 发送消息函数
async function sendMessage() {
    const messageInput = document.getElementById('messageInput');
    const sendButton = document.getElementById('sendButton');
    const message = messageInput.value.trim();
    
    if (!message) {
        return;
    }
    
    // 禁用输入和按钮
    messageInput.disabled = true;
    sendButton.disabled = true;
    
    // 显示发送按钮加载状态
    showSendButtonLoading();
    
    // 添加用户消息到界面
    addMessageToChat('user', message);
    
    // 清空输入框
    messageInput.value = '';
    
    try {
        // 发送请求到后端
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // 流式显示机器人回复
            await streamBotResponse(data.response, data.token_usage);
        } else {
            // 显示错误消息
            addErrorMessage(data.error || '发生未知错误');
        }
        
    } catch (error) {
        console.error('Error:', error);
        addErrorMessage('网络连接错误，请稍后重试');
    } finally {
        // 隐藏发送按钮加载状态
        hideSendButtonLoading();
        
        // 重新启用输入和按钮
        messageInput.disabled = false;
        sendButton.disabled = false;
        messageInput.focus();
    }
}

// 创建机器人消息容器
function createBotMessageContainer() {
    const chatMessages = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot-message';
    
    const now = new Date();
    const timestamp = now.toISOString().slice(0, 19).replace('T', ' ');
    
    messageDiv.innerHTML = `
        <div class="message-content">
            <div class="message-text"></div>
            <div class="message-time">
                ${timestamp}
                <span class="token-usage" style="display: none;"></span>
            </div>
        </div>
    `;
    
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
    
    return messageDiv;
}

// 流式显示机器人回复
async function streamBotResponse(fullResponse, tokenUsage = null) {
    // 在第一个字符出现时才创建消息容器
    let messageDiv = null;
    let messageTextDiv = null;
    let tokenUsageSpan = null;
    
    // 模拟打字机效果的流式显示
    const words = fullResponse.split('');
    let currentText = '';
    
    for (let i = 0; i < words.length; i++) {
        // 第一个字符时创建消息容器
        if (i === 0) {
            messageDiv = createBotMessageContainer();
            messageTextDiv = messageDiv.querySelector('.message-text');
            tokenUsageSpan = messageDiv.querySelector('.token-usage');
        }
        
        currentText += words[i];
        messageTextDiv.textContent = currentText;
        
        // 添加光标效果
        if (i < words.length - 1) {
            messageTextDiv.innerHTML = escapeHtml(currentText) + '<span class="typing-cursor">|</span>';
        } else {
            messageTextDiv.innerHTML = escapeHtml(currentText);
        }
        
        // 滚动到底部
        scrollToBottom();
        
        // 控制打字速度（可调整）
        await new Promise(resolve => setTimeout(resolve, 30));
    }
    
    // 显示token使用信息
    if (tokenUsage && tokenUsageSpan) {
        tokenUsageSpan.textContent = `Token: ${tokenUsage}`;
        tokenUsageSpan.style.display = 'inline';
    }
    
    // 最终滚动到底部
    scrollToBottom();
}
function addMessageToChat(type, content, tokenUsage = null) {
    const chatMessages = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}-message`;
    
    const now = new Date();
    const timestamp = now.toISOString().slice(0, 19).replace('T', ' ');
    
    let tokenInfo = '';
    if (type === 'bot' && tokenUsage) {
        tokenInfo = `<span class="token-usage">Token: ${tokenUsage}</span>`;
    }
    
    messageDiv.innerHTML = `
        <div class="message-content">
            <div class="message-text">${escapeHtml(content)}</div>
            <div class="message-time">
                ${timestamp}
                ${tokenInfo}
            </div>
        </div>
    `;
    
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

// 添加错误消息
function addErrorMessage(error) {
    const chatMessages = document.getElementById('chatMessages');
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = `错误: ${error}`;
    chatMessages.appendChild(errorDiv);
    scrollToBottom();
}

// 处理回车键发送
function handleKeyPress(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

// 清除聊天历史
async function clearHistory() {
    if (!confirm('确定要清除所有聊天记录吗？')) {
        return;
    }
    
    try {
        const response = await fetch('/clear_history', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            // 清空聊天界面
            document.getElementById('chatMessages').innerHTML = '';
            showNotification('聊天记录已清除', 'success');
        } else {
            showNotification('清除失败，请重试', 'error');
        }
        
    } catch (error) {
        console.error('Error:', error);
        showNotification('网络错误，请重试', 'error');
    }
}

// 滚动到底部
function scrollToBottom() {
    const chatMessages = document.getElementById('chatMessages');
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// 显示发送按钮加载状态
function showSendButtonLoading() {
    const sendButton = document.getElementById('sendButton');
    sendButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> 发送中...';
}

// 隐藏发送按钮加载状态
function hideSendButtonLoading() {
    const sendButton = document.getElementById('sendButton');
    sendButton.innerHTML = '<i class="fas fa-paper-plane"></i> 发送';
}

// HTML转义函数
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// 显示通知
function showNotification(message, type = 'info') {
    // 创建通知元素
    const notification = document.createElement('div');
    notification.className = `alert alert-${type === 'success' ? 'success' : 'danger'} alert-dismissible fade show`;
    notification.style.position = 'fixed';
    notification.style.top = '20px';
    notification.style.right = '20px';
    notification.style.zIndex = '10000';
    notification.style.minWidth = '300px';
    
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // 3秒后自动移除
    setTimeout(() => {
        if (notification.parentNode) {
            notification.parentNode.removeChild(notification);
        }
    }, 3000);
}

// 自动调整输入框高度
function autoResizeTextarea(textarea) {
    textarea.style.height = 'auto';
    textarea.style.height = textarea.scrollHeight + 'px';
}

// 格式化时间戳
function formatTimestamp(timestamp) {
    const date = new Date(timestamp);
    return date.toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    });
}

// 检查网络连接
function checkConnection() {
    return navigator.onLine;
}

// 网络状态监听
window.addEventListener('online', function() {
    showNotification('网络连接已恢复', 'success');
});

window.addEventListener('offline', function() {
    showNotification('网络连接已断开', 'error');
});

// 防抖函数
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// 节流函数
function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    }
}