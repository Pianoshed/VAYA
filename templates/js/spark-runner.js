// Spark Runner Game JavaScript - Enhanced Edition
// ═══════════════════════════════════════════════

// ═══════════ GAME STATE ═══════════
const gameState = {
    score: 0,
    active: false,
    playerY: 380,
    velocity: 0,
    glimmers: [],
    target: 10,
    isJumping: false,
    canDoubleJump: false,
    hasDoubleJumped: false,
    consecutiveMisses: 0,
    maxMisses: 5,
    lastSpawnTime: 0,
    minSpawnInterval: 900,
    baseSpeed: 6,
    currentSpeed: 6,
    speedMultiplier: 1.0,
    totalCollected: 0,
    savedGender: 'male',
    groundY: 380,
    // Powerup state
    powerups: [],
    lastPowerupSpawn: 0,
    powerupSpawnInterval: 18000,
    activePowerups: {},
    speedBoost: 1.0,
    scoreMultiplier: 1,
    jumpBoost: 1.0,
    words: [
        "Safety", "Comfort", "A Good Song", "Deep Breath", "Warm Tea",
        "Kindness", "Sunshine", "A Hug", "Laughter", "Nature",
        "Music", "Rest", "Hope", "Peace", "Love",
        "Brave", "Strong", "Faith", "Calm", "Grow",
        "Heal", "Joy", "Dream", "Rise", "Free"
    ],
    quotes: [
        "You are doing better than you think.",
        "This feeling is temporary. You are strong.",
        "Progress is not always a straight line.",
        "You deserve peace of mind.",
        "You have survived 100% of your bad days.",
        "Every small step forward is a victory.",
        "You are worthy of rest and healing.",
        "Your journey matters, even on difficult days.",
        "Be gentle with yourself. You're doing your best.",
        "The light always returns, even after the darkest night."
    ]
};

// ═══════════ POWERUP SYSTEM ═══════════
const POWERUP_TYPES = [
    { type: 'speed',      emoji: '🚀', name: 'Speed Boost', duration: 8000,  color: '#ff6b6b', border: '#ffcccc' },
    { type: 'shield',     emoji: '🛡️', name: 'Shield',      duration: 15000, color: '#4ecdc4', border: '#ccf2ff' },
    { type: 'multiplier', emoji: '⭐', name: '2x Score',     duration: 10000, color: '#ffd93d', border: '#fff5cc' },
    { type: 'superjump',  emoji: '🦘', name: 'Super Jump',   duration: 12000, color: '#b06ab3', border: '#e8ccff' }
];

function updatePowerupDisplay() {
    const container = document.getElementById('powerup-status');
    if (!container) return;
    container.innerHTML = '';

    Object.keys(gameState.activePowerups).forEach(type => {
        const pw = gameState.activePowerups[type];
        const timeLeft = Math.ceil((pw.endTime - Date.now()) / 1000);
        if (timeLeft > 0) {
            const cfg = POWERUP_TYPES.find(p => p.type === type);
            const div = document.createElement('div');
            div.className = 'powerup-active';
            div.style.borderColor = cfg.border;
            div.style.color = cfg.color;
            div.innerHTML = `${cfg.emoji} <span style="color:#fff">${timeLeft}s</span>`;
            container.appendChild(div);
        }
    });
}

function activatePowerup(type) {
    haptic('powerup');
    const cfg = POWERUP_TYPES.find(p => p.type === type);

    // Refresh if already active
    if (gameState.activePowerups[type]) {
        clearTimeout(gameState.activePowerups[type].timeout);
    }

    const endTime = Date.now() + cfg.duration;
    const timeout = setTimeout(() => deactivatePowerup(type), cfg.duration);
    gameState.activePowerups[type] = { endTime, timeout };

    // Apply effect
    if (type === 'speed')      gameState.speedBoost = 1.5;
    if (type === 'shield')     { const p = document.getElementById('player'); if (p) p.classList.add('shield-active'); }
    if (type === 'multiplier') gameState.scoreMultiplier = 2;
    if (type === 'superjump')  gameState.jumpBoost = 1.4;

    showPowerupBanner(cfg);
    updatePowerupDisplay();
}

