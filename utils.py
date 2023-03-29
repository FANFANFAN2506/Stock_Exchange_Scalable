from datetime import datetime


def getCurrentTime():
    current_time = datetime.now()
    time_str = current_time.strftime('%Y-%m-%d %H:%M:%S')
    return time_str
