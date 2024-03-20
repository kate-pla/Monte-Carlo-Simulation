import tkinter as tk
from tkinter import ttk
import random
import math
import time

class MonteCarlo:
    def __init__(self, root_window):
        self.window = root_window
        self.window.title("Monte Carlo PI App")
        self.window.resizable(False,False)
      
        # Initializes the values 
        self.do_animation = tk.BooleanVar(value=True)
        self.dot_size = tk.IntVar(value=3)
        self.hit_color=tk.StringVar(value="cornflowerblue")
        self.miss_color=tk.StringVar(value="lightcoral")
        self.calculate_pi = tk.StringVar(value='')
        self.x=None
        self.y=None
        
        
        #Creates the widgets and the drawing canvas
        self.drawing_canvas = tk.Canvas(self.window, width=300, height=300, highlightthickness=1, highlightbackground="steelblue", bg="white")
        self.animation=tk.Checkbutton(self.window, text="Animate Simulation", variable=self.do_animation, onvalue=True, offvalue=False)
        self.lbl_dotsize = tk.Label(self.window, text='Dart Count:')
        self.dotsize = tk.Scale(self.window, variable=self.dot_size, from_=10, to=1000, orient=tk.HORIZONTAL)
        self.lbl_hitcolor = tk.Label(self.window, text='Hit color:')
        self.hitcolor= ttk.Combobox(self.window, textvariable=self.hit_color,state=['readonly'], values=[ 'cornflowerblue','darkseagreen', 'lightcoral'])
        self.lbl_misscolor = tk.Label(self.window, text='Miss color:')
        self.misscolor= ttk.Combobox(self.window, textvariable=self.miss_color,state=['readonly'], values=[ 'lightcoral','cornflowerblue','darkseagreen'])
        self.run_button = tk.Button(self.window, text='Run Simulation', command=self.monteCarloPi)
        self.calculatepi= tk.Label(self.window, text='Calculate Pi:')
        self.calculatepi_entry = tk.Entry(self.window, textvariable=self.calculate_pi, state=['disabled'])
        self.clear_button = tk.Button(self.window, text='Clear Simulation', command=self.clear)

      # Sets the Position of the widgets
        self.drawing_canvas.grid(row=2,column=1,rowspan=6, padx=25, pady=10)
        self.animation.grid(row=2,column=3, padx=25, pady=10)
        self.lbl_dotsize.grid(row=3,column=2,padx=25, pady=10)
        self.dotsize.grid(row=3,column=3,padx=25, pady=10)
        self.lbl_hitcolor.grid(row=4,column=2,padx=25, pady=10)
        self.hitcolor.grid(row=4,column=3,padx=25, pady=10)
        self.lbl_misscolor.grid(row=5,column=2,padx=25, pady=10)
        self.misscolor.grid(row=5,column=3,padx=25, pady=10)
        self.run_button.grid(row=6,column=2, padx=25,pady=10)
        self.calculatepi.grid(row=7,column=2,padx=25,pady=10)
        self.calculatepi_entry.grid(row=7,column=3, padx=25, pady=10)
        self.clear_button.grid(row=6,column=3, padx=25, pady=10)
        
        
        

    def monteCarloPi(self):
        """ This function calculates Pi by throwing darts at the circle and 
        seeing how many land in the circle and dividing it by the number of darts 
        that were thrown.
         
        """
        # This gives me the coordinates of the square 
        botL_x = 0
        botL_y = self.drawing_canvas.winfo_height()
        topR_x = self.drawing_canvas.winfo_width()
        topR_y = 0
        # Gets me the valus of the dart count , color of miss and hit, and if the animate is true of false 
        animate= self.do_animation.get()
        dartCount=self.dot_size.get()
        hit= self.hit_color.get()
        miss = self.miss_color.get()
        dartsWithinCircle = 0
        # Gets me the x and y values of the center of the square 
        y2= self.drawing_canvas.winfo_height()/2
        x2= self.drawing_canvas.winfo_width()/2
       
        # Creates the circle in the square 
        self.drawing_canvas.create_oval(botL_x,botL_y,topR_x,topR_y)   
        self.drawing_canvas.create_line(botL_x+150,botL_y,topR_x-150,topR_y)   
        self.drawing_canvas.create_line(botL_x,botL_y-150,topR_x,topR_y+150)   
        
        for i in range(dartCount):  
            # It gives me the a random number between -1 and 1 
            self.x = random.uniform(-1,1)    
            self.y = random.uniform(-1,1)
            # It trandforms the coordinate to the scale of (0,0) (300,300)
            self.x, self.y= self.transform(self.x, self.y, -1, -1, 1, 1, botL_x, botL_y, topR_x, topR_y)
            
            # Calculates the distance 
            distance = math.sqrt((self.x-x2)**2 + (self.y-y2)**2)
            # Creates the darts the are in the circle
            if distance<150:        
                dartsWithinCircle = dartsWithinCircle + 1
                self.drawing_canvas.create_oval(self.x-3, self.y-3, self.x+3, self.y+ 3, fill= hit)
                
                    
            # Creates the dots that are outside the circle  
            else:
                self.drawing_canvas.create_oval(self.x-3, self.y-3, self.x+3, self.y+ 3, fill=miss )
            
            if(animate == True):
                time.sleep(1/9)
                
        pi = 4 * dartsWithinCircle / dartCount
        
        return self.calculate_pi.set(pi) 
    
    def transform(self, x, y, old_botL_x, old_botL_y, old_topR_x, old_topR_y,
                              new_botL_x, new_botL_y, new_topR_x, new_topR_y):
        """
            This function transforms the old coordinates to the new coordinates 
        """
        old_x = old_topR_x -old_botL_x
        new_x= new_topR_x-new_botL_x
        old_y = old_topR_y-old_botL_y
        new_y = new_topR_y - new_botL_y

        x= (x-old_botL_x)*(new_x/old_x) + new_botL_x
        y=(y-old_botL_y)*(new_y/old_y) + new_botL_y




        return x, y
    def clear(self):
        """
            This function clears the function
        """
        self.x= self.y = None
        self.drawing_canvas.delete('all')
        self.calculate_pi.set('') 

        return

window = tk.Tk()
app = MonteCarlo(window)
window.mainloop()

