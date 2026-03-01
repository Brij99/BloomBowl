/* ═══════════════════════════════════════════════════════════════════════
   BLOOMBOWL — Enhanced JavaScript v3.0
   Repeating scroll animations, particles, typed text, magnetic btns,
   parallax, 3D tilt, counters, cursor glow
   ═══════════════════════════════════════════════════════════════════════ */

document.addEventListener('DOMContentLoaded', () => {

    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    // ═══════════════════════════════════
    // SCROLL PROGRESS BAR
    // ═══════════════════════════════════
    const scrollProgress = document.getElementById('scrollProgress');
    function updateScrollProgress() {
        if (!scrollProgress) return;
        const scrollTop = window.scrollY;
        const docHeight = document.documentElement.scrollHeight - window.innerHeight;
        const percent = (scrollTop / docHeight) * 100;
        scrollProgress.style.width = percent + '%';
    }

    // ═══════════════════════════════════
    // NAVBAR
    // ═══════════════════════════════════
    const navbar = document.getElementById('navbar');
    function handleScroll() {
        if (navbar) navbar.classList.toggle('scrolled', window.scrollY > 60);
        const backToTop = document.getElementById('backToTop');
        if (backToTop) backToTop.classList.toggle('visible', window.scrollY > 500);
        updateActiveNav();
        updateScrollProgress();
    }
    window.addEventListener('scroll', handleScroll, { passive: true });
    handleScroll();

    function updateActiveNav() {
        const sections = document.querySelectorAll('section[id]');
        let current = '';
        sections.forEach(section => {
            const top = section.offsetTop - 120;
            if (window.scrollY >= top) current = section.getAttribute('id');
        });
        document.querySelectorAll('.nav-link').forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === '#' + current) link.classList.add('active');
        });
    }

    // ═══════════════════════════════════
    // MOBILE NAV
    // ═══════════════════════════════════
    const navToggle = document.getElementById('navToggle');
    const navLinks = document.getElementById('navLinks');
    if (navToggle) {
        navToggle.addEventListener('click', () => {
            navLinks.classList.toggle('active');
            const icon = navToggle.querySelector('i');
            icon.classList.toggle('fa-bars');
            icon.classList.toggle('fa-xmark');
        });
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', () => {
                navLinks.classList.remove('active');
                const icon = navToggle.querySelector('i');
                icon.classList.add('fa-bars');
                icon.classList.remove('fa-xmark');
            });
        });
        document.addEventListener('click', (e) => {
            if (!navLinks.contains(e.target) && !navToggle.contains(e.target)) {
                navLinks.classList.remove('active');
                const icon = navToggle.querySelector('i');
                if (icon) { icon.classList.add('fa-bars'); icon.classList.remove('fa-xmark'); }
            }
        });
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                navLinks.classList.remove('active');
                const icon = navToggle.querySelector('i');
                if (icon) { icon.classList.add('fa-bars'); icon.classList.remove('fa-xmark'); }
            }
        });
    }

    // ═══════════════════════════════════
    // DARK MODE
    // ═══════════════════════════════════
    const themeToggle = document.getElementById('themeToggle');
    const savedTheme = localStorage.getItem('bloombowl-theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);

    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            const current = document.documentElement.getAttribute('data-theme');
            const next = current === 'light' ? 'dark' : 'light';
            document.documentElement.setAttribute('data-theme', next);
            localStorage.setItem('bloombowl-theme', next);
            updateThemeIcon(next);
        });
    }
    function updateThemeIcon(theme) {
        if (!themeToggle) return;
        const icon = themeToggle.querySelector('i');
        if (icon) icon.className = theme === 'dark' ? 'fa-solid fa-sun' : 'fa-solid fa-moon';
    }

    // ═══════════════════════════════════
    // MENU TABS (preserved)
    // ═══════════════════════════════════
    const tabs = document.querySelectorAll('.menu-tab');
    const categories = document.querySelectorAll('.menu-category');
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            const cat = tab.dataset.category;
            categories.forEach(c => {
                if (cat === 'all') {
                    c.style.display = 'block';
                    c.style.animation = 'fadeSlideUp 0.5s ease forwards';
                } else if (c.dataset.cat === cat) {
                    c.style.display = 'block';
                    c.style.animation = 'fadeSlideUp 0.5s ease forwards';
                } else {
                    c.style.display = 'none';
                }
            });
            // Re-trigger scroll animations for visible items
            setTimeout(() => triggerVisibleAnimations(), 100);
        });
    });

    // ═══════════════════════════════════
    // FLASH MESSAGES (preserved)
    // ═══════════════════════════════════
    document.querySelectorAll('.flash-message').forEach(msg => {
        setTimeout(() => {
            msg.style.animation = 'slideOut 0.4s ease forwards';
            setTimeout(() => msg.remove(), 400);
        }, 5000);
    });

    // ═══════════════════════════════════
    // REPEATING SCROLL ANIMATIONS ⭐
    // Elements animate IN when scrolling into view,
    // and animate OUT when scrolling away — so they
    // replay every time you scroll back!
    // ═══════════════════════════════════
    const scrollElements = document.querySelectorAll('[data-scroll]');

    function createScrollObserver() {
        return new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('is-visible');
                } else {
                    // REMOVE the class so animation replays next time
                    entry.target.classList.remove('is-visible');
                }
            });
        }, {
            threshold: 0.12,
            rootMargin: '0px 0px -80px 0px'
        });
    }

    const scrollObserver = createScrollObserver();
    scrollElements.forEach(el => scrollObserver.observe(el));

    function triggerVisibleAnimations() {
        scrollElements.forEach(el => {
            const rect = el.getBoundingClientRect();
            if (rect.top < window.innerHeight && rect.bottom > 0) {
                el.classList.add('is-visible');
            }
        });
    }

    // ═══════════════════════════════════
    // SMOOTH SCROLLING (preserved)
    // ═══════════════════════════════════
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                const offset = 80;
                const top = target.getBoundingClientRect().top + window.scrollY - offset;
                window.scrollTo({ top, behavior: 'smooth' });
            }
        });
    });

    // ═══════════════════════════════════
    // COUNTER ANIMATION (replays!)
    // ═══════════════════════════════════
    const statsSection = document.querySelector('.stats-bar');
    let counterRunning = false;

    if (statsSection) {
        const counterObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting && !counterRunning) {
                    counterRunning = true;
                    animateCounters();
                } else if (!entry.isIntersecting) {
                    // Reset counters so they replay
                    counterRunning = false;
                    document.querySelectorAll('.stat-num[data-count]').forEach(el => {
                        el.textContent = '0';
                    });
                }
            });
        }, { threshold: 0.3 });
        counterObserver.observe(statsSection);
    }

    function animateCounters() {
        document.querySelectorAll('.stat-num[data-count]').forEach(el => {
            const target = parseInt(el.dataset.count);
            if (isNaN(target)) return;
            const duration = 2200;
            const startTime = performance.now();
            function tick(now) {
                const elapsed = now - startTime;
                const progress = Math.min(elapsed / duration, 1);
                const eased = 1 - Math.pow(1 - progress, 3);
                const suffix = el.dataset.suffix || '';
                el.textContent = Math.round(target * eased).toLocaleString() + suffix;
                if (progress < 1) requestAnimationFrame(tick);
            }
            requestAnimationFrame(tick);
        });
    }

    // ═══════════════════════════════════
    // BACK TO TOP
    // ═══════════════════════════════════
    const backToTop = document.getElementById('backToTop');
    if (backToTop) {
        backToTop.addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

    // ═══════════════════════════════════
    // TYPED TEXT EFFECT ⭐
    // ═══════════════════════════════════
    const typedEl = document.querySelector('.typed-text');
    if (typedEl && !prefersReducedMotion) {
        const words = JSON.parse(typedEl.dataset.words || '[]');
        if (words.length > 1) {
            let wordIndex = 0;
            let charIndex = 0;
            let isDeleting = false;
            const typeSpeed = 100;
            const deleteSpeed = 60;
            const pauseTime = 2000;

            function typeLoop() {
                const currentWord = words[wordIndex];

                if (isDeleting) {
                    charIndex--;
                    typedEl.textContent = currentWord.substring(0, charIndex);
                } else {
                    charIndex++;
                    typedEl.textContent = currentWord.substring(0, charIndex);
                }

                let delay = isDeleting ? deleteSpeed : typeSpeed;

                if (!isDeleting && charIndex === currentWord.length) {
                    delay = pauseTime;
                    isDeleting = true;
                } else if (isDeleting && charIndex === 0) {
                    isDeleting = false;
                    wordIndex = (wordIndex + 1) % words.length;
                    delay = 300;
                }

                setTimeout(typeLoop, delay);
            }

            setTimeout(typeLoop, 1500);
        }
    }

    // ═══════════════════════════════════
    // FLOATING PARTICLES ⭐
    // ═══════════════════════════════════
    const particlesContainer = document.getElementById('particles');
    if (particlesContainer && !prefersReducedMotion) {
        const particleCount = window.innerWidth < 768 ? 8 : 18;
        for (let i = 0; i < particleCount; i++) {
            const particle = document.createElement('div');
            particle.classList.add('particle');
            const size = Math.random() * 8 + 4;
            particle.style.width = size + 'px';
            particle.style.height = size + 'px';
            particle.style.left = Math.random() * 100 + '%';
            particle.style.animationDuration = (Math.random() * 15 + 12) + 's';
            particle.style.animationDelay = (Math.random() * 10) + 's';
            particlesContainer.appendChild(particle);
        }
    }

    // ═══════════════════════════════════
    // CURSOR GLOW (desktop)
    // ═══════════════════════════════════
    const cursorGlow = document.getElementById('cursorGlow');
    if (cursorGlow && window.innerWidth > 768 && !prefersReducedMotion) {
        let mouseX = 0, mouseY = 0, glowX = 0, glowY = 0;

        document.addEventListener('mousemove', (e) => {
            mouseX = e.clientX;
            mouseY = e.clientY;
        });

        function animateGlow() {
            glowX += (mouseX - glowX) * 0.08;
            glowY += (mouseY - glowY) * 0.08;
            cursorGlow.style.left = glowX + 'px';
            cursorGlow.style.top = glowY + 'px';
            requestAnimationFrame(animateGlow);
        }
        animateGlow();
    } else if (cursorGlow) {
        cursorGlow.style.display = 'none';
    }

    // ═══════════════════════════════════
    // MAGNETIC BUTTONS ⭐
    // ═══════════════════════════════════
    if (!prefersReducedMotion) {
        document.querySelectorAll('.magnetic-btn').forEach(btn => {
            btn.addEventListener('mousemove', (e) => {
                const rect = btn.getBoundingClientRect();
                const x = e.clientX - rect.left - rect.width / 2;
                const y = e.clientY - rect.top - rect.height / 2;
                btn.style.transform = `translate(${x * 0.2}px, ${y * 0.2}px)`;
            });
            btn.addEventListener('mouseleave', () => {
                btn.style.transform = '';
            });
        });
    }

    // ═══════════════════════════════════
    // 3D TILT ON TESTIMONIALS ⭐
    // ═══════════════════════════════════
    if (!prefersReducedMotion) {
        document.querySelectorAll('.testimonial-card').forEach(card => {
            card.addEventListener('mousemove', (e) => {
                const rect = card.getBoundingClientRect();
                const x = (e.clientX - rect.left) / rect.width - 0.5;
                const y = (e.clientY - rect.top) / rect.height - 0.5;
                card.style.transform = `translateY(-6px) scale(1.02) perspective(600px) rotateX(${y * -6}deg) rotateY(${x * 6}deg)`;
            });
            card.addEventListener('mouseleave', () => {
                card.style.transform = '';
            });
        });
    }

    // ═══════════════════════════════════
    // 3D HOVER ON ABOUT IMAGES ⭐
    // ═══════════════════════════════════
    if (!prefersReducedMotion) {
        document.querySelectorAll('.hover-3d').forEach(img => {
            img.addEventListener('mousemove', (e) => {
                const rect = img.getBoundingClientRect();
                const x = (e.clientX - rect.left) / rect.width - 0.5;
                const y = (e.clientY - rect.top) / rect.height - 0.5;
                img.style.transform = `scale(1.06) perspective(500px) rotateX(${y * -8}deg) rotateY(${x * 8}deg)`;
            });
            img.addEventListener('mouseleave', () => {
                img.style.transform = '';
            });
        });
    }

    // ═══════════════════════════════════
    // PARALLAX HERO BACKGROUND ⭐
    // ═══════════════════════════════════
    const heroVideo = document.querySelector('.hero-video');
    const heroFallback = document.querySelector('.hero-fallback-img');
    if (!prefersReducedMotion) {
        window.addEventListener('scroll', () => {
            const scrolled = window.scrollY;
            if (scrolled < window.innerHeight) {
                const target = heroVideo || heroFallback;
                if (target) {
                    target.style.transform = `scale(1.05) translateY(${scrolled * 0.12}px)`;
                }
            }
        }, { passive: true });
    }

    // ═══════════════════════════════════
    // PARALLAX CTA SECTION ⭐
    // ═══════════════════════════════════
    const parallaxVideo = document.querySelector('.parallax-video');
    if (parallaxVideo && !prefersReducedMotion) {
        window.addEventListener('scroll', () => {
            const section = document.querySelector('.parallax-cta');
            if (!section) return;
            const rect = section.getBoundingClientRect();
            if (rect.top < window.innerHeight && rect.bottom > 0) {
                const offset = (rect.top / window.innerHeight) * 40;
                parallaxVideo.style.transform = `translateY(${offset}px) scale(1.1)`;
            }
        }, { passive: true });
    }

    // ═══════════════════════════════════
    // MENU ITEM SPRING HOVER
    // ═══════════════════════════════════
    document.querySelectorAll('.menu-item').forEach(item => {
        item.addEventListener('mouseenter', () => {
            item.style.transition = 'all 0.35s cubic-bezier(0.34, 1.56, 0.64, 1)';
        });
        item.addEventListener('mouseleave', () => {
            item.style.transition = 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)';
        });
    });

    // ═══════════════════════════════════
    // FORM INPUT ANIMATIONS
    // ═══════════════════════════════════
    document.querySelectorAll('.form-input').forEach(input => {
        input.addEventListener('focus', () => {
            input.parentElement.style.transform = 'scale(1.02)';
            input.parentElement.style.transition = 'transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1)';
        });
        input.addEventListener('blur', () => {
            input.parentElement.style.transform = '';
        });
    });

    // ═══════════════════════════════════
    // ORDER FORM → WHATSAPP
    // ═══════════════════════════════════
    const orderForm = document.getElementById('orderForm');
    if (orderForm) {
        orderForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const name = document.getElementById('name')?.value.trim();
            const phone = document.getElementById('phone')?.value.trim();
            const items = document.getElementById('items')?.value.trim();

            if (!name || !phone) {
                alert('Please fill in your name and phone number.');
                return;
            }

            const message = `🌱 *New BloomBowl Order!*\n\n👤 Name: ${name}\n📱 Phone: ${phone}\n🛒 Items: ${items || 'Not specified'}\n\nPlease confirm my order. Thank you!`;
            const encoded = encodeURIComponent(message);
            window.open(`https://wa.me/918849570610?text=${encoded}`, '_blank');
        });
    }

    // ═══════════════════════════════════
    // MARQUEE PAUSE ON HOVER
    // ═══════════════════════════════════
    document.querySelectorAll('.marquee-track').forEach(track => {
        track.addEventListener('mouseenter', () => {
            track.style.animationPlayState = 'paused';
        });
        track.addEventListener('mouseleave', () => {
            track.style.animationPlayState = 'running';
        });
    });

    // ═══════════════════════════════════
    // DONE
    // ═══════════════════════════════════
    console.log('%c🌱 BloomBowl v3.0 Loaded — Animations Active', 'color: #22c55e; font-weight: bold; font-size: 14px;');

});
