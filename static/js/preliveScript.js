let odd_1 = document.getElementById("odd_1")
let odd_X = document.getElementById("odd_X")
let odd_2 = document.getElementById("odd_2")
let event_teams_home_1 = document.getElementById("event_teams_home_1")
let event_teams_away_2 = document.getElementById("event_teams_away_2")
let isLiveUpdatesEnabled = true

async function getEventOdds() {

    try {
        const response = await fetch('tests/test/latest_odds', {method: 'GET'})

        if (!response.ok) {
            const errorData = await response.json();
            console.error('Error details:', errorData);
            throw new Error(errorData.detail);
        }
        const data = await response.json();


        for (let e of response) {
            for (let bookmaker of e.bookmakers){
                for (let market of bookmaker.markets){
                    for (let outcome of market.outcomes){
                        for (let i = 0; i <= outcome.length; i++) {
                            odd_1.textContent = outcome.name

                        }
                        
                        let price = outcome.price
                    }

                }

            }
        }

        odd_1.textContent = data[0].bookmakers[0].markets[0].outcomes.find(outcome => outcome.name === "Notts County").price;
        odd_X.textContent = data[0].bookmakers[0].markets[0].outcomes.find(outcome => outcome.name === "Draw").price;
        odd_2.textContent = data[0].bookmakers[0].markets[0].outcomes.find(outcome => outcome.name === "Wimbledon").price;
                
                
    }catch(error){
        console.error('Login error:', error);
    }
}


async function fetchLiveUpdates() {
    if (!isLiveUpdatesEnabled) return;
    
    await getEventOdds();
    setTimeout(fetchLiveUpdates, 4000); // Poll every 1 second
}

window.addEventListener("DOMContentLoaded", fetchLiveUpdates);