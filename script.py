import pyautogui
import time

POLYGON_COUNT = "150000"
RC_IMG_PATH = "img/rc/"

IMG_FILE_NAMES = {
    "folder_icon": "select_folder.png",
    "rc_taskbar": "rc_taskbar.png",
    "folder_path": "folder_select.png",
    "simplify_mesh":"",
}

def move(to_x, to_y, duration):
    pyautogui.moveTo(to_x, to_y, duration, pyautogui.easeOutQuad)


def write(word):
    pyautogui.typewrite(message, interval=0.25)


def reset():
    screenWidth, screenHeight = pyautogui.size()
    pyautogui.moveTo(screenWidth / 2, screenHeight / 2)


def open_reality_capture():
    reset()
    path = RC_IMG_PATH + IMG_FILE_NAMES["rc_taskbar.png"]
    rc_x, rc_y = pyautogui.locateCenterOnScreen(path)
    pyautogui.click(rc_x, rc_y)


def select_img_folder():
    reset()
    path = RC_IMG_PATH + IMG_FILE_NAMES["folder_icon.png"]
    x, y = pyautogui.locateCenterOnScreen(path)
    move(x, y)
    pyautogui.click()
    path = "" + RC_IMG_PATH + IMG_FILE_NAMES["folder_path.png"]
    x, y = pyautogui.locateCenterOnScreen(path)
    move(x, y)
    pyautogui.click(clicks=2)
    write("this is a test123")
    pyautogui.enter()


def simplify_mesh():
    reset()
    rc_x, rc_y = pyautogui.locateCenterOnScreen(RC_IMG_PATH + IMG_FILE_NAMES["rc_taskbar.png"])
    pyautogui.click(rc_x, rc_y)


def change_rc_polygons():
    reset()
    p_x, p_x = pyautogui.locateCenterOnScreen('rc_polygon_box.png')
    pyautogui.typewrite(POLYGON_COUNT, interval=0.21)
    pyautogui.press('enter')


def run():
    open_reality_capture()
    select_img_folder()



run()