function deactivatePowerup(type) {
    if (!gameState.activePowerups[type]) return;
    delete gameState.activePowerups[type];

    if (type === 'speed')      gameState.speedBoost = 1.0;
    if (type === 'shield')     { const p = document.getElementById('player'); if (p) p.classList.remove('shield-active'); }
    if (type === 'multiplier') gameState.scoreMultiplier = 1;
    if (type === 'superjump')  gameState.jumpBoost = 1.0;

    updatePowerupDisplay();
}

function clearAllPowerups() {
    Object.keys(gameState.activePowerups).forEach(type => {
        clearTimeout(gameState.activePowerups[type].timeout);
    });
    gameState.activePowerups = {};
    gameState.speedBoost    = 1.0;
    gameState.scoreMultiplier = 1;
    gameState.jumpBoost     = 1.0;
    updatePowerupDisplay();
}

function showPowerupBanner(cfg) {
    const banner = document.getElementById('powerup-banner');
    if (!banner) return;
    banner.innerHTML = `<span style="color:${cfg.color}">${cfg.emoji} ${cfg.name.toUpperCase()}!</span>`;
    banner.classList.remove('show');
    void banner.offsetWidth;
    banner.classList.add('show');
    setTimeout(() => banner.classList.remove('show'), 2200);
}

// ═══════════ HAPTIC FEEDBACK ═══════════
function haptic(type) {
    if (!navigator.vibrate) return;
    const patterns = {
        light:    [10],
        medium:   [30],
        collect:  [15],
        miss:     [40],
        levelUp:  [20, 30, 20, 30, 50],
        gameOver: [100, 50, 100, 50, 200],
        powerup:  [10, 20, 10, 20, 30]
    };
    navigator.vibrate(patterns[type] || patterns.medium);
}

