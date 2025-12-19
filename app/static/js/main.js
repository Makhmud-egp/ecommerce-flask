// Loading spinner
function showLoading() {
    const spinner = document.createElement('div');
    spinner.id = 'loading-spinner';
    spinner.innerHTML = `
        <div style="position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                    background: rgba(0,0,0,0.5); display: flex; align-items: center;
                    justify-content: center; z-index: 9999;">
            <div style="background: white; padding: 2rem; border-radius: 8px;">
                <div style="border: 4px solid #f3f3f3; border-top: 4px solid #3498db;
                            border-radius: 50%; width: 40px; height: 40px;
                            animation: spin 1s linear infinite;"></div>
            </div>
        </div>
    `;
    document.body.appendChild(spinner);
}

function hideLoading() {
    const spinner = document.getElementById('loading-spinner');
    if (spinner) spinner.remove();
}

// CSS animation
const style = document.createElement('style');
style.innerHTML = `
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
`;
document.head.appendChild(style);

// API call with error handling
async function apiCall(url, options = {}) {
    showLoading();

    try {
        const response = await fetch(url, options);
        const data = await response.json();

        hideLoading();

        if (!response.ok) {
            throw new Error(data.error || 'Something went wrong');
        }

        return data;
    } catch (error) {
        hideLoading();
        alert('Error: ' + error.message);
        throw error;
    }
}