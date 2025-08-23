/**
 * Portfolio - Font Management System
 * Handles dynamic font palette switching and typography management
 */

(function() {
    'use strict';
    
    // Font palette configuration
    const FONT_PALETTES = {
        'modern-professional': {
            name: 'Modern Professional',
            description: 'Clean, readable, excellent for screens',
            heading: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif",
            body: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif",
            accent: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif",
            className: 'font-palette-modern-professional'
        },
        'creative-editorial': {
            name: 'Creative Editorial',
            description: 'Elegant serif for headers, clean sans-serif for body',
            heading: "'Playfair Display', 'Georgia', 'Times New Roman', serif",
            body: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif",
            accent: "'Playfair Display', 'Georgia', 'Times New Roman', serif",
            className: 'font-palette-creative-editorial'
        },
        'tech-minimalist': {
            name: 'Tech Minimalist',
            description: 'Modern monospace for tech-focused content',
            heading: "'JetBrains Mono', 'SF Mono', 'Monaco', 'Inconsolata', 'Roboto Mono', monospace",
            body: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif",
            accent: "'JetBrains Mono', 'SF Mono', 'Monaco', 'Inconsolata', 'Roboto Mono', monospace",
            className: 'font-palette-tech-minimalist'
        },
        'warm-humanist': {
            name: 'Warm Humanist',
            description: 'Friendly, approachable feel with excellent readability',
            heading: "'Source Sans Pro', 'Helvetica Neue', 'Arial', sans-serif",
            body: "'Source Sans Pro', 'Helvetica Neue', 'Arial', sans-serif",
            accent: "'Source Sans Pro', 'Helvetica Neue', 'Arial', sans-serif",
            className: 'font-palette-warm-humanist'
        }
    };
    
    // Current font palette
    let currentFontPalette = 'modern-professional';
    
    // DOM elements
    let fontPicker;
    let fontVariablesStyle;
    
    /**
     * Initialize font system
     */
    function init() {
        // Cache DOM elements
        cacheFontElements();
        
        // Load saved font preference
        loadFontPreferences();
        
        // Apply initial font palette
        applyFontPalette();
        
        // Create font picker if needed
        createFontPicker();
        
        // Set up event listeners
        setupFontEventListeners();
        
        console.log('Font management system initialized 🔤');
    }
    
    /**
     * Cache DOM elements
     */
    function cacheFontElements() {
        fontVariablesStyle = document.getElementById('font-variables') || createFontVariablesStyle();
    }
    
    /**
     * Create font variables style element
     */
    function createFontVariablesStyle() {
        const style = document.createElement('style');
        style.id = 'font-variables';
        document.head.appendChild(style);
        return style;
    }
    
    /**
     * Load font preferences from localStorage
     */
    function loadFontPreferences() {
        // Load saved font palette
        const savedFontPalette = localStorage.getItem('portfolio-font-palette');
        if (savedFontPalette && FONT_PALETTES[savedFontPalette]) {
            currentFontPalette = savedFontPalette;
        } else if (window.SITE_CONFIG?.ACTIVE_FONT_PALETTE) {
            currentFontPalette = window.SITE_CONFIG.ACTIVE_FONT_PALETTE;
        }
    }
    
    /**
     * Set up event listeners
     */
    function setupFontEventListeners() {
        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            // Alt + F for font picker
            if (e.altKey && e.code === 'KeyF') {
                e.preventDefault();
                toggleFontPicker();
            }
            
            // Alt + Number keys for quick font switching
            if (e.altKey && e.code.startsWith('Digit')) {
                e.preventDefault();
                const fontIndex = parseInt(e.code.slice(-1)) - 1;
                const fontKeys = Object.keys(FONT_PALETTES);
                if (fontKeys[fontIndex]) {
                    changeFontPalette(fontKeys[fontIndex]);
                }
            }
        });
    }
    
    /**
     * Apply current font palette
     */
    function applyFontPalette() {
        const palette = FONT_PALETTES[currentFontPalette];
        
        if (!palette) return;
        
        // Remove existing font palette classes
        document.documentElement.className = document.documentElement.className
            .replace(/font-palette-[\w-]+/g, '');
        
        // Add new font palette class
        document.documentElement.classList.add(palette.className);
        
        // Update CSS variables
        updateFontVariables(palette);
        
        // Save preferences
        saveFontPreferences();
        
        // Dispatch font change event
        dispatchFontChangeEvent();
    }
    
    /**
     * Update CSS variables for current font palette
     */
    function updateFontVariables(palette) {
        if (!fontVariablesStyle || !palette) return;
        
        const css = `
            :root {
                /* Font Family Variables */
                --font-heading: ${palette.heading};
                --font-body: ${palette.body};
                --font-accent: ${palette.accent};
            }
        `;
        
        fontVariablesStyle.textContent = css;
    }
    
    /**
     * Change font palette
     */
    function changeFontPalette(paletteKey) {
        if (!FONT_PALETTES[paletteKey]) return;
        
        currentFontPalette = paletteKey;
        applyFontPalette();
        
        // Update font picker selection
        updateFontPickerSelection();
        
        // Show feedback
        showFontChangeFeedback(FONT_PALETTES[paletteKey].name);
    }
    
    /**
     * Show font change feedback
     */
    function showFontChangeFeedback(fontName) {
        const feedback = document.createElement('div');
        feedback.className = 'position-fixed top-50 start-50 translate-middle bg-info text-white px-3 py-2 rounded shadow';
        feedback.style.zIndex = '9999';
        feedback.innerHTML = `
            <i class="bi bi-fonts me-2"></i>
            ${fontName} Applied
        `;
        
        document.body.appendChild(feedback);
        
        setTimeout(() => {
            feedback.remove();
        }, 2000);
    }
    
    /**
     * Create font picker UI
     */
    function createFontPicker() {
        fontPicker = document.createElement('div');
        fontPicker.className = 'font-picker';
        fontPicker.innerHTML = `
            <button class="font-picker-toggle" onclick="window.FontManager.toggleFontPicker()" title="Font Palette (Alt+F)">
                <i class="bi bi-fonts"></i>
            </button>
            <div class="p-3">
                <h6 class="mb-3">Choose Font Style</h6>
                <div class="font-options">
                    ${Object.entries(FONT_PALETTES).map(([key, palette]) => `
                        <div class="font-option ${key === currentFontPalette ? 'active' : ''}" 
                             data-font="${key}"
                             title="${palette.description}"
                             onclick="window.FontManager.changeFontPalette('${key}')">
                            <div class="font-preview ${palette.className}">
                                <div class="font-heading-preview">Aa</div>
                                <div class="font-name">${palette.name}</div>
                            </div>
                        </div>
                    `).join('')}
                </div>
                <hr class="my-3">
                <div class="font-info">
                    <small class="text-muted">
                        <strong>Keyboard Shortcuts:</strong><br>
                        Alt + F: Toggle font picker<br>
                        Alt + 1-4: Quick font switch
                    </small>
                </div>
            </div>
        `;
        
        document.body.appendChild(fontPicker);
    }
    
    /**
     * Toggle font picker visibility
     */
    function toggleFontPicker() {
        if (fontPicker) {
            fontPicker.classList.toggle('show');
        }
    }
    
    /**
     * Update font picker selection
     */
    function updateFontPickerSelection() {
        if (!fontPicker) return;
        
        const fontOptions = fontPicker.querySelectorAll('.font-option');
        fontOptions.forEach(option => {
            option.classList.toggle('active', option.dataset.font === currentFontPalette);
        });
    }
    
    /**
     * Save font preferences to localStorage
     */
    function saveFontPreferences() {
        localStorage.setItem('portfolio-font-palette', currentFontPalette);
    }
    
    /**
     * Dispatch font change event for other scripts
     */
    function dispatchFontChangeEvent() {
        const event = new CustomEvent('fontchange', {
            detail: {
                fontPalette: currentFontPalette,
                palette: FONT_PALETTES[currentFontPalette]
            }
        });
        
        document.dispatchEvent(event);
    }
    
    /**
     * Get current font information
     */
    function getCurrentFont() {
        return {
            fontPalette: currentFontPalette,
            palette: FONT_PALETTES[currentFontPalette]
        };
    }
    
    /**
     * Apply font from external source (like admin panel)
     */
    function applyExternalFont(fontKey) {
        if (FONT_PALETTES[fontKey]) {
            currentFontPalette = fontKey;
            applyFontPalette();
            updateFontPickerSelection();
        }
    }
    
    /**
     * Preload font families for better performance
     * Using dynamic CSS import instead of hardcoded WOFF2 URLs
     */
    function preloadFonts() {
        const fontFamilies = new Set();
        
        Object.values(FONT_PALETTES).forEach(palette => {
            fontFamilies.add(palette.heading);
            fontFamilies.add(palette.body);
            fontFamilies.add(palette.accent);
        });
        
        // Preload Google Fonts using CSS imports instead of direct WOFF2 URLs
        const googleFontsToLoad = [];
        
        fontFamilies.forEach(fontFamily => {
            if (fontFamily.includes('Inter') && !googleFontsToLoad.includes('Inter')) {
                googleFontsToLoad.push('Inter:wght@300;400;500;600;700;800');
            } else if (fontFamily.includes('Playfair') && !googleFontsToLoad.includes('Playfair Display')) {
                googleFontsToLoad.push('Playfair+Display:wght@400;500;600;700;800');
            } else if (fontFamily.includes('JetBrains') && !googleFontsToLoad.includes('JetBrains Mono')) {
                googleFontsToLoad.push('JetBrains+Mono:wght@300;400;500;600;700');
            } else if (fontFamily.includes('Source Sans Pro') && !googleFontsToLoad.includes('Source Sans Pro')) {
                googleFontsToLoad.push('Source+Sans+Pro:wght@300;400;600;700');
            }
        });
        
        // Create a single Google Fonts CSS link for all needed fonts
        if (googleFontsToLoad.length > 0) {
            const link = document.createElement('link');
            link.rel = 'preload';
            link.as = 'style';
            link.onload = function() { this.rel = 'stylesheet'; };
            link.href = `https://fonts.googleapis.com/css2?family=${googleFontsToLoad.join('&family=')}&display=swap`;
            
            // Add crossorigin for better caching
            link.crossOrigin = 'anonymous';
            
            document.head.appendChild(link);
            
            console.log('Preloaded Google Fonts:', googleFontsToLoad.join(', '));
        }
    }
    
    /**
     * Export public API
     */
    window.FontManager = {
        init,
        changeFontPalette,
        toggleFontPicker,
        getCurrentFont,
        applyExternalFont,
        FONT_PALETTES
    };
    
    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            init();
            preloadFonts();
        });
    } else {
        init();
        preloadFonts();
    }
    
    // Listen for font change requests from other parts of the app
    document.addEventListener('requestFontChange', (e) => {
        if (e.detail.fontPalette) {
            changeFontPalette(e.detail.fontPalette);
        }
    });
    
})();