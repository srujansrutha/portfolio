/* ==========================================================================
   J SRUJAN VISHWAKARMA - 3D MECH ROBOT & FUCH.AI INTERACTIVE CONTROLLER
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
    init3DMechRobot();
    initPromptChips();
    initTypingEffect();
    initProjectFiltering();
    initChatBot();
    initContactForm();
    initScrollSpy();
});

/* --------------------------------------------------------------------------
   1. THREE.JS 3D MECH ROBOT / CHARACTER SCENE (FUCH.AI CENTERPIECE)
   -------------------------------------------------------------------------- */
function init3DMechRobot() {
    const canvas = document.getElementById('mech-canvas');
    if (!canvas || typeof THREE === 'undefined') return;

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(45, canvas.clientWidth / canvas.clientHeight, 0.1, 1000);
    camera.position.set(0, 0, 5.5);

    const renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true, alpha: true });
    renderer.setSize(canvas.clientWidth, canvas.clientHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

    window.addEventListener('resize', () => {
        camera.aspect = canvas.clientWidth / canvas.clientHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(canvas.clientWidth, canvas.clientHeight);
    });

    // Robot Group
    const robot = new THREE.Group();

    // Metallic Materials
    const darkMetalMat = new THREE.MeshStandardMaterial({
        color: 0x11161B,
        roughness: 0.25,
        metalness: 0.85
    });

    const silverJointMat = new THREE.MeshStandardMaterial({
        color: 0x8A95A5,
        roughness: 0.3,
        metalness: 0.95
    });

    const glowingVisorMat = new THREE.MeshBasicMaterial({
        color: 0x05A89E
    });

    // 1. Robot Head
    const headGeo = new THREE.BoxGeometry(0.8, 0.65, 0.65);
    const head = new THREE.Mesh(headGeo, darkMetalMat);
    head.position.y = 1.1;

    // Glowing Visor
    const visorGeo = new THREE.BoxGeometry(0.55, 0.16, 0.05);
    const visor = new THREE.Mesh(visorGeo, glowingVisorMat);
    visor.position.set(0, 0.05, 0.33);
    head.add(visor);

    // Ears / Antenna Joints
    const earGeo = new THREE.CylinderGeometry(0.08, 0.08, 0.15, 16);
    const leftEar = new THREE.Mesh(earGeo, silverJointMat);
    leftEar.rotation.z = Math.PI / 2;
    leftEar.position.set(-0.45, 0.05, 0);
    head.add(leftEar);

    const rightEar = leftEar.clone();
    rightEar.position.x = 0.45;
    head.add(rightEar);

    robot.add(head);

    // 2. Neck
    const neckGeo = new THREE.CylinderGeometry(0.12, 0.14, 0.2, 16);
    const neck = new THREE.Mesh(neckGeo, silverJointMat);
    neck.position.y = 0.72;
    robot.add(neck);

    // 3. Torso
    const torsoGeo = new THREE.BoxGeometry(1.0, 1.1, 0.7);
    const torso = new THREE.Mesh(torsoGeo, darkMetalMat);
    torso.position.y = 0.1;

    // Chest Plate Light Accent
    const chestPlateGeo = new THREE.BoxGeometry(0.5, 0.3, 0.05);
    const chestPlate = new THREE.Mesh(chestPlateGeo, glowingVisorMat);
    chestPlate.position.set(0, 0.15, 0.36);
    torso.add(chestPlate);

    robot.add(torso);

    // 4. Arms & Shoulders
    const shoulderGeo = new THREE.SphereGeometry(0.2, 16, 16);
    const leftShoulder = new THREE.Mesh(shoulderGeo, silverJointMat);
    leftShoulder.position.set(-0.68, 0.5, 0);

    const leftArmGeo = new THREE.CylinderGeometry(0.1, 0.09, 0.7, 16);
    const leftArm = new THREE.Mesh(leftArmGeo, darkMetalMat);
    leftArm.position.set(0, -0.4, 0);
    leftShoulder.add(leftArm);
    robot.add(leftShoulder);

    const rightShoulder = leftShoulder.clone();
    rightShoulder.position.x = 0.68;
    robot.add(rightShoulder);

    // 5. Floating Base Ring (Hologram Stand)
    const ringGeo = new THREE.TorusGeometry(1.3, 0.02, 16, 100);
    const ringMat = new THREE.MeshBasicMaterial({ color: 0x05A89E, transparent: true, opacity: 0.6 });
    const ring = new THREE.Mesh(ringGeo, ringMat);
    ring.rotation.x = Math.PI / 2;
    ring.position.y = -1.1;
    robot.add(ring);

    scene.add(robot);

    // Lighting
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.7);
    scene.add(ambientLight);

    const dirLight = new THREE.DirectionalLight(0xffffff, 1.2);
    dirLight.position.set(5, 10, 7);
    scene.add(dirLight);

    const blueLight = new THREE.PointLight(0x05A89E, 2, 20);
    blueLight.position.set(-3, 2, 4);
    scene.add(blueLight);

    // Mouse Tracking for 3D Head & Body Tracking
    let mouseX = 0;
    let mouseY = 0;
    let targetX = 0;
    let targetY = 0;

    document.addEventListener('mousemove', (e) => {
        const windowHalfX = window.innerWidth / 2;
        const windowHalfY = window.innerHeight / 2;
        mouseX = (e.clientX - windowHalfX) / windowHalfX;
        mouseY = (e.clientY - windowHalfY) / windowHalfY;
    });

    const clock = new THREE.Clock();

    function animate() {
        requestAnimationFrame(animate);

        const elapsedTime = clock.getElapsedTime();

        // Idle floating oscillation
        robot.position.y = Math.sin(elapsedTime * 1.5) * 0.08;

        // Interactive Cursor Following
        targetX += (mouseX - targetX) * 0.05;
        targetY += (mouseY - targetY) * 0.05;

        head.rotation.y = targetX * 0.6;
        head.rotation.x = targetY * 0.4;

        torso.rotation.y = targetX * 0.25;
        ring.rotation.z = elapsedTime * 0.5;

        renderer.render(scene, camera);
    }
    animate();
}

