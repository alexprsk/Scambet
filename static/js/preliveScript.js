let odd_1 = document.getElementById("odd_1")


async function getEventOdds() {

    try {
        const response = await fetch('tests/test/latest_odds', {method: 'GET'})

        if (!response.ok) {
            const errorData = await response.json();
            console.error('Error details:', errorData);
            throw new Error(errorData.detail);
        }

        const data = await response.json();
        odd_1.textContent = data[0].bookmakers[0].markets[0].outcomes.find(outcome => outcome.name === "Notts County").price;
        
    }catch(error){
        console.error('Login error:', error);
    }
}

window.addEventListener('DOMContentLoaded', () => {
      getEventOdds(); // Use default or pass dynamic parameters
    });
