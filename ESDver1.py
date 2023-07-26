from cgi import test
from optparse import Values
from sqlite3 import Row
from time import time
import tkinter as tk
from tkinter import ttk
from turtle import width
import pyvisa
import time 
import keyboard
import time
import cv2
from PIL import Image, ImageTk
from webbrowser import get
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import threading as th
import minimalmodbus
from simple_pid import PID

root = tk.Tk()
root.title("ESD_ver1") 
root.geometry("1050x600+100+100") #가로*세로+x좌표+y좌표
root.resizable(False,False) #창크기 변경불가
# root.configure(background='white')

rm = pyvisa.ResourceManager()
# usb connection name 
print(rm.list_resources()) 

# connect the usb resource with python
# com_hv1 = rm.open_resource('ASRL13::INSTR')
# com_hv1.baud_rate = 9600
# com_hv2 = rm.open_resource('ASRL12::INSTR')
# com_hv2.baud_rate = 9600
# com_pxpy = rm.open_resource('ASRL11::INSTR')
# com_pxpy.baud_rate = 921600
# com_syr = rm.open_resource('ASRL6::INSTR')
# com_syr.baud_rate = 115200
# com_hot = minimalmodbus.Instrument('com14', 1, minimalmodbus.MODE_RTU)
# com_hot.serial.baudrate = 115200

AFTER=None

def PIDcontrol():
    print(taylor_height)
    # v = taylor_height
    control = pid(taylor_height)
    print(control)
    # com_hv1.write("VSET"+str(control)) 
    time.sleep(.5)
    global AFTER
    AFTER=root.after(100, PIDcontrol)
    

def PIDcontroloff():
    try:
        root.after_cancel(AFTER)
    except:
        pass



def controlonbutton():
    tm=temperature.get()
    px=position_x.get()
    py=position_y.get()
    sy1=syringe1.get()
    sy2=syringe2.get()
    sy3=syringe3.get()
    di1=diameter1.get()
    di2=diameter2.get()
    di3=diameter3.get()
    hv1=highvoltage1.get()
    hv2=highvoltage2.get()
    st=esdtime.get()    
    # after st time control off
    esdend=th.Timer(int(st)*60, controloffbutton) 
    esdend.start()
    # hotplate
    flo=float(tm)
    com_hot.write_float(548,flo)
    

    # x,y position
    com_pxpy.write('1MO')
    com_pxpy.write('2MO')
    com_pxpy.write('1PA'+str(px))
    com_pxpy.write('2PA'+str(py))
    time.sleep(1)

    #syringe pump
    
    com_syr.write('0svolume 5 ml')
    time.sleep(0.1)
    com_syr.write('0diameter '+str(di1))
    time.sleep(0.1)
    com_syr.write('0irate '+str(sy1)+' ul/min')
    time.sleep(0.1)
    com_syr.write('0irun')
    time.sleep(0.1)
    com_syr.write('1svolume 5 ml')
    time.sleep(0.1)
    com_syr.write('1diameter '+str(di2))
    time.sleep(0.1)
    com_syr.write('1irate '+str(sy2)+' ul/min')
    time.sleep(0.1)
    com_syr.write('1irun')
    time.sleep(0.1)

    com_syr.write('2svolume 5 ml')
    time.sleep(0.1)
    com_syr.write('2diameter '+str(di3))
    time.sleep(0.1)
    com_syr.write('2irate '+str(sy3)+' ul/min')
    time.sleep(0.1)
    com_syr.write('2irun')
    time.sleep(0.1)
    
    # high voltage
    com_hv1.write("HVON")
    com_hv1.write("VSET"+str(hv1))

    com_hv2.write("HVON")
    com_hv2.write("VSET"+str(hv2))

    # HV1.write("VSET"+str(voltage_data))
    # print(tm,px,py,sy1)

   
def controloffbutton():

    #hotplate
    com_hot.write_float(548,30.0)

    # x,y position
    com_pxpy.write('1PA0')
    com_pxpy.write('2PA0')
    # #syringe pump
    
    com_syr.write('0stop')
    com_syr.write('1stop')
    com_syr.write('2stop')
    # high voltage
    com_hv1.write("HVOF")
    com_hv2.write("HVOF")



    

