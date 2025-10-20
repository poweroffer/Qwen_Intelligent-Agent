import pyautogui
import time
import pyperclip
from PIL import ImageGrab
import cv2
import numpy as np
time.sleep(2)  # 给你2秒时间切换到桌面
def find_guge_on_screen(threshold=0.8):
    """
    在屏幕上查找模板图片位置
    :param threshold: 匹配阈值（0~1）
    :return: 匹配中心坐标 (x, y)，找不到返回 None
    """
    # 1️⃣ 截屏
    screenshot = ImageGrab.grab()  # 全屏
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # 2️⃣ 读取模板
    template = cv2.imread('./tutample/img.png')
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    w, h = template_gray.shape[::-1]

    # 3️⃣ 截屏灰度化
    screen_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    # 4️⃣ 模板匹配
    res = cv2.matchTemplate(screen_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    # 5️⃣ 判断是否匹配成功
    if max_val >= threshold:
        top_left = max_loc
        center_x = top_left[0] + w // 2
        center_y = top_left[1] + h // 2
        return (center_x, center_y)
    else:
        return None

def find_guge_sous_on_screen(threshold=0.8):
    """
    在屏幕上查找模板图片位置
    :param threshold: 匹配阈值（0~1）
    :return: 匹配中心坐标 (x, y)，找不到返回 None
    """
    # 1️⃣ 截屏
    screenshot = ImageGrab.grab()  # 全屏
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # 2️⃣ 读取模板
    lis = ['../tutample/white_sous.png',"../tutample/blank_sous.png"]
    ans = ()
    for i in lis:

        template = cv2.imread(i)
        template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        w, h = template_gray.shape[::-1]

        # 3️⃣ 截屏灰度化
        screen_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

        # 4️⃣ 模板匹配
        res = cv2.matchTemplate(screen_gray, template_gray, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    # 5️⃣ 判断是否匹配成功
        if max_val >= threshold:
            top_left = max_loc
            center_x = top_left[0] + w // 2
            center_y = top_left[1] + h // 2
            ans = (center_x, center_y)
            break
    if ans:
        return ans
    return None
def find_noneprompt_on_screen(threshold=0.8):
    """
    在屏幕上查找模板图片位置
    :param threshold: 匹配阈值（0~1）
    :return: 匹配中心坐标 (x, y)，找不到返回 None
    """
    # 1️⃣ 截屏
    screenshot = ImageGrab.grab()  # 全屏
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # 2️⃣ 读取模板
    template = cv2.imread('../tutample/noneprompt.png')
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    w, h = template_gray.shape[::-1]

    # 3️⃣ 截屏灰度化
    screen_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    # 4️⃣ 模板匹配
    res = cv2.matchTemplate(screen_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    # 5️⃣ 判断是否匹配成功
    if max_val >= threshold:
        top_left = max_loc
        center_x = top_left[0] + w // 2
        center_y = top_left[1] + h // 2
        return (center_x, center_y)
    else:
        return None

def find_theme_on_screen(threshold=0.6):
    """
    在屏幕上查找模板图片位置
    :param threshold: 匹配阈值（0~1）
    :return: 匹配中心坐标 (x, y)，找不到返回 None
    """
    # 1️⃣ 截屏
    screenshot = ImageGrab.grab()  # 全屏
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # 2️⃣ 读取模板
    template = cv2.imread('../tutample/theme.png')
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    w, h = template_gray.shape[::-1]

    # 3️⃣ 截屏灰度化
    screen_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    # 4️⃣ 模板匹配
    res = cv2.matchTemplate(screen_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    # 5️⃣ 判断是否匹配成功
    if max_val >= threshold:
        top_left = max_loc
        center_x = top_left[0] + w // 2
        center_y = top_left[1] + h // 2
        return (center_x, center_y)
    else:
        return None