/* ==========================================
   CYBERSAFE QR - PERSISTENT MULTI-PAGE LOGIC
   ========================================== */

document.addEventListener('DOMContentLoaded', () => {
    const totalScenarios = 8;

    // 1. Load Solved Scenarios from LocalStorage
    let solvedScenarios = new Set();
    const storedSolved = localStorage.getItem('cybersafe_solved_scenarios');
    if (storedSolved) {
        try {
            const parsed = JSON.parse(storedSolved);
            if (Array.isArray(parsed)) {
                parsed.forEach(id => solvedScenarios.add(id));
            }
        } catch (e) {
            console.error("Error parsing solved scenarios from localStorage", e);
        }
    }

    // Initialize Score Tracker
    updateTracker(solvedScenarios.size);

    // 2. Scroll Progress Bar Tracker
    const progressBar = document.getElementById('progressBar');
    if (progressBar) {
        window.addEventListener('scroll', () => {
            const winScroll = document.documentElement.scrollTop || document.body.scrollTop;
            const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
            const scrolled = height > 0 ? (winScroll / height) * 100 : 0;
            progressBar.style.width = scrolled + '%';
        });
    }

    // 3. Update Category Page Subtopic Cards on Load
    solvedScenarios.forEach(id => {
        const card = document.getElementById(`card-${id}`);
        const badge = document.getElementById(`badge-${id}`);
        
        if (card) {
            card.classList.add('card-solved');
        }
        if (badge) {
            badge.className = 'solve-status-badge status-solved';
            badge.innerHTML = '<i class="fa-solid fa-circle-check"></i> Solved 🛡️';
        }
    });

    // 4. Update Scenario Page on Load if Already Solved
    const activeScenarioCard = document.querySelector('.scenario-card');
    if (activeScenarioCard) {
        const scenarioId = activeScenarioCard.id.replace('scen-', '');
        
        if (solvedScenarios.has(scenarioId)) {
            // Already solved: Apply correct choice highlights and explanation immediately
            activeScenarioCard.setAttribute('data-solved', 'true');
            activeScenarioCard.classList.add('correct-solved');
            
            const optionBtns = activeScenarioCard.querySelectorAll('.option-btn');
            optionBtns.forEach(btn => {
                btn.classList.add('disabled-btn');
                if (btn.getAttribute('data-correct') === 'true') {
                    btn.classList.add('correct-choice', 'selected');
                    
                    // Show explanation panel matching the correct button
                    const explanationId = btn.getAttribute('data-explanation');
                    const feedbackPanel = document.getElementById(`explain-${explanationId}`);
                    if (feedbackPanel) {
                        setupFeedbackPanel(feedbackPanel, true);
                    }
                }
            });

            // Reveal Red Flags and highlight rings
            const flagMarkers = activeScenarioCard.querySelectorAll('.flag-marker');
            flagMarkers.forEach(flag => flag.classList.add('reveal-flag'));

            const mockupTargets = activeScenarioCard.querySelectorAll('.red-flag-target');
            mockupTargets.forEach(target => target.classList.add('highlight-rings'));
        }
    }

    // 5. Quiz Game Button Click Event Listeners
    const optionButtons = document.querySelectorAll('.option-btn');
    optionButtons.forEach(button => {
        button.addEventListener('click', () => {
            const parentCard = button.closest('.scenario-card');
            if (!parentCard) return;

            const scenarioId = parentCard.id.replace('scen-', '');
            const explanationId = button.getAttribute('data-explanation');
            const feedbackPanel = document.getElementById(`explain-${explanationId}`);
            
            const isCorrect = button.getAttribute('data-correct') === 'true';
            
            // Highlight choices and disable further interactions
            const allOptionsInBlock = parentCard.querySelectorAll('.option-btn');
            allOptionsInBlock.forEach(opt => {
                opt.classList.add('disabled-btn');
                if (opt.getAttribute('data-correct') === 'true') {
                    opt.classList.add('correct-choice');
                }
            });

            if (isCorrect) {
                button.classList.add('selected');
                setupFeedbackPanel(feedbackPanel, true);
            } else {
                button.classList.add('wrong-choice');
                setupFeedbackPanel(feedbackPanel, false);
            }

            // Reveal Red Flags 🚩 inside mockup visuals
            const flagMarkers = parentCard.querySelectorAll('.flag-marker');
            flagMarkers.forEach(flag => flag.classList.add('reveal-flag'));

            const mockupTargets = parentCard.querySelectorAll('.red-flag-target');
            mockupTargets.forEach(target => target.classList.add('highlight-rings'));

            // Record solved progress
            if (!solvedScenarios.has(scenarioId)) {
                solvedScenarios.add(scenarioId);
                parentCard.setAttribute('data-solved', 'true');
                parentCard.classList.add('correct-solved');
                
                // Write progress to localStorage
                localStorage.setItem('cybersafe_solved_scenarios', JSON.stringify(Array.from(solvedScenarios)));
                updateTracker(solvedScenarios.size);
            }
        });
    });

    // 6. Setup Explanation Panel Header and Info
    function setupFeedbackPanel(panel, isCorrect) {
        if (!panel) return;

        const iconBadge = panel.querySelector('.feedback-icon-badge');
        const titleText = panel.querySelector('.feedback-title-text');
        const introText = panel.querySelector('.feedback-intro');

        if (isCorrect) {
            panel.classList.remove('fail-style');
            panel.classList.add('success-style');
            if (iconBadge) iconBadge.innerHTML = '<i class="fa-solid fa-circle-check"></i>';
            if (titleText) titleText.textContent = 'CORRECT! 🛡️';
            if (introText) introText.textContent = "Fantastic job! You spotted the trap immediately. You've earned a shield of protection!";
        } else {
            panel.classList.remove('success-style');
            panel.classList.add('fail-style');
            if (iconBadge) iconBadge.innerHTML = '<i class="fa-solid fa-triangle-exclamation"></i>';
            if (titleText) titleText.textContent = 'INCORRECT! ⚠️';
            if (introText) introText.textContent = "Oh no, you fell for it! Don't worry, scams are built to be very tricky. Let's see how we can spot this next time!";
        }

        // Slide in panel
        panel.style.display = 'block';
    }

    // 7. Update Scoring Tracker
    function updateTracker(count) {
        const trackerText = document.getElementById('tracker-text');
        if (trackerText) {
            trackerText.textContent = `Scenarios Solved: ${count} / ${totalScenarios}`;
        }

        // Trigger Graduation Modal
        if (count === totalScenarios) {
            setTimeout(() => {
                const modal = document.getElementById('completionModal');
                if (modal) {
                    modal.classList.add('show');
                }
            }, 1000);
        }
    }

    // 8. Handle Restart Button click on Modal
    const restartBtn = document.getElementById('restart-progress-btn');
    if (restartBtn) {
        restartBtn.addEventListener('click', () => {
            localStorage.removeItem('cybersafe_solved_scenarios');
            window.location.href = '/';
        });
    }
});
