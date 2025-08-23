/**
 * Portfolio - Main JavaScript
 * Handles interactivity, animations, and dynamic features
 */

(function() {
    'use strict';
    
    // Global variables
    let isLoading = false;
    let searchTimeout;
    let scrollPosition = 0;
    
    // DOM Elements
    const elements = {
        navbar: null,
        backToTop: null,
        loadingSpinner: null,
        progressBar: null,
        searchInput: null,
        searchResults: null,
        cookieBanner: null,
        easterEgg: null
    };
    
    /**
     * Initialize the application
     */
    function init() {
        // Cache DOM elements
        cacheElements();
        
        // Initialize components
        initNavbar();
        initScrollEffects();
        initSearch();
        initAnimations();
        initCookieBanner();
        initEasterEggs();
        initTooltips();
        initProgressBar();
        initSmoothScrolling();
        
        // Initialize counters after page load
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', initCounters);
        } else {
            initCounters();
        }
        
        console.log('Portfolio initialized successfully! 🚀');
    }
    
    /**
     * Cache frequently used DOM elements
     */
    function cacheElements() {
        elements.navbar = document.getElementById('main-navbar');
        elements.backToTop = document.getElementById('back-to-top');
        elements.loadingSpinner = document.getElementById('loading-spinner');
        elements.progressBar = document.getElementById('page-progress');
        elements.searchInput = document.getElementById('search-input');
        elements.searchResults = document.getElementById('quick-search-results');
        elements.cookieBanner = document.getElementById('cookie-banner');
        elements.easterEgg = document.getElementById('easter-egg');
    }
    
    /**
     * Initialize navigation functionality
     */
    function initNavbar() {
        if (!elements.navbar) return;
        
        // Handle navbar scroll effect
        window.addEventListener('scroll', throttle(() => {
            const scrolled = window.pageYOffset > 50;
            elements.navbar.classList.toggle('scrolled', scrolled);
        }, 100));
        
        // Handle mobile menu close on link click
        const navLinks = elements.navbar.querySelectorAll('.nav-link');
        const navbarCollapse = elements.navbar.querySelector('.navbar-collapse');
        
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                if (window.innerWidth < 992) {
                    const bsCollapse = new bootstrap.Collapse(navbarCollapse, {
                        toggle: false
                    });
                    bsCollapse.hide();
                }
            });
        });
        
        // Active link highlighting
        highlightActiveNavLink();
        window.addEventListener('scroll', throttle(highlightActiveNavLink, 100));
    }
    
    /**
     * Highlight active navigation link based on scroll position
     */
    function highlightActiveNavLink() {
        const sections = document.querySelectorAll('section[id]');
        const navLinks = document.querySelectorAll('.nav-link[href^="#"]');
        
        let current = '';
        sections.forEach(section => {
            const sectionTop = section.offsetTop - 100;
            const sectionHeight = section.offsetHeight;
            
            if (window.pageYOffset >= sectionTop && 
                window.pageYOffset < sectionTop + sectionHeight) {
                current = section.getAttribute('id');
            }
        });
        
        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${current}`) {
                link.classList.add('active');
            }
        });
    }
    
    /**
     * Initialize scroll effects and back to top button
     */
    function initScrollEffects() {
        if (!elements.backToTop) return;
        
        // Back to top functionality
        elements.backToTop.addEventListener('click', () => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
        
        // Show/hide back to top button
        window.addEventListener('scroll', throttle(() => {
            const shouldShow = window.pageYOffset > 300;
            elements.backToTop.style.display = shouldShow ? 'block' : 'none';
            elements.backToTop.classList.toggle('show', shouldShow);
        }, 100));
    }
    
    /**
     * Initialize search functionality
     */
    function initSearch() {
        if (!elements.searchInput) return;
        
        // Real-time search
        elements.searchInput.addEventListener('input', (e) => {
            const query = e.target.value.trim();
            
            // Clear previous timeout
            clearTimeout(searchTimeout);
            
            if (query.length < 2) {
                hideSearchResults();
                return;
            }
            
            // Debounce search
            searchTimeout = setTimeout(() => {
                performSearch(query);
            }, 300);
        });
        
        // Search suggestions
        const suggestions = document.querySelectorAll('.search-suggestion');
        suggestions.forEach(suggestion => {
            suggestion.addEventListener('click', () => {
                elements.searchInput.value = suggestion.textContent;
                performSearch(suggestion.textContent);
            });
        });
        
        // Handle search form submission
        const searchForm = document.getElementById('search-form');
        if (searchForm) {
            searchForm.addEventListener('submit', (e) => {
                const query = elements.searchInput.value.trim();
                if (!query) {
                    e.preventDefault();
                    return;
                }
            });
        }
    }
    
    /**
     * Perform AJAX search
     */
    function performSearch(query) {
        if (!elements.searchResults) return;
        
        showLoading();
        
        fetch(`/api/search/?q=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                displaySearchResults(data);
                showSearchResults();
            })
            .catch(error => {
                console.error('Search error:', error);
                hideSearchResults();
            })
            .finally(() => {
                hideLoading();
            });
    }
    
    /**
     * Display search results
     */
    function displaySearchResults(data) {
        if (!elements.searchResults) return;
        
        const container = document.getElementById('search-results-container');
        container.innerHTML = '';
        
        // Projects
        if (data.projects && data.projects.length > 0) {
            container.appendChild(createSearchSection('Projects', data.projects, 'project'));
        }
        
        // Blog posts
        if (data.blog_posts && data.blog_posts.length > 0) {
            container.appendChild(createSearchSection('Articles', data.blog_posts, 'blog'));
        }
        
        // Services
        if (data.services && data.services.length > 0) {
            container.appendChild(createSearchSection('Services', data.services, 'service'));
        }
        
        if (container.children.length === 0) {
            container.innerHTML = '<div class="col-12"><p class="text-muted text-center">No results found.</p></div>';
        }
    }
    
    /**
     * Create search results section
     */
    function createSearchSection(title, items, type) {
        const section = document.createElement('div');
        section.className = 'col-12 mb-3';
        
        const sectionHTML = `
            <h6 class="text-muted mb-2">${title}</h6>
            <div class="list-group">
                ${items.map(item => `
                    <a href="${getItemUrl(item, type)}" class="list-group-item list-group-item-action">
                        <div class="d-flex justify-content-between align-items-center">
                            <div>
                                <h6 class="mb-1">${item.title || item.name}</h6>
                                <p class="mb-1 small text-muted">${truncateText(item.description || item.excerpt || '', 80)}</p>
                            </div>
                            <small><i class="bi bi-arrow-right"></i></small>
                        </div>
                    </a>
                `).join('')}
            </div>
        `;
        
        section.innerHTML = sectionHTML;
        return section;
    }
    
    /**
     * Get URL for search result item
     */
    function getItemUrl(item, type) {
        switch (type) {
            case 'project':
                return `/projects/${item.slug}/`;
            case 'blog':
                return `/blog/${item.slug}/`;
            case 'service':
                return `/services/#${item.slug}`;
            default:
                return '#';
        }
    }
    
    /**
     * Show/hide search results
     */
    function showSearchResults() {
        if (elements.searchResults) {
            elements.searchResults.style.display = 'block';
        }
    }
    
    function hideSearchResults() {
        if (elements.searchResults) {
            elements.searchResults.style.display = 'none';
        }
    }
    
    /**
     * Initialize animations and counters
     */
    function initAnimations() {
        // Initialize AOS if available and enabled
        if (typeof AOS !== 'undefined' && window.SITE_CONFIG?.ENABLE_ANIMATIONS) {
            AOS.refresh();
        }
        
        // Initialize custom animations
        initParallaxEffects();
        initHoverEffects();
    }
    
    /**
     * Initialize parallax effects
     */
    function initParallaxEffects() {
        const parallaxElements = document.querySelectorAll('.parallax');
        
        if (parallaxElements.length === 0) return;
        
        window.addEventListener('scroll', throttle(() => {
            const scrolled = window.pageYOffset;
            
            parallaxElements.forEach(element => {
                const rate = scrolled * -0.5;
                element.style.transform = `translateY(${rate}px)`;
            });
        }, 16)); // ~60fps
    }
    
    /**
     * Initialize hover effects
     */
    function initHoverEffects() {
        // Card hover effects
        const cards = document.querySelectorAll('.hover-lift');
        
        cards.forEach(card => {
            card.addEventListener('mouseenter', () => {
                if (window.SITE_CONFIG?.ENABLE_ANIMATIONS) {
                    card.style.transform = 'translateY(-10px) scale(1.02)';
                }
            });
            
            card.addEventListener('mouseleave', () => {
                card.style.transform = 'translateY(0) scale(1)';
            });
        });
    }
    
    /**
     * Initialize number counters
     */
    function initCounters() {
        const counters = document.querySelectorAll('[data-count]');
        
        counters.forEach(counter => {
            const target = parseInt(counter.getAttribute('data-count'));
            const duration = 2000; // 2 seconds
            const increment = target / (duration / 16); // 60fps
            
            let current = 0;
            const timer = setInterval(() => {
                current += increment;
                
                if (current >= target) {
                    current = target;
                    clearInterval(timer);
                }
                
                counter.textContent = Math.floor(current);
            }, 16);
        });
    }
    
    /**
     * Initialize cookie banner
     */
    function initCookieBanner() {
        if (!elements.cookieBanner) return;
        
        // Check if cookies were already accepted
        if (localStorage.getItem('cookiesAccepted')) {
            return;
        }
        
        // Show banner after delay
        setTimeout(() => {
            elements.cookieBanner.style.display = 'block';
        }, 2000);
        
        // Handle accept button
        const acceptBtn = document.getElementById('cookie-accept');
        if (acceptBtn) {
            acceptBtn.addEventListener('click', () => {
                localStorage.setItem('cookiesAccepted', 'true');
                elements.cookieBanner.style.display = 'none';
            });
        }
        
        // Handle decline button
        const declineBtn = document.getElementById('cookie-decline');
        if (declineBtn) {
            declineBtn.addEventListener('click', () => {
                elements.cookieBanner.style.display = 'none';
            });
        }
    }
    
    /**
     * Initialize easter eggs
     */
    function initEasterEggs() {
        let konamiCode = [];
        const konamiSequence = [
            'ArrowUp', 'ArrowUp', 'ArrowDown', 'ArrowDown',
            'ArrowLeft', 'ArrowRight', 'ArrowLeft', 'ArrowRight',
            'KeyB', 'KeyA'
        ];
        
        // Konami code easter egg
        document.addEventListener('keydown', (e) => {
            konamiCode.push(e.code);
            
            if (konamiCode.length > konamiSequence.length) {
                konamiCode.shift();
            }
            
            if (konamiCode.join(',') === konamiSequence.join(',')) {
                triggerEasterEgg();
                konamiCode = [];
            }
        });
        
        // Developer mode shortcut (Ctrl+Shift+D)
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.shiftKey && e.code === 'KeyD') {
                e.preventDefault();
                showDebugInfo();
            }
        });
        
        // Secret click sequence on logo
        let clickCount = 0;
        const logo = document.querySelector('.navbar-brand');
        if (logo) {
            logo.addEventListener('click', () => {
                clickCount++;
                
                if (clickCount === 5) {
                    triggerEasterEgg();
                    clickCount = 0;
                }
                
                setTimeout(() => {
                    clickCount = 0;
                }, 2000);
            });
        }
    }
    
    /**
     * Trigger easter egg
     */
    function triggerEasterEgg() {
        if (elements.easterEgg) {
            elements.easterEgg.classList.remove('d-none');
            
            // Add some fun effects
            document.body.style.animation = 'rainbow 2s ease-in-out';
            
            setTimeout(() => {
                document.body.style.animation = '';
            }, 2000);
        }
        
        console.log('🎉 Easter egg activated! You found the secret!');
    }
    
    /**
     * Show debug information
     */
    function showDebugInfo() {
        const debugInfo = {
            'Site Config': window.SITE_CONFIG,
            'Current Theme': document.documentElement.getAttribute('data-bs-theme'),
            'Screen Size': `${window.innerWidth}x${window.innerHeight}`,
            'User Agent': navigator.userAgent,
            'Performance': {
                'Load Time': `${performance.now().toFixed(2)}ms`,
                'DOM Nodes': document.querySelectorAll('*').length
            }
        };
        
        console.group('🔧 Debug Information');
        Object.entries(debugInfo).forEach(([key, value]) => {
            console.log(`${key}:`, value);
        });
        console.groupEnd();
        
        // Show visual debug panel
        showDebugPanel(debugInfo);
    }
    
    /**
     * Show visual debug panel
     */
    function showDebugPanel(info) {
        const panel = document.createElement('div');
        panel.className = 'position-fixed top-0 start-0 w-100 h-100 bg-dark bg-opacity-75 d-flex align-items-center justify-content-center';
        panel.style.zIndex = '9999';
        
        panel.innerHTML = `
            <div class="bg-white rounded p-4 shadow-lg" style="max-width: 500px; max-height: 80vh; overflow-y: auto;">
                <div class="d-flex justify-content-between align-items-center mb-3">
                    <h5 class="mb-0"><i class="bi bi-bug me-2"></i>Debug Information</h5>
                    <button class="btn-close" onclick="this.closest('.position-fixed').remove()"></button>
                </div>
                <pre class="small text-muted">${JSON.stringify(info, null, 2)}</pre>
            </div>
        `;
        
        document.body.appendChild(panel);
        
        // Auto-remove after 10 seconds
        setTimeout(() => {
            if (panel.parentNode) {
                panel.remove();
            }
        }, 10000);
    }
    
    /**
     * Initialize tooltips
     */
    function initTooltips() {
        const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
        const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => 
            new bootstrap.Tooltip(tooltipTriggerEl)
        );
    }
    
    /**
     * Initialize progress bar
     */
    function initProgressBar() {
        if (!elements.progressBar) return;
        
        window.addEventListener('scroll', throttle(() => {
            const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
            const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
            const scrolled = (winScroll / height) * 100;
            
            elements.progressBar.style.width = `${scrolled}%`;
        }, 16));
    }
    
    /**
     * Initialize smooth scrolling for anchor links
     */
    function initSmoothScrolling() {
        const anchorLinks = document.querySelectorAll('a[href^="#"]:not([href="#"])');
        
        anchorLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                const target = document.querySelector(link.getAttribute('href'));
                
                if (target) {
                    e.preventDefault();
                    
                    const offsetTop = target.offsetTop - 80; // Account for fixed navbar
                    
                    window.scrollTo({
                        top: offsetTop,
                        behavior: 'smooth'
                    });
                }
            });
        });
    }
    
    /**
     * Show loading spinner
     */
    function showLoading() {
        if (elements.loadingSpinner) {
            elements.loadingSpinner.style.display = 'flex';
            isLoading = true;
        }
    }
    
    /**
     * Hide loading spinner
     */
    function hideLoading() {
        if (elements.loadingSpinner) {
            elements.loadingSpinner.style.display = 'none';
            isLoading = false;
        }
    }
    
    /**
     * Utility: Throttle function
     */
    function throttle(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }
    
    /**
     * Utility: Truncate text
     */
    function truncateText(text, maxLength) {
        if (text.length <= maxLength) return text;
        return text.substring(0, maxLength).trim() + '...';
    }
    
    /**
     * Handle page visibility changes
     */
    document.addEventListener('visibilitychange', () => {
        if (document.hidden) {
            // Page is hidden
            scrollPosition = window.pageYOffset;
        } else {
            // Page is visible
            // Restore scroll position if needed
        }
    });
    
    /**
     * Handle window resize
     */
    window.addEventListener('resize', throttle(() => {
        // Refresh AOS on resize
        if (typeof AOS !== 'undefined' && window.SITE_CONFIG?.ENABLE_ANIMATIONS) {
            AOS.refresh();
        }
    }, 250));
    
    /**
     * Initialize everything when DOM is ready
     */
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
    
    // Export for debugging
    window.Portfolio = {
        init,
        showLoading,
        hideLoading,
        triggerEasterEgg,
        showDebugInfo
    };
    
})();