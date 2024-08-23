import datetime


def time_checker(updated_at, hour=None, minute=None):
    current_time = datetime.datetime.now().time()
    updated_time = updated_at.time()

    current_timedelta = datetime.timedelta(hours=current_time.hour, minutes=current_time.minute,
                                           seconds=current_time.second)
    updated_timedelta = datetime.timedelta(hours=updated_time.hour, minutes=updated_time.minute,
                                           seconds=updated_time.second)
    time_difference = current_timedelta - updated_timedelta

    given_time = None
    if hour:
        given_time = datetime.timedelta(hours=hour)
    elif minute:
        given_time = datetime.timedelta(minutes=minute)

    return time_difference > given_time if given_time else False
