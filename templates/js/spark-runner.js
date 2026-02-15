// Spark Runner Game JavaScript
// Game State
const gameState = {
    score: 0,
    active: false,
    playerY: 380,
    velocity: 0,
    glimmers: [],
    target: 10,
    isJumping: false,
    words: ["Safety", "Comfort", "A Good Song", "Deep Breath", "Warm Tea", 
            "Kindness", "Sunshine", "A Hug", "Laughter", "Nature", 
            "Music", "Rest", "Hope", "Peace", "Love"],
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

// Character SVGs
const femaleCharacter = `
<svg viewBox="0 0 100 140" style="filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));">
    <!-- Hair -->
    <ellipse cx="50" cy="32" rx="28" ry="32" fill="#4a2c2a"/>
    <path d="M 22 32 Q 22 15 50 10 Q 78 15 78 32 L 78 45 Q 78 35 50 35 Q 22 35 22 45 Z" fill="#5d3a37"/>
    
    <!-- Head -->
    <ellipse cx="50" cy="45" rx="22" fill="#ffdbac"/>
    <ellipse cx="50" cy="50" rx="20" ry="24" fill="#ffdbac"/>
    
    <!-- Eyes -->
    <ellipse cx="42" cy="48" rx="3" ry="4" fill="white"/>
    <ellipse cx="58" cy="48" rx="3" ry="4" fill="white"/>
    <circle cx="42" cy="49" r="2" fill="#3d2817"/>
    <circle cx="58" cy="49" r="2" fill="#3d2817"/>
    <circle cx="42.5" cy="48.5" r="0.8" fill="white" opacity="0.8"/>
    <circle cx="58.5" cy="48.5" r="0.8" fill="white" opacity="0.8"/>
    
    <!-- Eyebrows -->
    <path d="M 36 42 Q 42 40 46 41" stroke="#3d2817" stroke-width="1.5" fill="none" stroke-linecap="round"/>
    <path d="M 54 41 Q 58 40 64 42" stroke="#3d2817" stroke-width="1.5" fill="none" stroke-linecap="round"/>
    
    <!-- Nose -->
    <path d="M 50 52 L 48 57" stroke="#e5c49c" stroke-width="1" fill="none" stroke-linecap="round"/>
    
    <!-- Smile -->
    <path d="M 43 60 Q 50 63 57 60" stroke="#d4a574" stroke-width="1.5" fill="none" stroke-linecap="round"/>
    
    <!-- Neck -->
    <rect x="44" y="68" width="12" height="10" fill="#ffdbac" rx="2"/>
    
    <!-- Body - Running outfit -->
    <ellipse cx="50" cy="95" rx="24" ry="28" fill="#ff75a0"/>
    <path d="M 26 95 L 30 120 L 35 120 L 32 95 Z" fill="#ff75a0"/>
    <path d="M 74 95 L 70 120 L 65 120 L 68 95 Z" fill="#ff75a0"/>
    
    <!-- Arms -->
    <ellipse cx="28" cy="90" rx="6" ry="18" fill="#ffdbac" transform="rotate(-20 28 90)"/>
    <ellipse cx="72" cy="90" rx="6" ry="18" fill="#ffdbac" transform="rotate(20 72 90)"/>
    
    <!-- Legs -->
    <rect x="40" y="118" width="8" height="20" fill="#ff6b9d" rx="4"/>
    <rect x="52" y="118" width="8" height="20" fill="#ff6b9d" rx="4"/>
    
    <!-- Shoes -->
    <ellipse cx="44" cy="138" rx="6" ry="4" fill="#fff"/>
    <ellipse cx="56" cy="138" rx="6" ry="4" fill="#fff"/>
</svg>
`;

const maleCharacter = `
<svg viewBox="0 0 100 140" style="filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));">
    <!-- Hair -->
    <ellipse cx="50" cy="30" rx="24" ry="18" fill="#3d2817"/>
    <path d="M 26 35 Q 30 25 35 30 Q 40 25 45 30 Q 50 22 55 30 Q 60 25 65 30 Q 70 25 74 35" 
          fill="#3d2817" stroke="none"/>
    
    <!-- Head -->
    <ellipse cx="50" cy="45" rx="22" ry="26" fill="#f1c27d"/>
    
    <!-- Eyes -->
    <ellipse cx="42" cy="46" rx="3" ry="4" fill="white"/>
    <ellipse cx="58" cy="46" rx="3" ry="4" fill="white"/>
    <circle cx="42" cy="47" r="2" fill="#2c1810"/>
    <circle cx="58" cy="47" r="2" fill="#2c1810"/>
    <circle cx="42.5" cy="46.5" r="0.8" fill="white" opacity="0.8"/>
    <circle cx="58.5" cy="46.5" r="0.8" fill="white" opacity="0.8"/>
    
    <!-- Eyebrows -->
    <path d="M 36 40 Q 42 38 46 39" stroke="#2c1810" stroke-width="2" fill="none" stroke-linecap="round"/>
    <path d="M 54 39 Q 58 38 64 40" stroke="#2c1810" stroke-width="2" fill="none" stroke-linecap="round"/>
    
    <!-- Nose -->
    <path d="M 50 50 L 48 56" stroke="#d4a574" stroke-width="1.5" fill="none" stroke-linecap="round"/>
    
    <!-- Smile -->
    <path d="M 42 59 Q 50 62 58 59" stroke="#c49463" stroke-width="1.5" fill="none" stroke-linecap="round"/>
    
    <!-- Neck -->
    <rect x="43" y="68" width="14" height="12" fill="#f1c27d" rx="2"/>
    
    <!-- Body - Athletic shirt -->
    <ellipse cx="50" cy="98" rx="26" ry="30" fill="#4cc9f0"/>
    <rect x="24" y="85" width="52" height="15" fill="#4cc9f0" rx="3"/>
    
    <!-- Arms in running position -->
    <ellipse cx="26" cy="92" rx="7" ry="20" fill="#f1c27d" transform="rotate(-25 26 92)"/>
    <ellipse cx="74" cy="92" rx="7" ry="20" fill="#f1c27d" transform="rotate(25 74 92)"/>
    
    <!-- Shorts -->
    <rect x="38" y="118" width="24" height="18" fill="#2c5f7f" rx="4"/>
    
    <!-- Legs -->
    <rect x="40" y="130" width="8" height="8" fill="#f1c27d" rx="4"/>
    <rect x="52" y="130" width="8" height="8" fill="#f1c27d" rx="4"/>
    
    <!-- Shoes -->
    <ellipse cx="44" cy="138" rx="7" ry="4" fill="#2d3436"/>
    <ellipse cx="56" cy="138" rx="7" ry="4" fill="#2d3436"/>
    <ellipse cx="44" cy="138" rx="5" ry="2.5" fill="#fff"/>
    <ellipse cx="56" cy="138" rx="5" ry="2.5" fill="#fff"/>
</svg>
`;

// Helper Functions
function switchPage(pageId) {
    ['start-page', 'game-page', 'levelup-page'].forEach(id => {
        const page = document.getElementById(id);
        if (page) {
            page.style.display = 'none';
        }
    });
    const targetPage = document.getElementById(pageId);
    if (targetPage) {
        targetPage.style.display = 'flex';
    }
}

function spawnParticles() {
    const gamePage = document.getElementById('game-page');
    if (!gamePage) return;
    
    // Remove old particles first
    const oldParticles = gamePage.querySelectorAll('.particle');
    oldParticles.forEach(p => p.remove());
    
    for (let i = 0; i < 15; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.style.left = Math.random() * 900 + 'px';
        particle.style.animationDelay = Math.random() * 3 + 's';
        particle.style.animationDuration = (3 + Math.random() * 2) + 's';
        gamePage.appendChild(particle);
    }
}

// Game Functions
function initGame(gender) {
    console.log('Initializing game with character:', gender);
    
    gameState.score = 0;
    gameState.active = true;
    gameState.playerY = 380;
    gameState.velocity = 0;
    gameState.glimmers = [];
    gameState.isJumping = false;
    
    switchPage('game-page');
    
    // Update display
    const scoreEl = document.getElementById('score-val');
    const targetEl = document.getElementById('target-val');
    if (scoreEl) scoreEl.innerText = '✨ Glimmers: 0';
    if (targetEl) targetEl.innerText = '🎯 Target: ' + gameState.target;
    
    // Set character
    const player = document.getElementById('player');
    if (player) {
        player.innerHTML = gender === 'female' ? femaleCharacter : maleCharacter;
        console.log('Character set successfully');
    } else {
        console.error('Player element not found!');
    }
    
    // Clear old glimmers
    document.querySelectorAll('.glimmer').forEach(g => g.remove());
    
    // Spawn particles
    spawnParticles();
    
    // Start game loop
    console.log('Starting game loop...');
    gameLoop();
}

function returnToGame() {
    gameState.active = true;
    switchPage('game-page');
    gameLoop();
}

function jump(event) {
    if (event) {
        event.preventDefault();
    }
    
    if (gameState.active && !gameState.isJumping) {
        gameState.velocity = -12;
        gameState.isJumping = true;
        console.log('Jump!');
    }
}

function levelUp() {
    gameState.active = false;
    const randomQuote = gameState.quotes[Math.floor(Math.random() * gameState.quotes.length)];
    const quoteBox = document.getElementById('quote-box');
    if (quoteBox) {
        quoteBox.innerText = `"${randomQuote}"`;
    }
    switchPage('levelup-page');
    gameState.target += 10;
    
    // Save progress to backend
    saveProgress();
}

function gameLoop() {
    if (!gameState.active) return;
    
    // Physics
    gameState.velocity += 0.5;
    gameState.playerY += gameState.velocity;
    
    // Ground collision
    if (gameState.playerY > 400) {
        gameState.playerY = 400;
        gameState.velocity = 0;
        gameState.isJumping = false;
    }
    
    if (gameState.playerY < 0) {
        gameState.playerY = 0;
        gameState.velocity = 0;
    }
    
    // Update player position
    const player = document.getElementById('player');
    if (player) {
        player.style.top = gameState.playerY + 'px';
        player.className = gameState.isJumping ? 'jumping' : '';
    }
    
    // Spawn glimmers
    if (Math.random() < 0.025) {
        const word = gameState.words[Math.floor(Math.random() * gameState.words.length)];
        const gId = 'g-' + Date.now() + '-' + Math.random();
        const glimmer = document.createElement('div');
        glimmer.className = 'glimmer';
        glimmer.id = gId;
        glimmer.innerText = word;
        glimmer.style.left = '900px';
        const yPos = 100 + Math.random() * 280;
        glimmer.style.top = yPos + 'px';
        
        const gamePage = document.getElementById('game-page');
        if (gamePage) {
            gamePage.appendChild(glimmer);
            gameState.glimmers.push({ id: gId, x: 900, y: yPos });
        }
    }
    
    // Move glimmers
    for (let i = gameState.glimmers.length - 1; i >= 0; i--) {
        const g = gameState.glimmers[i];
        g.x -= 6;
        
        const el = document.getElementById(g.id);
        if (el) {
            el.style.left = g.x + 'px';
            
            // Collision detection
            const playerCenterY = gameState.playerY + 40;
            const glimmerCenterY = g.y + 20;
            
            if (g.x > 120 && g.x < 200 && Math.abs(playerCenterY - glimmerCenterY) < 60) {
                gameState.score++;
                const scoreEl = document.getElementById('score-val');
                if (scoreEl) {
                    scoreEl.innerText = '✨ Glimmers: ' + gameState.score;
                }
                
                // Collection effect
                el.style.transition = 'all 0.3s ease';
                el.style.transform = 'scale(1.5)';
                el.style.opacity = '0';
                
                setTimeout(() => {
                    if (el.parentNode) el.remove();
                }, 300);
                
                gameState.glimmers.splice(i, 1);
                
                if (gameState.score >= gameState.target) {
                    levelUp();
                    return;
                }
            } else if (g.x < -100) {
                el.remove();
                gameState.glimmers.splice(i, 1);
            }
        }
    }
    
    requestAnimationFrame(gameLoop);
}

// Backend API calls
async function saveProgress() {
    try {
        const response = await fetch('/api/save_progress', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                glimmers: gameState.score,
                target: gameState.target,
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

// Initialize when DOM is ready
function initializeGame() {
    console.log('Spark Runner Game Loaded! 🎮✨');
    
    // Make functions globally available
    window.initGame = initGame;
    window.returnToGame = returnToGame;
    window.jump = jump;
    
    // Event Listeners
    document.addEventListener('keydown', (e) => {
        if (e.code === 'Space' || e.key === ' ') {
            e.preventDefault();
            jump(e);
        }
    });

    // Add click listener to the entire game window
    const gameWindow = document.getElementById('game-window');
    if (gameWindow) {
        gameWindow.addEventListener('click', (e) => {
            // Don't trigger jump if clicking on buttons
            if (!e.target.classList.contains('btn')) {
                jump(e);
            }
        });
    }

    document.addEventListener('touchstart', (e) => {
        // Don't trigger jump if touching buttons
        if (!e.target.classList.contains('btn')) {
            jump(e);
        }
    });
    
    console.log('Event listeners initialized');
}

// Run initialization when DOM is fully loaded
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeGame);
} else {
    initializeGame();
}