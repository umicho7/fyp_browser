document.addEventListener('DOMContentLoaded', () => {
    const openChatbotButton = document.getElementById('open-chatbot');
    const chatbotContainer = document.getElementById('chatbot-container');
    const closeChatbotButton = document.getElementById('close-chatbot');
    const chatbotInput = document.getElementById('chatbot-input');
    const chatbotSend = document.getElementById('chatbot-send');
    const chatbotMessages = document.getElementById('chatbot-messages');

    // Open the chatbot
    openChatbotButton.addEventListener('click', () => {
        chatbotContainer.style.display = 'flex';
        openChatbotButton.style.display = 'none';
    });

    // Close the chatbot
    closeChatbotButton.addEventListener('click', () => {
        chatbotContainer.style.display = 'none';
        openChatbotButton.style.display = 'block';
    });

    // Handle sending messages
    chatbotSend.addEventListener('click', () => {
        const userMessage = chatbotInput.value.trim();
        if (userMessage) {
            displayMessage(userMessage, 'user-message');
            chatbotInput.value = '';
            sendMessageToBot(userMessage);
        }
    });

    // Listen for Enter key press in the input field
    chatbotInput.addEventListener('keypress', (event) => {
        if (event.key === 'Enter') {
            chatbotSend.click();
        }
    });

    // Function to display messages in the chatbot
    function displayMessage(message, className) {
        const messageElement = document.createElement('div');
        messageElement.textContent = message;
        messageElement.className = `message ${className}`;
        chatbotMessages.appendChild(messageElement);
        chatbotMessages.scrollTop = chatbotMessages.scrollHeight; // Scroll to the latest message
    }

    // Function to send user message to the backend
    async function sendMessageToBot(userMessage) {
        try {
            const response = await fetch('http://127.0.0.1:5000/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: userMessage })
            });

            const data = await response.json();

            if (response.ok && data.bot_message) {
                displayMessage(data.bot_message, 'bot-message');
            } else if (data.error) {
                displayMessage(`Error: ${data.error}`, 'bot-message');
            } else {
                displayMessage('Unexpected error occurred.', 'bot-message');
            }
        } catch (error) {
            displayMessage(`Network Error: ${error.message}`, 'bot-message');
        }
    }
});
