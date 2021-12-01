import mouse
from pyjoycon import JoyCon, get_R_id
import asyncio
import pyautogui
import math

sen_mode = 0

async def mouse_event(button_info: dict):
    global sen_mode
    if button_info['zr'] == 1:
        mouse.click('left')
        print('left clicked!')
    elif button_info['r'] == 1:
        mouse.click('right')
        print('right clicked')

    elif button_info['x'] == 1:
        mouse.wheel(1)
        await asyncio.sleep(0.1)
    elif button_info['b'] == 1:
        mouse.wheel(-1)
        await asyncio.sleep(0.1)
    elif button_info['sr'] == 1:
        sen_mode += 1
        sen_mode = min(3,sen_mode)
        await asyncio.sleep(0.1)
    elif button_info['sl'] == 1:
        sen_mode -= 1
        sen_mode = max(0,sen_mode)
        await asyncio.sleep(0.1)

async def stick_event(stick_info: dict):
    StickOffset_X = 2070
    StickOffset_Y = 1750

    mouse_x = stick_info['horizontal'] - StickOffset_X
    mouse_y = -(stick_info['vertical'] - StickOffset_Y)
    global sen_mode

    if sen_mode == 0:
        sensitivity = 0.005
    elif sen_mode == 1:
        sensitivity = 0.01
    elif sen_mode == 2:
        sensitivity = 0.015
    elif sen_mode == 3:
        sensitivity = 0.02

    threthold = 150
    if abs(mouse_x) > threthold or abs(mouse_y) > threthold:
        mouse_x = int(mouse_x*sensitivity)
        mouse_y = int(mouse_y*sensitivity)
        print(mouse_x,mouse_y)
        mouse.move(mouse_x,mouse_y,absolute=False,duration=0)
    await asyncio.sleep(0.02)

async def led_event(joycon: JoyCon):
    sen_txt = ''
    if sen_mode == 0:
        joycon.set_player_lamp_on(1)
        sen_txt = 'low'
    elif sen_mode == 1:
        joycon.set_player_lamp_on(2)
        sen_txt = 'mid-low'
    elif sen_mode == 2:
        joycon.set_player_lamp_on(3)
        sen_txt = 'mid-high'
    elif sen_mode == 3:
        joycon.set_player_lamp_on(4)
        sen_txt = 'high'
    #print('stick sensitivity is {}'.format(sen_txt))

async def accel_event(accel_status:dict):
    accel_back = 4000
    accel_foward = -4000
    accel = accel_status['y']
    if accel >= accel_back:
        print('browserback')
        pyautogui.hotkey('browserback')
        await asyncio.sleep(0.1)
    elif accel <= accel_foward:
        print('browserfoward')
        pyautogui.hotkey('browserforward')
        await asyncio.sleep(0.1)

def main():
    joycon_id = get_R_id()
    joycon = JoyCon(*joycon_id)
    joycon.set_accel_calibration([360,-45,-4000])
    loop = asyncio.get_event_loop()

    while 1:
        joycon_status = joycon.get_status()
        button_status = joycon_status['buttons']['right']
        stick_status = joycon_status['analog-sticks']['right']
        accel_status = joycon_status['accel']

        gather = asyncio.gather(
            mouse_event(button_status),
            stick_event(stick_status),
            led_event(joycon),
            accel_event(accel_status)
        )
        loop.run_until_complete(gather)
        '''
        task1 = asyncio.create_task(mouse_event(button_status))
        task2 = asyncio.create_task(stick_event(stick_status))
        await task1
        await task2
        '''

if __name__ == '__main__':
    main()