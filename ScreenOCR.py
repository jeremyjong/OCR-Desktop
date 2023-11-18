import pyautogui
import keyboard
import pyocr
import os
import time
from pynput import mouse


class ScreenOCR():
    def __init__(self):        
    
        TESSERACT_PATH = r'Tesseract-OCR'
        TESSDATA_PATH = r'Tesseract-OCR\tessdata' #tessdataのpath
        pyocr.tesseract.TESSERACT_CMD = r'Tesseract-OCR\tesseract.exe'
        
        os.environ["PATH"] += os.pathsep + os.getcwd() + "\\" + TESSERACT_PATH
        os.environ["TESSDATA_PREFIX"] = os.getcwd() + "\\" + TESSDATA_PATH
               
        
        #OCRエンジン取得
        tools = pyocr.get_available_tools()
        self.tool = tools[0]
        #OCRの設定 ※tesseract_layout=6が精度には重要。デフォルトは3
        self.builder = pyocr.builders.TextBuilder(tesseract_layout=6)       
        

    def capture_and_save(self,x1, y1, width, height):        

        # Capture the screen
        screenshot = pyautogui.screenshot(region=(x1, y1, width, height))
        # Save the image
        #screenshot.save(r'capture.png')        
        extracted_text = self.tool.image_to_string(screenshot , lang='eng+jpn', builder=self.builder)     
        #extracted_text = extracted_text.replace(" ","")
        print(extracted_text)
        with open('output.txt', 'w') as f:            
            f.write(extracted_text)
 

def on_click(x, y, button, pressed):
    global coords
    # Only store coordinates when the left button is pressed
    
    if button == mouse.Button.left and pressed:
        coords.append((x, y))
        # If two sets of coordinates have been recorded, stop the listener
        print("Click to pick BOTTOM RIGHT")
        if len(coords) == 2:
            return False  


def on_middle_click(x, y, button, pressed):
    if button == mouse.Button.middle and pressed:
        print("**************************************************")
        print("Middle button clicked at ({0}, {1})".format(x, y))
        socr = ScreenOCR() 
        socr.capture_and_save(x1, y1, width, height)
        return False
                
                
if __name__ == "__main__":     
    
    coords = []
    print("Click to pick TOP LEFT")
    # Start the mouse listener
    with mouse.Listener(on_click=on_click) as listener:        
        listener.join()

    # Calculate width and height from coordinates
    x1, y1 = coords[0]
    width, height = coords[1][0] - x1, coords[1][1] - y1

    print(f"x1: {x1}, y1: {y1}, width: {width}, height: {height}")
    
    with mouse.Listener(on_click=on_middle_click) as listener:            
        listener.join()
        time.sleep(1)
        
          