// ═══════════ IMPROVED FEMALE CHARACTER ═══════════
const femaleCharacter = `
<svg viewBox="0 0 80 130" xmlns="http://www.w3.org/2000/svg" style="filter:drop-shadow(0 3px 6px rgba(0,0,0,0.4))">
  <!-- Ponytail -->
  <ellipse cx="64" cy="22" rx="7" ry="13" fill="#5d3a37" transform="rotate(20 64 22)"/>
  <ellipse cx="62" cy="28" rx="4" ry="9"  fill="#4a2c2a" transform="rotate(25 62 28)"/>

  <!-- Hair top -->
  <ellipse cx="38" cy="18" rx="20" ry="17" fill="#5d3a37"/>
  <path d="M 18 20 Q 18 8 38 7 Q 56 8 58 20 L 56 30 Q 52 24 38 24 Q 24 24 22 30 Z" fill="#6b4441"/>

  <!-- Head -->
  <ellipse cx="38" cy="32" rx="18" ry="20" fill="#ffdbac"/>

  <!-- Eyes with lashes -->
  <ellipse cx="31" cy="30" rx="4" ry="4.5" fill="white"/>
  <ellipse cx="45" cy="30" rx="4" ry="4.5" fill="white"/>
  <circle cx="31" cy="31" r="2.5" fill="#3d2817"/>
  <circle cx="45" cy="31" r="2.5" fill="#3d2817"/>
  <circle cx="31.8" cy="30" r="1"   fill="white" opacity="0.9"/>
  <circle cx="45.8" cy="30" r="1"   fill="white" opacity="0.9"/>
  <!-- Upper lashes -->
  <path d="M 27 27 Q 31 25 35 27" stroke="#3d2817" stroke-width="1.4" fill="none" stroke-linecap="round"/>
  <path d="M 41 27 Q 45 25 49 27" stroke="#3d2817" stroke-width="1.4" fill="none" stroke-linecap="round"/>

  <!-- Eyebrows -->
  <path d="M 26 24 Q 31 22 35 23" stroke="#4a2c2a" stroke-width="1.6" fill="none" stroke-linecap="round"/>
  <path d="M 41 23 Q 45 22 50 24" stroke="#4a2c2a" stroke-width="1.6" fill="none" stroke-linecap="round"/>

  <!-- Nose -->
  <path d="M 38 35 Q 36 39 38 41 Q 40 39 38 35" stroke="#e5b48a" stroke-width="1" fill="rgba(200,140,100,0.2)" stroke-linecap="round"/>

  <!-- Lips -->
  <path d="M 33 44 Q 35 42 38 43 Q 41 42 43 44" fill="#e87b8c"/>
  <path d="M 33 44 Q 38 47 43 44" fill="#d4607a"/>
  <path d="M 33 44 Q 38 46 43 44" stroke="#c05570" stroke-width="0.5" fill="none"/>

  <!-- Cheeks -->
  <ellipse cx="27" cy="38" rx="5" ry="3" fill="rgba(255,160,150,0.3)"/>
  <ellipse cx="49" cy="38" rx="5" ry="3" fill="rgba(255,160,150,0.3)"/>

  <!-- Neck -->
  <rect x="32" y="50" width="12" height="8" rx="3" fill="#ffdbac"/>

  <!-- Sports bra top -->
  <path d="M 16 62 Q 17 58 22 57 L 54 57 Q 59 58 60 62 L 58 72 Q 52 70 38 70 Q 24 70 18 72 Z" fill="#ff6b9d"/>
  <ellipse cx="38" cy="65" rx="20" ry="8" fill="#ff75a0"/>

  <!-- Torso -->
  <ellipse cx="38" cy="84" rx="17" ry="18" fill="#ff75a0"/>

  <!-- Left arm - bent back (running pose) -->
  <path d="M 21 64 Q 12 72 10 84 Q 11 88 15 87 Q 16 78 22 72 Q 26 68 24 64 Z" fill="#ffdbac"/>
  <!-- Left forearm -->
  <ellipse cx="10" cy="84" rx="4" ry="10" fill="#ffdbac" transform="rotate(-10 10 84)"/>

  <!-- Right arm - bent forward (running pose) -->
  <path d="M 55 64 Q 64 72 66 84 Q 65 88 61 87 Q 60 78 54 72 Q 50 68 52 64 Z" fill="#ffdbac"/>
  <!-- Right forearm -->
  <ellipse cx="66" cy="84" rx="4" ry="10" fill="#ffdbac" transform="rotate(10 66 84)"/>

  <!-- Leggings -->
  <!-- Left leg (forward) -->
  <path d="M 30 98 Q 28 110 26 118 Q 25 124 28 124 Q 32 124 33 118 Q 35 110 36 98 Z" fill="#c9184a"/>
  <!-- Left shin -->
  <ellipse cx="27" cy="122" rx="4" ry="9" fill="#ffdbac" transform="rotate(-5 27 122)"/>
  <!-- Left shoe -->
  <path d="M 21 130 Q 24 128 30 129 Q 32 131 30 132 Q 24 132 21 131 Z" fill="#fff"/>
  <path d="M 22 128 Q 25 127 29 128" stroke="#ddd" stroke-width="0.8" fill="none"/>

  <!-- Right leg (back) -->
  <path d="M 46 98 Q 48 110 50 118 Q 51 124 48 124 Q 44 124 43 118 Q 41 110 40 98 Z" fill="#c9184a"/>
  <!-- Right shin -->
  <ellipse cx="49" cy="122" rx="4" ry="9" fill="#ffdbac" transform="rotate(8 49 122)"/>
  <!-- Right shoe -->
  <path d="M 44 130 Q 47 128 53 129 Q 55 131 53 132 Q 47 132 44 131 Z" fill="#fff"/>
  <path d="M 45 128 Q 48 127 52 128" stroke="#ddd" stroke-width="0.8" fill="none"/>

  <!-- Shoe accent stripes -->
  <path d="M 22 130 L 24 129" stroke="#4cc9f0" stroke-width="1" stroke-linecap="round"/>
  <path d="M 45 130 L 47 129" stroke="#4cc9f0" stroke-width="1" stroke-linecap="round"/>
</svg>`;

