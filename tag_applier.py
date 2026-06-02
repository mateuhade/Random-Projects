import pyperclip
import os
os.environ["QT_LOGGING_RULES"] = "*.warning=false"

import sys
def main():
    if len(sys.argv) < 2:
        print("Usage: python tag_copy.py [dataFile.txt]")
        return 1
    tags = 'oop'
    text = ""
    with open(sys.argv[1]) as file:
        for line in file:
            cleanLine = line.rstrip("\n")
            text += cleanLine + " " + tags + "\n"

    pyperclip.copy(text)

main()