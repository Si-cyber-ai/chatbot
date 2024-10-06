let conversationPhase = 0; // Track the conversation phase
let casualResponseCount = 0; // Track how many casual responses have been given

async function sendMessage() {
    const userInput = document.getElementById('userInput').value;
    const messageContainer = document.getElementById('messages');
    
    if (userInput.trim() === "") return;

    // Display user input in the chatbox
    const userMessage = document.createElement('div');
    userMessage.classList.add('message', 'user-message');
    userMessage.innerHTML = `<div class="message-text">You: ${userInput}</div>`;
    messageContainer.appendChild(userMessage);
    
    // Clear the input field
    document.getElementById('userInput').value = "";

    // Scroll the message container to the bottom
    messageContainer.scrollTop = messageContainer.scrollHeight;

    // Display typing indicator
    const typingIndicator = document.createElement('div');
    typingIndicator.classList.add('message', 'bot-message');
    typingIndicator.innerHTML = `<div class="bot-avatar"></div><div class="bot-typing">Bot is typing...</div>`;
    messageContainer.appendChild(typingIndicator);

    // Scroll to show typing indicator
    messageContainer.scrollTop = messageContainer.scrollHeight;

    // Simulate bot thinking time before sending a real response
    setTimeout(() => {
        typingIndicator.remove();

        if (conversationPhase === 0) {
            casualConversation(userInput, messageContainer);
        } else if (conversationPhase === 1) {
            transitionToMusicTopic(userInput, messageContainer);
        } else if (conversationPhase === 2) {
            askForRecommendation(messageContainer);
        } else if (conversationPhase === 3) {
            fetchMusicRecommendation(userInput, messageContainer);
        }

        // Scroll to the latest message
        messageContainer.scrollTop = messageContainer.scrollHeight;
    }, 1500);  // Simulate 1.5 seconds of bot "thinking"
}

// Phase 0: Casual conversation
function casualConversation(userInput, messageContainer) {
    const casualResponses = [
        "Hey there! How’s your day going?",
        "That’s awesome to hear! What have you been up to?",
        "That sounds nice! What do you usually do when you relax?",
    ];

    const botResponse = casualResponses[casualResponseCount] || "Interesting! Tell me more.";

    const botMessage = document.createElement('div');
    botMessage.classList.add('message', 'bot-message');
    botMessage.innerHTML = `<div class="bot-avatar"></div><div class="message-text">${botResponse}</div>`;
    messageContainer.appendChild(botMessage);

    casualResponseCount++;

    // After a few casual responses, move to discussing music
    if (casualResponseCount === 3) {
        conversationPhase = 1;
    }
}

// Phase 1: Transition to music topic
function transitionToMusicTopic(userInput, messageContainer) {
    const botResponse = "I love that! What kind of music do you enjoy?";

    const botMessage = document.createElement('div');
    botMessage.classList.add('message', 'bot-message');
    botMessage.innerHTML = `<div class="bot-avatar"></div><div class="message-text">${botResponse}</div>`;
    messageContainer.appendChild(botMessage);

    conversationPhase = 2; // Move to asking for recommendation after this
}

// Phase 2: Ask for music recommendation
function askForRecommendation(messageContainer) {
    const botMessage = document.createElement('div');
    botMessage.classList.add('message', 'bot-message');
    botMessage.innerHTML = `<div class="bot-avatar"></div><div class="message-text">Pop is great! Would you like me to recommend some music based on your mood right now?</div>`;
    messageContainer.appendChild(botMessage);
    
    conversationPhase = 3; // Move to recommendation phase
}

// Phase 3: Fetch recommendation based on user's input
async function fetchMusicRecommendation(userInput, messageContainer) {
    // Send the user's query to the Flask backend for recommendation
    const response = await fetch('/get_recommendation', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: userInput }),
    });

    const data = await response.json();

    // Display bot's recommendation in the chatbox
    const botMessage = document.createElement('div');
    botMessage.classList.add('message', 'bot-message');
    botMessage.innerHTML = `
        <div class="bot-avatar"></div>
        <div class="message-text">I recommend <a href="${data.url}" target="_blank">${data.song}</a>. Enjoy!</div>`;
    messageContainer.appendChild(botMessage);

    // Reset conversation phase to allow for another conversation
    conversationPhase = 0;
    casualResponseCount = 0; // Reset casual response count for next conversation
}
