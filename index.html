<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Advanced Music Recommendation Chatbot</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
        }
        .chat-container {
            width: 500px;
            margin: 50px auto;
            background-color: white;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        .chat-box {
            height: 400px;
            overflow-y: scroll;
            border: 1px solid #ddd;
            padding: 10px;
            margin-bottom: 10px;
        }
        .message {
            margin: 10px 0;
        }
        .bot-message {
            color: #007bff;
        }
        .user-message {
            color: #28a745;
            text-align: right;
        }
        .typing-indicator {
            font-style: italic;
            color: #999;
        }
        .music-cover {
            max-width: 100px;
            display: block;
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="chat-box" id="chat-box">
            <div class="message bot-message">Hello! What kind of music are you in the mood for?</div>
        </div>
        <input type="text" id="user-input" placeholder="Type your message here..." style="width: 100%; padding: 10px;" />
        <button id="send-btn" style="width: 100%; padding: 10px;">Send</button>
        <div class="typing-indicator" id="typing-indicator" style="display: none;">Bot is typing...</div>
    </div>

    <script>
        const chatBox = document.getElementById('chat-box');
        const userInput = document.getElementById('user-input');
        const sendBtn = document.getElementById('send-btn');
        const typingIndicator = document.getElementById('typing-indicator');

        sendBtn.addEventListener('click', () => {
            const message = userInput.value;
            if (message.trim() === "") return;

            // Display user message
            const userMessage = document.createElement('div');
            userMessage.classList.add('message', 'user-message');
            userMessage.textContent = message;
            chatBox.appendChild(userMessage);
            userInput.value = "";

            // Show typing indicator
            typingIndicator.style.display = "block";

            // Send user message to backend (Flask)
            fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message })
            })
            .then(response => response.json())
            .then(data => {
                // Hide typing indicator
                typingIndicator.style.display = "none";

                // Display chatbot's response
                const botMessage = document.createElement('div');
                botMessage.classList.add('message', 'bot-message');
                botMessage.textContent = data.response;
                chatBox.appendChild(botMessage);

                // Scroll to bottom
                chatBox.scrollTop = chatBox.scrollHeight;
            });
        });
    </script>
</body>
</html>
