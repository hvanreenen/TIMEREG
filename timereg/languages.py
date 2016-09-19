from timereg.config import config


def translate(msg):
    if config['lang'] == 'en':
        return msg
    elif msg in resources:
        return resources[msg][0]
    else:
        return msg

languages = ('en', 'nl')
resources = {
    'START time registry on {0:%Y-%m-%d} at {0:%H.%M}': ('START urenregistratie op {0:%Y-%m-%d} om {0:%H.%M}'),
    'Worked today: {}, this week: {}': ('Gewerkt vandaag: {}, deze week: {}'),
    'You forgot to registry the end time the other day.': ('Je bent een eerdere dag vergeten de eindtijd te registreren.'),
    'END time registry, started on {0:%Y-%m-%d} at {0:%H:%M}': ('EINDE urenregistratie, gestart op {0:%Y-%m-%d} om {0:%H:%M}'),
    'Registered time: {}': ('Aantal uren gewerkt: {}'),
    'Today: {}, this week: {}': ('Gewerkt vandaag: {}, deze week: {}'),
    'Start another time registry? [Y/N]': ('Nieuwe tijdmeting starten? [J/N]'),
    'Confirm/change start time {0:%H:%M} :': ('Bevestig/wijzig starttijd {0:%H:%M} :'),
    '': (''),
    '': (''),
    '': (''),


}