control = tk.LabelFrame(root, text= 'Parameter', font="time 20 bold",labelanchor=tk.N)
control.pack()
# control the every equipment
# 0row 
tk.Label(control, text = "Position", font = "Hevetica 20 bold").grid(row=0, column=0, columnspan=4)
tk.Label(control, text = "Syringe1", font = "Hevetica 20 bold").grid(row=0, column=6,columnspan=2)
tk.Label(control, text = "Syringe2", font = "Hevetica 20 bold").grid(row=0, column=9, columnspan=2)
tk.Label(control, text = "Syringe3", font = "Hevetica 20 bold").grid(row=0, column=12, columnspan=2)
tk.Label(control, text = "HV1", font = "Hevetica 20 bold").grid(row=0, column=15,columnspan=2)
tk.Label(control, text = "Time", font = "Hevetica 20 bold").grid(row=0, column=18, columnspan=2)
# 1row
tk.Label(control, text = "x:", font = "Times 20 bold").grid(row=1, column=0)
position_x=tk.Entry(control, width=5, font=10, validate='key')
position_x.grid(row=1, column=1)
tk.Label(control, text = "y:", font = "Times 20 bold").grid(row=1, column=2)
position_y=tk.Entry(control, width=5, font=10, validate='key')
position_y.grid(row=1, column=3)
# syringe pump control
syringe1=tk.Entry(control, width=5, font=10, validate='key')
syringe1.grid(row=1, column=6)
tk.Label(control, text = "ul/min", font = "Times 13").grid(row=1, column=7)
syringe2=tk.Entry(control, width=5, font=10, validate='key')
syringe2.grid(row=1, column=9)
tk.Label(control, text = "ul/min", font = "Times 13").grid(row=1, column=10)
syringe3=tk.Entry(control, width=5, font=10, validate='key')
syringe3.grid(row=1, column=12)
tk.Label(control, text = "ul/min", font = "Times 13").grid(row=1, column=13)
# hv1 control
highvoltage1=tk.Entry(control, width=5, font=10, validate='key')
highvoltage1.grid(row=1, column=15)
tk.Label(control, text = "V", font = "Times 13").grid(row=1, column=16)

esdtime=tk.Entry(control, width=5, font=10, validate='key')
esdtime.grid(row=1, column=18)
tk.Label(control, text = "min", font = "Times 13").grid(row=1, column=19)
#2row
tk.Label(control, text = "Temperature", font = "Hevetica 20 bold").grid(row=2, column=0, columnspan=5)
tk.Label(control, text = "Diameter1", font = "Hevetica 20 bold").grid(row=2, column=6,columnspan=2)
tk.Label(control, text = "Diameter2", font = "Hevetica 20 bold").grid(row=2, column=9, columnspan=2)
tk.Label(control, text = "Diameter3", font = "Hevetica 20 bold").grid(row=2, column=12, columnspan=2)
tk.Label(control, text = "HV2", font = "Hevetica 20 bold").grid(row=2, column=15,sticky='NS')
#3row
temperature=tk.Entry(control, width=5, font=10, validate='key')
temperature.grid(row=3, column=1)
tk.Label(control, text = u'\N{DEGREE SIGN}C', font = "Times 13").grid(row=3, column=2)
# diameter control
diameter1=tk.Entry(control, width=5, font=10, validate='key')
diameter1.grid(row=3, column=6)
tk.Label(control, text = "mm", font = "Times 13").grid(row=3, column=7)
diameter2=tk.Entry(control, width=5, font=10, validate='key')
diameter2.grid(row=3, column=9)
tk.Label(control, text = "mm", font = "Times 13").grid(row=3, column=10)
diameter3=tk.Entry(control, width=5, font=10, validate='key')
diameter3.grid(row=3, column=12)
tk.Label(control, text = "mm", font = "Times 13").grid(row=3, column=13)
# hv2 control
highvoltage2=tk.Entry(control, width=5, font=10, validate='key')
highvoltage2.grid(row=3, column=15)
tk.Label(control, text = "V", font = "Times 13").grid(row=3, column=16)

#start sop button of control
controlon=tk.Button(control, width=6, height=1, text='ON', font = "Arial 20 bold", command=controlonbutton)
controloff = tk.Button(control, width=6, height=1, text='OFF', font = "Arial 20 bold", command=controloffbutton) 
controlon.grid(row=0, column=21, padx=5)
controloff.grid(row=2, column=21, padx=5)

