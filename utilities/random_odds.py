

import random

event_odds = [
    {
        "id": "0172277b76bd88e935ee706b37c0b85e",
        "sport_key": "soccer_england_league2",
        "sport_title": "League 2",
        "commence_time": "2025-05-10T19:00:00Z",
        "home_team": "Notts County",
        "away_team": "Wimbledon",
        "bookmakers": [
            {
                "key": "pinnacle",
                "title": "Pinnacle",
                "last_update": "2025-05-04T09:43:44Z",
                "markets": [
                    {
                        "key": "h2h",
                        "last_update": "2025-05-04T09:43:44Z",
                        "outcomes": [
                            {
                                "name": "Notts County",
                                "price": 2.13
                            },
                            {
                                "name": "Wimbledon",
                                "price": 3.49
                            },
                            {
                                "name": "Draw",
                                "price": 3.27
                            }
                        ]
                    }
                ]
            },
            {
                "key": "sport888",
                "title": "888sport",
                "last_update": "2025-05-04T09:43:44Z",
                "markets": [
                    {
                        "key": "h2h",
                        "last_update": "2025-05-04T09:43:44Z",
                        "outcomes": [
                            {
                                "name": "Notts County",
                                "price": 2.1
                            },
                            {
                                "name": "Wimbledon",
                                "price": 3.4
                            },
                            {
                                "name": "Draw",
                                "price": 3.2
                            }
                        ]
                    }
                ]
            }
        ]
    }
]



list = event_odds





print(list)



def random_odds_generator(event_odds):
    
    list = event_odds

    for event in list:

        for bookmaker in event['bookmakers']:

            for market in bookmaker["markets"]:

                for outcome in market['outcomes']:
                            
                            outcome["price"] = round((2 * random.random()) + 1, 2)

    return list


print(random_odds_generator(event_odds))