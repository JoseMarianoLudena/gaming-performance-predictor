// Aim Test con medición de tiempo hasta cada hit
let aimState = {
    hits: 0,
    misses: 0,
    timesToHit: [],  // NUEVO: Array de tiempos
    targetSpawnTime: null,  // NUEVO: Momento en que apareció el target
    active: false,
    duration: 30,
    timeLeft: 30,
    testStartTime: null
};

function startAimTest() {
    const container = document.getElementById('aim-container');
    const startBtn = document.getElementById('start-aim');
    
    startBtn.style.display = 'none';
    container.innerHTML = '';
    container.classList.add('active');
    
    aimState.active = true;
    aimState.hits = 0;
    aimState.misses = 0;
    aimState.timesToHit = [];
    aimState.timeLeft = aimState.duration;
    aimState.testStartTime = Date.now();
    
    // Timer
    const timerInterval = setInterval(() => {
        aimState.timeLeft--;
        document.getElementById('aim-timer').textContent = aimState.timeLeft;
        
        if (aimState.timeLeft <= 0) {
            clearInterval(timerInterval);
            endAimTest();
        }
    }, 1000);
    
    // Click en el container (miss)
    container.addEventListener('click', handleContainerClick);
    
    // Spawn first target
    spawnTarget();
}

function spawnTarget() {
    if (! aimState.active) return;
    
    const container = document.getElementById('aim-container');
    const target = document.createElement('div');
    target.className = 'aim-target';
    
    // Random position
    const containerRect = container.getBoundingClientRect();
    const targetSize = 50;
    const maxX = containerRect.width - targetSize;
    const maxY = containerRect.height - targetSize;
    
    const x = Math.random() * maxX;
    const y = Math.random() * maxY;
    
    target.style.left = x + 'px';
    target.style.top = y + 'px';
    
    // NUEVO: Guardar momento de spawn
    aimState. targetSpawnTime = Date.now();
    
    // Click handler
    target.addEventListener('click', (e) => {
        e.stopPropagation();
        handleTargetHit(target, e);
    });
    
    container.appendChild(target);
    
    // Auto-remove after 2 seconds if not clicked
    setTimeout(() => {
        if (target.parentNode) {
            target.remove();
            if (aimState.active) {
                spawnTarget();
            }
        }
    }, 2000);
}

function handleTargetHit(target, event) {
    // NUEVO: Calcular tiempo desde que apareció el target
    const timeToHit = Date.now() - aimState.targetSpawnTime;
    aimState.timesToHit.push(timeToHit);
    
    aimState.hits++;
    
    // Visual feedback
    target.classList.add('hit');
    setTimeout(() => target.remove(), 200);
    
    updateAimStats();
    
    if (aimState.active) {
        spawnTarget();
    }
}

function handleContainerClick(e) {
    if (e.target.classList.contains('aim-target')) return;
    
    aimState.misses++;
    updateAimStats();
    
    // Visual feedback
    const miss = document.createElement('div');
    miss.className = 'miss-indicator';
    miss.style.left = e.offsetX + 'px';
    miss.style.top = e. offsetY + 'px';
    miss.textContent = 'X';
    
    document.getElementById('aim-container').appendChild(miss);
    setTimeout(() => miss.remove(), 500);
}

function updateAimStats() {
    document.getElementById('aim-hits').textContent = aimState. hits;
    document.getElementById('aim-misses').textContent = aimState.misses;
}

function endAimTest() {
    aimState.active = false;
    
    const container = document.getElementById('aim-container');
    const testDuration = (Date.now() - aimState.testStartTime) / 1000;
    
    container. innerHTML = `<p class="completed-message">✓ Aim test completed! <br>Hits: ${aimState.hits} | Misses: ${aimState.misses}</p>`;
    container.classList.remove('active');
    
    // Save results con TODAS las métricas
    testResults.aim_results = {
        hits: aimState.hits,
        misses: aimState.misses,
        times_to_hit: aimState. timesToHit,  // NUEVO
        duration: aimState.duration
    };
    
    testResults.aim_test_duration = testDuration;
    
    document.getElementById('next-after-aim').classList.remove('hidden');
}