// ═══════════ IMPROVED MALE CHARACTER ═══════════
const maleCharacter = `
<svg viewBox="0 0 80 130" xmlns="http://www.w3.org/2000/svg" style="filter:drop-shadow(0 3px 6px rgba(0,0,0,0.4))">
  <!-- Hair -->
  <ellipse cx="38" cy="16" rx="20" ry="14" fill="#3d2817"/>
  <path d="M 18 20 Q 18 10 38 8 Q 56 10 58 20 Q 54 14 38 15 Q 22 14 18 20 Z" fill="#4a3020"/>
  <!-- Hair texture lines -->
  <path d="M 24 14 Q 30 12 36 13" stroke="#5a3828" stroke-width="1" fill="none" stroke-linecap="round"/>
  <path d="M 38 12 Q 44 11 50 13" stroke="#5a3828" stroke-width="1" fill="none" stroke-linecap="round"/>

  <!-- Head -->
  <ellipse cx="38" cy="32" rx="20" ry="22" fill="#f1c27d"/>

  <!-- Eyes -->
  <ellipse cx="31" cy="30" rx="4" ry="4.5" fill="white"/>
  <ellipse cx="45" cy="30" rx="4" ry="4.5" fill="white"/>
  <circle cx="31" cy="31"   r="2.8" fill="#2c1810"/>
  <circle cx="45" cy="31"   r="2.8" fill="#2c1810"/>
  <circle cx="31.8" cy="30" r="1.1" fill="white" opacity="0.9"/>
  <circle cx="45.8" cy="30" r="1.1" fill="white" opacity="0.9"/>

  <!-- Eyebrows - thicker/straighter for male -->
  <path d="M 25 24 Q 31 22 35 23" stroke="#2c1810" stroke-width="2.2" fill="none" stroke-linecap="round"/>
  <path d="M 41 23 Q 45 22 51 24" stroke="#2c1810" stroke-width="2.2" fill="none" stroke-linecap="round"/>

  <!-- Nose - more defined for male -->
  <path d="M 38 34 L 36 40 Q 38 42 40 40 L 38 34" stroke="#d4a574" stroke-width="1.2" fill="rgba(180,120,70,0.15)" stroke-linecap="round" stroke-linejoin="round"/>

  <!-- Lips - thinner for male -->
  <path d="M 33 45 Q 38 44 43 45" stroke="#c49463" stroke-width="1.5" fill="none" stroke-linecap="round"/>
  <path d="M 33 45 Q 38 47 43 45" stroke="#b07840" stroke-width="1"   fill="none" stroke-linecap="round"/>

  <!-- Jaw definition -->
  <path d="M 19 36 Q 18 46 38 52 Q 58 46 57 36" stroke="rgba(180,120,60,0.15)" stroke-width="2" fill="none"/>

  <!-- Neck -->
  <rect x="31" y="52" width="14" height="10" rx="3" fill="#f1c27d"/>

  <!-- Tank top / Athletic shirt -->
  <path d="M 15 65 Q 16 60 22 58 L 54 58 Q 60 60 61 65 L 60 78 Q 52 76 38 76 Q 24 76 16 78 Z" fill="#4cc9f0"/>
  <!-- Shirt collar V-neck -->
  <path d="M 32 58 Q 38 66 44 58" stroke="#39b4d8" stroke-width="1.5" fill="none"/>
  <!-- Shirt body -->
  <ellipse cx="38" cy="88" rx="20" ry="18" fill="#4cc9f0"/>

  <!-- Shoulders wider for male -->
  <ellipse cx="16" cy="68" rx="7" ry="5" fill="#4cc9f0"/>
  <ellipse cx="60" cy="68" rx="7" ry="5" fill="#4cc9f0"/>

  <!-- Left arm - bent back (running pose) -->
  <path d="M 17 66 Q 6 76 5 90 Q 6 95 10 93 Q 11 82 18 74 Q 22 68 20 66 Z" fill="#f1c27d"/>
  <ellipse cx="5" cy="90" rx="4.5" ry="11" fill="#f1c27d" transform="rotate(-8 5 90)"/>

  <!-- Right arm - bent forward (running pose) -->
  <path d="M 59 66 Q 70 76 71 90 Q 70 95 66 93 Q 65 82 58 74 Q 54 68 56 66 Z" fill="#f1c27d"/>
  <ellipse cx="71" cy="90" rx="4.5" ry="11" fill="#f1c27d" transform="rotate(8 71 90)"/>

  <!-- Shorts -->
  <path d="M 18 94 Q 18 108 22 110 Q 30 112 38 112 Q 46 112 54 110 Q 58 108 58 94 Z" fill="#2c5f7f"/>
  <!-- Shorts seam -->
  <path d="M 38 94 L 38 112" stroke="#1a3f5f" stroke-width="1.2" fill="none"/>
  <!-- Shorts hem -->
  <path d="M 18 108 Q 38 114 58 108" stroke="#1a3f5f" stroke-width="1" fill="none"/>

  <!-- Left leg (forward) -->
  <path d="M 29 108 Q 26 116 24 122 Q 23 128 27 128 Q 31 128 32 122 Q 34 116 36 108 Z" fill="#f1c27d"/>
  <!-- Left shoe -->
  <path d="M 19 128 Q 23 126 30 127 Q 33 129 30 131 Q 23 131 19 130 Z" fill="#2d3436"/>
  <ellipse cx="26" cy="128" rx="5" ry="2.2" fill="white" opacity="0.7"/>
  <!-- Shoe stripe -->
  <path d="M 20 129 Q 25 128 29 129" stroke="#4cc9f0" stroke-width="0.9" fill="none" stroke-linecap="round"/>

  <!-- Right leg (back/lifted) -->
  <path d="M 47 108 Q 50 116 52 122 Q 53 128 49 128 Q 45 128 44 122 Q 42 116 40 108 Z" fill="#f1c27d"/>
  <!-- Right shoe -->
  <path d="M 43 128 Q 47 126 54 127 Q 57 129 54 131 Q 47 131 43 130 Z" fill="#2d3436"/>
  <ellipse cx="50" cy="128" rx="5" ry="2.2" fill="white" opacity="0.7"/>
  <path d="M 44 129 Q 49 128 53 129" stroke="#4cc9f0" stroke-width="0.9" fill="none" stroke-linecap="round"/>

  <!-- Muscle definition on arms (subtle) -->
  <path d="M 8 82 Q 6 86 7 90"  stroke="rgba(180,130,70,0.25)" stroke-width="2" fill="none" stroke-linecap="round"/>
  <path d="M 68 82 Q 70 86 69 90" stroke="rgba(180,130,70,0.25)" stroke-width="2" fill="none" stroke-linecap="round"/>
</svg>`;

