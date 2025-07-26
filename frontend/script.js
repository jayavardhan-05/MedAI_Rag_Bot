// Configuration
const API_BASE_URL = 'http://localhost:8000';

// DOM Elements
const questionForm = document.getElementById('questionForm');
const questionInput = document.getElementById('questionInput');
const sendButton = document.getElementById('sendButton');
const chatHistory = document.getElementById('chatHistory');
const sourcesContent = document.getElementById('sourcesContent');
const loadingOverlay = document.getElementById('loadingOverlay');
const errorToast = document.getElementById('errorToast');
const errorMessage = document.getElementById('errorMessage');
const charCount = document.getElementById('charCount');
const statusDot = document.getElementById('statusDot');
const statusText = document.getElementById('statusText');

// State management
let isLoading = false;
let conversationHistory = [];

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    setupEventListeners();
    checkBackendStatus();
});

function initializeApp() {
    // Clear any existing conversation
    conversationHistory = [];
    
    // Focus on input
    questionInput.focus();
    
    // Setup sample question clicks
    setupSampleQuestions();
    
    console.log('MED AI Frontend initialized');
}

function setupEventListeners() {
    // Form submission
    questionForm.addEventListener('submit', handleQuestionSubmit);
    
    // Character counter
    questionInput.addEventListener('input', updateCharacterCount);
    
    // Enter key handling
    questionInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            if (!isLoading && questionInput.value.trim()) {
                handleQuestionSubmit(e);
            }
        }
    });
    
    // Auto-resize functionality for better UX
    questionInput.addEventListener('input', function() {
        // Enable/disable send button based on input
        const hasContent = this.value.trim().length > 0;
        sendButton.disabled = !hasContent || isLoading;
    });
}

function setupSampleQuestions() {
    const sampleQuestions = document.querySelectorAll('.sample-questions li');
    sampleQuestions.forEach(li => {
        li.addEventListener('click', function() {
            const questionText = this.textContent.replace(/[""]/g, '');
            questionInput.value = questionText;
            updateCharacterCount();
            questionInput.focus();
            sendButton.disabled = false;
        });
    });
}

function updateCharacterCount() {
    const count = questionInput.value.length;
    charCount.textContent = count;
    
    // Update styling based on character count
    const charCountElement = charCount.parentElement;
    if (count > 900) {
        charCountElement.style.color = '#ef4444';
    } else if (count > 700) {
        charCountElement.style.color = '#f59e0b';
    } else {
        charCountElement.style.color = '#64748b';
    }
}

async function checkBackendStatus() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        const data = await response.json();
        
        if (response.ok && data.database_loaded) {
            updateStatus('connected', 'Connected');
        } else {
            updateStatus('error', 'Backend issues detected');
        }
    } catch (error) {
        updateStatus('error', 'Backend offline');
        console.error('Backend health check failed:', error);
    }
}

function updateStatus(status, text) {
    statusDot.className = `status-dot ${status}`;
    statusText.textContent = text;
}

async function handleQuestionSubmit(e) {
    e.preventDefault();
    
    const question = questionInput.value.trim();
    if (!question || isLoading) return;
    
    // Add user message to chat
    addMessageToChat('user', question);
    
    // Clear input and disable form
    questionInput.value = '';
    updateCharacterCount();
    setLoadingState(true);
    
    // Add thinking indicator
    const thinkingId = addThinkingIndicator();
    
    try {
        // Send question to backend
        const response = await fetch(`${API_BASE_URL}/ask`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ question: question })
        });
        
        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Remove thinking indicator
        removeThinkingIndicator(thinkingId);
        
        // Add AI response to chat
        addMessageToChat('ai', data.answer);
        
        // Update sources section
        updateSourcesSection(data.sources);
        
        // Store in conversation history
        conversationHistory.push({
            question: question,
            answer: data.answer,
            sources: data.sources,
            timestamp: new Date()
        });
        
    } catch (error) {
        console.error('Error asking question:', error);
        
        // Remove thinking indicator
        removeThinkingIndicator(thinkingId);
        
        // Show error message
        addMessageToChat('ai', 
            'I apologize, but I encountered an error while processing your question. ' +
            'Please check that the backend is running and try again.'
        );
        
        showError('Failed to get response from MED AI. Please try again.');
    } finally {
        setLoadingState(false);
        questionInput.focus();
    }
}

function addMessageToChat(sender, content) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.innerHTML = sender === 'user' ? '<i class="fas fa-user"></i>' : '<i class="fas fa-robot"></i>';
    
    const bubble = document.createElement('div');
    bubble.className = 'message-bubble';
    bubble.textContent = content;
    
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(bubble);
    
    // Remove welcome message if it exists
    const welcomeMessage = chatHistory.querySelector('.welcome-message');
    if (welcomeMessage) {
        welcomeMessage.remove();
    }
    
    chatHistory.appendChild(messageDiv);
    
    // Scroll to bottom
    scrollToBottom();
}

