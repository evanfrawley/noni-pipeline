import pyautogui
import time
import cv2
import numpy as np
import sys

POLYGON_COUNT = "150000"
RC_IMG_PATH = "img/rc/"

IMG_FILE_NAMES = {
    "folder_icon": "select_folder.png",
    "rc_taskbar": "rc_taskbar.png",
    "folder_path": "folder_select.png",
    "simplify_mesh":"",
}

POINTS = {
    "reality_capture_taskbar": {
        "x": 54,
        "y": 1060,
    },
    "photos_buttons": {
        "x": 68,
        "y": 68,
    },
    "align_images": {
        "x": 385,
        "y": 60,
    },
    "calculate_model": {
        "x": 385,
        "y": 80,
    },
    "simplify": {
        "x": 385,
        "y": 100,
    },
    "mesh": {
        "x": 590,
        "y": 104,
    },
    "photos_file_picker": {
        "x": 1080,
        "y": 653,
    },
    "photos_file_picker_ok": {
        "x": 980,
        "y": 688,
    },
}


def move(to_x, to_y, duration):
    pyautogui.moveTo(to_x, to_y, duration, pyautogui.easeOutQuad)
    time.sleep(0.5)


def write(word):
    pyautogui.typewrite(message, interval=0.25)


def reset():
    screenWidth, screenHeight = pyautogui.size()
    pyautogui.moveTo(screenWidth / 2, screenHeight / 2)


def open_reality_capture():
    reset()
    path = "" + RC_IMG_PATH + IMG_FILE_NAMES['rc_taskbar']
    print(IMG_FILE_NAMES['rc_taskbar'])
    print(path)
    rc_x, rc_y = pyautogui.locateCenterOnScreen(path)
    pyautogui.click(rc_x, rc_y)


def select_img_folder():
    reset()
    path = "" + RC_IMG_PATH + IMG_FILE_NAMES['folder_icon']
    print(IMG_FILE_NAMES['folder_icon'])
    print(path)
    x, y = pyautogui.locateCenterOnScreen(path)
    move(x, y)
    pyautogui.click()
    path = "" + RC_IMG_PATH + IMG_FILE_NAMES['folder_path']
    print(IMG_FILE_NAMES['folder_path'])
    print(path)
    x, y = pyautogui.locateCenterOnScreen(path)
    move(x, y)
    pyautogui.click(clicks=2)
    write("this is a test123")
    pyautogui.enter()


def simplify_mesh():
    reset()
    rc_x, rc_y = pyautogui.locateCenterOnScreen(RC_IMG_PATH + IMG_FILE_NAMES['folder_path'])
    pyautogui.click(rc_x, rc_y)


def change_rc_polygons():
    reset()
    p_x, p_x = pyautogui.locateCenterOnScreen('rc_polygon_box.png')
    pyautogui.typewrite(POLYGON_COUNT, interval=0.21)
    pyautogui.press('enter')


def click():
    pyautogui.click()


def double_click():
    pyautogui.click(clicks=2)


def get_x_y(key):
    return (POINTS[key]["x"], POINTS[key]["y"])


def move_and_click(key):
    x, y = get_x_y(key)
    move(x, y, 1)
    click()


def move_and_double_click(key):
    x, y = get_x_y(key)
    move(x, y, 1)
    double_click()


def check_working():
    is_working = True
    template = cv2.imread('img/rc/controls.png',0)
    w, h = template.shape[::-1]
    while is_working:
        time.sleep(10)
        img = cv2.cvtColor(np.array(pyautogui.screenshot()), cv2.COLOR_BGR2GRAY)
        method = eval('cv2.TM_CCORR_NORMED')
        res = cv2.matchTemplate(img,template,method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        is_working = max_val > 0.95
        print("percent match:", max_val, flush=True)


def paste_text(text):
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.typewrite(text, interval=0.21)


def get_user_confirmation():
    name = input("Ready to continue? [y/N]: ")
    if name.lower() == 'y':
        return
    elif name.lower() == 'n':
        print("OK. Waiting for another 30s")
        time.sleep(30)
        get_user_confirmation()
    else:
        print("Not sure what you inputted, exiting program.")
        exit()


def get_starting_step():
    print("*****************************")
    print("Welcome to the ModelScriptHelper!")
    resume = input("Are you resuming from the middle of a previous session? [y/N]?")
    if name.lower() == 'y':
        step = input("What was the last FULL COMPLETED step?")
        return step
    elif name.lower() == 'n':
        print("OK. Waiting for another 30s")
        time.sleep(30)
        get_user_confirmation()
    else:
        print("Not sure what you inputted, exiting program.")
        exit()


steps = [
    {
        "name": "move_and_click",
        "step_args": ["reality_capture_taskbar"]
    },
    {
        "name": "move_and_click",
        "step_args": ["photos_buttons"]
    },
    {
        "name": "move_and_click",
        "step_args": ["photos_file_picker"]
    },
    {
        "name": "paste_text",
        "step_args": ["AlfredoPasta"]
    },
    {
        "name": "move_and_click",
        "step_args": ["photos_file_picker_ok"]
    },
    {
        "name": "move_and_click",
        "step_args": ["align_images"]
    },
    {
        "name": "check_working",
        "step_args": []
    },
    {
        "name": "move_and_click",
        "step_args": ["calculate_model"]
    },
    {
        "name": "check_working",
        "step_args": []
    },
    {
        "name": "move_and_click",
        "step_args": ["simplify"]
    },
    {
        "name": "check_working",
        "step_args": []
    },
    {
        "name": "move_and_click",
        "step_args": ["mesh"]
    },
    {
        "name": "check_working",
        "step_args": []
    },
]


def run():
    print("**************************")
    for idx, step in enumerate(steps):
        print("Step", idx+1, "started")
        globals()[step["name"]](*step["step_args"])
        print("Step", idx+1, "completed")
        print("**************************")

    # get_user_confirmation()


run()