// ═══════════ HELPER FUNCTIONS ═══════════
function switchPage(pageId) {
    ['start-page', 'game-page', 'levelup-page'].forEach(id => {
        const page = document.getElementById(id);
        if (page) page.style.display = 'none';
    });
    const targetPage = document.getElementById(pageId);
    if (targetPage) targetPage.style.display = 'flex';
}

function spawnParticles() {
    const gamePage = document.getElementById('game-page');
    if (!gamePage) return;
    gamePage.querySelectorAll('.particle').forEach(p => p.remove());
    for (let i = 0; i < 15; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.style.left = Math.random() * 900 + 'px';
        particle.style.animationDelay = Math.random() * 3 + 's';
        particle.style.animationDuration = (3 + Math.random() * 2) + 's';
        gamePage.appendChild(particle);
    }
}

function updateSpeed() {
    const si = Math.floor(gameState.score / 5) * 0.15;
    gameState.speedMultiplier = 1.0 + si;
    gameState.currentSpeed = (gameState.baseSpeed * gameState.speedMultiplier) * gameState.speedBoost;

    const el = document.getElementById('speed-indicator');
    if (el) el.innerText = `⚡ ${(gameState.speedMultiplier * gameState.speedBoost).toFixed(1)}x`;
}

function updateMissDisplay() {
    const el = document.getElementById('miss-val');
    if (!el) return;
    el.innerText = `❌ ${gameState.consecutiveMisses}/5`;
    if (gameState.consecutiveMisses >= 3) {
        el.classList.add('danger');
        haptic('miss');
    } else {
        el.classList.remove('danger');
    }
}

function getGroundY() {
    const gp = document.getElementById('game-page');
    return gp ? gp.offsetHeight - 38 - 100 - 8 : 380;
}

