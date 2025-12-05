// Settings page functionality
document.addEventListener('DOMContentLoaded', async () => {
    await loadUserProfile();
    await loadPreferences();
    
    document.getElementById('profile-form')?.addEventListener('submit', saveProfile);
    document.getElementById('preferences-form')?.addEventListener('submit', savePreferences);
});

async function loadUserProfile() {
    try {
        const response = await fetch(`${API_BASE}/api/users/me`, {
            credentials: 'include'
        });
        
        if (response.ok) {
            const user = await response.json();
            document.getElementById('full-name').value = user.full_name || '';
            document.getElementById('email').value = user.email;
            
            // Store user_id for WebSocket
            localStorage.setItem('user_id', user.id);
            
            // Update subscription info
            document.getElementById('current-plan').textContent = user.is_premium ? 'Premium' : 'Free';
        }
    } catch (error) {
        console.error('Failed to load profile:', error);
    }
}

async function loadPreferences() {
    try {
        const response = await fetch(`${API_BASE}/api/users/preferences`, {
            credentials: 'include'
        });
        
        if (response.ok) {
            const prefs = await response.json();
            document.getElementById('sensitivity').value = prefs.gesture_sensitivity;
            document.getElementById('voice-id').value = prefs.preferred_voice_id;
        }
    } catch (error) {
        console.error('Failed to load preferences:', error);
    }
}

async function saveProfile(e) {
    e.preventDefault();
    
    const data = {
        full_name: document.getElementById('full-name').value
    };
    
    try {
        const response = await fetch(`${API_BASE}/api/users/me`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify(data)
        });
        
        if (response.ok) {
            showToast('Profile updated successfully', 'success');
        } else {
            showToast('Failed to update profile', 'error');
        }
    } catch (error) {
        showToast('Failed to update profile', 'error');
    }
}

async function savePreferences(e) {
    e.preventDefault();
    
    const data = {
        gesture_sensitivity: document.getElementById('sensitivity').value,
        preferred_voice_id: document.getElementById('voice-id').value
    };
    
    try {
        const response = await fetch(`${API_BASE}/api/users/preferences`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify(data)
        });
        
        if (response.ok) {
            showToast('Preferences updated successfully', 'success');
        } else {
            showToast('Failed to update preferences', 'error');
        }
    } catch (error) {
        showToast('Failed to update preferences', 'error');
    }
}
