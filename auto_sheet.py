import pyautogui as pg
import pytesseract
import time
from PIL import Image

#monitor 1 size = (1920, 1080)
CENTER = [960, 540]

def tests():
    print(find_text("11"))

def main():
    #open taskbar
    pg.press("Win")
    time.sleep(0.2)

    #click browser
    pg.moveTo(126, 1056)
    pg.click()
    time.sleep(0.5)

    #click system
    click_system()

    #click sheets
    click_sheets()

    pg.moveTo(126, 480)
    pg.click()

    for row in range(10):
        for column in range(16):
            pg.press("right")
        pg.press("down")
        for column in range(16):
            pg.press("left")

def click_system():
    with pg.hold("alt"):
        pg.press("1")
    time.sleep(0.2)
    pg.moveTo(960, 540)
    pg.click()

def click_sheets():
    with pg.hold("alt"):
        pg.press("2")
    time.sleep(0.2)
    pg.moveTo(960, 540)
    time.sleep(0.5)

# Returns (x, y) center of the text on screen, or None if not found.
def find_text(target_text):
    screenshot = pg.screenshot()
    cropped = screenshot.crop((0, 0, 100, screenshot.height))  # leftmost 100px

    data = pytesseract.image_to_data(cropped, output_type=pytesseract.Output.DICT)

    words = data['text']
    target_words = target_text.lower().split()

    for i in range(len(words) - len(target_words) + 1):
        chunk = [words[j].lower().strip() for j in range(i, i + len(target_words))]
        if chunk == target_words:
            x1 = data['left'][i]
            y1 = data['top'][i]
            last = i + len(target_words) - 1
            x2 = data['left'][last] + data['width'][last]
            y2 = max(data['top'][j] + data['height'][j] for j in range(i, i + len(target_words)))
            return (x1 + x2) // 2, (y1 + y2) // 2

    return None

def look_mouse():
    while True:
        print(pg.position())
        time.sleep(0.5)

main()