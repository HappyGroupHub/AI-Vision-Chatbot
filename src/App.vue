<template>
  <div id="app">
    <h1>Chat Bot</h1>
    <div class="chat-panel">
      <div class="messages" :style="{ maxHeight: messagesMaxHeight }">
        <div v-for="(message, index) in chatHistory" :key="index" class="message-container">
          <template v-if="message.fromUser && message.isImage">
            <!-- User's image message -->
            <div class="message user-message-right">
              <div class="message-header">
                <div class="sender-info">
                  <span class="sender-name">User</span>
                  <img class="sender-icon" src="./assets/user_icon.png" alt="User Icon"/>
                </div>
              </div>
              <p v-if="message.text">{{ message.text }}</p>
              <img v-if="message.imageUrl" :src="message.imageUrl" alt="Uploaded Image" class="uploaded-image"/>
            </div>
          </template>
          <template v-else-if="message.fromUser">
            <!-- User's text message -->
            <div class="message user-message-right">
              <div class="message-header">
                <div class="sender-info">
                  <span class="sender-name">User</span>
                  <img class="sender-icon" src="./assets/user_icon.png" alt="User Icon"/>
                </div>
              </div>
              {{ message.text }}
            </div>
          </template>
          <template v-else-if="message.fromUser === false && message.isImage">
            <!-- Bot's image response -->
            <div class="message bot-message-left">
              <div class="message-header">
                <div class="sender-info">
                  <img class="sender-icon" src="./assets/bot_icon.png" alt="Bot Icon"/>
                  <span class="sender-name">Bot's Response</span>
                </div>
              </div>
              <p v-if="message.text">{{ message.text }}</p>
              <img v-if="message.imageUrl" :src="message.imageUrl" alt="Image Respond" class="respond-image"/>
            </div>
          </template>
          <template>
            <!-- Bot's text response -->
            <div class="message bot-message-left">
              <div class="message-header">
                <div class="sender-info">
                  <img class="sender-icon" src="./assets/bot_icon.png" alt="Bot Icon"/>
                  <span class="sender-name">Bot's Response</span>
                </div>
              </div>
              {{ message.text }}
            </div>
          </template>
        </div>
      </div>
      <div class="input-container">
        <input v-model="userInput" @keyup.enter="sendMessage" placeholder="Type your message..."/>
        <button class="upload-icon" @click="openFileInput">📷</button>
        <div class="send-icon" @click="sendMessage">➤</div>
        <!-- Hidden file input for image selection -->
        <input ref="fileInput" type="file" accept="image/*" @change="handleImageUpload" style="display: none"/>
      </div>
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
      messagesMaxHeight: 'calc(70vh - 3rem)', // Adjust the value as needed
    };
  },
  methods: {
    async sendMessage() {
      // Add the user's message to the chat history
      this.chatHistory.push({text: this.userInput, fromUser: true});

      // Send the message to the backend and clear the input
      let userInput = this.userInput;
      this.userInput = '';
      console.log('Sending message:', userInput);

      let response = {botResponse: '', imagePath: '', imageUrl: ''};
      response = await sendMessageToBackend('generate_image', userInput);
      console.log('Received response:', response);

      if (response.botResponse) {
        this.chatHistory.push({text: response.botResponse, fromUser: false});
      }
      if (response.imagePath) {
        const blob = await this.fetchImageBlob(response.imagePath);
        const file = new File([blob], "image.png", {type: "image/png"});
        const imageUrl = URL.createObjectURL(file);
        console.log('Image URL:', imageUrl);
        this.chatHistory.push({imageUrl, fromUser: false, isImage: true});
      }
    },
    openFileInput() {
      // Trigger the file input
      this.$refs.fileInput.click();
    },
    handleImageUpload(event) {
      const file = event.target.files[0];
      if (file) {
        // Handle image upload logic
        const imageUrl = URL.createObjectURL(file);
        console.log('Image URL:', imageUrl)
        this.chatHistory.push({text: `User uploaded an image: ${file.name}`, fromUser: true});
        this.chatHistory.push({imageUrl, fromUser: true, isImage: true});
      }
    },
    async fetchImageBlob(imagePath) {
      const response = await fetch(imagePath);
      return await response.blob();
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
  width: 70vw; /* Use viewport width */
  margin: auto;
  border-radius: 8px;
  box-sizing: border-box;
  height: 70vh;
  display: flex;
  flex-direction: column;
}

.messages {
  overflow-y: auto;
}

.message-container {
  margin-bottom: 0.5rem;
}

.message {
  padding: 0.5rem;
  border-radius: 8px;
}

.user-message-right {
  text-align: right;
  background-color: #e0e0e0;
}

.bot-message-left {
  text-align: left;
  background-color: #f0f0f0;
}

.message-header {
  display: flex;
  justify-content: space-between;
}

.sender-info {
  display: flex;
  align-items: center;
}

.sender-name {
  font-weight: bold;
  margin-left: 5px;
}

.sender-icon {
  width: 20px;
  height: 20px;
  border-radius: 50%;
}

.input-container {
  display: flex;
  margin-top: auto;
}

input {
  flex-grow: 1;
}

.send-icon {
  cursor: pointer;
  font-size: 1rem;
  margin-left: 5px;
}

/* Adjust the styles for the sender info within user-message-right */
.user-message-right .message-header {
  display: flex;
  justify-content: flex-end;
}

.user-message-right .sender-info {
  margin-left: 5px;
}

.user-message-right .sender-name {
  font-weight: bold;
  margin-right: 5px;
}

.user-message-right .sender-icon {
  width: 20px;
  height: 20px;
  border-radius: 50%;
}

.upload-icon {
  cursor: pointer;
  font-size: 1rem;
  margin-right: 5px;
}

.uploaded-image {
  max-width: 100%;
  max-height: 200px;
  border-radius: 8px;
  margin-top: 5px;
}
</style>
