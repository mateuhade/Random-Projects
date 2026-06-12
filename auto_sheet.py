import pyautogui as pg
import pytesseract
import time
import pyperclip
from dataclasses import dataclass, field, asdict
from typing import List

# ------------------- CONSTANTS --------------------

MAX_XY = [1920, 1080]
CENTER = [960, 540]
MONTH = 0
YEAR = 1

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

# --------------------------- MAIN FUNCTIONS ------------------------------

def get_house(family_number):
    pg.click(236, 279)
    pg.press(str(family_number))

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
    copy_all(345, 500)
    street = pyperclip.paste()

    copy_all(594, 500)
    compliment = pyperclip.paste()

    copy_all(956, 500)
    number = pyperclip.paste()
    address = f"{street}, {number}, {compliment}"
    families[family_number-1].address = address

    # person responsible for the house
    copy_all(1417, 500)
    families[family_number-1].responsible = pyperclip.paste()
    
    # access house editing mode
    pg.click(104, 500)
    time.sleep(1)
    pg.press("pagedown")

    # number of rooms in house
    copy_all(180, 713)
    families[family_number-1].room_amount = pyperclip.paste()

    # number of residents in house
    copy_all(1120, 713)
    families[family_number-1].resident_amount = pyperclip.paste()

    # ********************************************
    # this part gets people information
    # access people in house
    pg.click(1450, 1000)
    print(families[0])

    ... #get_family(resident_amount)

    time.sleep(1)
    pg.moveTo(0, CENTER[1])
    time.sleep(0.2)
    pg.click(85, 25)


def get_family(residents):
    pg.click(123, 511) # pacient 1
    time.sleep(1)

    for resident in range(residents):
        copy_all(436, 360)  # pacient name
        person_tmp = Person(name=pyperclip.paste())
        copy_word(967, 249) # pacient age
        person_tmp = Person(age=pyperclip.paste())
        copy_word(991, 429) # pacient age magnitude
        person_tmp = Person(age_magnitude=pyperclip.paste())

        pg.press("pagedown")

        ...


main()



"""
PSEUDOCODIGO:
armazenar_familia(moradores):
    para morador em moradores:

        clicar possui alguma deficiencia?
        se checar_por_pixel_azul(sim/nao):
            se checar_por_pixel_azul(intelectual):
                morador[deficiencia_intelectual] = True
            se checar_por_pixel_azul(fisica):
                morador[deficiencia_fisica] = True
        
        morador[saneamento_bom] = True

        clicar desnutricao grave
        se checar_por_pixel_azul(sim/nao)
            morador[desnutricao_grave] = True

        clicar dependente ou abusa de drogas
        se checar_por_pixel_azul(sim/nao)
            morador[drogadicao] = True

        clicar analfabeto
        se checar_por_pixel_azul(sim/nao)
            morador[analfabetismo] = True
        
        se morador["idade_grandeza"].lower == "ano" or morador[idade_grandeza] == "anos":
            se int(morador[idade]) > 70:
                morador[idoso] = True
        senao se int(morador[idade]) < 6:
            morador[bebe] = True

        clicar hipertensao arterial
        se checar_por_pixel_azul(sim/nao)
            Pessoa[hipertensao] = True
        
        clicar diabetico
        se checar_por_pixel_azul(sim/nao)
            Pessoa[diabetes] = True
"""