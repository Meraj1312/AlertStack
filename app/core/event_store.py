from typing import List, Dict

EVENTS: List[Dict] = []
EVENT_IDS = set()


def add_event(event: Dict) -> bool:
    if event["event_id"] in EVENT_IDS:
        return False

    EVENTS.append(event)
    EVENT_IDS.add(event["event_id"])
    return True


def get_all_events() -> List[Dict]:
    return EVENTS  
