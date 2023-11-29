<template>
  <div id="app">
    <h1>Chat Bot</h1>
    <div class="chat-panel">
      <div class="messages">
        <div v-for="(message, index) in chatHistory" :key="index" :class="{ 'user-message': message.fromUser, 'bot-message': !message.fromUser }">
          <div v-if="message.fromUser" class="message user-message-right">{{ message.text }}</div>
          <div v-else class="message bot-message-left">{{ message.text }}</div>
        </div>
      </div>
      <input v-model="userInput" @keyup.enter="sendMessage" placeholder="Type your message..." />
    </div>
  </div>
</template>

<script>
import {sendMessageToBackend} from "./services/backendServices.js";

export default {
  data() {
    return {
      userInput: '',
      chatHistory: [],
    };
  },
  methods: {
    async sendMessage() {
      // Add the user's message to the chat history
      this.chatHistory.push({ text: this.userInput, fromUser: true });

      // Clear the input field
      this.userInput = '';

      // Send the message to the backend
      console.log('Sending message:', this.userInput);
      // const response = await sendMessageToBackend(this.userInput);
      this.receiveMessage('This is a sample response from the bot.');
    },
    receiveMessage(text) {
      // Add the bot's response to the chat history
      this.chatHistory.push({ text, fromUser: false });
    },
  },
};
</script>

<style>
#app {
  text-align: center;
  margin-top: 2rem;
}

h1 {
  font-size: 2rem;
}

.chat-panel {
  border: 1px solid #ccc;
  padding: 1rem;
  width: 400px; /* Increase the width */
  margin: auto;
  border-radius: 8px;
}

.messages {
  max-height: 400px; /* Increase the height */
  overflow-y: auto;
}

.message {
  padding: 0.5rem;
  border-radius: 8px;
  margin-bottom: 0.5rem;
}

.user-message-right {
  text-align: right;
  background-color: #e0e0e0;
}

.bot-message-left {
  text-align: left;
  background-color: #f0f0f0;
}

input {
  width: 100%;
  padding: 0.5rem;
  margin-top: 0.5rem;
}
</style>
