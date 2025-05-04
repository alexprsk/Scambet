
async function getEventOdds() {

    try {
        const response = await fetch('/sportsbook/odds', {method: 'GET'})

        if (!response.ok) {
            const errorData = await response.json();
            console.error('Error details:', errorData);
            throw new Error(errorData.detail);
        }

        const data = await response.json();
        console.log(data);

    }catch(error){
        console.error('Login error:', error);
    }
}

window.addEventListener('DOMContentLoaded', () => {
      getEventOdds(); // Use default or pass dynamic parameters
    });
