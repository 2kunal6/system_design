import time

print(str(time.time()).replace('.', ''))

from datetime import datetime

print(datetime.strptime('2025-02-01 21:30', '%Y-%m-%d %H:%M'))