/* --------------------------------------------------------------------------
   2. INTERACTIVE PROMPT CHIPS (FUCH.AI STYLE QUICK AI ANSWERS)
   -------------------------------------------------------------------------- */
function initPromptChips() {
    const chips = document.querySelectorAll('.prompt-chip');
    const chatDrawer = document.getElementById('chat-drawer');

    chips.forEach(chip => {
        chip.addEventListener('click', () => {
            const promptText = chip.getAttribute('data-prompt');
            if (!promptText) return;

            // Open Chat Drawer & Send Prompt
            if (chatDrawer) chatDrawer.classList.add('open');
            
            const chatInput = document.getElementById('chat-input');
            const sendBtn = document.getElementById('chat-send-btn');
            if (chatInput && sendBtn) {
                chatInput.value = promptText;
                sendBtn.click();
            }
        });
    });
}

/* --------------------------------------------------------------------------
   3. HERO TYPING EFFECT
   -------------------------------------------------------------------------- */
function initTypingEffect() {
    const el = document.getElementById('typing-text');
    if (!el) return;

    const textToType = "i'm srujan — ai & ml engineer. ask me anything about my work.";
    let charIndex = 0;

    function type() {
        if (charIndex < textToType.length) {
            el.textContent += textToType.charAt(charIndex);
            charIndex++;
            setTimeout(type, 40);
        }
    }
    el.textContent = "";
    type();
}

/* --------------------------------------------------------------------------
   4. PROJECT CATEGORY FILTERING & MODAL VIEWER
   -------------------------------------------------------------------------- */
function initProjectFiltering() {
    const filterBtns = document.querySelectorAll('.filter-btn, .pill-nav-item');
    const projectCards = document.querySelectorAll('.project-card');

    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const filter = btn.getAttribute('data-filter')?.toLowerCase();
            if (!filter) return;

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
                <h2 style="font-size: 2rem; margin-bottom: 12px; color: var(--primary-dark);">${project.title}</h2>
                <p style="color: var(--accent-teal); font-weight: 600; margin-bottom: 20px;">${project.tagline}</p>
                <p style="color: var(--text-muted); margin-bottom: 24px; line-height: 1.7;">${project.description}</p>
                
                <h4 style="color: var(--primary-dark); margin-bottom: 12px; font-size: 1.1rem;">Key Architecture & Deliverables:</h4>
                <ul style="list-style: none; margin-bottom: 24px;">
                    ${project.features.map(f => `<li style="color: var(--text-muted); margin-bottom: 8px; position: relative; padding-left: 20px;"><span style="position: absolute; left: 0; color: var(--accent-teal);">✓</span> ${f}</li>`).join('')}
                </ul>

                <h4 style="color: var(--primary-dark); margin-bottom: 12px; font-size: 1.1rem;">Tech Stack:</h4>
                <div style="display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 28px;">
                    ${project.tech_stack.map(t => `<span class="tech-tag" style="background: rgba(5, 168, 158, 0.1); border-color: rgba(5, 168, 158, 0.2); color: var(--accent-teal);">${t}</span>`).join('')}
                </div>

                <div style="display: flex; gap: 16px;">
                    ${project.github !== '#' ? `<a href="${project.github}" target="_blank" class="pill-nav-btn" style="padding: 10px 24px; font-size: 0.9rem;">View GitHub Repo</a>` : ''}
                    <button onclick="closeModal()" class="prompt-chip" style="padding: 10px 24px; font-size: 0.9rem;">Close Window</button>
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
            statusDiv.style.borderColor = 'var(--accent-teal)';
            statusDiv.style.color = 'var(--accent-teal)';
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
    const navLinks = document.querySelectorAll('.pill-nav-item');

    window.addEventListener('scroll', () => {
        let current = '';
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            if (pageYOffset >= sectionTop - 180) {
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
