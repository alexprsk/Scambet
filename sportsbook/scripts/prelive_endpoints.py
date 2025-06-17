import os
from dotenv import load_dotenv
import httpx
import asyncio

load_dotenv("prod.env")

API_KEY = os.getenv('ODDS_API_KEY')

SPORT = [] 

REGIONS = 'us' 

MARKETS = 'h2h,spreads' 

ODDS_FORMAT = 'decimal' 

DATE_FORMAT = 'iso' 

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#
#   Get a list of in-season sports
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

async def get_all_events():

    async with httpx.AsyncClient() as client:

        sports_response = await client.get(
            'https://api.the-odds-api.com/v4/sports', 
            params={
                'api_key': API_KEY
            }
        )

        if sports_response.status_code != 200:
                raise RuntimeError(f'Failed to get sports: {sports_response.status_code}, {sports_response.text}')

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        #
        #   Append all sports in a list
        #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

        sports_json = sports_response.json()
        print(sports_json)

        list_of_sports = [sport.get("key") for sport in sports_json]
        print(list_of_sports)

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        #
        #   Get all events and all leagues based on sport e.g soccer, baseball etc
        #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

        american_football_events = []
        baseball_events = []
        basketball_events = []
        soccer_events = []
        tennis_events = []

        for sport in list_of_sports:

            events_response = await client.get(
                f'https://api.the-odds-api.com/v4/sports/{sport}/events', 
                params={
                    'api_key': API_KEY
                }
            )

            if events_response.status_code != 200:

                print(f'Failed to get sports: status_code {events_response.status_code}, response body {events_response.text}')

            if events_response.status_code  == 200:

                events_json = events_response.json()

                # Now that I can append to the list based on sport

                if not events_json:
                    continue
                sport_key = events_json[0].get("sport_key", "")

                if "baseball" in sport_key:
                    baseball_events.extend(events_json)
                elif "americanfootball" in sport_key:
                    american_football_events.extend(events_json)
                elif "basketball" in sport_key:
                    basketball_events.extend(events_json)
                elif "soccer" in sport_key:
                    soccer_events.extend(events_json)
                elif "tennis" in sport_key:
                    tennis_events.extend(events_json)

    return{
        "baseball" : baseball_events,
        "american_football": american_football_events,
        "basketball" : basketball_events,
        "soccer": soccer_events,
        "tennis": tennis_events
        }


if __name__ == "__main__":
    asyncio.run(get_all_events())

