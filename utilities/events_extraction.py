response = [
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
            },
            {
                "key": "williamhill",
                "title": "William Hill",
                "last_update": "2025-05-04T09:43:03Z",
                "markets": [
                    {
                        "key": "h2h",
                        "last_update": "2025-05-04T09:43:03Z",
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
    },
    {
        "id": "1089796271b092b57e12f9a159e6856d",
        "sport_key": "soccer_england_league2",
        "sport_title": "League 2",
        "commence_time": "2025-05-11T14:30:00Z",
        "home_team": "Chesterfield FC",
        "away_team": "Walsall",
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
                                "name": "Chesterfield FC",
                                "price": 2.31
                            },
                            {
                                "name": "Walsall",
                                "price": 3.12
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
                "key": "onexbet",
                "title": "1xBet",
                "last_update": "2025-05-04T09:43:44Z",
                "markets": [
                    {
                        "key": "h2h",
                        "last_update": "2025-05-04T09:43:44Z",
                        "outcomes": [
                            {
                                "name": "Chesterfield FC",
                                "price": 2.27
                            },
                            {
                                "name": "Walsall",
                                "price": 3.2
                            },
                            {
                                "name": "Draw",
                                "price": 3.25
                            }
                        ]
                    }
                ]
            },
            {
                "key": "nordicbet",
                "title": "Nordic Bet",
                "last_update": "2025-05-04T09:43:47Z",
                "markets": [
                    {
                        "key": "h2h",
                        "last_update": "2025-05-04T09:43:47Z",
                        "outcomes": [
                            {
                                "name": "Chesterfield FC",
                                "price": 2.35
                            },
                            {
                                "name": "Walsall",
                                "price": 3.0
                            },
                            {
                                "name": "Draw",
                                "price": 3.3
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
                                "name": "Chesterfield FC",
                                "price": 2.25
                            },
                            {
                                "name": "Walsall",
                                "price": 3.0
                            },
                            {
                                "name": "Draw",
                                "price": 3.25
                            }
                        ]
                    }
                ]
            },
            {
                "key": "williamhill",
                "title": "William Hill",
                "last_update": "2025-05-04T09:43:03Z",
                "markets": [
                    {
                        "key": "h2h",
                        "last_update": "2025-05-04T09:43:03Z",
                        "outcomes": [
                            {
                                "name": "Chesterfield FC",
                                "price": 2.25
                            },
                            {
                                "name": "Walsall",
                                "price": 3.0
                            },
                            {
                                "name": "Draw",
                                "price": 3.25
                            }
                        ]
                    }
                ]
            }
        ]
    }
]

def get_bookmakers_info(response):
    for event in response:
        if 'bookmakers' not in event:
            return {"Message": "bookmakers key not found"}
        for bookmaker in event['bookmakers']:
            print(bookmaker['key'])
            print(bookmaker['title'])
            print(bookmaker['last_update'])



def get_bookmaker_markets(response):

    for event in response:

        if 'bookmakers' not in event:
            
            return {"Message": "bookmakers key not found"}
            
        
        for bookmaker in event['bookmakers']:
            if 'markets' not in bookmaker:
                print("Message:markets key not found for bookmaker: ")
            print(bookmaker['markets'])


get_bookmakers_info(response)
get_bookmaker_markets(response)











