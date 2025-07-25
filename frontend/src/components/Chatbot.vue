<template>
  <div>
    <div class="chatbot-icon" @click="toggleChat">
      <svg xmlns="http://www.w3.org/2000/svg" fill="white" viewBox="0 0 64 64" width="32" height="32">
        <path d="M32 4C17.64 4 6 15.64 6 30c0 7.73 3.88 14.56 9.88 19.04L16 60l10.96-5.88c1.56.28 3.16.44 4.96.44 14.36 0 26-11.64 26-26S46.36 4 32 4zm0 44c-9.94 0-18-8.06-18-18s8.06-18 18-18 18 8.06 18 18-8.06 18-18 18zm-3-27h-4v14h4v-14zm10 0h-4v14h4v-14z"/>
      </svg>
    </div>
    <div v-if="isOpen" class="chat-window">
      <div class="chat-header">
        <span>Quiz Master AI</span>
        <button @click="toggleChat" class="close-btn">&times;</button>
      </div>
      <div class="chat-messages" ref="messagesContainer">
        <div v-for="(msg, index) in messages" :key="index" :class="['message', msg.sender]">
          <div class="message-text" v-if="msg.sender === 'user'">{{ msg.text }}</div>
          <div class="message-text" v-else v-html="renderMarkdown(msg.text)"></div>
        </div>
      </div>
      <form @submit.prevent="sendMessage" class="chat-input-form">
        <input v-model="inputMessage" type="text" placeholder="Type your message..." autocomplete="off" />
        <button type="submit" :disabled="loading || !inputMessage.trim()">Send</button>
      </form>
    </div>
  </div>
</template>

<script>
import { marked } from 'marked';

const API_BASE = 'http://localhost:8001/api/chatbot';

export default {
  props: ['isQuizActive'],
  data() {
    return {
      isOpen: false,
      inputMessage: '',
      messages: [],
      loading: false
    };
  },
  methods: {
    toggleChat() {
      if (this.isQuizActive) {
        // Disable toggling chat when quiz is active
        return;
      }
      this.isOpen = !this.isOpen;
      if (this.isOpen) {
        this.$nextTick(() => {
          this.scrollToBottom();
        });
      }
    },
    scrollToBottom() {
      const container = this.$refs.messagesContainer;
      if (container) {
        container.scrollTop = container.scrollHeight;
      }
    },
    async sendMessage() {
      if (!this.inputMessage.trim()) return;
      const userMsg = this.inputMessage.trim();
      this.messages.push({ sender: 'user', text: userMsg });
      this.inputMessage = '';
      this.loading = true;
      this.$nextTick(() => {
        this.scrollToBottom();
      });

      try {
        const response = await fetch(`${API_BASE}/chat`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message: userMsg })
        });
        const data = await response.json();
        if (response.ok) {
          this.messages.push({ sender: 'ai', text: data.response });
        } else {
          this.messages.push({ sender: 'ai', text: 'Error: ' + (data.error || 'Unknown error') });
        }
      } catch (error) {
        this.messages.push({ sender: 'ai', text: 'Error: Failed to connect to server' });
      } finally {
        this.loading = false;
        this.$nextTick(() => {
          this.scrollToBottom();
        });
      }
    },
    renderMarkdown(text) {
      return marked.parse(text);
    }
  }
};
</script>

<style scoped>
.chatbot-icon {
  position: fixed;
  bottom: 60px;
  right: 20px;
  background: linear-gradient(45deg, #f093fb 0%, #f5576c 100%);
  border-radius: 50%;
  width: 64px;
  height: 64px;
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.25);
}

.chatbot-icon svg {
  fill: white;
}

.chat-window {
  position: fixed;
  bottom: 80px;
  right: 20px;
  width: 500px;
  max-height: 750px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  backdrop-filter: blur(10px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.25);
  display: flex;
  flex-direction: column;
  z-index: 1000;
}

.chat-header {
  background: linear-gradient(45deg, #f093fb 0%, #f5576c 100%);
  color: white;
  padding: 10px;
  font-weight: bold;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-top-left-radius: 20px;
  border-top-right-radius: 20px;
}

.close-btn {
  background: transparent;
  border: none;
  color: white;
  font-size: 20px;
  cursor: pointer;
}

.chat-messages {
  flex: 1;
  padding: 10px;
  overflow-y: auto;
  background: transparent;
  color: white;
}

.message {
  margin-bottom: 10px;
  max-width: 80%;
  word-wrap: break-word;
  color: white;
}

.message.user {
  align-self: flex-end;
  background: linear-gradient(45deg, #f093fb 0%, #f5576c 100%);
  border-radius: 10px 10px 0 10px;
  padding: 8px 12px;
  color: white;
}

.message.ai {
  align-self: flex-start;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 10px 10px 10px 0;
  padding: 8px 12px;
  color: white;
}

.chat-input-form {
  display: flex;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.chat-input-form input {
  flex: 1;
  border: none;
  padding: 10px;
  font-size: 14px;
  border-bottom-left-radius: 20px;
  background: rgba(255, 255, 255, 0.1);
  color: white;
}

.chat-input-form input::placeholder {
  color: rgba(255, 255, 255, 0.7);
}

.chat-input-form input:focus {
  outline: none;
  background: rgba(255, 255, 255, 0.15);
}

.chat-input-form button {
  background: linear-gradient(45deg, #f093fb 0%, #f5576c 100%);
  border: none;
  color: white;
  padding: 0 16px;
  cursor: pointer;
  border-bottom-right-radius: 20px;
  transition: background 0.3s ease;
}

.chat-input-form button:hover:not(:disabled) {
  background: #f5576c;
}

.chat-input-form button:disabled {
  background: rgba(255, 255, 255, 0.05);
  cursor: not-allowed;
}
</style>
