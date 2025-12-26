import os
import time
import pyautogui
import pyperclip
import pyttsx3
import google.generativeai as genai
import pygetwindow as gw

# === CONFIG ===
genai.configure(api_key="AIzaSyBbb2PHiTUEagg2fKGBcX-oJlIecE8xD4Q")

engine = pyttsx3.init()
engine.setProperty("rate", 180)
engine.setProperty("volume", 1.0)

# WhatsApp input box coordinates (adjust if needed)
INPUT_BOX_X = 1000
INPUT_BOX_Y = 980

# === Helper Functions ===
def speak(text):
    """Speak text aloud"""
    engine.say(text)
    engine.runAndWait()


def focus_whatsapp():
    """Bring WhatsApp Web window to front"""
    try:
        window = gw.getWindowsWithTitle("WhatsApp")[0]
        window.activate()
        time.sleep(0.3)
        print("✅ WhatsApp window activated")
    except Exception:
        print("⚠️ Could not focus WhatsApp window. Make sure it's open.")


def copy_chat_history(copy_coords):
    """Selects and copies chat messages reliably."""
    x1, y1, x2, y2 = copy_coords
    print("📋 Selecting chat messages...")

    pyautogui.click(x1, y1)
    time.sleep(0.5)
    pyautogui.mouseDown()
    pyautogui.moveTo(x2, y2, duration=1.2)
    pyautogui.mouseUp()
    time.sleep(0.5)

    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.5)

    copied = pyperclip.paste().strip()
    if not copied:
        print("⚠️ No text copied. Try adjusting coordinates.")
    else:
        print("✅ Chat copied successfully!")
        print("\n=== Last 10 Lines of Chat ===")
        print("\n".join(copied.split("\n")[-10:]))
        print("=============================\n")

    return copied


def analyze_sender(chat_text, target_name="Rawnak Prime"):
    """Detects if the last message belongs to the target user."""
    lines = [line.strip() for line in chat_text.split("\n") if line.strip()]
    if not lines:
        return None, None

    recent_segment = "\n".join(lines[-10:]).lower()
    sender_detected = target_name.lower() in recent_segment
    last_msg = lines[-1]
    return sender_detected, last_msg


def generate_roast(prompt):
    """Generate a humorous roast using Google Gemini"""
    model = genai.GenerativeModel("models/gemini-2.5-flash")
    roast_prompt = (
        "You are a sarcastic, funny friend who replies humorously but playfully.\n"
        "Here is the recent chat history:\n\n"
        f"{prompt}\n\n"
        "Now, generate one short, witty reply."
    )
    try:
        response = model.generate_content(roast_prompt)
        if hasattr(response, "text") and response.text:
            return response.text.strip()
        else:
            return "You’ve left me speechless this time 😏"
    except Exception as e:
        print("❌ Gemini error:", e)
        return "Oops, I forgot what I was going to say 😅"


def send_message(text):
    """Paste and send a message in WhatsApp Web"""
    focus_whatsapp()
    pyperclip.copy(text)
    pyautogui.click(INPUT_BOX_X, INPUT_BOX_Y)
    time.sleep(0.2)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(0.1)
    pyautogui.press("enter")
    print("✅ Message sent via WhatsApp Web")
    speak(text)


# === MAIN LOGIC ===
time.sleep(3)
print("🤖 Starting chat capture...")

# Adjust these coordinates to select your chat messages on screen
chat_history = copy_chat_history(copy_coords=(700, 200, 1800, 950))

if not chat_history:
    speak("No text copied. Please adjust the coordinates.")
    exit()

# Analyze last message
is_target, last_msg = analyze_sender(chat_history, target_name="Rawnak Prime")

if is_target:
    print(f"💬 Last message from target: {last_msg}")
    roast = generate_roast(chat_history)
    print("🔥 Generated Reply:", roast)
    send_message(roast)
else:
    print("No new message from target user.")
    speak("No new message from target user.")
