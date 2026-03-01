// ─── Navbar scroll effect ────────────────────────────────────────────────
const navbar = document.getElementById('navbar');
window.addEventListener('scroll', () => {
    navbar.classList.toggle('scrolled', window.scrollY > 60);
});

// ─── Mobile nav toggle ──────────────────────────────────────────────────
const navToggle = document.getElementById('navToggle');
const navLinks = document.getElementById('navLinks');
if (navToggle) {
    navToggle.addEventListener('click', () => {
        navLinks.classList.toggle('active');
        const icon = navToggle.querySelector('i');
        icon.classList.toggle('fa-bars');
        icon.classList.toggle('fa-xmark');
    });
    // Close mobile nav on link click
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', () => {
            navLinks.classList.remove('active');
            const icon = navToggle.querySelector('i');
            icon.classList.add('fa-bars');
            icon.classList.remove('fa-xmark');
        });
    });
}

// ─── Active nav link on scroll ──────────────────────────────────────────
const sections = document.querySelectorAll('section[id]');
window.addEventListener('scroll', () => {
    let current = '';
    sections.forEach(section => {
        const top = section.offsetTop - 120;
        if (window.scrollY >= top) current = section.getAttribute('id');
    });
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === '#' + current) link.classList.add('active');
    });
});

// ─── Menu category tabs ─────────────────────────────────────────────────
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
    });
});

// ─── Flash message auto-dismiss ─────────────────────────────────────────
document.querySelectorAll('.flash-message').forEach(msg => {
    setTimeout(() => {
        msg.style.animation = 'slideOut 0.4s ease forwards';
        setTimeout(() => msg.remove(), 400);
    }, 5000);
});

// ─── Scroll animations ──────────────────────────────────────────────────
const observerOptions = { threshold: 0.1, rootMargin: '0px 0px -50px 0px' };
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);
document.querySelectorAll('.menu-category, .menu-item, .testimonial-card, .contact-card, .about-feature, .about-img, .stat-item').forEach(el => {
    el.classList.add('animate-in');
    observer.observe(el);
});

// ─── Smooth scrolling ───────────────────────────────────────────────────
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
