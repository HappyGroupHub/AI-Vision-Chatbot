export async function sendMessageToBackend(mode, message) {
  try {
    let endpointURL = 'http://127.0.0.1:5000/api/'
    if (mode === 'echo') {
        endpointURL += 'echo'
    } else if (mode === 'generate_image') {
        endpointURL += 'generate_image'
    }
    const response = await fetch(endpointURL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ user_input: message }),
    });

    return await response.json();
  } catch (error) {
    console.error('Error sending message to backend:', error);
    throw error;
  }
}
