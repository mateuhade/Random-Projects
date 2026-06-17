import pyautogui as pg
import time

names = [
    "REDACTED"
]

numbers = [
    2, 1, 3, 1, 2, 1, 1,
    2, 4, 4, 1, 1, 3, 2,
]


print(len(names), len(numbers))

def lm():
    while True:
        print(pg.position())
        time.sleep(0.5)
#lm()
pg.click(161, 603)
for person in names:
    pg.press("enter")
    # with pg.hold("ctrl"):
    #     pg.press("a")
    # pg.press("backspace")
    pg.write(str(person))
    pg.press("enter")
