// Company Policies Q&A JavaScript

class PolicyChat {
    constructor() {
        this.chatMessages = document.getElementById('chatMessages');
        this.chatForm = document.getElementById('chatForm');
        this.questionInput = document.getElementById('questionInput');
        this.sendButton = document.getElementById('sendButton');
        this.loadingModal = new bootstrap.Modal(document.getElementById('loadingModal'));
        
        this.initializeEventListeners();
        this.checkSystemHealth();
        this.loadSystemStats();
        
        // Auto-focus input
        this.questionInput.focus();
    }
    
    initializeEventListeners() {
        // Form submission
        this.chatForm.addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleSubmit();
        });
        
        // Enter key handling
        this.questionInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.handleSubmit();
            }
        });
    }
    
    async handleSubmit() {
        const question = this.questionInput.value.trim();
        if (!question) return;
        
        // Add user message to chat
        this.addMessage(question, 'user');
        
        // Clear input and disable form
        this.questionInput.value = '';
        this.setFormEnabled(false);
        this.showLoading(true);
        
        try {
            // Send request to backend
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ question: question })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                // Add bot response
                this.addBotMessage(data);
                
                // Update recent sources
                if (data.sources && data.sources.length > 0) {
                    this.updateRecentSources(data.sources);
                }
            } else {
                // Handle error response
                this.addMessage(
                    data.answer || 'Sorry, I encountered an error processing your question.',
                    'bot'
                );
            }
            
        } catch (error) {
            console.error('Error:', error);
            this.addMessage(
                'Sorry, I encountered a network error. Please try again.',
                'bot'
            );
        } finally {
            this.showLoading(false);
            this.setFormEnabled(true);
            this.questionInput.focus();
        }
    }
    
    addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const icon = sender === 'user' ? 'fa-user' : 'fa-robot';
        
        messageDiv.innerHTML = `
            <div class="message-content">
                <i class="fas ${icon} message-icon"></i>
                <div class="message-text">
                    <p>${this.escapeHtml(text)}</p>
                </div>
            </div>
        `;
        
        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
    }
    
    addBotMessage(data) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message bot-message';
        
        let citationsHtml = '';
        if (data.citations && data.citations.length > 0) {
            citationsHtml = `
                <div class="citations">
                    <h6><i class="fas fa-quote-left"></i> Sources:</h6>
                    ${data.citations.map(citation => `
                        <div class="citation-item">
                            <div class="citation-title">
                                <a href="${citation.url}" target="_blank" class="citation-link">
                                    ${this.escapeHtml(citation.title)}
                                    <i class="fas fa-external-link-alt"></i>
                                </a>
                            </div>
                            <div class="citation-snippet">"${this.escapeHtml(citation.snippet)}"</div>
                            <div class="citation-source">From: ${this.escapeHtml(citation.filename)}</div>
                        </div>
                    `).join('')}
                </div>
            `;
        }
        
        let metaHtml = '';
        if (data.latency_ms || data.retrieved_chunks) {
            metaHtml = `
                <div class="response-meta">
                    ${data.latency_ms ? `<span class="badge bg-info">${data.latency_ms}ms</span>` : ''}
                    ${data.retrieved_chunks ? `<span class="badge bg-secondary">${data.retrieved_chunks} sources</span>` : ''}
                </div>
            `;
        }
        
        messageDiv.innerHTML = `
            <div class="message-content">
                <i class="fas fa-robot message-icon"></i>
                <div class="message-text">
                    <p>${this.escapeHtml(data.answer)}</p>
                    ${citationsHtml}
                    ${metaHtml}
                </div>
            </div>
        `;
        
        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
    }
    
    setFormEnabled(enabled) {
        this.questionInput.disabled = !enabled;
        this.sendButton.disabled = !enabled;
        
        if (enabled) {
            this.sendButton.innerHTML = '<i class="fas fa-paper-plane"></i>';
        } else {
            this.sendButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
        }
    }
    
    showLoading(show) {
        if (show) {
            this.loadingModal.show();
        } else {
            this.loadingModal.hide();
        }
    }
    
    scrollToBottom() {
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    async checkSystemHealth() {
        try {
            const response = await fetch('/health');
            const data = await response.json();
            
            const statusElement = document.getElementById('systemStatus');
            
            if (response.ok && data.status === 'healthy') {
                statusElement.innerHTML = '<span class="badge bg-success">Online</span>';
            } else {
                statusElement.innerHTML = '<span class="badge bg-danger">Offline</span>';
            }
        } catch (error) {
            console.error('Health check failed:', error);
            document.getElementById('systemStatus').innerHTML = '<span class="badge bg-danger">Error</span>';
        }
    }
    
    async loadSystemStats() {
        try {
            const response = await fetch('/api/stats');
            const data = await response.json();
            
            const statsElement = document.getElementById('systemStats');
            
            if (response.ok) {
                statsElement.innerHTML = `
                    <div class="small">
                        <div><strong>Documents:</strong> ${data.total_documents}</div>
                        <div><strong>Model:</strong> ${data.llm_model}</div>
                        <div><strong>Embeddings:</strong> ${data.embedding_model}</div>
                    </div>
                `;
            } else {
                statsElement.innerHTML = '<small class="text-danger">Failed to load</small>';
            }
        } catch (error) {
            console.error('Stats loading failed:', error);
            document.getElementById('systemStats').innerHTML = '<small class="text-danger">Error loading stats</small>';
        }
    }
    
    updateRecentSources(sources) {
        const sourcesElement = document.getElementById('recentSources');
        
        if (sources.length === 0) {
            sourcesElement.innerHTML = '<small class="text-muted">No sources</small>';
            return;
        }
        
        const uniqueSources = [...new Set(sources)];
        const sourceLinks = uniqueSources.slice(0, 5).map(source => {
            const filename = source.split('/').pop().split('\\').pop();
            const displayName = filename.replace('.md', '').replace(/-/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
            return `<a href="/policy/${filename}" target="_blank" class="source-link" title="${source}">
                ${displayName}
                <i class="fas fa-external-link-alt" style="font-size: 0.8em; margin-left: 4px;"></i>
            </a>`;
        }).join('');
        
        sourcesElement.innerHTML = sourceLinks;
    }
}

// Initialize the chat application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new PolicyChat();
});

// Add some utility functions for potential future use
window.PolicyChatUtils = {
    formatTimestamp: (timestamp) => {
        return new Date(timestamp).toLocaleTimeString();
    },
    
    copyToClipboard: async (text) => {
        try {
            await navigator.clipboard.writeText(text);
            return true;
        } catch (err) {
            console.error('Failed to copy text: ', err);
            return false;
        }
    },
    
    downloadChat: () => {
        const messages = document.querySelectorAll('.message');
        let chatText = 'Company Policies Chat Export\n';
        chatText += '================================\n\n';
        
        messages.forEach((message, index) => {
            const isUser = message.classList.contains('user-message');
            const text = message.querySelector('.message-text p').textContent;
            chatText += `${isUser ? 'User' : 'Assistant'}: ${text}\n\n`;
        });
        
        const blob = new Blob([chatText], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `chat-export-${new Date().toISOString().split('T')[0]}.txt`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }
};