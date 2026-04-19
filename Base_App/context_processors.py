from datetime import datetime
import pytz

def restaurant_status(request):
    # Set timezone to IST (India Standard Time)
    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.now(ist)
    day = now.strftime('%A')
    hour = now.hour
    minute = now.minute
    current_time_float = hour + minute / 60.0

    is_open = False
    
    if day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
        # 9 AM to 11 PM
        if 9.0 <= current_time_float < 23.0:
            is_open = True
    elif day == 'Saturday':
        # 10 AM to 12 AM (Midnight)
        if 10.0 <= current_time_float < 24.0:
            is_open = True
    elif day == 'Sunday':
        # 10 AM to 11 PM
        if 10.0 <= current_time_float < 23.0:
            is_open = True

    return {
        'is_restaurant_open': is_open,
        'current_day': day,
        'current_ist_time': now.strftime('%I:%M %p')
    }
