// WebSocket client for real-time gesture streaming
class WebSocketClient {
    constructor() {
        this.ws = null;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        this.reconnectDelay = 1000;
    }
    
    connect() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${window.location.host}/api/gestures/ws`;
        
        this.ws = new WebSocket(wsUrl);
        
        this.ws.onopen = () => {
            console.log('WebSocket connected');
            this.reconnectAttempts = 0;
            showToast('Connected to gesture service', 'success');
        };
        
        this.ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.handleGestureResponse(data);
        };
        
        this.ws.onerror = (error) => {
            console.error('WebSocket error:', error);
        };
        
        this.ws.onclose = () => {
            console.log('WebSocket disconnected');
            this.attemptReconnect();
        };
    }
    
    disconnect() {
        if (this.ws) {
            this.ws.close();
            this.ws = null;
        }
    }
    
    isConnected() {
        return this.ws && this.ws.readyState === WebSocket.OPEN;
    }
    
    sendGesture(type, data) {
        if (!this.isConnected()) {
            console.warn('WebSocket not connected');
            return;
        }
        
        // Get user_id from session (would be set during auth)
        const userId = localStorage.getItem('user_id') || 1;
        
        const message = {
            user_id: userId,
            gesture_type: type,
            data: data
        };
        
        this.ws.send(JSON.stringify(message));
    }
    
    handleGestureResponse(data) {
        console.log('Gesture processed:', data);
        
        // Update UI
        const outputText = document.getElementById('output-text');
        if (outputText && data.text) {
            outputText.innerHTML = `<p class="text-2xl font-bold">${data.text}</p>`;
        }
        
        const lastGesture = document.getElementById('last-gesture');
        if (lastGesture) {
            lastGesture.textContent = data.intention || 'Unknown';
        }
        
        const confidence = document.getElementById('confidence');
        if (confidence && data.confidence !== undefined) {
            confidence.textContent = `${Math.round(data.confidence * 100)}%`;
        }
        
        // Play audio
        if (data.audio_url) {
            const audioPlayer = document.getElementById('audio-player');
            if (audioPlayer) {
                audioPlayer.src = data.audio_url;
                audioPlayer.play();
            }
        }
        
        // Add to history
        this.addToHistory(data);
    }
    
    addToHistory(data) {
        const historyList = document.getElementById('gesture-history');
        if (!historyList) return;
        
        const item = document.createElement('div');
        item.className = 'bg-gray-50 p-4 rounded-lg';
        item.innerHTML = `
            <div class="flex justify-between items-center">
                <div>
                    <p class="font-semibold">${data.text || 'Unknown'}</p>
                    <p class="text-sm text-gray-600">
                        ${data.intention} • ${Math.round(data.confidence * 100)}% confidence
                    </p>
                </div>
                <span class="text-xs text-gray-400">${new Date().toLocaleTimeString()}</span>
            </div>
        `;
        
        historyList.insertBefore(item, historyList.firstChild);
        
        // Keep only last 10 items
        while (historyList.children.length > 10) {
            historyList.removeChild(historyList.lastChild);
        }
    }
    
    attemptReconnect() {
        if (this.reconnectAttempts >= this.maxReconnectAttempts) {
            showToast('Failed to reconnect. Please refresh the page.', 'error');
            return;
        }
        
        this.reconnectAttempts++;
        const delay = this.reconnectDelay * Math.pow(2, this.reconnectAttempts - 1);
        
        console.log(`Reconnecting in ${delay}ms (attempt ${this.reconnectAttempts})`);
        
        setTimeout(() => {
            this.connect();
        }, delay);
    }
}

// Initialize global WebSocket client
window.wsClient = new WebSocketClient();
