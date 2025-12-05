// History page functionality
document.addEventListener('DOMContentLoaded', () => {
    loadHistory();
    document.getElementById('search-btn')?.addEventListener('click', searchGestures);
});

async function loadHistory() {
    const loading = document.getElementById('loading');
    const historyList = document.getElementById('history-list');
    
    loading?.classList.remove('hidden');
    
    try {
        const response = await fetch(`${API_BASE}/api/gestures?limit=50`, {
            credentials: 'include'
        });
        
        if (response.ok) {
            const gestures = await response.json();
            displayHistory(gestures);
        } else {
            historyList.innerHTML = '<p class="text-red-500 text-center py-8">Failed to load history</p>';
        }
    } catch (error) {
        historyList.innerHTML = '<p class="text-red-500 text-center py-8">Failed to load history</p>';
    } finally {
        loading?.classList.add('hidden');
    }
}

async function searchGestures() {
    const query = document.getElementById('search-input').value;
    if (!query) {
        loadHistory();
        return;
    }
    
    const loading = document.getElementById('loading');
    const historyList = document.getElementById('history-list');
    
    loading?.classList.remove('hidden');
    
    try {
        const response = await fetch(`${API_BASE}/api/search/gestures?q=${encodeURIComponent(query)}`, {
            credentials: 'include'
        });
        
        if (response.ok) {
            const results = await response.json();
            displayHistory(results);
        }
    } catch (error) {
        console.error('Search failed:', error);
    } finally {
        loading?.classList.add('hidden');
    }
}

function displayHistory(gestures) {
    const historyList = document.getElementById('history-list');
    
    if (gestures.length === 0) {
        historyList.innerHTML = '<p class="text-gray-400 text-center py-8">No gestures found</p>';
        return;
    }
    
    historyList.innerHTML = gestures.map(gesture => `
        <div class="bg-gray-50 p-4 rounded-lg">
            <div class="flex justify-between items-start">
                <div class="flex-1">
                    <p class="text-lg font-semibold mb-1">${gesture.generated_text || 'Unknown'}</p>
                    <div class="flex items-center space-x-4 text-sm text-gray-600">
                        <span>Type: ${gesture.gesture_type}</span>
                        <span>Intention: ${gesture.intention || 'Unknown'}</span>
                        <span>Confidence: ${Math.round((gesture.confidence_score || 0) * 100)}%</span>
                    </div>
                </div>
                <div class="text-right">
                    <p class="text-sm text-gray-500">${new Date(gesture.created_at).toLocaleString()}</p>
                    ${gesture.audio_url ? `
                        <audio controls class="mt-2 h-8">
                            <source src="${gesture.audio_url}" type="audio/mpeg">
                        </audio>
                    ` : ''}
                </div>
            </div>
        </div>
    `).join('');
}
