// Reaction Time Test con detección de false starts
let reactionState = {
    attempts: 0,
    maxAttempts: 10,
    times: [],
    falseStarts: 0,
    startTime: null,
    waiting: false,
    testStartTime: null
};

function initReactionTest() {
    const box = document.getElementById('reaction-box');
    const text = document.getElementById('reaction-text');
    
    box.addEventListener('click', handleReactionClick);
}

function handleReactionClick() {
    const box = document.getElementById('reaction-box');
    const text = document. getElementById('reaction-text');
    
    if (reactionState.attempts >= reactionState.maxAttempts) {
        return;
    }
    
    // Si está esperando (rojo), FALSE START detectado
    if (reactionState.waiting) {
        reactionState.falseStarts++;
        
        text.textContent = `❌ False Start!  (${reactionState.falseStarts} total)`;
        box.classList.remove('waiting', 'ready');
        box.classList.add('early');
        
        setTimeout(() => {
            box.classList.remove('early');
            box.classList.add('waiting');
            text.textContent = 'Espera el verde... ';
            startReactionRound();
        }, 1500);
        return;
    }
    
    // Si está en verde, medir tiempo
    if (box.classList.contains('ready')) {
        const reactionTime = Date.now() - reactionState.startTime;
        reactionState.times.push(reactionTime);
        reactionState.attempts++;
        
        updateReactionStats(reactionTime);
        
        if (reactionState.attempts < reactionState.maxAttempts) {
            box.classList.remove('ready');
            box.classList.add('waiting');
            text.textContent = 'Espera... ';
            setTimeout(startReactionRound, 1000);
        } else {
            // Test completado
            const testDuration = (Date.now() - reactionState.testStartTime) / 1000;
            
            testResults. reaction_times = reactionState.times;
            testResults.false_starts = reactionState.falseStarts;
            testResults.reaction_test_duration = testDuration;
            
            box.classList.remove('ready');
            box.classList.add('completed');
            text.textContent = `✓ Test completado!\nPromedio: ${getAverage(reactionState.times).toFixed(0)} ms\nFalse Starts: ${reactionState.falseStarts}`;
            document.getElementById('next-after-reaction').classList.remove('hidden');
        }
        return;
    }
    
    // Si está en espera inicial, comenzar
    if (box.classList.contains('waiting')) {
        text.textContent = 'Espera... ';
        document.getElementById('reaction-stats').classList.remove('hidden');
        reactionState.testStartTime = Date.now();
        startReactionRound();
    }
}

function startReactionRound() {
    const box = document.getElementById('reaction-box');
    const text = document.getElementById('reaction-text');
    
    reactionState.waiting = true;
    
    // Random delay entre 1-4 segundos
    const delay = Math.random() * 3000 + 1000;
    
    setTimeout(() => {
        box.classList.remove('waiting');
        box.classList.add('ready');
        text.textContent = '¡CLIC AHORA!';
        reactionState.startTime = Date. now();
        reactionState.waiting = false;
    }, delay);
}

function updateReactionStats(lastTime) {
    document.getElementById('reaction-attempts').textContent = reactionState.attempts;
    document.getElementById('reaction-last').textContent = lastTime;
    document.getElementById('reaction-avg').textContent = getAverage(reactionState.times).toFixed(0);
}

function getAverage(arr) {
    return arr.reduce((a, b) => a + b, 0) / arr.length;
}

// Initialize when page loads
if (document.getElementById('reaction-box')) {
    initReactionTest();
}