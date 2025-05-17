let odd_1 = document.getElementById("odd_1")
let odd_X = document.getElementById("odd_X")
let odd_2 = document.getElementById("odd_2")
let event_teams_home_1 = document.getElementById("event_teams_home_1")
let event_teams_away_2 = document.getElementById("event_teams_away_2")
let isLiveUpdatesEnabled = true

async function getEventOdds() {
    try {
        const response = await fetch('/tests/test/latest_odds', {method: 'GET'});
        
        if (!response.ok) {
            const errorData = await response.json();
            console.error('Error details:', errorData);
            throw new Error(errorData.detail);
        }
        
        const data = await response.json();
        if (!data || !data.length) {
            throw new Error('No event data received');
        }

        // Get all event rows
        const eventRows = document.querySelectorAll('.event_row');
        
        // Update each event row with corresponding data
        eventRows.forEach((row, index) => {
            // Use the first event for all rows (or data[index] if you have multiple events)
            const event = data[0]; 
            const pinnacle = event.bookmakers?.find(b => b.key === "pinnacle");
            
            // Find elements within this specific row
            const homeTeamEl = row.querySelector('.event_teams_home_1');
            const awayTeamEl = row.querySelector('.event_teams_away_2');
            const oddsButtons = row.querySelectorAll('[id="odds_sock"]');
            
            // Update team names
            if (homeTeamEl) homeTeamEl.textContent = event.home_team || 'N/A';
            if (awayTeamEl) awayTeamEl.textContent = event.away_team || 'N/A';
            
            // Update odds if pinnacle data exists
            if (pinnacle) {
                const market = pinnacle.markets?.find(m => m.key === "h2h");
                if (market) {
                    const homeOdd = market.outcomes?.find(o => o.name === event.home_team)?.price;
                    const drawOdd = market.outcomes?.find(o => o.name === "Draw")?.price;
                    const awayOdd = market.outcomes?.find(o => o.name === event.away_team)?.price;
                    
                    // Update odds buttons (1, X, 2 order)
                    if (oddsButtons.length >= 3) {
                        oddsButtons[0].textContent = homeOdd || 'N/A';
                        oddsButtons[1].textContent = drawOdd || 'N/A';
                        oddsButtons[2].textContent = awayOdd || 'N/A';
                    }
                }
            }
        });
                    
    } catch(error) {
        console.error('Error fetching odds:', error.message);
    }
}

async function fetchLiveUpdates() {
    if (!isLiveUpdatesEnabled) return;
    
    await getEventOdds();
    setTimeout(fetchLiveUpdates, 4000); // Poll every 4 seconds
}

window.addEventListener("DOMContentLoaded", fetchLiveUpdates);