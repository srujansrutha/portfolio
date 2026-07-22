/* ==========================================================================
   J SRUJAN VISHWAKARMA - THREE.JS 3D QUANTUM NEURAL CORE & ENGINE
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
    init3DQuantumCore();
    init3DCardPhysics();
    initTypingEffect();
    initProjectFiltering();
    initChatBot();
    initContactForm();
    initScrollSpy();
});

/* --------------------------------------------------------------------------
   1. THREE.JS 3D QUANTUM NEURAL CORE SCENE
   -------------------------------------------------------------------------- */
function init3DQuantumCore() {
    const container = document.getElementById('webgl-container');
    const canvas = document.getElementById('webgl-canvas');
    if (!container || !canvas || typeof THREE === 'undefined') return;

    // 3D Scene, Camera, Renderer
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(55, container.clientWidth / container.clientHeight, 0.1, 1000);
    camera.position.z = 4.8;

    const renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true, alpha: true });
    renderer.setSize(container.clientWidth, container.clientHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

    // Handle Window Resize
    window.addEventListener('resize', () => {
        if (!container) return;
        camera.aspect = container.clientWidth / container.clientHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(container.clientWidth, container.clientHeight);
    });

    // 1. Central 3D Quantum Outer Icosahedron
    const outerGeo = new THREE.IcosahedronGeometry(1.6, 2);
    const outerMat = new THREE.MeshBasicMaterial({
        color: 0x00F2FE,
        wireframe: true,
        transparent: true,
        opacity: 0.4
    });
    const outerCore = new THREE.Mesh(outerGeo, outerMat);
    scene.add(outerCore);

    // 2. Inner Glowing Core
    const innerGeo = new THREE.IcosahedronGeometry(0.95, 1);
    const innerMat = new THREE.MeshPhongMaterial({
        color: 0x8A2BE2,
        emissive: 0x4FACFE,
        emissiveIntensity: 0.7,
        shininess: 90,
        wireframe: false
    });
    const innerCore = new THREE.Mesh(innerGeo, innerMat);
    scene.add(innerCore);

    // 3. Orbiting Neural Particle Constellation
    const particleCount = 700;
    const particleGeo = new THREE.BufferGeometry();
    const particlePos = new Float32Array(particleCount * 3);
    const particleColors = new Float32Array(particleCount * 3);

    const color1 = new THREE.Color(0x00F2FE);
    const color2 = new THREE.Color(0x8A2BE2);

    for (let i = 0; i < particleCount; i++) {
        const radius = 2.2 + (Math.random() - 0.5) * 0.7;
        const theta = Math.random() * Math.PI * 2;
        const phi = (Math.random() - 0.5) * Math.PI;

        particlePos[i * 3] = radius * Math.cos(theta) * Math.cos(phi);
        particlePos[i * 3 + 1] = radius * Math.sin(phi);
        particlePos[i * 3 + 2] = radius * Math.sin(theta) * Math.cos(phi);

        const mixedColor = color1.clone().lerp(color2, Math.random());
        particleColors[i * 3] = mixedColor.r;
        particleColors[i * 3 + 1] = mixedColor.g;
        particleColors[i * 3 + 2] = mixedColor.b;
    }

    particleGeo.setAttribute('position', new THREE.BufferAttribute(particlePos, 3));
    particleGeo.setAttribute('color', new THREE.BufferAttribute(particleColors, 3));

    const particleMat = new THREE.PointsMaterial({
        size: 0.045,
        vertexColors: true,
        transparent: true,
        opacity: 0.85
    });

    const particleRing = new THREE.Points(particleGeo, particleMat);
    scene.add(particleRing);

    // Lighting Setup
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
    scene.add(ambientLight);

    const cyanLight = new THREE.PointLight(0x00F2FE, 2.5, 50);
    cyanLight.position.set(5, 5, 5);
    scene.add(cyanLight);

    const violetLight = new THREE.PointLight(0x8A2BE2, 2.5, 50);
    violetLight.position.set(-5, -5, 5);
    scene.add(violetLight);

    // Mouse Cursor Tracking
    let mouseX = 0;
    let mouseY = 0;
    let targetX = 0;
    let targetY = 0;

    document.addEventListener('mousemove', (e) => {
        const windowHalfX = window.innerWidth / 2;
        const windowHalfY = window.innerHeight / 2;
        mouseX = (e.clientX - windowHalfX) / 100;
        mouseY = (e.clientY - windowHalfY) / 100;
    });

    const clock = new THREE.Clock();

    function animate() {
        requestAnimationFrame(animate);

        const elapsedTime = clock.getElapsedTime();

        // 3D Core Rotation
        outerCore.rotation.x = elapsedTime * 0.15;
        outerCore.rotation.y = elapsedTime * 0.25;

        innerCore.rotation.x = -elapsedTime * 0.3;
        innerCore.rotation.y = -elapsedTime * 0.2;

        particleRing.rotation.y = elapsedTime * 0.1;
        particleRing.rotation.z = elapsedTime * 0.05;

        // Smooth Mouse Parallax Lerp
        targetX += (mouseX - targetX) * 0.05;
        targetY += (mouseY - targetY) * 0.05;

        scene.rotation.y = targetX * 0.4;
        scene.rotation.x = targetY * 0.4;

        renderer.render(scene, camera);
    }
    animate();
}