function addThinkingIndicator() {
    const thinkingDiv = document.createElement('div');
    thinkingDiv.className = 'message ai';
    thinkingDiv.id = `thinking-${Date.now()}`;
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.innerHTML = '<i class="fas fa-robot"></i>';
    
    const thinkingIndicator = document.createElement('div');
    thinkingIndicator.className = 'thinking-indicator';
    
    const thinkingText = document.createElement('span');
    thinkingText.textContent = 'Thinking';
    
    const thinkingDots = document.createElement('div');
    thinkingDots.className = 'thinking-dots';
    for (let i = 0; i < 3; i++) {
        const dot = document.createElement('div');
        dot.className = 'thinking-dot';
        thinkingDots.appendChild(dot);
    }
    
    thinkingIndicator.appendChild(thinkingText);
    thinkingIndicator.appendChild(thinkingDots);
    
    thinkingDiv.appendChild(avatar);
    thinkingDiv.appendChild(thinkingIndicator);
    
    chatHistory.appendChild(thinkingDiv);
    scrollToBottom();
    
    return thinkingDiv.id;
}

function removeThinkingIndicator(thinkingId) {
    const thinkingElement = document.getElementById(thinkingId);
    if (thinkingElement) {
        thinkingElement.remove();
    }
}

function updateSourcesSection(sources) {
    // Clear existing content
    sourcesContent.innerHTML = '';
    
    if (!sources || sources.length === 0) {
        sourcesContent.innerHTML = `
            <div class="sources-placeholder">
                <div class="placeholder-icon">
                    <i class="fas fa-file-medical"></i>
                </div>
                <p>No sources were found for this question.</p>
            </div>
        `;
        return;
    }
    
    // Create source cards
    sources.forEach((source, index) => {
        const sourceCard = createSourceCard(source, index + 1);
        sourcesContent.appendChild(sourceCard);
    });
}

function createSourceCard(source, index) {
    const card = document.createElement('div');
    card.className = 'source-card';
    
    const header = document.createElement('div');
    header.className = 'source-header';
    
    const sourceNumber = document.createElement('span');
    sourceNumber.className = 'source-number';
    sourceNumber.textContent = `Source ${index}`;
    
    const sourceTitle = document.createElement('span');
    sourceTitle.className = 'source-title';
    sourceTitle.textContent = getSourceTitle(source.metadata);
    
    header.appendChild(sourceNumber);
    header.appendChild(sourceTitle);
    
    const content = document.createElement('div');
    content.className = 'source-content';
    content.textContent = truncateText(source.content, 800);
    
    card.appendChild(header);
    card.appendChild(content);
    
    return card;
}

function getSourceTitle(metadata) {
    // Extract meaningful title from metadata
    if (metadata && metadata.source) {
        const source = metadata.source;
        const filename = source.split('/').pop() || source;
        return filename.replace(/\.[^/.]+$/, ""); // Remove file extension
    }
    return 'Medical Literature';
}

function truncateText(text, maxLength) {
    if (text.length <= maxLength) return text;
    return text.slice(0, maxLength) + '...';
}

function setLoadingState(loading) {
    isLoading = loading;
    
    // Update UI elements
    questionInput.disabled = loading;
    sendButton.disabled = loading || !questionInput.value.trim();
    
    if (loading) {
        sendButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
        questionInput.placeholder = 'MED AI is processing your question...';
    } else {
        sendButton.innerHTML = '<i class="fas fa-paper-plane"></i>';
        questionInput.placeholder = 'Ask a medical question...';
    }
}

function scrollToBottom() {
    chatHistory.scrollTop = chatHistory.scrollHeight;
}

function showError(message) {
    errorMessage.textContent = message;
    errorToast.classList.add('show');
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        hideError();
    }, 5000);
}

function hideError() {
    errorToast.classList.remove('show');
}

// Utility functions for enhanced UX
function highlightKeywords(text, keywords) {
    if (!keywords || keywords.length === 0) return text;
    
    let highlightedText = text;
    keywords.forEach(keyword => {
        const regex = new RegExp(`(${keyword})`, 'gi');
        highlightedText = highlightedText.replace(regex, '<span class="highlight">$1</span>');
    });
    
    return highlightedText;
}

function formatAnswer(answer) {
    // Basic formatting for better readability
    return answer
        .replace(/\n\n/g, '</p><p>')
        .replace(/\n/g, '<br>')
        .replace(/^/, '<p>')
        .replace(/$/, '</p>');
}

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + K to focus on input
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        questionInput.focus();
        questionInput.select();
    }
    
    // Escape to clear input
    if (e.key === 'Escape' && document.activeElement === questionInput) {
        questionInput.value = '';
        updateCharacterCount();
        sendButton.disabled = true;
    }
});

// Periodic backend health check
setInterval(checkBackendStatus, 30000); // Check every 30 seconds

// Handle page visibility changes
document.addEventListener('visibilitychange', function() {
    if (!document.hidden) {
        // Page became visible, check backend status
        checkBackendStatus();
    }
});

// Export functions for potential testing or external use
window.MedAI = {
    askQuestion: handleQuestionSubmit,
    showError: showError,
    hideError: hideError,
    checkStatus: checkBackendStatus,
    conversationHistory: conversationHistory
};