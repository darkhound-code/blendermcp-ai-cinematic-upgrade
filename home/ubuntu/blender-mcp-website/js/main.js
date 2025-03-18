/**
 * BlenderMCP Ultimate Cinematic Upgrade Website
 * Main JavaScript File
 */

// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize mobile navigation
    initMobileNav();
    
    // Initialize 3D viewer on homepage if it exists
    if (document.querySelector('.hero-3d-viewer')) {
        init3DViewer();
    }
    
    // Initialize FAQ accordions
    initFaqAccordions();
    
    // Initialize testimonial slider
    initTestimonialSlider();
    
    // Initialize comparison slider
    initComparisonSlider();
    
    // Initialize documentation sidebar
    initDocSidebar();
    
    // Initialize tutorial filters
    initTutorialFilters();
    
    // Initialize newsletter form
    initNewsletterForm();
    
    // Initialize contact form
    initContactForm();
    
    // Initialize interactive demos
    initInteractiveDemos();
});

/**
 * Initialize mobile navigation
 */
function initMobileNav() {
    const burger = document.querySelector('.burger');
    const nav = document.querySelector('.nav-links');
    
    if (burger && nav) {
        burger.addEventListener('click', function() {
            // Toggle navigation
            nav.classList.toggle('active');
            
            // Animate burger
            burger.classList.toggle('toggle');
            
            // Toggle burger animation
            const lines = burger.querySelectorAll('div');
            if (lines.length === 3) {
                if (nav.classList.contains('active')) {
                    lines[0].style.transform = 'rotate(-45deg) translate(-5px, 6px)';
                    lines[1].style.opacity = '0';
                    lines[2].style.transform = 'rotate(45deg) translate(-5px, -6px)';
                } else {
                    lines[0].style.transform = 'none';
                    lines[1].style.opacity = '1';
                    lines[2].style.transform = 'none';
                }
            }
        });
        
        // Close mobile nav when clicking on a link
        const navLinks = nav.querySelectorAll('a');
        navLinks.forEach(link => {
            link.addEventListener('click', function() {
                nav.classList.remove('active');
                
                // Reset burger animation
                const lines = burger.querySelectorAll('div');
                if (lines.length === 3) {
                    lines[0].style.transform = 'none';
                    lines[1].style.opacity = '1';
                    lines[2].style.transform = 'none';
                }
            });
        });
    }
}

/**
 * Initialize 3D viewer on homepage
 */
function init3DViewer() {
    const container = document.querySelector('.hero-3d-viewer');
    
    if (!container || typeof THREE === 'undefined') return;
    
    // Set up scene
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x2980b9);
    
    // Set up camera
    const camera = new THREE.PerspectiveCamera(75, container.clientWidth / container.clientHeight, 0.1, 1000);
    camera.position.z = 5;
    
    // Set up renderer
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(container.clientWidth, container.clientHeight);
    container.appendChild(renderer.domElement);
    
    // Add lights
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
    scene.add(ambientLight);
    
    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
    directionalLight.position.set(1, 1, 1);
    scene.add(directionalLight);
    
    // Create Blender logo-inspired geometry
    const geometry = new THREE.TorusKnotGeometry(1, 0.3, 100, 16);
    const material = new THREE.MeshPhongMaterial({ 
        color: 0xffffff,
        shininess: 100,
        specular: 0x111111
    });
    const torusKnot = new THREE.Mesh(geometry, material);
    scene.add(torusKnot);
    
    // Add particles
    const particlesGeometry = new THREE.BufferGeometry();
    const particlesCount = 1000;
    
    const posArray = new Float32Array(particlesCount * 3);
    
    for (let i = 0; i < particlesCount * 3; i++) {
        posArray[i] = (Math.random() - 0.5) * 10;
    }
    
    particlesGeometry.setAttribute('position', new THREE.BufferAttribute(posArray, 3));
    
    const particlesMaterial = new THREE.PointsMaterial({
        size: 0.02,
        color: 0xffffff
    });
    
    const particlesMesh = new THREE.Points(particlesGeometry, particlesMaterial);
    scene.add(particlesMesh);
    
    // Animation loop
    function animate() {
        requestAnimationFrame(animate);
        
        torusKnot.rotation.x += 0.01;
        torusKnot.rotation.y += 0.01;
        
        particlesMesh.rotation.y += 0.001;
        
        renderer.render(scene, camera);
    }
    
    animate();
    
    // Handle window resize
    window.addEventListener('resize', function() {
        camera.aspect = container.clientWidth / container.clientHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(container.clientWidth, container.clientHeight);
    });
}

