
from sportsbook.models_mongo import Event


from datetime import datetime

async def insert_events_from_api(api_response_data: list):
    events = []

    for raw_event in api_response_data:
            event = Event(
                event_id=raw_event["id"],
                sport_key=raw_event["sport_key"],
                sport_title=raw_event["sport_title"],
                commence_time=datetime.fromisoformat(raw_event["commence_time"].replace("Z", "+00:00")),
                home_team=raw_event["home_team"],
                away_team=raw_event["away_team"],
                bookmakers=raw_event.get("bookmakers", [])
            )
            events.append(event)

    await Event.insert_many(events)
    return f"{len(events)} events inserted."
