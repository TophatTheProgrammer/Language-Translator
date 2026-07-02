class Settings:
    """a class for Settings"""
    def __init__(self):
        #language
        self.presentable_language = "english"
        self.to_lang = "en"
        
        #output window
        self.font = ("Arial", 10, "bold")
        self.self_destruct_time = 10000 #ms

        #selection window
        self.alpha = 0.1
        self.bg = "red"