/* --------------------------------------------------------------------------
   2. 3D CARD TILT PHYSICS
   -------------------------------------------------------------------------- */
function init3DCardPhysics() {
    const cards = document.querySelectorAll('.project-card, .timeline-content, .skill-category-card');

    cards.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            const centerX = rect.width / 2;
            const centerY = rect.height / 2;

            const rotateX = (centerY - y) / 16;
            const rotateY = (x - centerX) / 16;

            card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.02, 1.02, 1.02)`;
        });

        card.addEventListener('mouseleave', () => {
            card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)';
        });
    });
}

/* --------------------------------------------------------------------------
   3. HERO TYPING EFFECT
   -------------------------------------------------------------------------- */
function initTypingEffect() {
    const el = document.getElementById('typing-text');
    if (!el) return;

    const titles = [
        "AI & ML Engineer",
        "Generative AI Specialist",
        "Multi-Agent RAG Architect",
        "Vision-Language Model Fine-Tuner",
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
            typingSpeed = 40;
        } else {
            el.textContent = currentTitle.substring(0, charIndex + 1);
            charIndex++;
            typingSpeed = 90;
        }

        if (!isDeleting && charIndex === currentTitle.length) {
            typingSpeed = 2200; // Pause at full title
            isDeleting = true;
        } else if (isDeleting && charIndex === 0) {
            isDeleting = false;
            titleIndex = (titleIndex + 1) % titles.length;
            typingSpeed = 400;
        }

        setTimeout(type, typingSpeed);
    }
    type();
}

/* --------------------------------------------------------------------------
   4. PROJECT CATEGORY FILTERING & MODAL VIEWER
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
                <div class="project-badge" style="margin-bottom: 14px; display: inline-block;">${project.category} • ${project.period}</div>
                <h2 style="font-size: 2rem; margin-bottom: 14px;">${project.title}</h2>
                <p style="color: var(--primary-cyan); font-weight: 600; margin-bottom: 22px; font-size: 1.05rem;">${project.tagline}</p>
                <p style="color: var(--text-muted); margin-bottom: 26px; line-height: 1.8;">${project.description}</p>
                
                <h4 style="color: #FFF; margin-bottom: 14px; font-size: 1.15rem;">Key Architecture & Deliverables:</h4>
                <ul style="list-style: none; margin-bottom: 28px;">
                    ${project.features.map(f => `<li style="color: var(--text-muted); margin-bottom: 10px; position: relative; padding-left: 24px;"><span style="position: absolute; left: 0; color: var(--accent-emerald);">✓</span> ${f}</li>`).join('')}
                </ul>

                <h4 style="color: #FFF; margin-bottom: 14px; font-size: 1.15rem;">Tech Stack:</h4>
                <div style="display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 32px;">
                    ${project.tech_stack.map(t => `<span class="tech-tag" style="background: rgba(0, 242, 254, 0.1); border-color: rgba(0, 242, 254, 0.3); color: var(--primary-cyan); font-size: 0.85rem; padding: 6px 14px;">${t}</span>`).join('')}
                </div>

                <div style="display: flex; gap: 16px;">
                    ${project.github !== '#' ? `<a href="${project.github}" target="_blank" class="btn-primary" style="padding: 12px 28px; font-size: 0.92rem;">View GitHub Repo</a>` : ''}
                    <button onclick="closeModal()" class="btn-secondary" style="padding: 12px 28px; font-size: 0.92rem;">Close Window</button>
                </div>
            `;

            document.getElementById('project-modal').classList.add('open');
        });
}

function closeModal() {
    document.getElementById('project-modal').classList.remove('open');
}

/* --------------------------------------------------------------------------
   5. AI CHATBOT DRAWER
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

        appendBubble(text, 'user');
        chatInput.value = '';

        const typingId = appendBubble('Processing query...', 'bot');

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
            document.getElementById(typingId).textContent = "Sorry, I am temporarily offline. Reach out via srujansrutha01@gmail.com!";
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
   6. CONTACT FORM SUBMISSION
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
        statusDiv.textContent = "Transmitting message...";

        fetch('/api/contact', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, email, message })
        })
        .then(res => res.json())
        .then(data => {
            statusDiv.textContent = data.message;
            statusDiv.style.borderColor = 'var(--accent-emerald)';
            statusDiv.style.color = 'var(--accent-emerald)';
            form.reset();
        })
        .catch(() => {
            statusDiv.textContent = "Message failed. Direct email: srujansrutha01@gmail.com";
        });
    });
}

/* --------------------------------------------------------------------------
   7. SCROLLSPY FOR NAVBAR
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
