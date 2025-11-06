// Dashboard functionality

// DOM elements
const loadingEl = document.getElementById('loading');
const statsContainer = document.getElementById('stats-container');

// Load statistics
async function loadStatistics() {
    try {
        loadingEl.style.display = 'block';
        statsContainer.style.display = 'none';
        
        const stats = await apiCall('/api/statistics');
        
        displayStatistics(stats);
        
        loadingEl.style.display = 'none';
        statsContainer.style.display = 'block';
        
    } catch (error) {
        showNotification('Error loading statistics: ' + error.message, 'error');
        loadingEl.style.display = 'none';
    }
}

// Display statistics
function displayStatistics(stats) {
    // Update stat cards
    document.getElementById('total-images').textContent = stats.total_images || 0;
    document.getElementById('total-views').textContent = stats.total_views || 0;
    document.getElementById('tagged-images').textContent = stats.tagged_images || 0;
    
    // Calculate percentage
    const percentage = stats.total_images > 0 
        ? Math.round((stats.tagged_images / stats.total_images) * 100) 
        : 0;
    document.getElementById('bias-percentage').textContent = percentage + '%';
    
    // Display bias type breakdown
    displayBiasChart(stats.bias_types || []);
    
    // Display recent tagged images
    displayRecentImages(stats.recent_tagged || []);
}

// Display bias chart
function displayBiasChart(biasTypes) {
    const chartContainer = document.getElementById('bias-chart');
    chartContainer.innerHTML = '';
    
    if (biasTypes.length === 0) {
        chartContainer.innerHTML = '<p style="text-align: center; color: var(--text-secondary);">No bias tags yet</p>';
        return;
    }
    
    // Find max count for scaling
    const maxCount = Math.max(...biasTypes.map(b => b.count));
    
    // Create bars
    biasTypes.forEach(bias => {
        const barDiv = document.createElement('div');
        barDiv.className = 'bias-bar';
        
        const percentage = (bias.count / maxCount) * 100;
        
        barDiv.innerHTML = `
            <div class="bias-bar-label">
                <span>${formatBiasType(bias.bias_type)}</span>
                <span>${bias.count} tag${bias.count !== 1 ? 's' : ''}</span>
            </div>
            <div style="background: #e2e8f0; border-radius: 8px; overflow: hidden;">
                <div class="bias-bar-fill" style="width: ${percentage}%"></div>
            </div>
        `;
        
        chartContainer.appendChild(barDiv);
    });
}

// Display recent images
function displayRecentImages(images) {
    const container = document.getElementById('recent-images');
    container.innerHTML = '';
    
    if (images.length === 0) {
        container.innerHTML = '<p style="text-align: center; color: var(--text-secondary);">No tagged images yet</p>';
        return;
    }
    
    images.forEach(image => {
        const card = document.createElement('div');
        card.className = 'image-card';
        
        const biasTypesList = image.bias_types ? image.bias_types.split(',') : [];
        const biasTagsHtml = biasTypesList
            .map(type => `<span class="bias-tag">${formatBiasType(type.trim())}</span>`)
            .join('');
        
        card.innerHTML = `
            <img src="${image.url}" alt="${image.prompt || 'AI Generated Image'}">
            <div class="image-card-info">
                <div style="font-size: 0.75rem; color: var(--text-secondary); margin-bottom: 0.5rem;">
                    ${truncateText(image.prompt || 'No prompt', 50)}
                </div>
                <div class="bias-tags-list">
                    ${biasTagsHtml}
                </div>
            </div>
        `;
        
        container.appendChild(card);
    });
}

// Format bias type for display
function formatBiasType(type) {
    const types = {
        'ageism': 'Ageism',
        'genderism': 'Genderism',
        'ableism': 'Ableism',
        'colorism': 'Colorism'
    };
    return types[type.toLowerCase()] || type;
}

// Truncate text
function truncateText(text, maxLength) {
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
}

// Auto-refresh every 30 seconds
setInterval(loadStatistics, 30000);

// Load statistics on page load
loadStatistics();
