/**
 * Portfolio - Font Size Management System
 * Handles dynamic font size scaling and accessibility features
 */

(function() {
    'use strict';
    
    // Font size configuration
    const FONT_SIZE_SETTINGS = {
        'extra-small': {
            name: 'Extra Small',
            scale: 0.8,
            baseSize: '14px',
            description: 'Compact text for dense content'
        },
        'small': {
            name: 'Small', 
            scale: 0.9,
            baseSize: '15px',
            description: 'Slightly smaller for more content'
        },
        'normal': {
            name: 'Normal',
            scale: 1.0,
            baseSize: '16px',
            description: 'Standard readable size'
        },
        'large': {
            name: 'Large',
            scale: 1.1,
            baseSize: '18px',
            description: 'Larger for better readability'
        },
        'extra-large': {
            name: 'Extra Large',
            scale: 1.25,
            baseSize: '20px',
            description: 'Maximum size for accessibility'
        }
    };
    
    // Current font size settings
    let currentFontSize = 'normal';
    let currentBaseSize = '16px';
    let currentHeadingScale = 1.25;
    let currentSmallScale = 0.875;
    
    // DOM elements
    let fontSizePicker;
    let fontSizeVariablesStyle;
    
    /**
     * Initialize font size system
     */
    function init() {
        // Cache DOM elements
        cacheFontSizeElements();
        
        // Load saved font size preferences
        loadFontSizePreferences();
        
        // Load server-side font size settings
        loadServerFontSettings();
        
        // Apply initial font sizes
        applyFontSizes();
        
        // Create font size picker if needed
        createFontSizePicker();
        
        // Set up event listeners
        setupFontSizeEventListeners();
        
        console.log('Font size management system initialized 📏');
    }
    
    /**
     * Cache DOM elements
     */
    function cacheFontSizeElements() {
        fontSizeVariablesStyle = document.getElementById('font-size-variables') || createFontSizeVariablesStyle();
    }
    
    /**
     * Create font size variables style element
     */
    function createFontSizeVariablesStyle() {
        const style = document.createElement('style');
        style.id = 'font-size-variables';
        document.head.appendChild(style);
        return style;
    }
    
    /**
     * Load font size preferences from localStorage
     */
    function loadFontSizePreferences() {
        const savedFontSize = localStorage.getItem('portfolio-font-size');
        if (savedFontSize && FONT_SIZE_SETTINGS[savedFontSize]) {
            currentFontSize = savedFontSize;
        }
    }
    
    /**
     * Load server-side font settings from site configuration
     */
    function loadServerFontSettings() {
        if (window.SITE_CONFIG) {
            if (window.SITE_CONFIG.BASE_FONT_SIZE) {
                currentBaseSize = window.SITE_CONFIG.BASE_FONT_SIZE;
            }
            if (window.SITE_CONFIG.HEADING_FONT_SCALE) {
                currentHeadingScale = window.SITE_CONFIG.HEADING_FONT_SCALE;
            }
            if (window.SITE_CONFIG.SMALL_FONT_SCALE) {
                currentSmallScale = window.SITE_CONFIG.SMALL_FONT_SCALE;
            }
        }
    }
    
    /**
     * Set up event listeners
     */
    function setupFontSizeEventListeners() {
        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            // Alt + S for font size picker
            if (e.altKey && e.code === 'KeyS') {
                e.preventDefault();
                toggleFontSizePicker();
            }
            
            // Alt + Plus for increase font size
            if (e.altKey && (e.code === 'Equal' || e.code === 'NumpadAdd')) {
                e.preventDefault();
                increaseFontSize();
            }
            
            // Alt + Minus for decrease font size
            if (e.altKey && (e.code === 'Minus' || e.code === 'NumpadSubtract')) {
                e.preventDefault();
                decreaseFontSize();
            }
            
            // Alt + 0 for reset font size
            if (e.altKey && (e.code === 'Digit0' || e.code === 'Numpad0')) {
                e.preventDefault();
                resetFontSize();
            }
        });
    }
    
    /**
     * Apply current font sizes
     */
    function applyFontSizes() {
        const setting = FONT_SIZE_SETTINGS[currentFontSize];
        if (!setting) return;
        
        // Calculate actual sizes based on base size and scales
        const basePixels = parseFloat(currentBaseSize);
        const scaledBase = basePixels * setting.scale;
        
        // Update CSS variables
        updateFontSizeVariables(scaledBase);
        
        // Save preferences
        saveFontSizePreferences();
        
        // Dispatch font size change event
        dispatchFontSizeChangeEvent();
    }
    
    /**
     * Update CSS variables for current font sizes
     */
    function updateFontSizeVariables(scaledBase) {
        if (!fontSizeVariablesStyle) return;
        
        const css = `
            :root {
                /* Font Size Variables */
                --font-size-base: ${scaledBase}px;
                --font-size-xs: ${scaledBase * 0.75}px;
                --font-size-sm: ${scaledBase * currentSmallScale}px;
                --font-size-lg: ${scaledBase * 1.125}px;
                --font-size-xl: ${scaledBase * 1.25}px;
                
                /* Heading Sizes */
                --font-size-h1: ${scaledBase * currentHeadingScale * 2.5}px;
                --font-size-h2: ${scaledBase * currentHeadingScale * 2}px;
                --font-size-h3: ${scaledBase * currentHeadingScale * 1.75}px;
                --font-size-h4: ${scaledBase * currentHeadingScale * 1.5}px;
                --font-size-h5: ${scaledBase * currentHeadingScale * 1.25}px;
                --font-size-h6: ${scaledBase * currentHeadingScale}px;
                
                /* Display Sizes */
                --font-size-display-1: ${scaledBase * currentHeadingScale * 6}px;
                --font-size-display-2: ${scaledBase * currentHeadingScale * 5.5}px;
                --font-size-display-3: ${scaledBase * currentHeadingScale * 4.5}px;
                --font-size-display-4: ${scaledBase * currentHeadingScale * 3.5}px;
            }
            
            /* Apply font sizes to elements */
            body {
                font-size: var(--font-size-base) !important;
            }
            
            h1, .h1 { font-size: var(--font-size-h1) !important; }
            h2, .h2 { font-size: var(--font-size-h2) !important; }
            h3, .h3 { font-size: var(--font-size-h3) !important; }
            h4, .h4 { font-size: var(--font-size-h4) !important; }
            h5, .h5 { font-size: var(--font-size-h5) !important; }
            h6, .h6 { font-size: var(--font-size-h6) !important; }
            
            .display-1 { font-size: var(--font-size-display-1) !important; }
            .display-2 { font-size: var(--font-size-display-2) !important; }
            .display-3 { font-size: var(--font-size-display-3) !important; }
            .display-4 { font-size: var(--font-size-display-4) !important; }
            
            .fs-1 { font-size: var(--font-size-xl) !important; }
            .fs-2 { font-size: var(--font-size-lg) !important; }
            .fs-3 { font-size: var(--font-size-base) !important; }
            .fs-4 { font-size: var(--font-size-sm) !important; }
            .fs-5 { font-size: var(--font-size-xs) !important; }
            
            small, .small { font-size: var(--font-size-sm) !important; }
        `;
        
        fontSizeVariablesStyle.textContent = css;
    }
    
    /**
     * Change font size setting
     */
    function changeFontSize(sizeKey) {
        if (!FONT_SIZE_SETTINGS[sizeKey]) return;
        
        currentFontSize = sizeKey;
        applyFontSizes();
        
        // Update font size picker selection
        updateFontSizePickerSelection();
        
        // Show feedback
        showFontSizeChangeFeedback(FONT_SIZE_SETTINGS[sizeKey].name);
    }
    
    /**
     * Increase font size
     */
    function increaseFontSize() {
        const sizeKeys = Object.keys(FONT_SIZE_SETTINGS);
        const currentIndex = sizeKeys.indexOf(currentFontSize);
        const nextIndex = Math.min(currentIndex + 1, sizeKeys.length - 1);
        
        if (nextIndex !== currentIndex) {
            changeFontSize(sizeKeys[nextIndex]);
        }
    }
    
    /**
     * Decrease font size
     */
    function decreaseFontSize() {
        const sizeKeys = Object.keys(FONT_SIZE_SETTINGS);
        const currentIndex = sizeKeys.indexOf(currentFontSize);
        const prevIndex = Math.max(currentIndex - 1, 0);
        
        if (prevIndex !== currentIndex) {
            changeFontSize(sizeKeys[prevIndex]);
        }
    }
    
    /**
     * Reset font size to normal
     */
    function resetFontSize() {
        changeFontSize('normal');
    }
    
    /**
     * Show font size change feedback
     */
    function showFontSizeChangeFeedback(sizeName) {
        const feedback = document.createElement('div');
        feedback.className = 'position-fixed top-50 start-50 translate-middle bg-success text-white px-3 py-2 rounded shadow';
        feedback.style.zIndex = '9999';
        feedback.innerHTML = `
            <i class="bi bi-type me-2"></i>
            Font Size: ${sizeName}
        `;
        
        document.body.appendChild(feedback);
        
        setTimeout(() => {
            feedback.remove();
        }, 2000);
    }
    
    /**
     * Create font size picker UI
     */
    function createFontSizePicker() {
        fontSizePicker = document.createElement('div');
        fontSizePicker.className = 'font-size-picker';
        fontSizePicker.innerHTML = `
            <button class="font-size-picker-toggle" onclick="window.FontSizeManager.toggleFontSizePicker()" title="Font Size (Alt+S)">
                <i class="bi bi-type"></i>
            </button>
            <div class="p-3">
                <h6 class="mb-3">Font Size</h6>
                <div class="font-size-options">
                    ${Object.entries(FONT_SIZE_SETTINGS).map(([key, setting]) => `
                        <div class="font-size-option ${key === currentFontSize ? 'active' : ''}" 
                             data-size="${key}"
                             title="${setting.description}"
                             onclick="window.FontSizeManager.changeFontSize('${key}')">
                            <div class="font-size-preview" style="font-size: ${setting.baseSize};">
                                <div class="font-size-demo">Aa</div>
                                <div class="font-size-name">${setting.name}</div>
                            </div>
                        </div>
                    `).join('')}
                </div>
                <hr class="my-3">
                <div class="font-size-controls">
                    <button class="btn btn-sm btn-outline-secondary me-2" onclick="window.FontSizeManager.decreaseFontSize()">
                        <i class="bi bi-dash-lg"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-secondary me-2" onclick="window.FontSizeManager.resetFontSize()">
                        <i class="bi bi-arrow-clockwise"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-secondary" onclick="window.FontSizeManager.increaseFontSize()">
                        <i class="bi bi-plus-lg"></i>
                    </button>
                </div>
                <div class="font-size-info mt-3">
                    <small class="text-muted">
                        <strong>Keyboard Shortcuts:</strong><br>
                        Alt + S: Toggle size picker<br>
                        Alt + Plus/Minus: Resize<br>
                        Alt + 0: Reset to normal
                    </small>
                </div>
            </div>
        `;
        
        document.body.appendChild(fontSizePicker);
    }
    
    /**
     * Toggle font size picker visibility
     */
    function toggleFontSizePicker() {
        if (fontSizePicker) {
            fontSizePicker.classList.toggle('show');
        }
    }
    
    /**
     * Update font size picker selection
     */
    function updateFontSizePickerSelection() {
        if (!fontSizePicker) return;
        
        const sizeOptions = fontSizePicker.querySelectorAll('.font-size-option');
        sizeOptions.forEach(option => {
            option.classList.toggle('active', option.dataset.size === currentFontSize);
        });
    }
    
    /**
     * Save font size preferences to localStorage
     */
    function saveFontSizePreferences() {
        localStorage.setItem('portfolio-font-size', currentFontSize);
    }
    
    /**
     * Dispatch font size change event for other scripts
     */
    function dispatchFontSizeChangeEvent() {
        const event = new CustomEvent('fontsizechange', {
            detail: {
                fontSize: currentFontSize,
                setting: FONT_SIZE_SETTINGS[currentFontSize],
                baseSize: currentBaseSize,
                headingScale: currentHeadingScale,
                smallScale: currentSmallScale
            }
        });
        
        document.dispatchEvent(event);
    }
    
    /**
     * Get current font size information
     */
    function getCurrentFontSize() {
        return {
            fontSize: currentFontSize,
            setting: FONT_SIZE_SETTINGS[currentFontSize],
            baseSize: currentBaseSize,
            headingScale: currentHeadingScale,
            smallScale: currentSmallScale
        };
    }
    
    /**
     * Apply font size from external source (like admin panel)
     */
    function applyExternalFontSize(sizeKey) {
        if (FONT_SIZE_SETTINGS[sizeKey]) {
            currentFontSize = sizeKey;
            applyFontSizes();
            updateFontSizePickerSelection();
        }
    }
    
    /**
     * Update server-side font settings
     */
    function updateServerFontSettings(baseSize, headingScale, smallScale) {
        if (baseSize) currentBaseSize = baseSize;
        if (headingScale) currentHeadingScale = headingScale;
        if (smallScale) currentSmallScale = smallScale;
        
        applyFontSizes();
    }
    
    /**
     * Export public API
     */
    window.FontSizeManager = {
        init,
        changeFontSize,
        increaseFontSize,
        decreaseFontSize,
        resetFontSize,
        toggleFontSizePicker,
        getCurrentFontSize,
        applyExternalFontSize,
        updateServerFontSettings,
        FONT_SIZE_SETTINGS
    };
    
    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
    
    // Listen for font size change requests from other parts of the app
    document.addEventListener('requestFontSizeChange', (e) => {
        if (e.detail.fontSize) {
            changeFontSize(e.detail.fontSize);
        }
    });
    
})();