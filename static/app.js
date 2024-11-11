let conversationPhase = 0; // Track the conversation phase 
let casualResponseCount = 0; // Track how many casual responses have been given

// Handle 'Enter' key to trigger message send
document.getElementById('userInput').addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        event.preventDefault();
        sendMessage();
    }
});

// Main function to send message
async function sendMessage() {
    const userInput = document.getElementById('userInput').value.trim();
    
    if (userInput === "") return; // Prevent sending empty messages

    // Display the user's message
    displayMessage(`You: ${userInput}`, 'user-message');

    // Clear input and refocus for smooth interaction
    document.getElementById('userInput').value = "";
    document.getElementById('userInput').focus();

    // Show bot typing indicator
    displayTypingIndicator();

    // Simulate bot thinking and handle conversation phase after delay
    setTimeout(() => {
        removeTypingIndicator();
        handleConversationPhase(userInput); // Process input based on conversation phase
    }, 1500);
}
// Function to reset the chat
function restartChat() {
    const messagesContainer = document.getElementById('messages');
    messagesContainer.innerHTML = ""; // Clear all chat messages
    conversationPhase = 0; // Reset conversation phase
    casualResponseCount = 0; // Reset casual response count
    displayMessage("Welcome back! How can I assist you with music recommendations?", 'bot-message');
}

// Existing functions like sendMessage() remain unchanged


// Function to display messages in the chat
function displayMessage(content, className) {
    const messageContainer = document.getElementById('messages');
    const message = document.createElement('div');
    message.classList.add('message', className);
    message.innerHTML = `<div class="message-text">${content}</div>`;
    messageContainer.appendChild(message);
    scrollToBottom();
}

// Function to show the bot's typing indicator
function displayTypingIndicator() {
    const typingIndicator = document.querySelector('.bot-typing');
    if (!typingIndicator) { // Ensure only one typing indicator is created
        const messageContainer = document.getElementById('messages');
        const typingMessage = document.createElement('div');
        typingMessage.classList.add('message', 'bot-message');
        typingMessage.innerHTML = `<div class="bot-avatar"></div><div class="bot-typing">Bot is typing...</div>`;
        messageContainer.appendChild(typingMessage);
        scrollToBottom();
    }
}

// Function to remove the bot's typing indicator
function removeTypingIndicator() {
    const typingIndicator = document.querySelector('.bot-typing');
    if (typingIndicator) typingIndicator.parentElement.remove();
}

// Ensure chat scrolls to the bottom after a message is added
function scrollToBottom() {
    const messageContainer = document.getElementById('messages');
    messageContainer.scrollTop = messageContainer.scrollHeight;
}

// Handle conversation phases to control bot's responses
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

// Phase 0: Casual conversation with multiple bot responses
function casualConversation() {
    const casualResponses = [
        "Hey there! How’s your day going?",
        "That’s awesome to hear! What have you been up to?",
        "That sounds nice! What do you usually do when you relax?"
    ];

    const botResponse = casualResponses[casualResponseCount] || "Interesting! Tell me more.";
    displayMessage(botResponse, 'bot-message');
    casualResponseCount++;

    // Move to the next phase after a certain number of casual responses
    if (casualResponseCount >= casualResponses.length) {
        conversationPhase = 1; // Move to music topic phase
    }
}

// Phase 1: Transition to music conversation
function transitionToMusicTopic() {
    const botResponse = "I love that! What kind of music do you enjoy?";
    displayMessage(botResponse, 'bot-message');
    conversationPhase = 2;
}

// Phase 2: Ask for music recommendation
function askForRecommendation() {
    const botResponse = "Pop is great! Would you like me to recommend some music based on your mood right now?";
    displayMessage(botResponse, 'bot-message');
    conversationPhase = 3;
}

// Phase 3: Fetch music recommendation from the server
async function fetchMusicRecommendation(userInput) {
    try {
        const response = await fetch('/get_recommendation', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query: userInput }),
        });

        if (!response.ok) {
            throw new Error("Network response was not ok.");
        }

        const data = await response.json();
        if (data && data.song && data.url) {
            displayMessage(`I recommend <a href="${data.url}" target="_blank">${data.song}</a>. Enjoy!`, 'bot-message');
        } else {
            displayMessage("Sorry, I couldn't find any recommendations.", 'bot-message');
        }

    } catch (error) {
        console.error("Fetch error:", error);
        displayMessage("Oops! Something went wrong. Please try again.", 'bot-message');
    } finally {
        resetConversation();
    }
}

// Reset conversation to the beginning
function resetConversation() {
    conversationPhase = 0;
    casualResponseCount = 0;
}