// ═══════════ GAME FUNCTIONS ═══════════
function initGame(gender) {
    console.log('Initializing game with character:', gender);

    const gnd = getGroundY();

    gameState.score             = 0;
    gameState.active            = true;
    gameState.playerY           = gnd;
    gameState.groundY           = gnd;
    gameState.velocity          = 0;
    gameState.glimmers          = [];
    gameState.isJumping         = false;
    gameState.canDoubleJump     = false;
    gameState.hasDoubleJumped   = false;
    gameState.consecutiveMisses = 0;
    gameState.currentSpeed      = gameState.baseSpeed;
    gameState.speedMultiplier   = 1.0;
    gameState.lastSpawnTime     = Date.now();
    gameState.savedGender       = gender;
    gameState.totalCollected    = 0;
    gameState.powerups          = [];
    gameState.lastPowerupSpawn  = Date.now();

    clearAllPowerups();
    switchPage('game-page');

    // Update HUD
    const scoreEl = document.getElementById('score-val');
    const targetEl = document.getElementById('target-val');
    const missEl = document.getElementById('miss-val');
    if (scoreEl)  scoreEl.innerText  = '✨ Glimmers: 0';
    if (targetEl) targetEl.innerText = '🎯 Target: ' + gameState.target;
    if (missEl)   { missEl.innerText = '❌ 0/5'; missEl.classList.remove('danger'); }

    const speedEl = document.getElementById('speed-indicator');
    if (speedEl) speedEl.innerText = '⚡ 1.0x';

    // Set character
    const player = document.getElementById('player');
    if (player) {
        player.innerHTML = gender === 'female' ? femaleCharacter : maleCharacter;
        player.classList.remove('jumping', 'shield-active');
        player.style.top = gnd + 'px';
    }

    // Clean up old elements
    document.querySelectorAll('.glimmer').forEach(g => g.remove());
    document.querySelectorAll('.powerup-item').forEach(p => p.remove());

    spawnParticles();
    console.log('Starting game loop...');
    gameLoop();
}

function returnToGame() {
    gameState.active  = true;
    gameState.groundY = getGroundY();
    switchPage('game-page');
    gameLoop();
}

function tryAgain() {
    initGame(gameState.savedGender);
}

function jump(event) {
    if (event) event.preventDefault();
    if (!gameState.active) return;

    const boost = gameState.jumpBoost || 1.0;

    if (!gameState.isJumping) {
        haptic('light');
        gameState.velocity        = -13 * boost;
        gameState.isJumping       = true;
        gameState.canDoubleJump   = true;
        gameState.hasDoubleJumped = false;
    } else if (gameState.canDoubleJump && !gameState.hasDoubleJumped) {
        haptic('light');
        gameState.velocity        = -12 * boost;
        gameState.hasDoubleJumped = true;
    }
}

function levelUp() {
    gameState.active = false;
    const randomQuote = gameState.quotes[Math.floor(Math.random() * gameState.quotes.length)];
    const quoteBox = document.getElementById('quote-box');
    if (quoteBox) quoteBox.innerText = `"${randomQuote}"`;
    switchPage('levelup-page');
    gameState.target            += 10;
    gameState.consecutiveMisses  = 0;
    haptic('levelUp');
    saveProgress();
}

function gameOver() {
    gameState.active = false;
    clearAllPowerups();
    const finalScore = document.getElementById('final-score');
    if (finalScore) finalScore.innerText = `Score: ${gameState.score} ✨`;
    haptic('gameOver');

    // If the HTML has a gameover-page, go there; otherwise stay on levelup-page
    const goPage = document.getElementById('gameover-page');
    if (goPage) {
        switchPage('gameover-page');
    } else {
        // Fallback: show levelup page with a game over message
        const quoteBox = document.getElementById('quote-box');
        if (quoteBox) quoteBox.innerText = `"You missed 5 in a row — but every run makes you stronger."`;
        switchPage('levelup-page');
    }
}

