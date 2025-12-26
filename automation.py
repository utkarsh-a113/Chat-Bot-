import pyautogui, time

time.sleep(5)
print("Typing test starting...")
pyautogui.click(1000, 980)  # 👈 Adjust this later
pyautogui.typewrite("This is a typing test from bot.", interval=0.05)
pyautogui.press("enter")
print("Done!")
