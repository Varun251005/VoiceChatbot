let isListening = false;
let isProcessing = false;
let shouldSkip = false;

const startBtn = document.getElementById('startBtn');
const stopBtn = document.getElementById('stopBtn');
const skipBtn = document.getElementById('skipBtn');
const chatMessages = document.getElementById('chatMessages');
const statusIndicator = document.getElementById('statusIndicator');
const statusText = document.getElementById('statusText');

// Update Status
function updateStatus(status, message) {
    const dot = statusIndicator.querySelector('.status-dot');
    const text = statusIndicator.querySelector('.status-text');
    
    dot.className = `status-dot ${status}`;
    text.textContent = message;
}

// Add message to chat
function addMessage(text, isUser = true) {
    // Remove welcome message if it exists
    const welcomeMsg = chatMessages.querySelector('.welcome-message');
    if (welcomeMsg) {
        welcomeMsg.remove();
    }

    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user' : 'bot'}`;
    
    const labelDiv = document.createElement('div');
    labelDiv.className = 'message-label';
    labelDiv.textContent = isUser ? '🎤 You' : '🤖 LLaMA';
    
    const bubbleDiv = document.createElement('div');
    bubbleDiv.className = 'message-bubble';
    bubbleDiv.textContent = text;
    
    messageDiv.appendChild(labelDiv);
    messageDiv.appendChild(bubbleDiv);
    
    chatMessages.appendChild(messageDiv);
    
    // Scroll to bottom
    setTimeout(() => {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }, 100);
}

// Start Button
startBtn.addEventListener('click', async () => {
    if (isListening || isProcessing) return;
    
    isListening = true;
    shouldSkip = false;
    
    startBtn.disabled = true;
    stopBtn.disabled = false;
    skipBtn.disabled = true;
    
    updateStatus('listening', 'Listening...');
    
    try {
        const response = await fetch('/listen', { method: 'POST' });
        const data = await response.json();
        
        if (data.success) {
            addMessage(data.text, true);
            
            if (data.text.toLowerCase() === 'exit') {
                updateStatus('ready', 'Goodbye!');
                addMessage('Goodbye! Thanks for chatting! 👋', false);
                startBtn.disabled = false;
                stopBtn.disabled = true;
                isListening = false;
                return;
            }
            
            // Process with LLaMA
            processWithLLaMA(data.text);
        } else {
            addMessage('❌ Could not understand audio. Please try again.', false);
            updateStatus('ready', 'Ready');
            startBtn.disabled = false;
            stopBtn.disabled = true;
            isListening = false;
        }
    } catch (error) {
        console.error('Error:', error);
        addMessage(`❌ Error: ${error.message}`, false);
        updateStatus('error', 'Error');
        startBtn.disabled = false;
        stopBtn.disabled = true;
        isListening = false;
    }
});

// Process with LLaMA
async function processWithLLaMA(text) {
    isListening = false;
    isProcessing = true;
    
    startBtn.disabled = true;
    stopBtn.disabled = false;
    skipBtn.disabled = false;
    
    updateStatus('processing', 'Processing...');
    
    try {
        const response = await fetch('/generate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: text })
        });
        
        const data = await response.json();
        
        if (shouldSkip) {
            shouldSkip = false;
            isProcessing = false;
            updateStatus('ready', 'Ready');
            startBtn.disabled = false;
            stopBtn.disabled = true;
            skipBtn.disabled = true;
            return;
        }
        
        if (data.success) {
            addMessage(data.response, false);
            
            // Speak response
            speakResponse(data.response);
        } else {
            addMessage(`❌ Error: ${data.error}`, false);
            updateStatus('ready', 'Ready');
            startBtn.disabled = false;
            stopBtn.disabled = true;
            skipBtn.disabled = true;
            isProcessing = false;
        }
    } catch (error) {
        console.error('Error:', error);
        addMessage(`❌ Error: ${error.message}`, false);
        updateStatus('error', 'Error');
        startBtn.disabled = false;
        stopBtn.disabled = true;
        skipBtn.disabled = true;
        isProcessing = false;
    }
}

// Speak Response
async function speakResponse(text) {
    try {
        const response = await fetch('/speak', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: text })
        });
        
        const data = await response.json();
        
        if (data.success) {
            updateStatus('ready', 'Ready');
            startBtn.disabled = false;
            stopBtn.disabled = true;
            skipBtn.disabled = true;
            isProcessing = false;
        }
    } catch (error) {
        console.error('Error speaking:', error);
        updateStatus('ready', 'Ready');
        startBtn.disabled = false;
        stopBtn.disabled = true;
        skipBtn.disabled = true;
        isProcessing = false;
    }
}

// Stop Button
stopBtn.addEventListener('click', () => {
    isListening = false;
    isProcessing = false;
    shouldSkip = false;
    
    startBtn.disabled = false;
    stopBtn.disabled = true;
    skipBtn.disabled = true;
    
    updateStatus('ready', 'Ready');
    
    fetch('/stop', { method: 'POST' }).catch(err => console.error('Stop error:', err));
});

// Skip Button
skipBtn.addEventListener('click', () => {
    shouldSkip = true;
    
    skipBtn.disabled = true;
    stopBtn.disabled = true;
    startBtn.disabled = false;
    
    updateStatus('ready', 'Ready');
    
    fetch('/stop', { method: 'POST' }).catch(err => console.error('Skip error:', err));
    
    isProcessing = false;
});

// Initial status
updateStatus('ready', 'Ready');

