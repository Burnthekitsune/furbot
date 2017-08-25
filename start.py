import time

import furbot_v2

while True:
    # noinspection PyBroadException
    try:
        furbot_v2
    except Exception as e:
        print('Furbot Crashed! Restarting...')
        pass
    time.sleep(10)
