// Pricing page functionality
document.getElementById('upgrade-btn')?.addEventListener('click', async () => {
    const btn = document.getElementById('upgrade-btn');
    const originalText = btn.textContent;
    
    try {
        btn.disabled = true;
        btn.textContent = 'Processing...';
        
        const response = await fetch(`${API_BASE}/api/payments/create-checkout-session`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify({ tier: 'premium' })
        });
        
        const data = await response.json();
        
        if (data.success && data.url) {
            showToast('Redirecting to checkout...', 'success');
            window.location.href = data.url;
        } else if (data.redirect) {
            showToast(data.error || 'Please log in first', 'warning');
            setTimeout(() => window.location.href = data.redirect, 1500);
        } else if (data.demo_mode) {
            showToast('Payment system not configured yet. This is a demo environment.', 'info');
            btn.disabled = false;
            btn.textContent = originalText;
        } else {
            showToast(data.error || 'Failed to create checkout session', 'error');
            btn.disabled = false;
            btn.textContent = originalText;
        }
    } catch (error) {
        console.error('Checkout error:', error);
        showToast('Unable to connect to payment system. Please try again later.', 'error');
        btn.disabled = false;
        btn.textContent = originalText;
    }
});
