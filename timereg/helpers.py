class Formatter():
    @staticmethod
    def duration_to_time_format(duration: float) -> str:
        hours = int(duration)
        rest = duration - int(duration)
        minutes = int(60 * rest)
        return '{0:02d}:{1:02d}'.format(hours, minutes)

    @staticmethod
    def format_time(tm):
        if tm:
            return tm.strftime("%Y-%m-%d %H:%M")
        else:
            return ''

    @staticmethod
    def format_date(dt):
        if dt:
            return dt.strftime("%Y-%m-%d")
        else:
            return ''