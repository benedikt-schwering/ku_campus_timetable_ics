from datetime import datetime
from bs4 import BeautifulSoup
from models import Event
import pytz

timezone = pytz.timezone("Europe/Berlin")

def parse_timetable(timetable_html: str) -> list[Event]:
    soup = BeautifulSoup(timetable_html, 'html.parser')

    table = soup.find('div', id='ctl00_WebPartManager1_ResultatAnzeigenWP1')

    events = []

    for row in table.find_all('tr', class_='result-row'):
        time, description, notice, resources = row.find_all('td')

        time_date, time_time = time.text.strip().split(' ', maxsplit=1)
        time_start, time_end = time_time.split(' - ')

        begin = datetime.strptime(f"{time_date} {time_start}", "%d.%m.%Y %H:%M").replace(tzinfo=timezone)
        end = datetime.strptime(f"{time_date} {time_end}", "%d.%m.%Y %H:%M").replace(tzinfo=timezone)

        name = description.text.strip()
        url = description.find('a')['href'].replace('..', 'https://campus.ku.de')

        lecturers = []
        locations = []

        for type, resource in zip(
            resources.find_all('span'),
            resources.find_all('a'),
        ):
            type = type.text.strip()

            if 'Lehrkraft' in type:
                lecturers.append(resource.text.strip())
            elif 'Raum' in type:
                locations.append(resource.text.strip())

        events.append(
            Event(
                name=name,
                begin=begin,
                end=end,
                description='\n'.join(lecturers),
                location=', '.join(locations),
                url=url,
            )
        )

    return events
