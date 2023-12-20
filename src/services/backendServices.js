// src/services/backendService.js

export async function sendMessageToBackend(mode, message) {
  try {
    let endpointURL = 'http://127.0.0.1:5000/api/'
    if (mode === 'echo') {
        endpointURL += 'echo'
    }
    const response = await fetch(endpointURL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ 'message': message }),
    });

    const data = await response.json();
    return data.botResponse;
  } catch (error) {
    console.error('Error sending message to backend:', error);
    throw error;
  }
}
