// Tagging interface functionality

let currentImage = null;
let imagesTagged = 0;

// DOM elements
const loadingEl = document.getElementById('loading');
const noImagesEl = document.getElementById('no-images');
const imageContainerEl = document.getElementById('image-container');
const currentImageEl = document.getElementById('current-image');
const imageSourceEl = document.getElementById('image-source');
const imageGeneratorEl = document.getElementById('image-generator');
const imagePromptEl = document.getElementById('image-prompt');
const imageTagsEl = document.getElementById('image-tags');
const likeCountEl = document.getElementById('like-count');
const shareCountEl = document.getElementById('share-count');
const notesEl = document.getElementById('notes');
const submitBtn = document.getElementById('submit-btn');
const noBiasBtn = document.getElementById('no-bias-btn');
const progressText = document.getElementById('progress-text');

// Load next image
async function loadNextImage() {
    try {
        // Show loading
        loadingEl.style.display = 'block';
        imageContainerEl.style.display = 'none';
        noImagesEl.style.display = 'none';
        
        // Clear previous selections
        document.querySelectorAll('input[name="bias"]').forEach(cb => cb.checked = false);
        notesEl.value = '';
        
        // Fetch next image
        const data = await apiCall('/api/next-image');
        
        if (data.has_more && data.image) {
            currentImage = data.image;
            displayImage(data.image);
        } else {
            showNoImages();
        }
    } catch (error) {
        if (error.message.includes('No more images')) {
            showNoImages();
        } else {
            showNotification('Error loading image: ' + error.message, 'error');
        }
    }
}

// Display image
function displayImage(image) {
    // Use media_url if available, fallback to url
    const imageUrl = image.media_url || image.url || '';
    currentImageEl.src = imageUrl;
    currentImageEl.alt = image.prompt || 'AI Generated Image';
    
    // Generate fictional data
    const sources = ['CGDream', 'Gencraft', 'CivitAI'];
    const generators = ['DALL-E 2', 'DALL-E 3', 'Stable Diffusion', 'Stable Diffusion XL', 'Midjourney', 'FLUX', 'Firefly', 'Leonardo AI'];
    const randomSource = sources[Math.floor(Math.random() * sources.length)];
    const randomGenerator = generators[Math.floor(Math.random() * generators.length)];
    const randomLikes = Math.floor(Math.random() * 350) + 1;
    const randomShares = Math.floor(Math.random() * 225) + 1;
    
    imageSourceEl.textContent = randomSource;
    imageGeneratorEl.textContent = randomGenerator;
    imagePromptEl.textContent = image.prompt || 'No prompt available';
    
    const tags = Array.isArray(image.tags) ? image.tags : [];
    imageTagsEl.textContent = tags.length > 0 ? tags.join(', ') : 'None';
    
    likeCountEl.textContent = randomLikes;
    shareCountEl.textContent = randomShares;
    
    loadingEl.style.display = 'none';
    imageContainerEl.style.display = 'block';
}

// Show no images message
function showNoImages() {
    loadingEl.style.display = 'none';
    imageContainerEl.style.display = 'none';
    noImagesEl.style.display = 'block';
}

// Submit bias tags
async function submitTags() {
    if (!currentImage) return;
    
    const checkboxes = document.querySelectorAll('input[name="bias"]:checked');
    const biasTags = Array.from(checkboxes).map(cb => cb.value);
    const notes = notesEl.value.trim();
    
    if (biasTags.length === 0) {
        showNotification('Please select at least one bias type or click "No Bias"', 'error');
        return;
    }
    
    try {
        submitBtn.disabled = true;
        submitBtn.textContent = 'Submitting...';
        
        await apiCall('/api/submit-tags', {
            method: 'POST',
            body: JSON.stringify({
                image_id: currentImage.id,
                bias_tags: biasTags,
                notes: notes
            })
        });
        
        imagesTagged++;
        updateProgress();
        showNotification('Tags submitted successfully!', 'success');
        
        // Load next image
        setTimeout(() => loadNextImage(), 500);
        
    } catch (error) {
        showNotification('Error submitting tags: ' + error.message, 'error');
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Submit Tags';
    }
}

// Skip image (no bias)
async function skipImage() {
    if (!currentImage) return;
    
    try {
        noBiasBtn.disabled = true;
        noBiasBtn.textContent = 'Skipping...';
        
        await apiCall('/api/skip-image', {
            method: 'POST',
            body: JSON.stringify({
                image_id: currentImage.id
            })
        });
        
        imagesTagged++;
        updateProgress();
        
        // Load next image
        loadNextImage();
        
    } catch (error) {
        showNotification('Error skipping image: ' + error.message, 'error');
    } finally {
        noBiasBtn.disabled = false;
        noBiasBtn.textContent = 'No Bias - Next Image';
    }
}

// Update progress
function updateProgress() {
    progressText.innerHTML = `Images tagged this session: <strong>${imagesTagged}</strong>`;
}

// Event listeners
submitBtn.addEventListener('click', submitTags);
noBiasBtn.addEventListener('click', skipImage);

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && e.ctrlKey) {
        submitTags();
    } else if (e.key === 'ArrowRight' && e.ctrlKey) {
        skipImage();
    }
});

// Load first image on page load
loadNextImage();