ttk.Separator(control, orient="vertical").grid(row=0,column=4, rowspan=4, ipady=100, padx=10, pady=10)
ttk.Separator(control, orient="vertical").grid(row=0,column=8, rowspan=4, ipady=100, padx=10, pady=10)
ttk.Separator(control, orient="vertical").grid(row=0,column=11, rowspan=4, ipady=100, padx=10, pady=10)
ttk.Separator(control, orient="vertical").grid(row=0,column=14, rowspan=4, ipady=100, padx=10, pady=10)
ttk.Separator(control, orient="vertical").grid(row=0,column=17, rowspan=4, ipady=100, padx=10, pady=10)
ttk.Separator(control, orient="vertical").grid(row=0,column=20, rowspan=4, ipady=100, padx=10, pady=10)

# camera image of taylor cone
cap = cv2.VideoCapture(0)
# decide the size of image
width= 360
height= 280
# print(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
# print(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
cap.set(cv2.CAP_PROP_FRAME_WIDTH,width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,height)

# frame of visualization
cam = tk.Frame(root, bd=1)
cam.pack(side='bottom')

# measuring the nozzle position using scale
scale = tk.Scale(cam, from_=1, to=height, orient=tk.VERTICAL, length=height)
scale.grid(row=0,column=1, rowspan=3, sticky='N')


video = tk.Label(cam)
video.grid(row=0,column=0, rowspan=4, sticky='N')

ttk.Separator(cam, orient="vertical").grid(row=0,column=3, rowspan=4, ipady=200, padx=10, pady=10)

tk.Label(cam, text = "PID control", font = "Times 20 bold").grid(row=0, column=4, rowspan=2, padx=10, sticky='N')

PIDon=tk.Button(cam, width=6, height=1, text='ON', font = "Arial 20 bold", command=PIDcontrol)
PIDoff = tk.Button(cam, width=6, height=1, text='OFF', font = "Arial 20 bold", command=PIDcontroloff) 
PIDon.grid(row=1, column=4, pady=1, padx=5,sticky='N')
PIDoff.grid(row=2, column=4, padx=5, sticky='N')




def show_frame():
    _, frame = cap.read() #ret : success, frame : get image from video
    
    frame = cv2.flip(frame, 1) # right left change
    
    nozzle_position=scale.get() # get the nozzle position through scale


    # nozzle part
    crop1=frame[0:nozzle_position,0:width] 
    crop_gray = cv2.cvtColor(crop1, cv2.COLOR_BGR2GRAY)
    
    # talor cone part /change rgb and remove the nozzle for edge detection

    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    cv2image[0:nozzle_position,0:width] = 0
    canny = cv2.Canny(cv2image, 150, 200)    

    # taylor cone size 
    edge_position=np.nonzero(canny)
    edge_max=np.max(edge_position[0])
   
    global taylor_height
    taylor_height=edge_max-nozzle_position
         
    # for cam combine the nozzle and taylor cone
    canny[0:nozzle_position,0:width] = crop_gray[:,:]
    
    img = Image.fromarray(canny) 
    imgtk = ImageTk.PhotoImage(image=img)
    video.image = imgtk
    video.configure(image=imgtk)
    global after_id 
    after_id=video.after(100, show_frame)
    

   
def quit():
    """Cancel all scheduled callbacks and quit."""
    video.after_cancel(after_id)
    root.quit()



fig = plt.figure(figsize=(4,3))
fig.set_facecolor('#F0F0F0')
ax = fig.add_subplot(1, 1, 1)
xs = []
ys = []


# This function is called periodically from FuncAnimation
def animate(i, xs, ys):

    # Read temperature (Celsius) from TMP102
    temp_c = round(taylor_height, 2)

    # Add x and y to lists
    xs.append(dt.datetime.now().strftime('%M:%S'))
    ys.append(temp_c)

    # Limit x and y lists to 20 items
    xs = xs[-20:]
    ys = ys[-20:]

    # Draw x and y lists
    ax.clear()
    ax.plot(xs, ys, '--')
    # ax.set_facecolor('grey')
    # Format plot
    # plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(left=0.20)
    plt.title('Taylorcone_height')
    plt.ylabel('height')


canvas = FigureCanvasTkAgg(fig, master=cam)
canvas.get_tk_widget().grid(row=0,column=2, rowspan=4,sticky='N')

ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=200)

pid = PID(1, 0.1, 0.05, setpoint=100)
# Assume we have a system we want to control in controlled_system

pid.output_limits = (0, 10)



root.after(20,show_frame)
root.protocol('WM_DELETE_WINDOW', quit)
root.mainloop()