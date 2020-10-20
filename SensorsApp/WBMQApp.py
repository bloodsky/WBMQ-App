import requests 
from requests import get
import time
from flask import Flask
from flask import jsonify
from flask import request
import random
import threading
from functools import partial
from tkinter import *
import socket
from tkinter import ttk
from tkinter import messagebox
import re
import struct
from concurrent.futures import ThreadPoolExecutor


class class_one:

    def runBackground(self, th_data): 
        first_request = True
        final_id = ""
        
        data = {}
        data['current_sector'] = th_data['e1']
        data['type'] = th_data['e2']
        ack = ""
        while True:    
            
            sleep_simulation = random.choices(self.times_sensor, self.prob_sensor)
            time.sleep(sleep_simulation[0])

            data['msg'] = str(round(random.uniform(25.5, 50.9),4))
            data['pbrtx'] = False
            
            
            data['id'] = final_id
            
            try: 
                # Happy scenario
             
                r = requests.post('http://'+self.remoteaddr+'/sensor', json=data, timeout=5)
                if final_id =="":
                    final_id = r.json()['id']
                ack = r.json()['msg']


            except requests.exceptions.ConnectionError:
                print("Pub: Error requesting backend!")

            except requests.exceptions.Timeout:

                while ack != "Ack on message : " +  data['msg'] + " on sensorn :" + final_id:
                    
                    try:
                        data['pbrtx'] = True
                        r = requests.post('http://'+self.remoteaddr+'/sensor', json=data, timeout=5)
                        if final_id =="":
                            final_id = r.json()['id']

                        ack = r.json()['msg']

                    except requests.exceptions.ConnectionError:
                        print("Pub: Error requesting backend!")

                    except requests.exceptions.Timeout:
                        continue

    def sel_sens(self):
        self.e2_sens = str(self.var_sens.get())
    def sel_sens2(self):
        self.e1_sens = str(self.var_sens2.get())

    def spawnsensor(self, newWin):
        if self.e1_sens != '' and self.e2_sens != '':
            th_data = {}
            th_data['e1'] = self.e1_sens
            th_data['e2'] = self.e2_sens
            if newWin != None:
                newWin.destroy()
            maincal = threading.Thread(target=self.runBackground, args=(th_data,))
            maincal.start()
        else:
            messagebox.showerror("Error!","You must select both sector and topic!")

    def spawnSensorCallBack(self):
        newWindow = Toplevel(self.root)
        newWindow.title("Spawing sensor")

        x_cor = int((self.screen_width / 2) - (236 / 2))
        y_cor = int((self.screen_height / 2) - (67 / 2))

        newWindow.geometry("{}x{}+{}+{}".format(286, 180, x_cor, y_cor))

        self.var_sens2 = StringVar(value="1")
        Label(newWindow, text="Choose sector:").grid(row=0, column=0)
        R1_sector = Radiobutton(newWindow, text="A1", variable=self.var_sens2, value="A1",command=self.sel_sens2)
        R1_sector.grid(row=1, column=0)
        
        R2_sector = Radiobutton(newWindow, text="A2", variable=self.var_sens2, value="A2",command=self.sel_sens2)
        R2_sector.grid(row=2, column=0)
        
        R3_sector = Radiobutton(newWindow, text="B1", variable=self.var_sens2, value="B1",command=self.sel_sens2)
        R3_sector.grid(row=3, column=0)

        R4_sector = Radiobutton(newWindow, text="B2", variable=self.var_sens2, value="B2",command=self.sel_sens2)
        R4_sector.grid(row=4, column=0)

        R5_sector = Radiobutton(newWindow, text="B3", variable=self.var_sens2, value="B3",command=self.sel_sens2)
        R5_sector.grid(row=5, column=0)

        R6_sector = Radiobutton(newWindow, text="C1", variable=self.var_sens2, value="C1",command=self.sel_sens2)
        R6_sector.grid(row=1, column=1)

        R7_sector = Radiobutton(newWindow, text="C2", variable=self.var_sens2, value="C2",command=self.sel_sens2)
        R7_sector.grid(row=2, column=1)

        R8_sector = Radiobutton(newWindow, text="D1", variable=self.var_sens2, value="D1",command=self.sel_sens2)
        R8_sector.grid(row=3, column=1)

        R9_sector = Radiobutton(newWindow, text="D2", variable=self.var_sens2, value="D2",command=self.sel_sens2)
        R9_sector.grid(row=4, column=1)

        R10_sector = Radiobutton(newWindow, text="D3", variable=self.var_sens2, value="D3",command=self.sel_sens2)
        R10_sector.grid(row=5, column=1)

        
        Label(newWindow, text="Choose topic:").grid(row=0, column=4)
        newWindow.grid_columnconfigure(3, minsize=50)
        
        self.var_sens = StringVar(value="1")
        R1_topic = Radiobutton(newWindow, text="Humidity", variable=self.var_sens, value="Humidity",command=self.sel_sens)
        R1_topic.grid(row=1, column=4,sticky="w")

        R2_topic = Radiobutton(newWindow, text="Motion", variable=self.var_sens, value="Motion",command=self.sel_sens)
        R2_topic.grid(row=2, column=4,sticky="w")

        R3_topic = Radiobutton(newWindow, text="Temperature", variable=self.var_sens, value="Temperature",command=self.sel_sens)
        R3_topic.grid(row=3, column=4,sticky="w")

        action_with_arg = partial(self.spawnsensor, newWindow)
        B7 = Button(newWindow, text="Spawn", command=action_with_arg, width=7).grid(row=7, column=3)


    def bot_task_Background(self, th_data):

        ip = get('https://api.ipify.org').text
        # Richiedo la sub
        data = {}
        if 'id' in th_data:
            data['id'] = th_data['id']
        else:
            data['id'] = ""

        data['current_sector'] = th_data['e1']
        data['topic'] = th_data['e2']
        data['ipaddr'] = ip
        # gestire try except
        r = requests.post('http://'+self.remoteaddr+'/bot', json=data)
        # Ricevo ACK dal broker
        id = r.json()['id']
        # UI UPDATE
        children = self.listBox.get_children('')
        if 'id' in th_data:
            for child in children:
                values = self.listBox.item(child, 'values')
                if values[0] == "["+th_data['id']+"]"+" in "+th_data['e1'] and values[1] == "unsubbed" and values[2] == " ... ":                 
                    self.listBox.set(child, column="#2", value="waiting")
                    self.listBox.set(child, column="#3", value="waiting")
                    break
        else:
            self.listBox.insert("", "end", values=("["+id+"]"+" in "+data['current_sector'], "waiting", "waiting",data['topic']))

    def spawnbot(self, newWin):
        if self.e1_bot != '' and self.e2_bot != '':
            th_data = {}
            th_data['e1'] = self.e1_bot
            th_data['e2'] = self.e2_bot
            if newWin != None:
                newWin.destroy()
            maincal = threading.Thread(target=self.bot_task_Background, args=(th_data,))
            maincal.start()
        else:
            messagebox.showerror("Error!","You must select both sector and topic!")

    def sel(self):
        self.e2_bot = str(self.var.get())
    def sel2(self):
        self.e1_bot = str(self.var2.get())

    def spawnBotCallBack(self):
        newWindow = Toplevel(self.root)
        newWindow.title("Spawing bot")

        x_cor = int((self.screen_width / 2) - (236 / 2))
        y_cor = int((self.screen_height / 2) - (67 / 2))

        newWindow.geometry("{}x{}+{}+{}".format(286, 180, x_cor, y_cor))

        self.var2 = StringVar(value="1")
        Label(newWindow, text="Choose sector:").grid(row=0, column=0)

        R1_sector= Radiobutton(newWindow, text="A1", variable=self.var2, value="A1",command=self.sel2)

        R1_sector.grid(row=1, column=0)
        
        R2_sector = Radiobutton(newWindow, text="A2", variable=self.var2, value="A2",command=self.sel2)

        R2_sector.grid(row=2, column=0)
        
        R3_sector = Radiobutton(newWindow, text="B1", variable=self.var2, value="B1",command=self.sel2)

        R3_sector.grid(row=3, column=0)

        R4_sector = Radiobutton(newWindow, text="B2", variable=self.var2, value="B2",command=self.sel2)

        R4_sector.grid(row=4, column=0)

        R5_sector = Radiobutton(newWindow, text="B3", variable=self.var2, value="B3",command=self.sel2)

        R5_sector.grid(row=5, column=0)

        R6_sector = Radiobutton(newWindow, text="C1", variable=self.var2, value="C1",command=self.sel2)

        R6_sector.grid(row=1, column=1)

        R7_sector = Radiobutton(newWindow, text="C2", variable=self.var2, value="C2",command=self.sel2)

        R7_sector.grid(row=2, column=1)

        R8_sector = Radiobutton(newWindow, text="D1", variable=self.var2, value="D1",command=self.sel2)

        R8_sector.grid(row=3, column=1)

        R9_sector = Radiobutton(newWindow, text="D2", variable=self.var2, value="D2",command=self.sel2)

        R9_sector.grid(row=4, column=1)

        R10_sector = Radiobutton(newWindow, text="D3", variable=self.var2, value="D3",command=self.sel2)

        R10_sector.grid(row=5, column=1)

        Label(newWindow, text="Choose topic:").grid(row=0, column=4)
        newWindow.grid_columnconfigure(3, minsize=50)
        self.var = StringVar(value="1")

        R1_topic = Radiobutton(newWindow, text="Humidity", variable=self.var, value="Humidity",command=self.sel)

        R1_topic.grid(row=1, column=4,sticky="w")

        R2_topic = Radiobutton(newWindow, text="Motion", variable=self.var, value="Motion",command=self.sel)

        R2_topic.grid(row=2, column=4,sticky="w")

        R3_topic = Radiobutton(newWindow, text="Temperature", variable=self.var, value="Temperature",command=self.sel)

        R3_topic.grid(row=3, column=4,sticky="w")

        action_with_arg = partial(self.spawnbot, newWindow)
        B2 = Button(newWindow, text="Spawn", command=action_with_arg, width=7).grid(row=7, column=3)
    

    def resubBot(self):
        
        curItem = self.listBox.focus()
        if len(self.listBox.item(curItem)['values']) == 0:
            messagebox.showerror("Error!","You must select a row first!")
        else:
            col1 = self.listBox.item(curItem)['values'][0]
            col2 = self.listBox.item(curItem)['values'][1]
            col3 = self.listBox.item(curItem)['values'][2]
            col4 = self.listBox.item(curItem)['values'][3]

            unsubbed = col2
            threep = col3
            if unsubbed == "unsubbed" and threep == " ... ":
                botID = col1.split()[0].replace('[','').replace(']','')
                sector = col1.split()[2]
                topic = col4
        
                th_data = {}
                th_data['id'] = botID
                th_data['e1'] = sector
                th_data['e2'] = topic
                maincal = threading.Thread(target=self.bot_task_Background, args=(th_data,))
                maincal.start()
            else:
                messagebox.showerror("Error!","You must select an unsubbed bot!")

    def unsubBot(self):
        
        curItem = self.listBox.focus()
        if len(self.listBox.item(curItem)['values']) == 0:
            messagebox.showerror("Error!","You must select a row first!")
        else:
            col1 = self.listBox.item(curItem)['values'][0]
            col2 = self.listBox.item(curItem)['values'][1]
            col3 = self.listBox.item(curItem)['values'][2]
            col4 = self.listBox.item(curItem)['values'][3]

            botID = col1.split()[0].replace('[','').replace(']','')
            sector = col1.split()[2]
            topic = col4
            
            if col2 == "unsubbed" and col3 == " ... ":
                messagebox.showerror("Error!","Cannot unsub and unsubbed bot!")
            else:
                data = {}
                data['id'] = botID
                data['current_sector'] = sector
                data['topic'] = topic
                data['ipaddr'] = 'notneeded'
    

                r = requests.post('http://'+self.remoteaddr+'/unsubscribeBot', json=data)
                if r.json()['id'] == "null" and r.json()['current_sector'] == "null" and r.json()['topic'] == "null" and r.json()['ipaddr'] == "null":
                    # UI UPDATE
                    children = self.listBox.get_children('')
                    for child in children:
                        values = self.listBox.item(child, 'values')
                        if values[0] == "["+botID+"]"+" in "+sector:
                            subchildren = self.listBox.get_children(child)
                            self.listBox.set(child, column="#2", value="unsubbed")
                            self.listBox.set(child, column="#3", value=" ... ")                   
                            if len(subchildren) != 0:
                                for subchild in subchildren:
                                    self.listBox.delete(subchild)
                            break                      


    def heartBeatCallback(self):
        threading.Timer(6.0, self.heartBeatCallback).start()
        try:
            
            r = requests.get('http://'+self.remoteaddr+'/status')
            if r.json()['status'] == "alivectx":
                context = 1
                self.my_string_var.set("System is running\nin context-aware mode")
            elif r.json()['status'] == "alive":
                self.my_string_var.set("System is running\nwithout context")
            self.limg.configure(image=self.working)
            self.limg.image =self.working
            #self.totbot  = r.json()['totbot']
            #self.totsens = r.json()['totsens']

        except requests.exceptions.ConnectionError:
            self.my_string_var.set("System is down!")
            self.limg.configure(image=self.stopped)
            self.limg.image = self.stopped
            #self.totbot = "Error retriving data!"
            #self.totsens= "Error retriving data!"

    def save(self):
        pass

    def save_values_bot(self, hard_num, nw):
        prev = self.hardness_bot
        self.hardness_bot = hard_num.get()
        self.canvas_bot.move(self.location_bot, -(prev-self.hardness_bot), 0)
        hardness_bot_internal = self.hardness_bot / 10
        
        if hardness_bot_internal >= 4.8 and hardness_bot_internal <= 5.2:
            self.prob_bot = [0.1, 0.69, 0.2, 0.01]
        elif hardness_bot_internal < 4.8 and hardness_bot_internal >= 3.8:
            self.prob_bot = [0.29, 0.6, 0.1, 0.01]
        elif hardness_bot_internal < 3.8 and hardness_bot_internal >= 2.8:
            self.prob_bot = [0.39, 0.5, 0.1, 0.01]
        elif hardness_bot_internal < 2.8 and hardness_bot_internal >= 1.8:
            self.prob_bot = [0.67, 0.319, 0.01, 0.001]
        elif hardness_bot_internal < 1.8 and hardness_bot_internal >= 0.8:
            self.prob_bot = [0.8, 0.19, 0.009, 0.001]
        elif hardness_bot_internal < 0.8 and hardness_bot_internal >= 0.1:
            self.prob_bot = [0.999, 0.0001, 0.0005, 0.0004]
        elif hardness_bot_internal > 5.2 and hardness_bot_internal <= 6.2:
            self.prob_bot = [0.01, 0.59, 0.38, 0.02]
        elif hardness_bot_internal > 6.2 and hardness_bot_internal <= 7.2:
            self.prob_bot = [0.01, 0.5, 0.46, 0.03]
        elif hardness_bot_internal > 7.2 and hardness_bot_internal <= 8.2:
            self.prob_bot = [0.001, 0.3, 0.499, 0.2]
        elif hardness_bot_internal > 8.2 and hardness_bot_internal <= 9.2:
            self.prob_bot = [0.0001, 0.003, 0.3469, 0.65]
        elif hardness_bot_internal > 9.2 and hardness_bot_internal <= 9.9:
            self.prob_bot = [0.0004, 0.0005, 0.0001, 0.999]

        nw.destroy()
        print(self.prob_bot)
        

    def save_values_sensor(self, hard_num, nw):
        prev = self.hardness_sensor
        self.hardness_sensor = hard_num.get()
        self.canvas_sens.move(self.location_sens, -(prev-self.hardness_sensor), 0)
        hardness_sensor_internal = self.hardness_sensor / 10
        
        if hardness_sensor_internal >= 4.8 and hardness_sensor_internal <= 5.2:
            self.prob_sensor = [0.1, 0.69, 0.2, 0.01]
        elif hardness_sensor_internal < 4.8 and hardness_sensor_internal >= 3.8:
            self.prob_sensor = [0.29, 0.6, 0.1, 0.01]
        elif hardness_sensor_internal < 3.8 and hardness_sensor_internal >= 2.8:
            self.prob_sensor = [0.39, 0.5, 0.1, 0.01]
        elif hardness_sensor_internal < 2.8 and hardness_sensor_internal >= 1.8:
            self.prob_sensor = [0.67, 0.319, 0.01, 0.001]
        elif hardness_sensor_internal < 1.8 and hardness_sensor_internal >= 0.8:
            self.prob_sensor = [0.8, 0.19, 0.009, 0.001]
        elif hardness_sensor_internal < 0.8 and hardness_sensor_internal >= 0.1:
            self.prob_sensor = [0.999, 0.0001, 0.0005, 0.0004]
        elif hardness_sensor_internal > 5.2 and hardness_sensor_internal <= 6.2:
            self.prob_sensor = [0.01, 0.59, 0.38, 0.02]
        elif hardness_sensor_internal > 6.2 and hardness_sensor_internal <= 7.2:
            self.prob_sensor = [0.01, 0.5, 0.46, 0.03]
        elif hardness_sensor_internal > 7.2 and hardness_sensor_internal <= 8.2:
            self.prob_sensor = [0.001, 0.3, 0.499, 0.2]
        elif hardness_sensor_internal > 8.2 and hardness_sensor_internal <= 9.2:
            self.prob_sensor = [0.0001, 0.003, 0.3469, 0.65]
        elif hardness_sensor_internal > 9.2 and hardness_sensor_internal <= 9.9:
            self.prob_sensor = [0.0004, 0.0005, 0.0001, 0.999]

        nw.destroy()
        print(self.prob_sensor)

    def killSingleBot(self):
        
        newWindow = Toplevel(self.root)
        newWindow.title("Bot death frequencies")
        x_cor = int((self.screen_width / 2) - (236 / 2))
        y_cor = int((self.screen_height / 2) - (67 / 2))
        newWindow.geometry("{}x{}+{}+{}".format(334, 170, x_cor, y_cor))
        newWindow.resizable(False, False)

        w = Scale(newWindow ,from_=1, to=99, orient=HORIZONTAL, length=276)
        w.set(50)
        w.pack()
        
        canvas = Canvas(newWindow)
        canvas.create_rectangle(30, 30, 120, 55,
            outline="#000000", fill="#17F71E")
        canvas.create_rectangle(121, 30, 211, 55,
            outline="#000000", fill="#F7E317")
        canvas.create_rectangle(212, 30, 302, 55,
            outline="#000000", fill="#F71717")
        canvas.pack()

        action_with_arg = partial(self.save_values_bot, w, newWindow)
        Button(newWindow, text='Set', width='10', command=action_with_arg).place(x=127,y=133)

    def killSingleSensor(self):

        newWindow = Toplevel(self.root)
        newWindow.title("Sensor death frequencies")
        x_cor = int((self.screen_width / 2) - (236 / 2))
        y_cor = int((self.screen_height / 2) - (67 / 2))
        newWindow.geometry("{}x{}+{}+{}".format(334, 170, x_cor, y_cor))
        newWindow.resizable(False, False)

        w = Scale(newWindow ,from_=1, to=99, orient=HORIZONTAL, length=276)
        w.set(50)
        w.pack()
        
        canvas = Canvas(newWindow)
        canvas.create_rectangle(30, 30, 120, 55,
            outline="#000000", fill="#17F71E")
        canvas.create_rectangle(121, 30, 211, 55,
            outline="#000000", fill="#F7E317")
        canvas.create_rectangle(212, 30, 302, 55,
            outline="#000000", fill="#F71717")
        canvas.pack()

        action_with_arg = partial(self.save_values_sensor, w, newWindow)
        Button(newWindow, text='Set', width='10', command=action_with_arg).place(x=127,y=133)

    def main_form(self):

        self.root = Tk()
        
        self.root.wm_title("WBMQ Controller Application")
        self.root.call('wm', 'iconphoto', self.root._w, PhotoImage(file='ic_controller.png'))

        self.e2_bot = ''
        self.e1_bot = ''
        self.e1_sens = ''
        self.e2_sens = ''
        # for random spawn and unsub
        self.topics = ['Humidity','Motion','Temperature']
        self.sectors = ['A1','A2','B1','B2','B3','C1','C2','D1','D2','D3']
        # for timing
        self.hardness_bot = 50
        self.hardness_sensor = 50

        #localhost:5000
        self.remoteaddr = 'wbmqsystemproject-dev.us-east-2.elasticbeanstalk.com'

        self.times_bot =    [0  ,    1,   5,   60]
        self.prob_bot  =    [0.1, 0.69, 0.2, 0.01]

        self.times_sensor = [0  ,    1,   5,   60]
        self.prob_sensor  = [0.1, 0.69, 0.2, 0.01]


        self.root.resizable(False, False)
        self.window_height = 600
        self.window_width = 1020

        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        self.x_cordinate = int((self.screen_width / 2) - (self.window_width / 2))
        self.y_cordinate = int((self.screen_height / 2) - (self.window_height / 2))

        self.load = PhotoImage(file="timer.png").subsample(10, 10)
        self.working = PhotoImage(file="reverse-engineering.png").subsample(8, 8)
        self.stopped = PhotoImage(file="futuristic.png").subsample(8, 8)

        self.root.geometry("{}x{}+{}+{}".format(self.window_width, self.window_height, self.x_cordinate, self.y_cordinate))

        wrapper1 = LabelFrame(self.root, text="Console")
        wrapper2 = LabelFrame(self.root, text="Sensors operation")
        self.wrapper3 = LabelFrame(self.root, text="Bots operation")
        wrapper4 = LabelFrame(self.root, text="System status")

        mycanv = Canvas(wrapper1)
        mycanv.pack(side=LEFT, fill="both", expand="yes")

        yscrollbar = Scrollbar(wrapper1, orient="vertical", command=mycanv.yview)
        yscrollbar.pack(side=RIGHT, fill="y")

        mycanv.configure(yscrollcommand=yscrollbar.set)
        mycanv.bind('<Configure>', lambda e: mycanv.configure(scrollregion=mycanv.bbox('all')))

        myframe = Frame(mycanv)
        mycanv.create_window((0, 0), window=myframe, anchor="nw")

        wrapper1.pack(side=RIGHT, fill="both", expand="yes", padx=0, pady=0)
        self.wrapper3.pack(side=BOTTOM, fill="both", expand="no", padx=0, pady=0)
        wrapper4.pack(side=BOTTOM, fill="both", expand="yes", padx=0, pady=0)
        wrapper2.pack(side=TOP, fill="both", expand="no", padx=0, pady=0)


        cols = ('#1','#2','#3','#4')
        
        def fixed_map(option):
        # Fix for setting text colour for Tkinter 8.6.9
        # From: https://core.tcl.tk/tk/info/509cafafae
        #
        # Returns the style map for 'option' with any styles starting with
        # ('!disabled', '!selected', ...) filtered out.

        # style.map() returns an empty list for missing options, so this
        # should be future-safe.
            return [elm for elm in style.map('Treeview', query_opt=option) if
                elm[:2] != ('!disabled', '!selected')]

        
        style = ttk.Style()
        style.map('Treeview', foreground=fixed_map('foreground'), background=fixed_map('background'))
        self.listBox = ttk.Treeview(myframe,height=35)
        self.listBox['columns'] = cols

        self.listBox.column('#0', width=5, anchor='center')
        self.listBox.column('#1', width=200)
        self.listBox.column('#2', width=200, anchor='center')
        self.listBox.column('#3', width=200)
        self.listBox.column('#4', width=200, anchor='center')

        self.listBox.heading('#0', text='+')
        self.listBox.heading('#1', text='Bot')
        self.listBox.heading('#2', text='Received value')
        self.listBox.heading('#3', text='Sensor')
        self.listBox.heading('#4', text='Topic')
        
        self.listBox.pack()


        B = Button(self.wrapper3, text="Subscribe a new bot", command=self.botsub_thread, width=25).pack()
        B3 = Button(self.wrapper3, text="Subscribe random bots", command=self.spawnRandomBots_thread, width=25).pack()
        
            
        B4 = Button(wrapper2, text="Publish a new value", command=self.sensorpub_thread, width=25).pack()
        B5 = Button(wrapper2, text="Publish random values", command=self.spawnRandomSensor_thread, width=25).pack()
        
        Bremove = Button(self.wrapper3, text="Unsubscribe bot", command=self.botunsub_thread, width=25).pack()
        Bresub = Button(self.wrapper3, text="Resubscribe bot", command=self.botresub_thread, width=25).pack()

        B45 = Button(self.wrapper3, text="Bot killing frequencies", command=self.killbot_thread, width=25).pack()
        Bkill = Button(wrapper2, text="Sensor killing frequencies", command=self.killsensor_thread, width=25).pack()

        #B455 = Button(wrapper2, text="Draw up report", command=self.killbot_thread, width=25).pack()

        self.my_string_var = StringVar(value="Checking system status ...")
        self.totbot = StringVar(value="0")
        self.totsens = StringVar(value="0")

        space4 = Label(wrapper4, text="")
        space4.pack()
        space5 = Label(wrapper4, text="")
        space5.pack()

        self.limg = Label(wrapper4, image=self.load)
        self.limg.pack()
        my_label = Label(wrapper4, textvariable=self.my_string_var)
        my_label.pack()

        space3 = Label(wrapper4, text="")
        space3.pack()


        ph_ok_sens = PhotoImage(file = 'ok.png').subsample(30, 30)
        self.canvas_sens = Canvas(wrapper4, width=154, height=57)
        self.canvas_sens .create_rectangle(2, 40, 52, 55,
            outline="#000000", fill="#17F71E")
        self.canvas_sens .create_rectangle(53, 40, 103, 55,
            outline="#000000", fill="#F7E317")
        self.canvas_sens .create_rectangle(104, 40, 154, 55,
            outline="#000000", fill="#F71717")
        self.canvas_sens .pack(anchor=CENTER)
        infos = Label(wrapper4, text="Sensor death frequency")
        infos.pack()
        self.location_sens = self.canvas_sens.create_image(self.hardness_sensor+28,48, image=ph_ok_sens)

        ph_ok_bot = ph_ok_sens
        self.canvas_bot = Canvas(wrapper4, width=154, height=60)
        self.canvas_bot .create_rectangle(2, 40, 52, 55,
            outline="#000000", fill="#17F71E")
        self.canvas_bot .create_rectangle(53, 40, 103, 55,
            outline="#000000", fill="#F7E317")
        self.canvas_bot .create_rectangle(104, 40, 154, 55,
            outline="#000000", fill="#F71717")
        self.canvas_bot .pack(anchor=CENTER)
        infob = Label(wrapper4, text="Bot death frequency")
        infob.pack(anchor=CENTER)
        self.location_bot = self.canvas_bot.create_image(self.hardness_sensor+28,48, image=ph_ok_sens)

        executor = ThreadPoolExecutor(50)
        future = executor.submit(self.task, ("Completed"))
        
        self.heartbeat_thread()
        self.root.update()
        self.root.mainloop()

    def get_ip_address(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]

    def task(self, message):
        app = Flask(__name__)
       
        @app.route("/", methods = ['POST'])
        def wait_for_message():

            sleep_simulation = random.choices(self.times_bot, self.prob_bot)
            time.sleep(sleep_simulation[0])

            data = request.get_json()
            msg = data.get('msg', '')
            botId = data.get('botId', '')
            bot_cs = data.get('bot_cs', '')
            sensor = data.get('sensor', '')
            sensor_cs = data.get('sensor_cs', '')
            topic = data.get('topic', '')

            print(botId+" "+bot_cs+" "+sensor+" "+sensor_cs+" "+topic)           
            # UI UPDATE
            children = self.listBox.get_children('')
            for child in children:
                values = self.listBox.item(child, 'values')
                if values[0] == "["+botId+"]"+" in "+bot_cs and values[2] == "["+sensor+"]"+" in "+sensor_cs:                 
                    self.listBox.set(child, column="#2", value=msg)
                    break
                elif values[0] == "["+botId+"]"+" in "+bot_cs and values[2].startswith("[") and values[2] != "["+sensor+"]"+" in "+sensor_cs:
                    subchildren = self.listBox.get_children(child)
                    if len(subchildren) == 0:
                        self.listBox.insert(child, "end",values=("["+botId+"]"+" in "+bot_cs, msg, "["+sensor+"]"+" in "+sensor_cs, topic),tags = ('subrow',))
                        self.listBox.tag_configure('subrow', background='#EFF0F0')
                        break
                    else:
                        found = False;
                        for subchild in subchildren:
                            subvalue = self.listBox.item(subchild, 'values')

                            if subvalue[0] == "["+botId+"]"+" in "+bot_cs and subvalue[2] == "["+sensor+"]"+" in "+sensor_cs:
                                self.listBox.set(subchild, column="#2", value=msg)
                                found = True
                                break

                        if (not found):
                            self.listBox.insert(child, "end",values=("["+botId+"]"+" in "+bot_cs, msg, "["+sensor+"]"+" in "+sensor_cs, topic),tags = ('subrow',))
                            self.listBox.tag_configure('subrow', background='#EFF0F0')
                        break
                elif values[0] == "["+botId+"]"+" in "+bot_cs and values[2] == "waiting":
                    self.listBox.set(child, column="#2", value=msg)
                    self.listBox.set(child, column="#3", value="["+sensor+"]"+" in "+sensor_cs)
                    break
                

            # ACK
            data = {'id': botId,'message': msg}
            return jsonify(data)
                 
        app.run(debug=True, use_reloader=False, host=self.get_ip_address(), port=5001)
       

    def spawnRandomSensor_thread(self):
        # non random per adesso.
        for _ in range(5):
            self.e1_sens = random.choice(self.sectors)
            self.e2_sens = random.choice(self.topics)
            maincal = threading.Thread(target=self.spawnsensor(None))
            maincal.start()

    def spawnRandomBots_thread(self):
        # non random per adesso.
        for _ in range(5):
            self.e1_bot = random.choice(self.sectors) 
            self.e2_bot = random.choice(self.topics)
            maincal = threading.Thread(target=self.spawnbot(None))
            maincal.start()

    def botresub_thread(self):
        maincal = threading.Thread(target=self.resubBot)
        maincal.start()
    
    def botunsub_thread(self):
        maincal = threading.Thread(target=self.unsubBot)
        maincal.start()
    
    def botsub_thread(self):
        maincal = threading.Thread(target=self.spawnBotCallBack)
        maincal.start()

    def sensorpub_thread(self):
        maincal = threading.Thread(target=self.spawnSensorCallBack)
        maincal.start()

    def killbot_thread(self):
        maincal = threading.Thread(target=self.killSingleBot)
        maincal.start()

    def killsensor_thread(self):
        maincal = threading.Thread(target=self.killSingleSensor)
        maincal.start()

    def heartbeat_thread(self):
        maincal = threading.Thread(target=self.heartBeatCallback)
        maincal.start()

co = class_one()
mainfz = threading.Thread(target=co.main_form)
mainfz.start() 