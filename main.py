import time


from color import Color

import functions as f
from functions import set_color, turn_off_all
from photos_maker import photo_maker
from servo import hand, camera
from servo.hand import put_down

if __name__ == "__main__":
    s = f.create_connect()

    #{0: 'ball', 1: 'basket', 2: 'blue_button', 3: 'cube', 4: 'green_button', 5: 'robot'}

