import pyautogui
import time
import pyperclip
from PIL import ImageGrab
import cv2
import numpy as np
from tools.utils.setting import s_h_r,s_w_r
from tools.utils.screen_souss import find_guge_sous_on_screen,find_noneprompt_on_screen,find_theme_on_screen,find_localtion_on_screen


def choose_all_app(name:str):
    pyautogui.press('winleft')
    pyperclip.copy(name)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(2)
    try:
        x, y = find_noneprompt_on_screen()
        return {"status":"OK","content":f"没有名字叫{name}的软件"}
    except:
        pyautogui.click(966*s_w_r, 696*s_h_r)
        return {"status": "OK", "content": f"已经成功打开{name}软件"}

def play_music(name,app="音乐"):

    choose_all_app(app)
    time.sleep(5)
    try:
        x, y = find_guge_sous_on_screen()
        print(x,y)
        pyautogui.moveTo(x,y)
    except:
        try:
            x_1,y_2 = find_theme_on_screen()
            pyautogui.click(x_1,y_2)
            time.sleep(2)
            location = pyautogui.locateOnScreen('../tutample/theme_use.png')  # 查找屏幕上按钮的位置
            if location:
                pyautogui.click(location)
            time.sleep(2)
            x, y = find_guge_sous_on_screen()
        except:
            return {"status":"error","content":"更换主题失败"}
    pyautogui.click(x,y)
    time.sleep(1)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('backspace')
    pyperclip.copy(name)
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press('enter')
    time.sleep(3)
    try:
        x, y = find_localtion_on_screen()
        pyautogui.click(x+42 * s_w_r, y+80 * s_h_r)
        return {"status": "OK", "content": f"已经成功播放{name}"}
    except:

        pass

if __name__ == '__main__':
    # choose_all_app("音乐")
    print(play_music("爱你没差", app="音乐"))