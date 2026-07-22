/* ==========================================================================
   J SRUJAN VISHWAKARMA - PORTFOLIO INTERACTIVE LOGIC & NEURAL PARTICLES
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
    initNeuralCanvas();
    initTypingEffect();
    initProjectFiltering();
    initChatBot();
    initContactForm();
    initScrollSpy();
});

/* --------------------------------------------------------------------------
   1. NEURAL PARTICLE CANVAS ANIMATION
   -------------------------------------------------------------------------- */
function initNeuralCanvas() {
    const canvas = document.getElementById('neural-canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    
    let width = canvas.width = window.innerWidth;
    let height = canvas.height = window.innerHeight;
    
    window.addEventListener('resize', () => {
        width = canvas.width = window.innerWidth;
        height = canvas.height = window.innerHeight;
    });

    const particles = [];
    const particleCount = Math.min(Math.floor(width / 18), 70);

    for (let i = 0; i < particleCount; i++) {
        particles.push({
            x: Math.random() * width,
            y: Math.random() * height,
            vx: (Math.random() - 0.5) * 0.8,
            vy: (Math.random() - 0.5) * 0.8,
            radius: Math.random() * 2 + 1,
            color: Math.random() > 0.5 ? '#00F2FE' : '#4FACFE'
        });
    }

    function animate() {
        ctx.clearRect(0, 0, width, height);

        for (let i = 0; i < particles.length; i++) {
            let p = particles[i];
            p.x += p.vx;
            p.y += p.vy;

            if (p.x < 0 || p.x > width) p.vx *= -1;
            if (p.y < 0 || p.y > height) p.vy *= -1;

            ctx.beginPath();
            ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
            ctx.fillStyle = p.color;
            ctx.shadowBlur = 8;
            ctx.shadowColor = p.color;
            ctx.fill();

            // Connect nearby nodes
            for (let j = i + 1; j < particles.length; j++) {
                let p2 = particles[j];
                let dist = Math.hypot(p.x - p2.x, p.y - p2.y);
                if (dist < 130) {
                    ctx.beginPath();
                    ctx.moveTo(p.x, p.y);
                    ctx.lineTo(p2.x, p2.y);
                    ctx.strokeStyle = `rgba(0, 242, 254, ${1 - dist / 130 * 0.85})`;
                    ctx.lineWidth = 0.5;
                    ctx.stroke();
                }
            }
        }
        requestAnimationFrame(animate);
    }
    animate();
}

/* --------------------------------------------------------------------------
   2. HERO TYPING ANIMATION EFFECT
   -------------------------------------------------------------------------- */
function initTypingEffect() {
    const el = document.getElementById('typing-text');
    if (!el) return;
    
    const titles = [
        "AI Engineer",
        "Generative AI Specialist",
        "Multi-Agent RAG Architect",
        "Vision-Language Model Developer",
        "Cloud MLOps Innovator"
    ];
    
    let titleIndex = 0;
    let charIndex = 0;
    let isDeleting = false;
    let typingSpeed = 100;

    function type() {
        const currentTitle = titles[titleIndex];
        
        if (isDeleting) {
            el.textContent = currentTitle.substring(0, charIndex - 1);
            charIndex--;
            typingSpeed = 50;
        } else {
            el.textContent = currentTitle.substring(0, charIndex + 1);
            charIndex++;
            typingSpeed = 100;
        }

        if (!isDeleting && charIndex === currentTitle.length) {
            typingSpeed = 2000; // Pause at end
            isDeleting = true;
        } else if (isDeleting && charIndex === 0) {
            isDeleting = false;
            titleIndex = (titleIndex + 1) % titles.length;
            typingSpeed = 500;
        }

        setTimeout(type, typingSpeed);
    }
    type();
}

/* --------------------------------------------------------------------------
   3. PROJECT CATEGORY FILTERING & MODAL VIEWER
   -------------------------------------------------------------------------- */
function initProjectFiltering() {
    const filterBtns = document.querySelectorAll('.filter-btn');
    const projectCards = document.querySelectorAll('.project-card');

    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            const filter = btn.getAttribute('data-filter').toLowerCase();

            projectCards.forEach(card => {
                const category = card.getAttribute('data-category').toLowerCase();
                if (filter === 'all' || category.includes(filter)) {
                    card.style.display = 'flex';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });
}

function openProjectModal(projectId) {
    fetch('/api/projects')
        .then(res => res.json())
        .then(projects => {
            const project = projects.find(p => p.id === projectId);
            if (!project) return;

            const modalBody = document.getElementById('modal-body-content');
            modalBody.innerHTML = `
                <div class="project-badge" style="margin-bottom: 12px; display: inline-block;">${project.category} • ${project.period}</div>
                <h2 style="font-size: 1.8rem; margin-bottom: 12px;">${project.title}</h2>
                <p style="color: var(--primary-cyan); font-weight: 600; margin-bottom: 20px;">${project.tagline}</p>
                <p style="color: var(--text-muted); margin-bottom: 24px; line-height: 1.7;">${project.description}</p>
                
                <h4 style="color: #FFF; margin-bottom: 12px; font-size: 1.1rem;">Key Architecture & Deliverables:</h4>
                <ul style="list-style: none; margin-bottom: 24px;">
                    ${project.features.map(f => `<li style="color: var(--text-muted); margin-bottom: 8px; position: relative; padding-left: 20px;"><span style="position: absolute; left: 0; color: var(--accent-green);">✓</span> ${f}</li>`).join('')}
                </ul>

                <h4 style="color: #FFF; margin-bottom: 12px; font-size: 1.1rem;">Tech Stack:</h4>
                <div style="display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 28px;">
                    ${project.tech_stack.map(t => `<span class="tech-tag" style="background: rgba(0, 242, 254, 0.1); border-color: rgba(0, 242, 254, 0.2); color: var(--primary-cyan);">${t}</span>`).join('')}
                </div>

                <div style="display: flex; gap: 16px;">
                    ${project.github !== '#' ? `<a href="${project.github}" target="_blank" class="btn-primary" style="padding: 10px 24px; font-size: 0.9rem;">View GitHub Repo</a>` : ''}
                    <button onclick="closeModal()" class="btn-secondary" style="padding: 10px 24px; font-size: 0.9rem;">Close Window</button>
                </div>
            `;
            
            document.getElementById('project-modal').classList.add('open');
        });
}

function closeModal() {
    document.getElementById('project-modal').classList.remove('open');
}

/* --------------------------------------------------------------------------
   4. INTERACTIVE AI CHATBOT DRAWER
   -------------------------------------------------------------------------- */
function initChatBot() {
    const chatBtn = document.getElementById('chat-widget-btn');
    const chatDrawer = document.getElementById('chat-drawer');
    const closeBtn = document.getElementById('chat-close-btn');
    const sendBtn = document.getElementById('chat-send-btn');
    const chatInput = document.getElementById('chat-input');
    const chatMessages = document.getElementById('chat-messages');

    if (!chatBtn || !chatDrawer) return;

    chatBtn.addEventListener('click', () => {
        chatDrawer.classList.toggle('open');
    });

    closeBtn.addEventListener('click', () => {
        chatDrawer.classList.remove('open');
    });

    function handleSend() {
        const text = chatInput.value.trim();
        if (!text) return;

        // User Bubble
        appendBubble(text, 'user');
        chatInput.value = '';

        // Bot Typing Indicator
        const typingId = appendBubble('Thinking...', 'bot');

        fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: text })
        })
        .then(res => res.json())
        .then(data => {
            document.getElementById(typingId).textContent = data.response;
            chatMessages.scrollTop = chatMessages.scrollHeight;
        })
        .catch(() => {
            document.getElementById(typingId).textContent = "Sorry, I am temporarily offline. Please check Srujan's email or LinkedIn!";
        });
    }

    function appendBubble(text, sender) {
        const id = 'msg-' + Date.now();
        const bubble = document.createElement('div');
        bubble.id = id;
        bubble.className = `chat-bubble ${sender}`;
        bubble.textContent = text;
        chatMessages.appendChild(bubble);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        return id;
    }

    sendBtn.addEventListener('click', handleSend);
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') handleSend();
    });
}

