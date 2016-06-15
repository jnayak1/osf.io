from dateutil.tz import tzutc
from dateutil.parser import parse
from datetime import datetime, timedelta

from framework.mongo import database


def set_maintenance(start=None, end=None):
    """Set the time period for the maintenance notice to be displayed.
    If no start or end values are given, default to starting now in UTC
    and ending 24 hours from now.
    All given times will be converted to UTC automatically.
    """
    start = parse(start).replace(tzinfo=tzutc()) if start else datetime.utcnow()
    end = parse(end).replace(tzinfo=tzutc()) if end else start + timedelta(1)

    database.drop_collection('maintenance')
    database.maintenance.insert({'maintenance': True, 'start': start.isoformat(), 'end': end.isoformat()})


def get_maintenance():
    """Get the current start and end times for the maintenance state.
    Return None for start and end if there is no maintenance state
    """
    maintenance_state = database.maintenance.find_one({'maintenance': True})
    state = {}
    if maintenance_state:
        state['start'] = maintenance_state.get('start')
        state['end'] = maintenance_state.get('end')

    return state if state else None


def unset_maintenance():
    database.drop_collection('maintenance')
