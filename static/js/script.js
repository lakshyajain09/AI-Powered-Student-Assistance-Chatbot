document.addEventListener('DOMContentLoaded', function() {
    const chatBox = document.getElementById('chat-box');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const queryChips = document.querySelectorAll('.query-chip');
    
    // Function to add user message to chat
    function addUserMessage(message) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('chat-message', 'user-message');
        messageDiv.innerHTML = `<p>${escapeHTML(message)}</p>`;
        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    }
    
    // Function to add bot message to chat
    function addBotMessage(message) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('chat-message', 'bot-message');
        
        // Simulate typing effect
        const typingIndicator = document.createElement('p');
        messageDiv.appendChild(typingIndicator);
        chatBox.appendChild(messageDiv);
        
        let i = 0;
        const speed = 15; // Typing speed
        const text = message;
        
        function typeWriter() {
            if (i < text.length) {
                typingIndicator.innerHTML = escapeHTML(text.substring(0, i+1));
                i++;
                chatBox.scrollTop = chatBox.scrollHeight;
                setTimeout(typeWriter, speed);
            }
        }
        
        typeWriter();
        chatBox.scrollTop = chatBox.scrollHeight;
    }
    
    // Function to escape HTML
    function escapeHTML(str) {
        return str.replace(/[&<>'"]/g, 
            tag => ({
                '&': '&amp;',
                '<': '&lt;',
                '>': '&gt;',
                "'": '&#39;',
                '"': '&quot;'
            }[tag]));
    }
    
    // Function to get bot response
    async function getBotResponse(userMessage) {
        // Add loading indicator
        const loadingDiv = document.createElement('div');
        loadingDiv.classList.add('chat-message', 'bot-message');
        loadingDiv.innerHTML = '<p><i>Typing...</i></p>';
        chatBox.appendChild(loadingDiv);
        
        try {
            const response = await fetch('/get_response', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: userMessage }),
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            
            // Remove loading indicator
            chatBox.removeChild(loadingDiv);
            
            // Add bot response
            addBotMessage(data.response);
        } catch (error) {
            // Remove loading indicator
            chatBox.removeChild(loadingDiv);
            
            // Add error message
            addBotMessage("Sorry, I'm having trouble connecting to the server. Please try again later.");
            console.error('Error:', error);
        }
    }
    
    // Function to handle submission
    function handleSubmit() {
        const message = userInput.value.trim();
        if (message) {
            addUserMessage(message);
            userInput.value = '';
            getBotResponse(message);
        }
    }
    
    // Event listener for send button
    sendBtn.addEventListener('click', handleSubmit);
    
    // Event listener for Enter key
    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            handleSubmit();
        }
    });
    
    // Event listeners for suggested query chips
    queryChips.forEach(chip => {
        chip.addEventListener('click', function() {
            const query = this.textContent;
            addUserMessage(query);
            getBotResponse(query);
        });
    });
    
    // Focus on input field when page loads
    userInput.focus();
});