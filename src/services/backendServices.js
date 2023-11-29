// src/services/backendService.js

export async function sendMessageToBackend(message) {
  try {
    const response = await fetch('http://127.0.0.1:5000/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message }),
    });

    const data = await response.json();
    return data.reply;
  } catch (error) {
    console.error('Error sending message to backend:', error);
    throw error;
  }
}
