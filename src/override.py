from models import Event
import yaml, re

def apply_override_rules(events: list[Event]) -> list[Event]:
    with open("override_rules.yml", "r") as f:
        override_rules = yaml.safe_load(f)

    for event in events:
        for rule in override_rules["rules"]:
            if re.search(rule["event_regex"], event.name):
                if "override_url" in rule:
                    event.url = rule["override_url"]
                    event.description += "\n\n" + rule["override_url"]

                if "extend_description" in rule:
                    event.description += "\n\n" + rule["extend_description"]

                event.description = event.description.strip()

    return events
