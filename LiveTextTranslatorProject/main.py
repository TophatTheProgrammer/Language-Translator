
import keyboard
from threading import Thread
import time

import Settings
import Translator
import TextExtractor

class Main:
    """A class that creates the main program"""
    
    def __init__(self):
        """Initialize the main program"""
        self.AltHold = False
        self.Prep_ScreenShot = False
        self.settings = Settings.Settings()
        self.translator = Translator.Translator(self.settings.to_lang, self.settings.presentable_language)
        self.textextractor = TextExtractor.TextExtractor(self)

    def activate(self, event):
        """Detect events globaly"""

        #check if alt is held
        if event.name == "alt" and not self.Prep_ScreenShot:
            if event.event_type == "down":
                self.AltHold = True
            else:
                self.AltHold = False
        #Activate when p is clicked and alt is held down
        elif event.name == "p" and event.event_type == "down" and self.AltHold:
            self.AltHold = False
            self.Prep_ScreenShot = True
        #grab the for the screenshot
        elif event.name == "g" and event.event_type == "down" and self.Prep_ScreenShot:
            self.textextractor.grabArea()
            

    def take_screenshot(self):
        """Take the screenshot with the obtained points"""
        #check if there are 2 points and then activate.
        if self.textextractor.times == 2:
            self.write_point = False
            self.Prep_ScreenShot = False
            self.textextractor.TakeScreenShot()
            self.textextractor.times = 0
        #if there are atleast 1 point created, create the selection rectangle
        if self.textextractor.times == 1 and self.textextractor.positions:
            self.textextractor.create_selection()

    def Keyboard_listner(self):
        """listens for keyboard inputs."""
        keyboard.hook(main.activate)
        keyboard.wait()




if __name__ == "__main__":
    main = Main()

    #create the thread and start it so that the selection rectangle doesn't stop keyboard.hook
    thread = Thread(target=main.Keyboard_listner, daemon=True)
    thread.start()

    print("Active.")
    
    #check every 0.5 seconds if take_screenshot() can do anything.
    while True:
        main.take_screenshot()
        time.sleep(0.5)