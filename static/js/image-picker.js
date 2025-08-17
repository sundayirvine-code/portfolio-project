/**
 * Image Picker Widget - Handles file upload and Base64 conversion
 */

document.addEventListener('DOMContentLoaded', function() {
    initializeImagePickers();
});

function initializeImagePickers() {
    const imagePickerContainers = document.querySelectorAll('.image-picker-container');
    
    imagePickerContainers.forEach(container => {
        setupImagePicker(container);
    });
}

function setupImagePicker(container) {
    const fileInput = container.querySelector('.image-file-input');
    const textarea = container.querySelector('textarea');
    const previewContainer = container.querySelector('.image-preview-container');
    const previewImg = container.querySelector('.image-preview');
    const removeBtn = container.querySelector('.remove-image');
    const toggleBtn = container.querySelector('.toggle-base64');
    const base64Container = container.querySelector('.base64-container');
    
    // Initialize display state
    updatePreviewDisplay();
    
    // File input change handler
    if (fileInput) {
        fileInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                handleImageFile(file);
            }
        });
    }
    
    // Remove image handler
    if (removeBtn) {
        removeBtn.addEventListener('click', function() {
            clearImage();
        });
    }
    
    // Toggle base64 visibility
    if (toggleBtn) {
        toggleBtn.addEventListener('click', function() {
            textarea.classList.toggle('d-none');
        });
    }
    
    // Monitor textarea changes
    if (textarea) {
        textarea.addEventListener('input', function() {
            updatePreviewFromBase64();
        });
    }
    
    function handleImageFile(file) {
        // Validate file type
        if (!file.type.startsWith('image/')) {
            alert('Please select a valid image file.');
            return;
        }
        
        // Validate file size (2MB limit)
        const maxSize = 2 * 1024 * 1024; // 2MB
        if (file.size > maxSize) {
            alert('Image file is too large. Please select an image smaller than 2MB.');
            return;
        }
        
        // Read file and convert to base64
        const reader = new FileReader();
        reader.onload = function(e) {
            const base64Data = e.target.result;
            textarea.value = base64Data;
            updatePreviewDisplay();
        };
        reader.onerror = function() {
            alert('Error reading file. Please try again.');
        };
        reader.readAsDataURL(file);
    }
    
    function updatePreviewDisplay() {
        const base64Data = textarea.value.trim();
        
        if (base64Data && isValidBase64Image(base64Data)) {
            previewImg.src = base64Data;
            previewContainer.style.display = 'block';
        } else {
            previewContainer.style.display = 'none';
        }
    }
    
    function updatePreviewFromBase64() {
        setTimeout(updatePreviewDisplay, 100); // Small delay for input processing
    }
    
    function clearImage() {
        textarea.value = '';
        previewContainer.style.display = 'none';
        if (fileInput) {
            fileInput.value = '';
        }
    }
    
    function isValidBase64Image(str) {
        if (!str) return false;
        
        // Check for data URL format
        if (str.startsWith('data:image/')) {
            return true;
        }
        
        // Check for raw base64 (basic validation)
        try {
            return btoa(atob(str)) === str;
        } catch (err) {
            return false;
        }
    }
}

// Utility function to compress image if needed
function compressImage(file, maxWidth = 800, quality = 0.8) {
    return new Promise((resolve) => {
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        const img = new Image();
        
        img.onload = function() {
            // Calculate new dimensions
            let { width, height } = img;
            if (width > maxWidth) {
                height = (height * maxWidth) / width;
                width = maxWidth;
            }
            
            // Set canvas size
            canvas.width = width;
            canvas.height = height;
            
            // Draw and compress
            ctx.drawImage(img, 0, 0, width, height);
            const compressedBase64 = canvas.toDataURL('image/jpeg', quality);
            resolve(compressedBase64);
        };
        
        img.src = URL.createObjectURL(file);
    });
}

// Auto-initialize for dynamically added elements
const observer = new MutationObserver(function(mutations) {
    mutations.forEach(function(mutation) {
        mutation.addedNodes.forEach(function(node) {
            if (node.nodeType === 1) { // Element node
                const containers = node.querySelectorAll ? 
                    node.querySelectorAll('.image-picker-container') : [];
                containers.forEach(setupImagePicker);
            }
        });
    });
});

observer.observe(document.body, {
    childList: true,
    subtree: true
});