/**
 * Initialize FAQ accordions
 */
function initFaqAccordions() {
    const faqItems = document.querySelectorAll('.faq-item');
    
    faqItems.forEach(item => {
        const question = item.querySelector('.faq-question');
        const answer = item.querySelector('.faq-answer');
        const toggle = item.querySelector('.faq-toggle');
        
        if (question && answer && toggle) {
            // Hide answers initially
            answer.style.display = 'none';
            
            question.addEventListener('click', function() {
                // Toggle answer visibility
                if (answer.style.display === 'none') {
                    answer.style.display = 'block';
                    toggle.innerHTML = '<i class="fas fa-minus"></i>';
                } else {
                    answer.style.display = 'none';
                    toggle.innerHTML = '<i class="fas fa-plus"></i>';
                }
            });
        }
    });
}

/**
 * Initialize testimonial slider
 */
function initTestimonialSlider() {
    const slider = document.querySelector('.testimonial-slider');
    
    if (!slider) return;
    
    const testimonials = slider.querySelectorAll('.testimonial');
    const prevBtn = slider.querySelector('.prev-btn');
    const nextBtn = slider.querySelector('.next-btn');
    
    if (testimonials.length <= 1) return;
    
    let currentIndex = 0;
    
    // Hide all testimonials except the first one
    testimonials.forEach((testimonial, index) => {
        if (index !== 0) {
            testimonial.style.display = 'none';
        }
    });
    
    // Function to show testimonial at specific index
    function showTestimonial(index) {
        testimonials.forEach((testimonial, i) => {
            testimonial.style.display = i === index ? 'block' : 'none';
        });
    }
    
    // Event listeners for navigation buttons
    if (prevBtn) {
        prevBtn.addEventListener('click', function() {
            currentIndex = (currentIndex - 1 + testimonials.length) % testimonials.length;
            showTestimonial(currentIndex);
        });
    }
    
    if (nextBtn) {
        nextBtn.addEventListener('click', function() {
            currentIndex = (currentIndex + 1) % testimonials.length;
            showTestimonial(currentIndex);
        });
    }
    
    // Auto-rotate testimonials
    setInterval(function() {
        currentIndex = (currentIndex + 1) % testimonials.length;
        showTestimonial(currentIndex);
    }, 5000);
}

/**
 * Initialize comparison slider
 */
function initComparisonSlider() {
    const sliders = document.querySelectorAll('.comparison-slider');
    
    sliders.forEach(slider => {
        const container = slider.querySelector('.comparison-container');
        const after = slider.querySelector('.comparison-after');
        const input = slider.querySelector('.comparison-slider-input');
        
        if (!container || !after || !input) return;
        
        // Set initial position
        after.style.width = '50%';
        
        // Update slider position on input change
        input.addEventListener('input', function() {
            after.style.width = this.value + '%';
        });
    });
}

/**
 * Initialize documentation sidebar
 */
function initDocSidebar() {
    const sidebar = document.querySelector('.documentation-sidebar');
    
    if (!sidebar) return;
    
    // Handle sidebar navigation
    const navItems = sidebar.querySelectorAll('.sidebar-nav-item');
    const subNavs = sidebar.querySelectorAll('.sidebar-subnav');
    
    // Hide all subnavs initially
    subNavs.forEach(subnav => {
        subnav.style.display = 'none';
    });
    
    navItems.forEach((item, index) => {
        item.addEventListener('click', function(e) {
            // If the item has a subnav, toggle it
            if (subNavs[index]) {
                e.preventDefault();
                
                if (subNavs[index].style.display === 'none') {
                    subNavs[index].style.display = 'block';
                    item.classList.add('active');
                } else {
                    subNavs[index].style.display = 'none';
                    item.classList.remove('active');
                }
            }
        });
    });
    
    // Handle search functionality
    const searchInput = sidebar.querySelector('.sidebar-search input');
    const searchButton = sidebar.querySelector('.sidebar-search button');
    
    if (searchInput && searchButton) {
        searchButton.addEventListener('click', function() {
            searchDocumentation(searchInput.value);
        });
        
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                searchDocumentation(searchInput.value);
            }
        });
    }
    
    function searchDocumentation(query) {
        if (!query) return;
        
        query = query.toLowerCase();
        
        // Get all documentation sections
        const sections = document.querySelectorAll('.doc-section');
        
        let foundResults = false;
        
        sections.forEach(section => {
            const text = section.textContent.toLowerCase();
            const heading = section.querySelector('h2, h3, h4');
            
            if (text.includes(query)) {
                section.style.display = 'block';
                
                if (heading) {
                    // Highlight the section
                    heading.scrollIntoView({ behavior: 'smooth' });
                    foundResults = true;
                    
                    // Add temporary highlight effect
                    heading.style.backgroundColor = 'rgba(52, 152, 219, 0.2)';
                    setTimeout(() => {
                        heading.style.backgroundColor = 'transparent';
                    }, 2000);
                }
            } else {
                section.style.display = 'none';
            }
        });
        
        if (!foundResults) {
            alert('No results found for "' + query + '"');
            
            // Reset display
            sections.forEach(section => {
                section.style.display = 'block';
            });
        }
    }
}

