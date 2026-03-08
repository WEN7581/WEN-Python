import time
from datetime import datetime
for __count in range(100000):
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    print(current_time)
    time.sleep(0.01)