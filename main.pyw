import os
import widget
import time
import tkinter as tk
from tkinter import messagebox
from internetConnection import isConnected
from ocr import parseImage
from PIL import Image, ImageGrab
from pynput import keyboard
import pyperclip
# import SnippingMenu

popUp = widget.Widget()

# Variables
debugMode = False


# Open welcome window
popUp.welcome()

# Activation hotkey triggers this procedure
def parseClipboard(openPopUp: bool = False):
    clipboard = ImageGrab.grabclipboard()

    # Play sound
    if openPopUp:
        popUp.playSoundEffect("Coin 3.mp3")
    else:
        popUp.playSoundEffect("Coin 2.mp3")

    # Check clipboard contents
    # If clipboard contains image
    if clipboard:
        # File name returned
        if isinstance(clipboard, list):
            # Use the clipboard image to parse
            clipboard = clipboard[0]
            text = parseImage(clipboard)
        # Image file returned
        else:
            clipboard.save("Assets/clipboard.png")
            text = parseImage("Assets/clipboard.png")
        
        # Copy to clipboard if text isn't empty
        if text:
            pyperclip.copy(text)
            print(text)
            # Open translation widget
            if openPopUp:
                popUp.open(text)

    # if clibpoard contains text
    elif pyperclip.paste() and openPopUp:
        # No need to copy to clipboard
        text = pyperclip.paste()
        print(text)
        # Open translation widget
        popUp.open(text)
            
    # Clipboard contains nothing
    else:
        print("Error: Empty clipboard")
        messagebox.showwarning(title="Error", message="Your clipboard is empty")

def main():
    # Check if connected to internet
    if not isConnected():
        print("Warning: No internet connection")

    # Hotkey implementation
    if not debugMode:
        with keyboard.GlobalHotKeys({'<alt>+q': lambda : parseClipboard(True),
                                     '<alt>+w': lambda : parseClipboard(False)}) as h:
            h.join()

    # Debug mode
    if debugMode:
        input("Whenever you're ready: ")
        parseClipboard()

if __name__ == "__main__":
    main()