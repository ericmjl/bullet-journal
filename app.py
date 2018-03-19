from datetime import date, datetime

from dateutil.parser import parse

from flask import Flask, render_template, redirect

import humanize

from utils import get_next_events

import yaml

import os

app = Flask(__name__)

home_dir = os.path.expanduser('~')
gdrive_folder = os.path.join(home_dir, 'Google Drive', 'personal-dashboard')
log_path = os.path.join(gdrive_folder, 'daily_log.yaml')


@app.route('/')
def daily_log():
    with open(log_path, 'r+') as f:
        entries = yaml.load(f)

    for entry in entries['daily_log']:
        d = parse(entry['date'])
        entry['humanized_date'] = humanize.naturaldate(d)

    events = get_next_events(n=10)
    todays_events = []
    for event in events:
        d = parse(event['start']['dateTime'], ignoretz=True)
        delta = humanize.naturaldelta(d - datetime.now())
        d_human = humanize.naturaldate(d.date())
        today = humanize.naturaldate(date.today())
        if d_human == today and d > datetime.now():
            event['start']['humanized_date'] = d_human
            event['start']['humanized_delta'] = delta
            todays_events.append(event)

    return render_template('dashboard.html.j2',
                           entries=entries['daily_log'],
                           events=todays_events)


@app.route('/dinner')
def dinners():
    """
    Answers the question, will I be home for dinner?
    """
    events = get_next_events(n=10)
    dinner_events = []
    for event in events:
        if 'dateTime' in event['start'].keys():
            event_startdate = parse(event['start']['dateTime'], ignoretz=True)
            event_starttime = event_startdate.time()

            event_enddate = parse(event['end']['dateTime'], ignoretz=True)
            event_endtime = event_enddate.time()

            if event_endtime.hour >= 18 and event_endtime.hour <= 21:
                dinner_events.append(event)

    print(dinner_events)
    return redirect('/')



if __name__ == '__main__':
    app.run(debug=True)
