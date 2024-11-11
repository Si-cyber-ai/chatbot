let conversationPhase = 0; 
let casualResponseCount = 0; 

document.getElementById('userInput').addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        event.preventDefault();
        sendMessage();
    }
});

async function sendMessage() {
    const userInput = document.getElementById('userInput').value.trim();
    if (userInput === "") return;

    displayMessage(`You: ${userInput}`, 'user-message');
    document.getElementById('userInput').value = "";
    document.getElementById('userInput').focus();
    displayTypingIndicator();

    setTimeout(() => {
        removeTypingIndicator();
        handleConversationPhase(userInput);
    }, 1500);
}

function restartChat() {
    document.getElementById('messages').innerHTML = ""; 
    conversationPhase = 0;
    casualResponseCount = 0;
    displayMessage("Welcome back! How can I assist you with music recommendations?", 'bot-message');
}

function displayMessage(content, className) {
    const messageContainer = document.getElementById('messages');
    const message = document.createElement('div');
    message.classList.add('message', className);
    message.innerHTML = `<div class="message-text">${content}</div>`;
    messageContainer.appendChild(message);
    scrollToBottom();
}

function displayTypingIndicator() {
    const typingMessage = document.createElement('div');
    typingMessage.classList.add('message', 'bot-message');
    typingMessage.innerHTML = `<div class="bot-avatar"></div><div class="bot-typing">Bot is typing...</div>`;
    document.getElementById('messages').appendChild(typingMessage);
    scrollToBottom();
}

function removeTypingIndicator() {
    const typingIndicator = document.querySelector('.bot-typing');
    if (typingIndicator) typingIndicator.parentElement.remove();
}

function scrollToBottom() {
    const messageContainer = document.getElementById('messages');
    messageContainer.scrollTop = messageContainer.scrollHeight;
}

function handleConversationPhase(userInput) {
    switch (conversationPhase) {
        case 0:
            casualConversation();
            break;
        case 1:
            transitionToMusicTopic();
            break;
        case 2:
            askForRecommendation();
            break;
        case 3:
            fetchMusicRecommendation(userInput);
            break;
        default:
            resetConversation();
            break;
    }
}

function casualConversation() {
    const responses = ["Hey there! How’s your day going?", "That’s awesome to hear! What are you been up to?", "That sound Nice! What do you usually do to relax?"];
    displayMessage(responses[casualResponseCount] || "Tell me more.", 'bot-message');
    casualResponseCount++;
    if (casualResponseCount >= responses.length) conversationPhase = 1;
}

function transitionToMusicTopic() {
    displayMessage("I love that! What kind of music do you enjoy?", 'bot-message');
    conversationPhase = 2;
}

function askForRecommendation() {
    displayMessage("Would you like a music recommendation based on your mood?", 'bot-message');
    conversationPhase = 3;
}

async function fetchMusicRecommendation(userInput) {
    try {
        const response = await fetch('/get_recommendation', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query: userInput })
        });

        const data = await response.json();
        if (data.recommendations) {
            data.recommendations.forEach(rec => {
                displayMessage(`<a href="${rec.url}" target="_blank">${rec.song}</a>`, 'bot-message');
            });
        } else if (data.song) {
            displayMessage(`<a href="${data.url}" target="_blank">${data.song}</a>`, 'bot-message');
        } else {
            displayMessage("Sorry, I couldn't find any recommendations.", 'bot-message');
        }
    } catch (error) {
        displayMessage("Oops! Something went wrong. Please try again.", 'bot-message');
    }
}

function resetConversation() {
    conversationPhase = 0;
    casualResponseCount = 0;
}
