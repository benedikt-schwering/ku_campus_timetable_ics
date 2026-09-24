from dotenv import load_dotenv, find_dotenv
from fastapi import FastAPI, Response
from parser import parse_timetable
from crawler import get_timetable
from ics import Calendar, Event
import os


load_dotenv(find_dotenv())

auth_token = os.getenv("AUTH_TOKEN")

app = FastAPI(
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)

@app.get("/timetable.ics")
def get_timetable_ics(token: str):
    if token != auth_token:
        return Response(
            content="Unauthorized",
            status_code=401,
        )

    timetable_html = get_timetable(
        username=os.getenv("KU_USERNAME"),
        password=os.getenv("KU_PASSWORD")
    )

    events = parse_timetable(
        timetable_html=timetable_html,
    )

    calendar = Calendar()

    for event in events:
        ics_event = Event(
            name=event.name,
            begin=event.begin,
            end=event.end,
            description=event.description,
            location=event.location,
            url=event.url,
        )
        calendar.events.add(ics_event)

    return Response(
        content=calendar.serialize(),
        media_type="text/calendar",
    )
