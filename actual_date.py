from datetime import datetime
import pytz

def get_date():
    moscow_tz = pytz.timezone("Europe/Moscow")
    moscow_now = datetime.now(moscow_tz)
    date_str = moscow_now.strftime("%d.%m.%Y")
    time_str = moscow_now.strftime("%H:%M")
    return date_str, time_str 
