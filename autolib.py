import pycurl
import json
from datetime import datetime, timedelta
from urllib.parse import urlencode

def get_bookings(account):
    bookings = []
    
    booking_date = (datetime.today() + timedelta(days=2)).strftime('%Y-%m-%d')

    for i in range(6):
        booking_time = datetime.strptime(account['booking_times'][i], '%H:%M')

        start_time = booking_time.strftime('%H:%M')
        end_time = (booking_time + timedelta(minutes=30)).strftime('%H:%M')

        booking = dict()
        booking['id'] = (i + 1)
        booking['eid'] = 10488
        booking['gid'] = 2753
        booking['lid'] = 1536
        booking['start'] = booking_date + '+' + start_time
        booking['end'] = booking_date + '+' + end_time

        bookings.append(booking)
    
    return bookings

c = pycurl.Curl()
c.setopt(pycurl.URL, 'https://cal.lib.uoguelph.ca/ajax/space/book')
c.setopt(pycurl.REFERER, 'https://cal.lib.uoguelph.ca/reserve/5-person-study-rooms')

with open('./accounts.json', 'r') as f:
    accounts = json.load(f)

    for account in accounts:
        post_data = {
            'fname': account['fname'],
            'lname': account['lname'],
            'email': account['email'],
            'bookings': get_bookings(account)
        }

        post_fields = urlencode(post_data)

        c.setopt(pycurl.POSTFIELDS, post_fields)
        c.perform()

c.close()