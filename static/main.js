document.getElementById("gambleForm").addEventListener("submit", function(e) {
    e.preventDefault();
    const formData = new FormData(this);

    fetch("/submit", { method: "POST", body: formData })
        .then(res => res.json())
        .then(data => {
            if (data.status === "exists") {
                window.location.href = data.redirect; 
            } else if (data.status === "ok") {
                spinWheel(formData);
            } else if (data.status === "error") {
                alert(data.message);
            }
        });
});

function spinWheel(formData) {
    const reels = document.querySelectorAll('.reel');
    const button = document.querySelector('button');

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
            if (random <= 0) return icon.symbol;
        }
        return icons[0].symbol;
    }

    function checkWin(results) {
        return results[0] === results[1] && results[1] === results[2] ? "success" : "fail";
    }

    button.disabled = true;
    reels.forEach(r => r.classList.add('spinning'));

    setTimeout(() => {
        const results = [];
        reels.forEach(reel => {
            const icon = getRandomIcon();
            reel.textContent = icon;
            results.push(icon);
            reel.classList.remove('spinning');
        });

        const resultType = checkWin(results);

        formData.append("result", resultType);
        fetch("/record_result", { method: "POST", body: formData })
            .then(res => res.json())
            .then(data => {
                if (data.status === "ok") {
                    window.location.href = data.redirect; 
                } else {
                    alert(data.message);
                }
            });

    }, 2000);
}
