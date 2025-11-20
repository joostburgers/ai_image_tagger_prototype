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
    
    // Display engagement vs bias analysis
    displayEngagementChart(stats.bias_types || []);
    
    // Display most tagged image
    displayMostTaggedImage(stats.most_tagged || null);
    
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

// Display most tagged image
function displayMostTaggedImage(image) {
    const container = document.getElementById('most-tagged-image');
    container.innerHTML = '';
    
    // Use placeholder if no data
    if (!image) {
        image = {
            url: '/images/gen_01k77q60r0e4t91tcm2b29tb26.jpg',
            prompt: 'A candid photo from the early 2000s of a 20 year old American woman, standing outside a house, taken with an early 2000s digital compact camera, low resolution, slightly grainy, muted colours, soft focus, visible noise, harsh flash, slight motion blur, 2:3 aspect ratio, unedited amateur snapshot look.\nThe woman stands next to a silver 1989 Volvo 240 GL station wagon parked on the driveway of a house in a suburb. She looks at the camera and smiles, with her hands in her jacket pockets. Its snowing and the area is covered in snow, though the driveway is clear. The woman wears black rimmed glasses, a light orange parka jacket, black trousers and grey woolly gloves. Her light brown hair is in a 90s style mop top',
            bias_types: 'age,gender,race',
            tag_count: 12
        };
    }
    
    const biasTypesList = image.bias_types ? image.bias_types.split(',') : [];
    const biasTagsHtml = biasTypesList
        .map(type => `<span class="bias-tag">${formatBiasType(type.trim())}</span>`)
        .join('');
    
    const tagCount = image.tag_count || biasTypesList.length;
    
    container.innerHTML = `
        <div class="most-tagged-content">
            <div class="most-tagged-image-wrapper">
                <img src="${image.url}" alt="${image.prompt || 'AI Generated Image'}">
                <div class="tag-count-badge">${tagCount} tag${tagCount !== 1 ? 's' : ''}</div>
            </div>
            <div class="most-tagged-info">
                <div class="info-row">
                    <strong>Prompt:</strong> ${image.prompt || 'No prompt available'}
                </div>
                <div class="info-row">
                    <strong>Detected Biases:</strong>
                    <div class="bias-tags-list" style="margin-top: 0.5rem;">
                        ${biasTagsHtml}
                    </div>
                </div>
            </div>
        </div>
    `;
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
        'ageism': 'Age Discrimination',
        'genderism': 'Gender',
        'ableism': 'Ableism',
        'colorism': 'Race & Ethnicity',
        'age': 'Age Discrimination',
        'gender': 'Gender',
        'race': 'Race & Ethnicity',
        'class': 'Class & Socioeconomic Status'
    };
    return types[type.toLowerCase()] || type;
}

// Display engagement vs bias chart
function displayEngagementChart(biasTypes) {
    const chartContainer = document.getElementById('engagement-chart');
    chartContainer.innerHTML = '';
    
    if (biasTypes.length === 0) {
        chartContainer.innerHTML = '<p style="text-align: center; color: var(--text-secondary);">No data available yet</p>';
        return;
    }
    
    // Generate simulated engagement data for each bias type
    const engagementData = biasTypes.map(bias => {
        // Simulate average engagement (likes + shares) for images with this bias
        const avgEngagement = Math.floor(Math.random() * 400) + 50;
        return {
            biasType: bias.bias_type,
            count: bias.count,
            avgEngagement: avgEngagement
        };
    });
    
    // Sort by engagement (highest first)
    engagementData.sort((a, b) => b.avgEngagement - a.avgEngagement);
    
    const maxEngagement = Math.max(...engagementData.map(d => d.avgEngagement));
    
    // Create chart
    engagementData.forEach(data => {
        const barDiv = document.createElement('div');
        barDiv.className = 'engagement-bar';
        
        const percentage = (data.avgEngagement / maxEngagement) * 100;
        
        barDiv.innerHTML = `
            <div class="bias-bar-label">
                <span>${formatBiasType(data.biasType)}</span>
                <span>${data.avgEngagement} avg engagement (${data.count} images)</span>
            </div>
            <div style="background: #e2e8f0; border-radius: 8px; overflow: hidden;">
                <div class="engagement-bar-fill" style="width: ${percentage}%"></div>
            </div>
        `;
        
        chartContainer.appendChild(barDiv);
    });
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