/* --------------------------------------------------------------------------
   5. CONTACT FORM HANDLER
   -------------------------------------------------------------------------- */
function initContactForm() {
    const form = document.getElementById('contact-form');
    const statusDiv = document.getElementById('contact-status');
    if (!form) return;

    form.addEventListener('submit', (e) => {
        e.preventDefault();
        const name = document.getElementById('form-name').value;
        const email = document.getElementById('form-email').value;
        const message = document.getElementById('form-message').value;

        statusDiv.style.display = 'block';
        statusDiv.className = 'section-tag';
        statusDiv.textContent = "Sending message...";

        fetch('/api/contact', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, email, message })
        })
        .then(res => res.json())
        .then(data => {
            statusDiv.textContent = data.message;
            statusDiv.style.borderColor = 'var(--accent-green)';
            statusDiv.style.color = 'var(--accent-green)';
            form.reset();
        })
        .catch(() => {
            statusDiv.textContent = "Failed to send. Please reach out via srujansrutha01@gmail.com";
        });
    });
}

/* --------------------------------------------------------------------------
   6. SCROLLSPY FOR NAVBAR
   -------------------------------------------------------------------------- */
function initScrollSpy() {
    const sections = document.querySelectorAll('section');
    const navLinks = document.querySelectorAll('.nav-link');

    window.addEventListener('scroll', () => {
        let current = '';
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            if (pageYOffset >= sectionTop - 150) {
                current = section.getAttribute('id');
            }
        });

        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${current}`) {
                link.classList.add('active');
            }
        });
    });
}
