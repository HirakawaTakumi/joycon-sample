from pyjoycon import JoyCon, get_R_id
import time
import math

joycon_id = get_R_id()
joycon = JoyCon(*joycon_id)
joycon.set_accel_calibration([360,-45,-4000])

while 1:
    status = joycon.get_status()['accel']
    print(status['y'])
    accel = math.sqrt(status['x']**2 + status['y']**2 + status['z']**2)
    #print(accel)
    time.sleep(0.1)
