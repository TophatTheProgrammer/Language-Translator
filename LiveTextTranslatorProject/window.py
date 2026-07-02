import tkinter as tk

class Window:
    """A class that creates a window where the output will be shown"""

    def __init__(self, TextExtractor):
        """Initialize a window"""
        self.window = tk.Tk()

        #make the window buttons obsulete and make the new window appear over every window
        self.window.overrideredirect(True)
        self.window.attributes(topmost=True)
        
        #get the required information.
        self.main = TextExtractor
        self.settings = TextExtractor.settings
        self.font = self.settings.font
        self.time = self.settings.self_destruct_time
        Area = self.main.area

        #grab the Area location
        self.y = Area["top"]
        self.x = Area["left"]
        self.height = Area["height"]
        self.width = Area["width"]

        #size up the window accordingly
        self.window.geometry(f"{self.width}x{self.height}+{self.x}+{self.y}")

    def WriteText(self, translated_text, detected_language):
        """put the text on the window and then start the window mainloop()"""

        #get the output language string.
        translated_text_into = self.main.translator.presentable_lang

        #check if its empty
        if translated_text == "":
            #if yes, make a window and show that the text is not detected.
            Text = tk.Label(
                            self.window,
                            text="No text detected.",
                            wraplength=self.width-12, 
                            font=self.font,
                            )
        else:
            #if its not empty, put the output in a label and display the window.
            formulated_text = f"{translated_text} ({detected_language} -> {translated_text_into})"

            Text = tk.Label(
                            self.window,
                            text=formulated_text,
                            wraplength=self.width-12, 
                            font=self.font,
                            )
        
        Text.pack(expand=True, fill="both")

        #kill the window after some time.
        self._AutoDestruct()

        #starts the tk mainloop
        self.window.mainloop()

    def _AutoDestruct(self):
        """KILL IT."""
        self.window.after(self.time, lambda: self.window.destroy())

        

