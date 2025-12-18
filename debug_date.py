import dateparser
from datetime import datetime

print("Now:", datetime.now())
text = "Schedule a meeting tomorrow at 5pm"
dt = dateparser.parse(text)
print("Parsed 1:", dt)

dt2 = dateparser.parse(text, settings={'PREFER_DATES_FROM': 'future'})
print("Parsed 2:", dt2)