/**
 * Initialize tutorial filters
 */
function initTutorialFilters() {
    const filters = document.querySelector('.tutorial-filters');
    
    if (!filters) return;
    
    const categorySelect = filters.querySelector('select[name="category"]');
    const difficultySelect = filters.querySelector('select[name="difficulty"]');
    const searchInput = filters.querySelector('input[name="search"]');
    const searchButton = filters.querySelector('button');
    
    const tutorialCards = document.querySelectorAll('.tutorial-card, .featured-tutorial');
    
    function filterTutorials() {
        const category = categorySelect ? categorySelect.value : 'all';
        const difficulty = difficultySelect ? difficultySelect.value : 'all';
        const searchQuery = searchInput ? searchInput.value.toLowerCase() : '';
        
        tutorialCards.forEach(card => {
            const cardCategory = card.getAttribute('data-category') || '';
            const cardDifficulty = card.getAttribute('data-difficulty') || '';
            const cardTitle = card.querySelector('h3, h4')?.textContent.toLowerCase() || '';
            const cardDescription = card.querySelector('p')?.textContent.toLowerCase() || '';
            
            const matchesCategory = category === 'all' || cardCategory === category;
            const matchesDifficulty = difficulty === 'all' || cardDifficulty === difficulty;
            const matchesSearch = !searchQuery || cardTitle.includes(searchQuery) || cardDescription.includes(searchQuery);
            
            if (matchesCategory && matchesDifficulty && matchesSearch) {
                card.style.display = '';
            } else {
                card.style.display = 'none';
            }
        });
    }
    
    // Add event listeners
    if (categorySelect) {
        categorySelect.addEventListener('change', filterTutorials);
    }
    
    if (difficultySelect) {
        difficultySelect.addEventListener('change', filterTutorials);
    }
    
    if (searchButton && searchInput) {
        searchButton.addEventListener('click', filterTutorials);
        
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                filterTutorials();
            }
        });
    }
}

/**
 * Initialize newsletter form
 */
function initNewsletterForm() {
    const forms = document.querySelectorAll('.newsletter-form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const emailInput = form.querySelector('input[type="email"]');
            
            if (!emailInput || !emailInput.value) {
                alert('Please enter a valid email address.');
                return;
            }
            
            // Simulate form submission
            const submitButton = form.querySelector('button');
            if (submitButton) {
                submitButton.disabled = true;
                submitButton.textContent = 'Subscribing...';
                
                setTimeout(() => {
                    alert('Thank you for subscribing to our newsletter!');
                    emailInput.value = '';
                    submitButton.disabled = false;
                    submitButton.textContent = 'Subscribe';
                }, 1500);
            }
        });
    });
}

/**
 * Initialize contact form
 */
function initContactForm() {
    const form = document.querySelector('.contact-form');
    
    if (!form) return;
    
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Basic form validation
        const name = form.querySelector('#name');
        const email = form.querySelector('#email');
        const subject = form.querySelector('#subject');
        const message = form.querySelector('#message');
        const privacy = form.querySelector('#privacy');
        
        if (!name || !email || !subject || !message || !privacy) {
            alert('Please fill in all required fields.');
            return;
        }
        
        if (!name.value || !email.value || !subject.value || !message.value) {
            alert('Please fill in all required fields.');
            return;
        }
        
        if (!privacy.checked) {
            alert('Please agree to the Privacy Policy.');
            return;
        }
        
        // Simulate form submission
        const submitButton = form.querySelector('button[type="submit"]');
        if (submitButton) {
            submitButton.disabled = true;
            submitBu<response clipped><NOTE>To save on context only part of this file has been shown to you. You should retry this tool after you have searched inside the file with `grep -n` in order to find the line numbers of what you are looking for.</NOTE>