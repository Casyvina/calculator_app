import customtkinter as ctk
from buttons import Button, ImageButton, NumButton, MathButton, MathImageButton
import darkdetect
from PIL import Image
from settings import *
try:
    from ctypes import windll, byref, sizeof, c_int
except:
    pass

class Calculator(ctk.CTk):
    def __init__(self, is_dark):
        super().__init__(fg_color= (WHITE, BLACK))
        
        ctk.set_appearance_mode(f'{"dark" if is_dark else "light"}')
        
        self.geometry(f'{APP_SIZE[0]}x{APP_SIZE[1]}')
        self.resizable(False, False)
        
        self.title('')
        self.iconbitmap('empty.ico')
        self.title_bar_color(is_dark)
        
        # grid layout
        self.rowconfigure(list(range(MAIN_ROWS)), weight=1, uniform='a')
        self.columnconfigure(list(range(MAIN_COLUMNS)), weight=1, uniform='a')
        
        # data
        self.result_string = ctk.StringVar(value = '0')
        self.formula_string = ctk.StringVar(value = '')
        
        # widgets
        self.create_widget()
        
        self.mainloop()
        
    def title_bar_color(self, is_dark):
        try:
            HWND = windll.user32.GetParent(self.winfo_id())
            DWMWA_ATTRIBUTE = 35
            COLOR = TITLE_BAR_HEX_COLORS['dark'] if is_dark else TITLE_BAR_HEX_COLORS['light']
            windll.dwmapi.DwmSetWindowAttribute(HWND, DWMWA_ATTRIBUTE, byref(c_int(COLOR)), sizeof(c_int))
        except:
            pass
        
    def create_widget(self):
        # fonts
        main_font = ctk.CTkFont(family = FONT, size = NORMAL_FONT_SIZE)
        result_font = ctk.CTkFont(family = FONT, size = OUTPUT_FONT_SIZE)
        
        # output labels
        OutputLabel(self, 0, 'SE', main_font, self.formula_string) # formula
        OutputLabel(self, 1, 'E', result_font, self.result_string) # result
        
        # clear (AC) button
        Button(
            parent = self,
            func = self.clear,
            text = OPERATORS['clear']['text'],
            col=OPERATORS['clear']['col'], 
            row=OPERATORS['clear']['row'],
            font = main_font,
            span=1,)
            
        
        # exercise
        # percentage(%) button
        Button(
            parent = self,
            func = self.percentage,
            text = OPERATORS['percent']['text'],
            col = OPERATORS['percent']['col'],
            row = OPERATORS['percent']['row'],
            font = main_font,
            span=1,
        )
        
        # invert button
        # exercise 
        # import the image and create the image button
        invert_image = ctk.CTkImage(
            light_image= Image.open(OPERATORS['invert']['image path']['dark']),
            dark_image = Image.open(OPERATORS['invert']['image path']['light'])
        )
        ImageButton(
            parent = self,
            text = '',
            func = self.invert,
            col = OPERATORS['invert']['col'],
            row = OPERATORS['invert']['row'],
            image = invert_image
        )
       
        # number buttons
        for num, data in NUM_POSITIONS.items():
            NumButton(
                parent = self,
                text = num,
                func = self.num_press,
                col = data['col'],
                row = data['row'],
                font = main_font,
                span = data['span']
            )
            
        # math buttons
        for operator, data in MATH_POSITIONS.items():
            if data['image path']:
                divide_image = ctk.CTkImage(
                    light_image = Image.open(data['image path']['dark']),
                    dark_image= Image.open(data['image path']['light'])
                )
                
                MathImageButton(
                    parent=self,
                    operator = operator, 
                    func = self.math_press, 
                    col = data['col'], 
                    row = data['row'], 
                    image = divide_image
                )
            else:
                MathButton(
                    parent= self,
                    text = data['character'],
                    operator= operator,
                    func= self.math_press,
                    col= data['col'],
                    row = data['row'],
                    font= main_font,
                    span = 1
                )
                
    def math_press(self, value):
        print(value)        
    
    def num_press(self, value):
        print(value)
        
    def invert(self):
        print('invert') 
        
    def percentage(self):
        print('percent')
    
    def clear(self):
        print('clear')
    
class OutputLabel(ctk.CTkLabel):
    def __init__(self, parent, row, anchor, font, string_var):
        super().__init__(master = parent, text= '123', font=font, textvariable= string_var)
        self.grid(column=0, columnspan=4, row=row, sticky= anchor, padx=10)

if __name__ == '__main__':  
    Calculator(darkdetect.isDark())
