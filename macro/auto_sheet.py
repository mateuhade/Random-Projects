import pyautogui as pg
import pytesseract
import time
import pyperclip
from dataclasses import dataclass, field, asdict
from typing import List

# ------------------- CONSTANTS --------------------

MAX_XY = [1920, 1080]
CENTER = [960, 540]
MONTH = False
YEAR = True

# ------------------- CLASSES --------------------
@dataclass
class Person:
    name: str = ""
    age: int = 0
    age_magnitude: bool = False
    intellectual_deficiency: bool = False
    physical_deficiency: bool = False
    good_sanitation: bool = False
    severe_malnutrition: bool = False
    drug_addicted: bool = False
    illiterate: bool = False
    elderly: bool = False
    baby: bool = False
    hypertensive: bool = False
    diabetes: bool = False

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Person":
        return cls(**data)
@dataclass
class Family:
    address: str = ""
    responsible: str = ""
    room_amount: int = 0
    resident_amount: int = 0
    members: List[Person] = field(default_factory=list)  # empty list by default

    def add_member(self, person: Person):
        self.members.append(person)
        self.resident_amount = len(self.members)  # keeps count in sync

    def to_dict(self) -> dict:
        return asdict(self)  # handles nested Person objects automatically

    @classmethod
    def from_dict(cls, data: dict) -> "Family":
        members = [Person.from_dict(p) for p in data.get("members", [])]
        return cls(
            address=data["address"],
            responsible=data["responsible"],
            room_amount=data["room_amount"],
            resident_amount=data["resident_amount"],
            members=members
        )

families: list[Family] = []

# -------------------- MAIN ------------------------



def main():
    # open_zen_browser()
    open_zen_browser()

    pg.click(924, 23)

    click_system()

    get_house(1)

    click_sheets()

    

# ------------------------------- SIDE FUNCTIONS --------------------------

def open_zen_browser():
    # open taskbar
    pg.press("Win")
    time.sleep(0.2)

    # open browser
    pg.write("zen")
    time.sleep(0.5)
    pg.press("enter")
    time.sleep(10)

    pg.click(121, 1057)

def click_system():
    with pg.hold("alt"):
        pg.press("1")
    time.sleep(0.2)
    pg.click(960, 540)
    time.sleep(0.5)

def click_sheets():
    with pg.hold("alt"):
        pg.press("2")
    time.sleep(0.5)

# Returns (x, y) center of the text on screen, or None if not found.
def find_text(target_text):
    screenshot = pg.screenshot()

    data = pytesseract.image_to_data(screenshot, output_type=pytesseract.Output.DICT)

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

def copy_all(x, y):
    pg.moveTo(x, y)
    pg.tripleClick()
    with pg.hold("ctrl"):
        pg.press("c")

def copy_word(x, y):
    pg.moveTo(x, y)
    pg.doubleClick()
    with pg.hold("ctrl"):
        pg.press("c")

def get_pixel_color(x, y):
    screenshot = pg.screenshot()
    return screenshot.getpixel((x, y))

def is_selected(x, y):
    if get_pixel_color(x, y) == (53, 132, 228):
        return True
    return False

def return_page():
    pg.moveTo(0, CENTER[1])
    time.sleep(1)
    pg.doubleClick(80, 25)
    pg.moveTo(CENTER[0], CENTER[1])
    time.sleep(2)

# --------------------------- MAIN FUNCTIONS ------------------------------
def get_house(house_ID):
    pg.click(236, 279)
    pg.press(str(house_ID))
    house_ID -= 4

    # press area 60 number
    pg.click(212, 347)
    pg.write("t")
    pg.press("down", presses=79)
    pg.press("enter")
    
    # press microarea 13 number
    pg.click(1182, 351)
    pg.press("s")
    pg.press("down", presses=2)
    pg.press("enter")
    
    # Press search
    pg.click(100, 435)
    time.sleep(1)
    # ********************************************
    # this part gets house information
    family_temp = Family()
    families.append(family_temp)

    # house adress
    copy_all(433, 500)
    street = pyperclip.paste()

    copy_all(691, 500)
    compliment = pyperclip.paste()

    copy_all(974, 500)
    number = pyperclip.paste()
    address = f"{street}, {number}, {compliment}"
    families[house_ID-1].address = address

    # person responsible for the house
    copy_all(1417, 500)
    families[house_ID-1].responsible = pyperclip.paste()
    
    # access house editing mode
    
    pg.click(pg.center(pg.locateOnScreen("editar.png")))
    time.sleep(1)
    pg.press("pagedown")
    time.sleep(1)

    # number of rooms in house
    copy_all(180, 681)
    families[house_ID-1].room_amount = pyperclip.paste()

    # number of residents in house
    copy_all(1120, 681)
    families[house_ID-1].resident_amount = pyperclip.paste()

    # ********************************************
    # this part gets people information

    # access list of people in the house
    pg.click(1450, 975)

    get_family(int(families[house_ID-1].resident_amount), house_ID)
    print(families[0])

def get_family(residents, current_family):
    current_Y = 511

    for resident in range(residents):
        pg.click(134, current_Y) # click view resident
        time.sleep(1)

        # Creates new resident
        person_tmp = Person()

        copy_all(436, 360)  # resident name
        person_tmp.name = pyperclip.paste()

        copy_word(970, 429) # resident age
        person_tmp.age = pyperclip.paste()

        copy_word(991, 429) # resident age magnitude
        age_magnitude = pyperclip.paste()
        if ((age_magnitude.lower() == "ano") or (age_magnitude.lower() == "anos")):
            person_tmp.age_magnitude = YEAR

        pg.press("pagedown")
        time.sleep(1)

        pg.click(291, 153)
        if is_selected(287, 215): # resident deficiency
            if is_selected(423, 410): # resident intelectual deficiency
                person_tmp.intellectual_deficiency = True
            if is_selected(975, 411): # resident physical deficiency
                person_tmp.physical_deficiency = True

        person_tmp.good_sanitation = True

        pg.doubleClick(1046, 518) # resident severe malnutrition
        if is_selected(1044, 580): 
            person_tmp.severe_malnutrition = True
        
        pg.doubleClick(503, 447)
        if is_selected(500, 503):
            person_tmp.drug_addicted = True

        pg.doubleClick(210, 589)
        if is_selected(220, 652):
            person_tmp.illiterate = True
        
        if person_tmp.age_magnitude:
            if int(person_tmp.age) > 70:
                person_tmp.elderly = True
        elif int(person_tmp.age) < 6:
            person_tmp.baby = True
        
        pg.doubleClick(780, 444)
        if is_selected(771, 505):
            person_tmp.hypertensive = True
        
        pg.doubleClick(1040, 444)
        if is_selected(1040, 555):
            person_tmp.diabetes = True

        print(person_tmp)
        # Adds new resident to current family
        return_page()
        current_Y += 21
        families[current_family-1].add_member(person_tmp)

        
        
    return 0


#main() #252 507
#get_house(5)
#look_mouse()
#return_page()
