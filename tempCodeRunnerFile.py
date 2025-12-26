

# Step 2: Drag from start to end position to select text
pyautogui.moveTo(770, 142)
pyautogui.dragTo(1860, 944, duration=1, button='left')
time.sleep(0.5)

# Step 3: Copy the selected text (Ctrl + C)
pyautogui.hotkey('ctrl', 'c')
time.sleep(0.5)

# Step 4: Get the copied text into a variable
copied_text = pyperclip.paste()

print("Copied text:\n", copied_text)
