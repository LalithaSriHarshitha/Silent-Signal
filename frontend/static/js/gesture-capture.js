// Gesture capture and detection
class GestureCapture {
    constructor() {
        this.video = document.getElementById('camera-feed');
        this.canvas = document.getElementById('gesture-canvas');
        this.ctx = this.canvas?.getContext('2d');
        this.stream = null;
        this.isCapturing = false;
        this.lastBlinkTime = 0;
        this.blinkThreshold = 500; // ms
    }
    
    async startCamera() {
        try {
            this.stream = await navigator.mediaDevices.getUserMedia({
                video: { width: 640, height: 480 }
            });
            this.video.srcObject = this.stream;
            this.isCapturing = true;
            this.updateStatus('active');
            this.detectGestures();
            return true;
        } catch (error) {
            console.error('Camera access denied:', error);
            showToast('Camera access denied', 'error');
            return false;
        }
    }
    
    stopCamera() {
        if (this.stream) {
            this.stream.getTracks().forEach(track => track.stop());
            this.stream = null;
        }
        this.isCapturing = false;
        this.updateStatus('inactive');
    }
    
    detectGestures() {
        if (!this.isCapturing) return;
        
        // Simple blink detection (placeholder - would use actual CV library)
        const now = Date.now();
        if (now - this.lastBlinkTime > this.blinkThreshold) {
            // Simulate random blink detection for demo
            if (Math.random() < 0.05) {
                this.onGestureDetected('blink', {
                    duration: 200,
                    intensity: 0.8,
                    eye: 'both',
                    timestamp: now
                });
                this.lastBlinkTime = now;
            }
        }
        
        requestAnimationFrame(() => this.detectGestures());
    }
    
    onGestureDetected(type, data) {
        console.log('Gesture detected:', type, data);
        if (window.wsClient && window.wsClient.isConnected()) {
            window.wsClient.sendGesture(type, data);
        }
    }
    
    updateStatus(status) {
        const indicator = document.getElementById('status-indicator');
        const text = document.getElementById('status-text');
        
        if (status === 'active') {
            indicator?.classList.remove('gesture-inactive');
            indicator?.classList.add('gesture-active');
            if (text) text.textContent = 'Active';
        } else {
            indicator?.classList.remove('gesture-active');
            indicator?.classList.add('gesture-inactive');
            if (text) text.textContent = 'Inactive';
        }
    }
}

// Initialize
const gestureCapture = new GestureCapture();

document.getElementById('start-capture')?.addEventListener('click', async () => {
    const success = await gestureCapture.startCamera();
    if (success) {
        document.getElementById('start-capture').classList.add('hidden');
        document.getElementById('stop-capture').classList.remove('hidden');
        
        // Connect WebSocket
        if (window.wsClient) {
            window.wsClient.connect();
        }
    }
});

document.getElementById('stop-capture')?.addEventListener('click', () => {
    gestureCapture.stopCamera();
    document.getElementById('start-capture').classList.remove('hidden');
    document.getElementById('stop-capture').classList.add('hidden');
    
    // Disconnect WebSocket
    if (window.wsClient) {
        window.wsClient.disconnect();
    }
});