// ═══════════ MAIN GAME LOOP ═══════════
function gameLoop() {
    if (!gameState.active) return;

    const gnd = gameState.groundY || 380;

    // ── Physics ──────────────────────────
    gameState.velocity += 0.52;
    gameState.playerY  += gameState.velocity;

    if (gameState.playerY >= gnd) {
        gameState.playerY       = gnd;
        gameState.velocity      = 0;
        gameState.isJumping     = false;
        gameState.canDoubleJump = false;
        gameState.hasDoubleJumped = false;
    }
    if (gameState.playerY < 0) {
        gameState.playerY  = 0;
        gameState.velocity = 0;
    }

    // ── Update player element ────────────
    const player = document.getElementById('player');
    if (player) {
        player.style.top = Math.round(gameState.playerY) + 'px';
        // Only set class if shield-active isn't present
        if (!gameState.activePowerups['shield']) {
            player.className = gameState.isJumping ? 'jumping' : '';
        } else {
            player.className = gameState.isJumping ? 'jumping shield-active' : 'shield-active';
        }
    }

    const now = Date.now();
    const gameWidth = (document.getElementById('game-page') || {}).offsetWidth || 900;

    // ── Spawn glimmers ───────────────────
    const spawnInterval = Math.max(500, gameState.minSpawnInterval / gameState.speedMultiplier);
    if (now - gameState.lastSpawnTime > spawnInterval && Math.random() < 0.045) {
        const word  = gameState.words[Math.floor(Math.random() * gameState.words.length)];
        const gId   = 'g-' + now + '-' + Math.floor(Math.random() * 9999);
        const glimmer = document.createElement('div');
        glimmer.className  = 'glimmer';
        glimmer.id         = gId;
        glimmer.innerText  = word;
        glimmer.style.left = gameWidth + 'px';

        const yOffsets = [gnd - 10, gnd - 60, gnd - 120, gnd - 190, gnd - 240, gnd - 30, gnd - 90, gnd - 150];
        const yPos     = Math.max(60, yOffsets[Math.floor(Math.random() * yOffsets.length)]);
        glimmer.style.top = yPos + 'px';

        const gamePage = document.getElementById('game-page');
        if (gamePage) {
            gamePage.appendChild(glimmer);
            gameState.glimmers.push({ id: gId, x: gameWidth, y: yPos, missed: false });
        }
        gameState.lastSpawnTime = now;
    }

    // ── Spawn powerups ───────────────────
    if (now - gameState.lastPowerupSpawn > gameState.powerupSpawnInterval && Math.random() < 0.025) {
        const cfg  = POWERUP_TYPES[Math.floor(Math.random() * POWERUP_TYPES.length)];
        const pid  = 'pu-' + now + '-' + Math.floor(Math.random() * 9999);
        const pel  = document.createElement('div');
        pel.className = 'powerup-item';
        pel.id        = pid;
        pel.innerText = cfg.emoji;
        pel.style.left = gameWidth + 'px';
        pel.style.borderColor = cfg.border;
        pel.style.boxShadow   = `0 0 16px ${cfg.color}, 0 0 32px ${cfg.color}55`;

        const yPos = Math.max(80, gnd - 20 - Math.floor(Math.random() * 200));
        pel.style.top = yPos + 'px';

        const gamePage = document.getElementById('game-page');
        if (gamePage) {
            gamePage.appendChild(pel);
            gameState.powerups.push({ id: pid, x: gameWidth, y: yPos, type: cfg.type });
        }
        gameState.lastPowerupSpawn = now;
    }

    // ── Player hit-box ───────────────────
    const playerCenterX = (document.getElementById('game-page') || {}).offsetWidth
        ? Math.floor(document.getElementById('game-page').offsetWidth * 0.10) + 30
        : 120;
    const playerCenterY = gameState.playerY + 50;

    // ── Move & check glimmers ────────────
    for (let i = gameState.glimmers.length - 1; i >= 0; i--) {
        const g  = gameState.glimmers[i];
        g.x     -= gameState.currentSpeed;
        const el = document.getElementById(g.id);
        if (!el) { gameState.glimmers.splice(i, 1); continue; }
        el.style.left = Math.round(g.x) + 'px';

        const glimmerCX = g.x + 50;
        const glimmerCY = g.y + 18;

        // Collect
        if (Math.abs(playerCenterX - glimmerCX) < 65 && Math.abs(playerCenterY - glimmerCY) < 55) {
            haptic('collect');
            const pts = 1 * gameState.scoreMultiplier;
            gameState.score          += pts;
            gameState.totalCollected++;
            gameState.consecutiveMisses = 0;

            const scoreEl = document.getElementById('score-val');
            if (scoreEl) scoreEl.innerText = '✨ Glimmers: ' + gameState.score;
            updateMissDisplay();
            updateSpeed();

            el.style.transition = 'all 0.3s ease';
            el.style.transform  = 'scale(2) rotate(360deg)';
            el.style.opacity    = '0';
            setTimeout(() => { if (el.parentNode) el.remove(); }, 300);
            gameState.glimmers.splice(i, 1);

            if (gameState.score >= gameState.target) { levelUp(); return; }

        // Miss
        } else if (g.x < -120) {
            if (!g.missed) {
                g.missed = true;
                if (gameState.activePowerups['shield']) {
                    // Shield absorbs this miss
                    deactivatePowerup('shield');
                } else {
                    gameState.consecutiveMisses++;
                    updateMissDisplay();
                    if (gameState.consecutiveMisses >= gameState.maxMisses) {
                        el.remove();
                        gameState.glimmers.splice(i, 1);
                        gameOver();
                        return;
                    }
                }
            }
            el.remove();
            gameState.glimmers.splice(i, 1);
        }
    }

    // ── Move & check powerups ────────────
    for (let i = gameState.powerups.length - 1; i >= 0; i--) {
        const pow = gameState.powerups[i];
        pow.x    -= gameState.currentSpeed;
        const el  = document.getElementById(pow.id);
        if (!el) { gameState.powerups.splice(i, 1); continue; }
        el.style.left = Math.round(pow.x) + 'px';

        const powCX = pow.x + 20;
        const powCY = pow.y + 20;

        if (Math.abs(playerCenterX - powCX) < 50 && Math.abs(playerCenterY - powCY) < 50) {
            activatePowerup(pow.type);
            el.style.transition = 'all 0.3s ease';
            el.style.transform  = 'scale(2.5) rotate(360deg)';
            el.style.opacity    = '0';
            setTimeout(() => { if (el.parentNode) el.remove(); }, 300);
            gameState.powerups.splice(i, 1);
        } else if (pow.x < -60) {
            el.remove();
            gameState.powerups.splice(i, 1);
        }
    }

    // ── Refresh powerup timers ───────────
    updatePowerupDisplay();

    requestAnimationFrame(gameLoop);
}

