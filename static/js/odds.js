const obj = [
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
            }
        ]
    }
]


"sport_title": "League 2",
"commence_time": "2025-05-10T19:00:00Z",
"home_team": "Notts County",
"away_team": "Wimbledon",

const id = obj[0].id;
const sportKey = obj[0].sport_key;
const sportTitle = obj[0].sport_title;
const commenceTime = obj[0].commence_time;
const homeTeam = obj[0].home_team;
const awayTeam = obj[0].away_team;

const bookmakerKey = obj[0].bookmakers[0].key
const bookmakerTitle = obj[0].bookmakers[0].title
const bookmakerLastUpdate = obj[0].bookmakers[0].last_update
const bookmakerMarkets = obj[0].bookmakers[0].markets

const h2hMarket = obj[0].bookmakers[0].markets[0].key
const lastUpdate = obj[0].bookmakers[0].markets[0].last_update
const TeamOne = obj[0].bookmakers[0].markets[0].outcomes[0].name
const TeamTwo = obj[0].bookmakers[0].markets[0].outcomes[1].name
const Draw = obj[0].bookmakers[0].markets[0].outcomes[2].name


const {
    id,
    sport_key: sportKey,
    sport_title: sportTitle,
    commence_time: commenceTime,
    home_team: homeTeam,
    away_team: awayTeam
  } = obj[0];

console.log[0][id]