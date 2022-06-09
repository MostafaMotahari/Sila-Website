from curses import resetty
import datetime
from pytz import timezone

def iranDateTime(dateAndTime: datetime.datetime):
    return dateAndTime.astimezone(timezone('Asia/Tehran'))