// ═══════════ BACKEND API ═══════════
async function saveProgress() {
    try {
        const response = await fetch('/api/save_progress', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                glimmers:  gameState.score,
                target:    gameState.target,
                timestamp: new Date().toISOString()
            })
        });
        if (response.ok) {
            const data = await response.json();
            console.log('Progress saved:', data);
        }
    } catch (error) {
        console.log('Could not save to backend:', error);
    }
}

// ═══════════ INITIALIZATION ═══════════
function initializeGame() {
    console.log('Spark Runner Game Loaded! 🎮✨');

    // Expose functions globally (preserves all existing HTML onclick bindings)
    window.initGame     = initGame;
    window.returnToGame = returnToGame;
    window.tryAgain     = tryAgain;
    window.jump         = jump;

    // ── Keyboard ──────────────────────────
    document.addEventListener('keydown', e => {
        if (e.code === 'Space' || e.key === ' ') {
            e.preventDefault();
            jump(e);
        }
    });

    // ── Click/Tap (skip buttons & links) ──
    const gameWindow = document.getElementById('game-window');
    if (gameWindow) {
        gameWindow.addEventListener('click', e => {
            const tag = e.target.tagName;
            if (tag === 'BUTTON' || tag === 'A') return;
            jump(e);
        });
    }

    document.addEventListener('touchstart', e => {
        const tag = e.target.tagName;
        if (tag === 'BUTTON' || tag === 'A') return;
        if (gameState.active) { e.preventDefault(); jump(e); }
    }, { passive: false });

    console.log('Event listeners initialized ✅');
}

// ── Boot ──────────────────────────────────
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeGame);
} else {
    initializeGame();
}