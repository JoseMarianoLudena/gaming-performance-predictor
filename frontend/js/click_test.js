// Click Speed Test (ya incluye error_rate correctamente)
let clickState = {
    clicks: 0,
    errors: 0,
    active: false,
    duration: 10,
    timeLeft: 10,
    lastClickTime: 0,
    testStartTime:  null
};

function startClickTest() {
    const box = document.getElementById('click-box');
    const startBtn = document.getElementById('start-click');
    
    startBtn.style.display = 'none';
    box.classList.add('active');
    box.innerHTML = '<p class="click-prompt">CLICK! </p>';
    
    clickState.active = true;
    clickState.clicks = 0;
    clickState.errors = 0;
    clickState.timeLeft = clickState.duration;
    clickState.lastClickTime = Date.now();
    clickState.testStartTime = Date.now();
    
    // Timer
    const timerInterval = setInterval(() => {
        clickState.timeLeft--;
        document.getElementById('click-timer').textContent = clickState.timeLeft;
        
        if (clickState.timeLeft <= 0) {
            clearInterval(timerInterval);
            endClickTest();
        }
    }, 1000);
    
    // Click handler
    box.addEventListener('click', handleClick);
}

function handleClick(e) {
    if (! clickState.active) return;
    
    const now = Date.now();
    const timeSinceLastClick = now - clickState.lastClickTime;
    
    clickState.clicks++;
    
    // Detectar error (doble clic demasiado rápido < 50ms)
    if (timeSinceLastClick < 50) {
        clickState.errors++;
    }
    
    clickState.lastClickTime = now;
    
    // Visual feedback
    const box = document.getElementById('click-box');
    box.classList.add('clicked');
    setTimeout(() => box.classList.remove('clicked'), 100);
    
    updateClickStats();
}

function updateClickStats() {
    const elapsed = clickState.duration - clickState.timeLeft;
    const cpm = elapsed > 0 ? Math.round((clickState.clicks / elapsed) * 60) : 0;
    
    document.getElementById('click-count').textContent = clickState.clicks;
    document.getElementById('click-cpm').textContent = cpm;
}

function endClickTest() {
    clickState.active = false;
    
    const box = document.getElementById('click-box');
    const totalDuration = (Date.now() - clickState.testStartTime) / 1000;
    
    box.classList.remove('active');
    box.classList.add('completed');
    box. innerHTML = `<p class="completed-message">✓ Test completed!<br>${clickState.clicks} clicks in ${clickState.duration} seconds</p>`;
    
    // Save results
    testResults.click_test = {
        clicks: clickState. clicks,
        duration: clickState.duration,
        errors: clickState.errors
    };
    
    testResults.click_test_duration = totalDuration;
    
    document.getElementById('submit-results').classList.remove('hidden');
}