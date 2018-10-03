import pyautogui
import time
import cv2
import numpy as np
from twilio.rest import Client

POLYGON_COUNT = "150000"
RC_IMG_PATH = "img/rc/"

CONTROLS_CONF_LEVEL = 0.97

IMG_FILE_NAMES = {
    "folder_icon": "select_folder.png",
    "rc_taskbar": "rc_taskbar.png",
    "folder_path": "folder_select.png",
    "controls": "controls.png",
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

# Your Account SID from twilio.com/console
account_sid = "ACf6d6aabda889393fc8de587d55874b7a"
# Your Auth Token from twilio.com/console
auth_token  = "47c4fe081246aca68dae928e65cc3c19"

def send_text(msg):
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to="+16262418919",
        from_="+14156505222",
        body=msg)

    print(message.sid)


def get_img_path(key):
    return RC_IMG_PATH + IMG_FILE_NAMES[key];


def move(to_x, to_y, duration):
    pyautogui.moveTo(to_x, to_y, duration, pyautogui.easeOutQuad)
    time.sleep(0.5)


def write(message):
    pyautogui.typewrite(message, interval=0.25)


def reset():
    screenWidth, screenHeight = pyautogui.size()
    pyautogui.moveTo(screenWidth / 2, screenHeight / 2)


def click():
    pyautogui.click()


def double_click():
    pyautogui.click(clicks=2)


def get_x_y(key):
    return (POINTS[key]["x"], POINTS[key]["y"])


def move_and_click(key):
    x, y = get_x_y(key)
    move(x, y, 1)
    # click()


def move_and_double_click(key):
    x, y = get_x_y(key)
    move(x, y, 1)
    double_click()


def check_working():
    is_working = True
    template = cv2.imread(get_img_path("controls"), 0)
    w, h = template.shape[::-1]
    while is_working:
        time.sleep(10)
        img = cv2.cvtColor(np.array(pyautogui.screenshot()), cv2.COLOR_BGR2GRAY)
        method = eval('cv2.TM_CCORR_NORMED')
        res = cv2.matchTemplate(img,template,method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        is_working = max_val > CONTROLS_CONF_LEVEL
        print("  percent match:", max_val, flush=True)


def select_all():
    pyautogui.hotkey('ctrl', 'a')


def paste_text(text):
    select_all()
    write(text)


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


def to_user_step(step):
    return int(step) + 1


def from_user_step(step):
    return int(step) - 1


def get_starting_step():
    print("*****************************")
    print("Welcome to the ModelScriptHelper!")
    resume = input("Are you resuming from the middle of a previous session? [y/N]? ")
    if resume.lower() == 'y':
        step = input("What was the last FULL COMPLETED step? ")
        return from_user_step(step)
    elif resume.lower() == 'n':
        return 0
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
    start = get_starting_step()
    print("**************************")
    for idx in range(start, len(steps)):
        step = steps[idx]
        print("Step", to_user_step(idx), "started")
        globals()[step["name"]](*step["step_args"])
        print("Step", to_user_step(idx), "completed")
        print("**************************")


run()
