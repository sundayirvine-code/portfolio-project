/**
 * Portfolio - Theme Management System
 * Handles dynamic color palette switching and dark/light mode
 */

(function() {
    'use strict';
    
    // Theme configuration
    const THEMES = {
        'electric-neon': {
            name: 'Electric Neon',
            light: {
                primary: '#6366f1',
                secondary: '#8b5cf6',
                accent: '#06b6d4',
                background: '#f8fafc',
                text: '#1e293b'
            },
            dark: {
                primary: '#818cf8',
                secondary: '#a78bfa',
                accent: '#67e8f9',
                background: '#0f172a',
                text: '#f1f5f9'
            }
        },
        'sunset-gradient': {
            name: 'Sunset Gradient',
            light: {
                primary: '#f59e0b',
                secondary: '#ef4444',
                accent: '#ec4899',
                background: '#fefbf3',
                text: '#292524'
            },
            dark: {
                primary: '#fbbf24',
                secondary: '#f87171',
                accent: '#f472b6',
                background: '#1c1917',
                text: '#fafaf9'
            }
        },
        'ocean-deep': {
            name: 'Ocean Deep',
            light: {
                primary: '#0ea5e9',
                secondary: '#06b6d4',
                accent: '#10b981',
                background: '#f0f9ff',
                text: '#0c4a6e'
            },
            dark: {
                primary: '#38bdf8',
                secondary: '#22d3ee',
                accent: '#34d399',
                background: '#082f49',
                text: '#e0f2fe'
            }
        },
        'forest-modern': {
            name: 'Forest Modern',
            light: {
                primary: '#059669',
                secondary: '#7c3aed',
                accent: '#f59e0b',
                background: '#f0fdf4',
                text: '#064e3b'
            },
            dark: {
                primary: '#10b981',
                secondary: '#a855f7',
                accent: '#fbbf24',
                background: '#022c22',
                text: '#ecfdf5'
            }
        }
    };
    
    // Current settings
    let currentTheme = 'electric-neon';
    let currentMode = 'auto';
    
    // DOM elements
    let themeToggle;
    let themeIcon;
    let themeVariablesStyle;
    let themePicker;
    
    /**
     * Initialize theme system
     */
    function init() {
        // Cache DOM elements
        cacheElements();
        
        // Load saved preferences
        loadThemePreferences();
        
        // Set up event listeners
        setupEventListeners();
        
        // Apply initial theme
        applyTheme();
        
        // Create theme picker
        createThemePicker();
        
        // Listen for system theme changes
        watchSystemTheme();
        
        console.log('Theme system initialized 🎨');
    }
    
    /**
     * Cache DOM elements
     */
    function cacheElements() {
        themeToggle = document.getElementById('theme-toggle');
        themeIcon = document.getElementById('theme-icon');
        themeVariablesStyle = document.getElementById('theme-variables');
    }
    
    /**
     * Load theme preferences from localStorage
     */
    function loadThemePreferences() {
        // Load saved theme
        const savedTheme = localStorage.getItem('portfolio-theme');
        if (savedTheme && THEMES[savedTheme]) {
            currentTheme = savedTheme;
        } else if (window.SITE_CONFIG?.ACTIVE_PALETTE) {
            currentTheme = window.SITE_CONFIG.ACTIVE_PALETTE;
        }
        
        // Load saved mode
        const savedMode = localStorage.getItem('portfolio-mode');
        if (savedMode && ['light', 'dark', 'auto'].includes(savedMode)) {
            currentMode = savedMode;
        } else if (window.SITE_CONFIG?.DEFAULT_THEME) {
            currentMode = window.SITE_CONFIG.DEFAULT_THEME;
        }
    }
    
    /**
     * Set up event listeners
     */
    function setupEventListeners() {
        // Theme toggle button
        if (themeToggle) {
            themeToggle.addEventListener('click', toggleMode);
        }
        
        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            // Alt + T for theme toggle
            if (e.altKey && e.code === 'KeyT') {
                e.preventDefault();
                toggleMode();
            }
            
            // Alt + P for theme picker
            if (e.altKey && e.code === 'KeyP') {
                e.preventDefault();
                toggleThemePicker();
            }
        });
    }
    
    /**
     * Apply current theme and mode
     */
    function applyTheme() {
        const resolvedMode = getResolvedMode();
        const theme = THEMES[currentTheme];
        
        if (!theme) return;
        
        // Set data attribute for Bootstrap theme
        document.documentElement.setAttribute('data-bs-theme', resolvedMode);
        
        // Apply theme class
        document.documentElement.className = document.documentElement.className
            .replace(/theme-\w+/g, '') + ` theme-${currentTheme}`;
        
        // Update CSS variables
        updateCSSVariables(theme, resolvedMode);
        
        // Update theme toggle icon
        updateThemeIcon(resolvedMode);
        
        // Save preferences
        saveThemePreferences();
        
        // Dispatch theme change event
        dispatchThemeChangeEvent();
    }
    
    /**
     * Get resolved mode (convert 'auto' to actual mode)
     */
    function getResolvedMode() {
        if (currentMode === 'auto') {
            return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
        }
        return currentMode;
    }
    
    /**
     * Update CSS variables for current theme
     */
    function updateCSSVariables(theme, mode) {
        if (!themeVariablesStyle || !theme) return;
        
        const colors = theme[mode];
        
        const css = `
            :root {
                /* Portfolio Theme Variables */
                --portfolio-primary: ${colors.primary};
                --portfolio-secondary: ${colors.secondary};
                --portfolio-accent: ${colors.accent};
                --portfolio-bg: ${colors.background};
                --portfolio-text: ${colors.text};
                
                /* Bootstrap Override Variables */
                --bs-primary: ${colors.primary};
                --bs-primary-rgb: ${hexToRgb(colors.primary)};
                --bs-secondary: ${colors.secondary};
                --bs-secondary-rgb: ${hexToRgb(colors.secondary)};
                
                /* Custom Gradient Variables */
                --theme-gradient-primary: linear-gradient(135deg, ${colors.primary}, ${colors.secondary});
                --theme-gradient-accent: linear-gradient(135deg, ${colors.accent}, ${colors.primary});
                --theme-gradient-hero: linear-gradient(135deg, ${colors.primary} 0%, ${colors.secondary} 50%, ${colors.accent} 100%);
            }
            
            [data-bs-theme="${mode}"] {
                --portfolio-primary: ${colors.primary};
                --portfolio-secondary: ${colors.secondary};
                --portfolio-accent: ${colors.accent};
                --portfolio-bg: ${colors.background};
                --portfolio-text: ${colors.text};
            }
        `;
        
        themeVariablesStyle.textContent = css;
    }
    
    /**
     * Update theme toggle icon
     */
    function updateThemeIcon(mode) {
        if (!themeIcon) return;
        
        const icons = {
            light: 'bi-sun-fill',
            dark: 'bi-moon-fill',
            auto: 'bi-circle-half'
        };
        
        // Remove all icon classes
        Object.values(icons).forEach(iconClass => {
            themeIcon.classList.remove(iconClass);
        });
        
        // Add current icon
        const iconClass = currentMode === 'auto' ? icons.auto : icons[mode];
        themeIcon.classList.add(iconClass);
    }
    
    /**
     * Toggle between light, dark, and auto modes
     */
    function toggleMode() {
        const modes = ['light', 'dark', 'auto'];
        const currentIndex = modes.indexOf(currentMode);
        const nextIndex = (currentIndex + 1) % modes.length;
        
        currentMode = modes[nextIndex];
        applyTheme();
        
        // Show feedback
        showModeChangeFeedback();
    }
    
    /**
     * Show mode change feedback
     */
    function showModeChangeFeedback() {
        const feedback = document.createElement('div');
        feedback.className = 'position-fixed top-50 start-50 translate-middle bg-dark text-white px-3 py-2 rounded shadow';
        feedback.style.zIndex = '9999';
        feedback.innerHTML = `
            <i class="${themeIcon.className} me-2"></i>
            ${currentMode.charAt(0).toUpperCase() + currentMode.slice(1)} Mode
        `;
        
        document.body.appendChild(feedback);
        
        setTimeout(() => {
            feedback.remove();
        }, 1500);
    }
    
    /**
     * Change theme palette
     */
    function changeTheme(themeKey) {
        if (!THEMES[themeKey]) return;
        
        currentTheme = themeKey;
        applyTheme();
        
        // Update theme picker
        updateThemePickerSelection();
        
        // Show feedback
        showThemeChangeFeedback(THEMES[themeKey].name);
    }
    
    /**
     * Show theme change feedback
     */
    function showThemeChangeFeedback(themeName) {
        const feedback = document.createElement('div');
        feedback.className = 'position-fixed top-50 start-50 translate-middle bg-primary text-white px-3 py-2 rounded shadow';
        feedback.style.zIndex = '9999';
        feedback.innerHTML = `
            <i class="bi bi-palette me-2"></i>
            ${themeName} Applied
        `;
        
        document.body.appendChild(feedback);
        
        setTimeout(() => {
            feedback.remove();
        }, 2000);
    }
    
    /**
     * Create theme picker UI
     */
    function createThemePicker() {
        themePicker = document.createElement('div');
        themePicker.className = 'theme-picker';
        themePicker.innerHTML = `
            <button class="theme-picker-toggle" onclick="window.ThemeManager.toggleThemePicker()">
                <i class="bi bi-palette"></i>
            </button>
            <div class="p-3">
                <h6 class="mb-3">Choose Theme</h6>
                <div class="theme-options d-flex flex-wrap justify-content-center">
                    ${Object.entries(THEMES).map(([key, theme]) => `
                        <div class="theme-option ${key === currentTheme ? 'active' : ''}" 
                             data-theme="${key}"
                             title="${theme.name}"
                             onclick="window.ThemeManager.changeTheme('${key}')">
                        </div>
                    `).join('')}
                </div>
                <hr class="my-3">
                <div class="mode-options">
                    <h6 class="mb-2 small">Display Mode</h6>
                    <div class="btn-group btn-group-sm w-100" role="group">
                        <button type="button" class="btn btn-outline-secondary ${currentMode === 'light' ? 'active' : ''}" 
                                onclick="window.ThemeManager.setMode('light')">
                            <i class="bi bi-sun"></i> Light
                        </button>
                        <button type="button" class="btn btn-outline-secondary ${currentMode === 'dark' ? 'active' : ''}" 
                                onclick="window.ThemeManager.setMode('dark')">
                            <i class="bi bi-moon"></i> Dark
                        </button>
                        <button type="button" class="btn btn-outline-secondary ${currentMode === 'auto' ? 'active' : ''}" 
                                onclick="window.ThemeManager.setMode('auto')">
                            <i class="bi bi-circle-half"></i> Auto
                        </button>
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(themePicker);
    }
    
    /**
     * Toggle theme picker visibility
     */
    function toggleThemePicker() {
        if (themePicker) {
            themePicker.classList.toggle('show');
        }
    }
    
    /**
     * Update theme picker selection
     */
    function updateThemePickerSelection() {
        if (!themePicker) return;
        
        // Update theme options
        const themeOptions = themePicker.querySelectorAll('.theme-option');
        themeOptions.forEach(option => {
            option.classList.toggle('active', option.dataset.theme === currentTheme);
        });
        
        // Update mode buttons
        const modeButtons = themePicker.querySelectorAll('.mode-options .btn');
        modeButtons.forEach(button => {
            const mode = button.textContent.trim().toLowerCase().split(' ')[1] || button.textContent.trim().toLowerCase();
            button.classList.toggle('active', mode === currentMode);
        });
    }
    
    /**
     * Set specific mode
     */
    function setMode(mode) {
        if (['light', 'dark', 'auto'].includes(mode)) {
            currentMode = mode;
            applyTheme();
            updateThemePickerSelection();
        }
    }
    
    /**
     * Watch for system theme changes
     */
    function watchSystemTheme() {
        const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
        
        mediaQuery.addEventListener('change', () => {
            if (currentMode === 'auto') {
                applyTheme();
            }
        });
    }
    
    /**
     * Save theme preferences to localStorage
     */
    function saveThemePreferences() {
        localStorage.setItem('portfolio-theme', currentTheme);
        localStorage.setItem('portfolio-mode', currentMode);
    }
    
    /**
     * Dispatch theme change event for other scripts
     */
    function dispatchThemeChangeEvent() {
        const event = new CustomEvent('themechange', {
            detail: {
                theme: currentTheme,
                mode: currentMode,
                resolvedMode: getResolvedMode(),
                colors: THEMES[currentTheme]
            }
        });
        
        document.dispatchEvent(event);
    }
    
    /**
     * Get current theme information
     */
    function getCurrentTheme() {
        return {
            theme: currentTheme,
            mode: currentMode,
            resolvedMode: getResolvedMode(),
            colors: THEMES[currentTheme]
        };
    }
    
    /**
     * Apply theme from external source (like admin panel)
     */
    function applyExternalTheme(themeKey, mode = null) {
        if (THEMES[themeKey]) {
            currentTheme = themeKey;
        }
        
        if (mode && ['light', 'dark', 'auto'].includes(mode)) {
            currentMode = mode;
        }
        
        applyTheme();
        updateThemePickerSelection();
    }
    
    /**
     * Utility: Convert hex to RGB
     */
    function hexToRgb(hex) {
        const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
        return result 
            ? `${parseInt(result[1], 16)}, ${parseInt(result[2], 16)}, ${parseInt(result[3], 16)}`
            : '0, 0, 0';
    }
    
    /**
     * Export public API
     */
    window.ThemeManager = {
        init,
        changeTheme,
        setMode,
        toggleMode,
        toggleThemePicker,
        getCurrentTheme,
        applyExternalTheme,
        THEMES
    };
    
    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
    
    // Listen for theme change requests from other parts of the app
    document.addEventListener('requestThemeChange', (e) => {
        if (e.detail.theme) {
            changeTheme(e.detail.theme);
        }
        if (e.detail.mode) {
            setMode(e.detail.mode);
        }
    });
    
})();