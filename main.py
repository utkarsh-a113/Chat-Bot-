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

INPUT_BOX_X = 1000
INPUT_BOX_Y = 980
COPY_COORDS = (700, 200, 1800, 950)  # adjust to your chat area

def speak(text):
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

def copy_chat_history():
    """Copy visible messages"""
    x1, y1, x2, y2 = COPY_COORDS
    focus_whatsapp()
    pyautogui.click(x1 + 50, y1 + 50)
    time.sleep(0.4)
    pyautogui.moveTo(x1, y1)
    pyautogui.mouseDown()
    pyautogui.moveTo(x2, y2, duration=1.2)
    pyautogui.mouseUp()
    time.sleep(0.4)
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.4)
    copied = pyperclip.paste().strip()
    return copied

def get_last_message(chat_text):
    lines = [line.strip() for line in chat_text.split("\n") if line.strip()]
    if not lines:
        return None
    return lines[-1]

def generate_reply(prompt):
    """Generate a friendly reply"""
    model = genai.GenerativeModel("models/gemini-2.5-flash")
    try:
        response = model.generate_content(
            "You are a human-like chatbot who replies politely and humorously:\n"
            f"{prompt}\n\nGenerate one short natural reply."
        )
        return response.text.strip() if hasattr(response, "text") else "Haha okay!"
    except Exception as e:
        print("❌ Gemini error:", e)
        return "Oops, I zoned out 😅"

def send_message(text):
    focus_whatsapp()
    pyperclip.copy(text)
    pyautogui.click(INPUT_BOX_X, INPUT_BOX_Y)
    time.sleep(0.2)
    pyautogui.hotkey("ctrl", "v")
    pyautogui.press("enter")
    print(f"✅ Sent reply: {text}")
    speak(text)

# === MAIN LOOP ===
time.sleep(3)
print("🤖 Universal auto-reply started! Keep WhatsApp chat open.")

last_seen_message = None

while True:
    chat = copy_chat_history()
    if not chat:
        print("⚠️ Empty chat area. Check coordinates.")
        time.sleep(3)
        continue

    last_msg = get_last_message(chat)
    if not last_msg:
        time.sleep(3)
        continue

    if last_msg != last_seen_message:
        print(f"💬 New message detected: {last_msg}")
        reply = generate_reply(chat)
        send_message(reply)
        last_seen_message = last_msg
    else:
        print("⏳ Waiting for new message...")

    time.sleep(5)
