document.addEventListener('DOMContentLoaded', () => {
    
   // ==========================================
// 1. NAVIGATION MOBILE SWITCH ARCHITECTURE (Local Client Patch)
// ==========================================
const mobileMenuBtn = document.getElementById('mobile-menu');
const navMenu = document.querySelector('.nav-menu');
const navLinks = document.querySelectorAll('.nav-link');

if (mobileMenuBtn) {
    mobileMenuBtn.addEventListener('click', () => {
        mobileMenuBtn.classList.toggle('is-active');
        navMenu.classList.toggle('active');
    });
}

// Fixed for local filesystem path evaluation
const currentPath = window.location.pathname.toLowerCase();
navLinks.forEach(link => {
    const linkHref = link.getAttribute('href').toLowerCase();
    
    // Check if the current filesystem URL path ends with the link target
    if (currentPath.endsWith(linkHref) || (currentPath.endsWith('/') && linkHref === 'index.html')) {
        link.classList.add('active');
    } else {
        link.classList.remove('active');
    }
});

    // ==========================================
    // 2. CYBER TYPING SIMULATOR (Only on Home Page)
    // ==========================================
    const textTarget = document.querySelector('.typing-text');
    if (textTarget) {
        const rolesArray = [
            "Cybersecurity Student.",
            "API Security Enthusiast.",
            "Future Founder of AfzoSec."
        ];
        let roleIndex = 0;
        let charIndex = 0;
        let isDeleting = false;
        let typeSpeed = 100;

        function executeTypingAnimation() {
            const currentRole = rolesArray[roleIndex];
            
            if (isDeleting) {
                textTarget.textContent = currentRole.substring(0, charIndex - 1);
                charIndex--;
                typeSpeed = 40; 
            } else {
                textTarget.textContent = currentRole.substring(0, charIndex + 1);
                charIndex++;
                typeSpeed = 120; 
            }

            if (!isDeleting && charIndex === currentRole.length) {
                typeSpeed = 2000; 
                isDeleting = true;
            } else if (isDeleting && charIndex === 0) {
                isDeleting = false;
                roleIndex = (roleIndex + 1) % rolesArray.length;
                typeSpeed = 500;
            }

            setTimeout(executeTypingAnimation, typeSpeed);
        }
        executeTypingAnimation();
    }

    // ==========================================
    // 3. INPUT BUTTON RIPPLE MECHANISM
    // ==========================================
    const rippleButtons = document.querySelectorAll('.ripple');
    rippleButtons.forEach(btn => {
        btn.addEventListener('click', function(e) {
            const x = e.clientX - e.target.getBoundingClientRect().left;
            const y = e.clientY - e.target.getBoundingClientRect().top;
            
            const rippleSpan = document.createElement('span');
            rippleSpan.classList.add('ripple-effect');
            rippleSpan.style.left = `${x}px`;
            rippleSpan.style.top = `${y}px`;
            
            this.appendChild(rippleSpan);
            
            setTimeout(() => {
                rippleSpan.remove();
            }, 600);
        });
    });

    // ==========================================
    // 4. FORM HANDLER TEMPLATE
    // ==========================================
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', (e) => {
            e.preventDefault();
            alert("Payload intercepted safely! Form logic configured. Connect this directly to your Flask router endpoint in development.");
            contactForm.reset();
        });
    }
});