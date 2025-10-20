import pyautogui
import time
import pyperclip
from PIL import ImageGrab
import cv2
import numpy as np
from utils.screen_souss import find_guge_sous_on_screen,find_noneprompt_on_screen,find_theme_on_screen


def choose_all_app(name:str):
    pyautogui.press('winleft')
    pyperclip.copy(name)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1)
    try:
        x, y = find_noneprompt_on_screen()
        print("未找到")
    except:
        print("找到了")
        pyautogui.click(966, 696)

def play_music(name,app="音乐"):
    choose_all_app(app)
    try:
        x,y = find_guge_sous_on_screen()
        print("找到")
    except:
        try:
            print("没找到")
            x_1,y_2 = find_theme_on_screen()
            pyautogui.click(x_1,y_2)
            time.sleep(1)
            location = pyautogui.locateOnScreen('../tutample/theme_use.png')  # 查找屏幕上按钮的位置
            if location:
                pyautogui.click(location)
            time.sleep(1)
            x, y = find_guge_sous_on_screen()
        except:
            return {"status":"error","content":"更换主题失败"}
    pyautogui.click(x,y)
    time.sleep(0.5)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('backspace')
    pyperclip.copy(name)
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press('enter')

if __name__ == '__main__':
    # choose_all_app("音乐")
    print(play_music("爱你没差", app="音乐"))