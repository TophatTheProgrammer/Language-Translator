import pytesseract
import mss
import cv2
import pyautogui
import numpy as np
import tkinter

import window

pytesseract.pytesseract.tesseract_cmd = r"your-directory"

class TextExtractor:
    """A class that is used to extract text"""

    def __init__(self, main_program):
        """initialize the TextExtractor class"""
        self.positions = []
        self.times = 0
        self.screen = mss.MSS()
        self.area = {}
        self.img = None

        #get the necesary information from the main program
        self.main_program = main_program
        self.settings = self.main_program.settings
        self.translator = self.main_program.translator

        #window information
        self.TpWindow=None
        self.bg = self.settings.bg
        self.alpha = self.settings.alpha

    def grabArea(self):
        """grab the area where the screenshot will be done"""

        #make a point and add one to times
        pos = pyautogui.position()
        self.positions.append(pos)
        self.times += 1

        #when times is = 2, calculate the area needed for the screenshot and clear the positions list.
        if self.times == 2:
            x1,x2 = self.positions[0].x, self.positions[1].x
            y1,y2 = self.positions[0].y, self.positions[1].y
            self.area = self.CalculateSquare(x1, x2, y1, y2)
            self.positions.clear()

    def CalculateSquare(self, x1, x2, y1, y2):

        #check if first point position and second point position valid
        x2 = x2 if x1+10 < x2 else x1+10
        y2 = y2 if y1+10 < y2 else y1+10

        try:
            if x1 > x2:
                raise ValueError("points is not correctly placed")
            elif y1 > y2:
                raise ValueError("points is not correctly placed")
        except ValueError as e:
            print(e)
        
        #gets the necesary info for mss.grab, and then return it as a dict
        top = y1
        left = x1
        width = x2-x1
        height = y2-y1

        return {"top": top, "left": left, "width": width, "height": height}
    
    def TakeScreenShot(self):
        """Take a screenshot with the area selected"""

        #take the screenshot with the obtained area
        self.img = self.screen.grab(self.area)

        #prepare the image for the OCR
        self.img = self._prep_image()

        #write the text (TEMP! just used for debugging)
        cv2.imwrite("Screenshot.png", self.img)

        #now send it to the OCR!
        text = self._TextExtraction(self.img)
        splitted_text = text.split()

        
        #turn the text into one line
        text = " ".join(splitted_text)
        print(text)
        
        #translate the text
        translated_text, langdetected = self.translator.Translation(text)

        #output the text as a window
        new_window = window.Window(self)
        new_window.WriteText(translated_text, langdetected)

    def _prep_image(self):
        """Prepare the image"""
        #Turn the image into grayscale
        screenshot_color = np.array(self.img)
        gray_screenshot = cv2.cvtColor(screenshot_color, cv2.COLOR_BGRA2GRAY)

        #scale the image using cv2.inter_cubic
        scale = 3
        height = int(gray_screenshot.shape[0] * scale)
        width = int(gray_screenshot.shape[1] * scale)

        resized_gray_img = cv2.resize(gray_screenshot, (width, height), interpolation=cv2.INTER_CUBIC)

        #now change every pixel to white or black and apply otsu algorithm
        _, binary_gray_img = cv2.threshold(resized_gray_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        #grab the average color of the image
        average_color = cv2.mean(binary_gray_img)[0]

        #check if its mostly black or white, if thesres more white than black, inverse. (text will always be less.)
        if average_color < 127:
            #mostly black.
            binary_gray_img = cv2.bitwise_not(binary_gray_img)

        #filter it more smooth.
        smooth_binary_gray_img = cv2.bilateralFilter(binary_gray_img, 6, 23, 15)

        #return the preped image
        return smooth_binary_gray_img

    def _TextExtraction(self,image):
        """extract the string from a given image"""
        langs = "afr+ara+ben+bul+cat+ces+chi_sim+chi_tra+cym+dan+deu+ell+est+fas+fil+fin+fra+guj"
        langs += "+heb+hin+hrv+hun+ind+ita+jpn+kan+lav+lit+mal+mar+mkd+nep+nld+nor+pan+pol+por"
        langs += "+rus+slk+slv+spa+sqi+swa+swe+tam+tel+tha+tur+ukr+urd+vie"
        return pytesseract.image_to_string(image, lang=langs, config=r"--oem 3 --psm 3")

    def create_selection(self):
        """creates a selection window to see the image size for more precise screenshoting"""
        self.TpWindow = tkinter.Tk()
        self.TpWindow.overrideredirect(True)
        self.TpWindow.attributes(topmost=True, alpha=self.alpha)
        self.TpWindow.config(bg=self.bg)

        #update the window.
        self._update_selection()

        #start the selection mainloop
        self.TpWindow.mainloop()

    def _update_selection(self):
        """"Update the selection size to follow the mouse"""
        #stop when there are no more positions (the screenshot has been done.)
        if not self.positions:
            self.TpWindow.destroy()
            return
        else:
            #take the first point position and the current mouse position
            starting_point = self.positions[0]
            end_point = pyautogui.position()

            #get the required information for grabbing the area
            x1, x2 = starting_point.x, end_point.x
            y1, y2 = starting_point.y, end_point.y

            #change the window size            
            Rectangle = self.CalculateSquare(x1, x2, y1 ,y2)
            size_position = f"{Rectangle["width"]}x{Rectangle["height"]}+{Rectangle["left"]}+{Rectangle["top"]}"
            self.TpWindow.geometry(size_position)

            #loop.
            self.TpWindow.after(10, self._update_selection)