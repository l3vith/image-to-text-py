from tkinter import *
import pyautogui
from PIL import *
import pytesseract
import os
import webbrowser
import datetime

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\%s\AppData\Local\Tesseract-OCR\tesseract.exe'%os.getenv('username')

class Application():
    def __init__(self, master):
        self.master = master
        self.rect = None
        self.x = self.y = 0
        self.start_x = None
        self.start_y = None
        self.curX = None
        self.curY = None

        # root.configure(background = 'red')
        # root.attributes("-transparentcolor","red")

        root.attributes("-transparent", "blue")
        root.geometry('400x50+200+200')  # set new geometry
        root.title('Searchinator ~ 𝖑𝖊𝖛𝖆𝖎𝖙𝖍𝖆𝖓')
        self.menu_frame = Frame(master, bg="blue")
        self.menu_frame.pack(fill=BOTH, expand=YES)

        self.buttonBar = Frame(self.menu_frame,bg="")
        self.buttonBar.pack(fill=BOTH,expand=YES)

        self.snipButton = Button(self.buttonBar, width=3, command=self.createScreenCanvas, background="green")
        self.snipButton.pack(expand=YES)

        self.master_screen = Toplevel(root)
        self.master_screen.withdraw()
        self.master_screen.attributes("-transparent", "blue")
        self.picture_frame = Frame(self.master_screen, background = "blue")
        self.picture_frame.pack(fill=BOTH, expand=YES)

    def takeBoundedScreenShot(self, x1, y1, x2, y2):
        im = pyautogui.screenshot(region=(x1, y1, x2, y2))
        x = datetime.datetime.now()
        
        fileName = "croppedImage.png"
        im.save("croppedImage.png")
        query = pytesseract.image_to_string(Image.open("croppedImage.png"))
        url = "https://www.google.com/search?q="+ query
        webbrowser.open(url)
        

    def createScreenCanvas(self):
        self.master_screen.deiconify()
        root.withdraw()

        self.screenCanvas = Canvas(self.picture_frame, cursor="cross", bg="grey11")
        self.screenCanvas.pack(fill=BOTH, expand=YES)

        self.screenCanvas.bind("<ButtonPress-1>", self.on_button_press)
        self.screenCanvas.bind("<B1-Motion>", self.on_move_press)
        self.screenCanvas.bind("<ButtonRelease-1>", self.on_button_release)

        self.master_screen.attributes('-fullscreen', True)
        self.master_screen.attributes('-alpha', .3)
        self.master_screen.lift()
        self.master_screen.attributes("-topmost", True)

    def on_button_release(self, event):
        self.recPosition()

        if self.start_x <= self.curX and self.start_y <= self.curY:
            print("right down")
            self.takeBoundedScreenShot(self.start_x, self.start_y, self.curX - self.start_x, self.curY - self.start_y)

        elif self.start_x >= self.curX and self.start_y <= self.curY:
            print("left down")
            self.takeBoundedScreenShot(self.curX, self.start_y, self.start_x - self.curX, self.curY - self.start_y)

        elif self.start_x <= self.curX and self.start_y >= self.curY:
            print("right up")
            self.takeBoundedScreenShot(self.start_x, self.curY, self.curX - self.start_x, self.start_y - self.curY)

        elif self.start_x >= self.curX and self.start_y >= self.curY:
            print("left up")
            self.takeBoundedScreenShot(self.curX, self.curY, self.start_x - self.curX, self.start_y - self.curY)

        self.exitScreenshotMode()
        return event

    def exitScreenshotMode(self):
        print("Screenshot mode exited")
        self.screenCanvas.destroy()
        self.master_screen.withdraw()
        root.deiconify()

    def exit_application(self):
        print("Application exit")
        root.quit()

    def on_button_press(self, event):
        # save mouse drag start position
        self.start_x = self.screenCanvas.canvasx(event.x)
        self.start_y = self.screenCanvas.canvasy(event.y)

        self.rect = self.screenCanvas.create_rectangle(self.x, self.y, 1, 1, outline='red', width=3, fill="blue")

    def on_move_press(self, event):
        self.curX, self.curY = (event.x, event.y)
        # expand rectangle as you drag the mouse
        self.screenCanvas.coords(self.rect, self.start_x, self.start_y, self.curX, self.curY)

    def recPosition(self):
        print(self.start_x)
        print(self.start_y)
        print(self.curX)
        print(self.curY)
        


if __name__ == '__main__':
    root = Tk()
    app = Application(root)
    root.mainloop()
    
    
