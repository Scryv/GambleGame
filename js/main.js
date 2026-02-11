document.querySelector('.spin-button').addEventListener('click', function() {
    const reels = document.querySelectorAll('.reel');
    const button = this;
    const icons = [
        { symbol: '🍒', weight: 30 },
        { symbol: '🍋', weight: 25 },
        { symbol: '🍊', weight: 20 },
        { symbol: '🍇', weight: 15 },
        { symbol: '💎', weight: 5 }
    ];
    function getRandomIcon() {
        const totalWeight = icons.reduce((sum, icon) => sum + icon.weight, 0);
        let random = Math.random() * totalWeight;
        
        for (let icon of icons) {
            random -= icon.weight;
            if (random <= 0) {
                return icon.symbol;
            }
        }
        return icons[0].symbol; // fallback
    }
    function checkWin(results) {
        if (results[0] === results[1] && results[1] === results[2]) {
            return 'jackpot';
        }
        if (results[0] === results[1] || results[1] === results[2] || results[0] === results[2]) {
            return 'small win';
        }
        return 'lose';
    }
    // Disable button during spin
    button.disabled = true;
    
    // Add spinning class to all reels
    reels.forEach(reel => {
        reel.classList.add('spinning');
    });
    
    // Stop spinning after 2 seconds
    setTimeout(() => {
        const results = [];
        
        reels.forEach(reel => {
            // Pick a weighted random icon
            const randomIcon = getRandomIcon();
            reel.textContent = randomIcon;
            results.push(randomIcon);
            
            // Remove spinning class
            reel.classList.remove('spinning');
        });
        console.log(checkWin(results));
        button.disabled = false;
    }, 2000);
});
