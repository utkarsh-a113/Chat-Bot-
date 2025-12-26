import pyautogui, pyperclip, time

def copy_chat_history(copy_coords):
    x1, y1, x2, y2 = copy_coords
    print("Selecting...")
    pyautogui.moveTo(x1, y1)
    pyautogui.mouseDown()
    pyautogui.moveTo(x2, y2, duration=1)
    pyautogui.mouseUp()
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.5)
    print("Copied text:", pyperclip.paste())

time.sleep(3)
copy_chat_history((700, 200, 1800, 950))
