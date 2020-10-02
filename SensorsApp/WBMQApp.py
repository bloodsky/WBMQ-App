import requests
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
            time.sleep(5)
            data['msg'] = str(random.uniform(25.5, 50.9))
            data['pbrtx'] = False
            
            
            data['id'] = final_id
            
            try: 
                # Happy scenario
             
                r = requests.post('http://localhost:5000/sensor', json=data, timeout=5)
                if final_id =="":
                    final_id = r.json()['id']
                ack = r.json()['msg']

                #self.Console.insert(INSERT, "\n")
                #self.Console.insert(INSERT, ack + "\n")
                time.sleep(5)
            except requests.exceptions.ConnectionError:
                print("Pub: Error requesting backend!")
                #self.Console.insert(INSERT, "\n")
                #self.Console.insert(INSERT, "Error requesting backend!")
            except requests.exceptions.Timeout:

                while ack != "Ack on message : " +  data['msg'] + " on sensorn :" + final_id:
                    
                    try:
                        data['pbrtx'] = True
                        #self.Console.insert(INSERT, "\n BEFORE REQUEST RETRASMIT...\n")
                        r = requests.post('http://localhost:5000/sensor', json=data, timeout=5)
                        if final_id =="":
                            final_id = r.json()['id']

                        ack = r.json()['msg']

                        #self.Console.insert(INSERT, "\n RETRANSMITTING...\n")
                        #self.Console.insert(INSERT, ack + "\n")
                    except requests.exceptions.ConnectionError:
                        print("Pub: Error requesting backend!")
                        #self.Console.insert(INSERT, "\n")
                        #self.Console.insert(INSERT, "Error requesting backend!")
                    except requests.exceptions.Timeout:
                        #self.Console.insert(INSERT, "\n CE STAMO POPO A RIPROVA...\n")
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
        hostname = socket.gethostname()    
        IPAddr = socket.gethostbyname(hostname)
        # Richiedo la sub
        data = {}
        data['id'] = ""
        data['current_sector'] = th_data['e1']
        data['topic'] = th_data['e2']
        data['ipaddr'] = IPAddr
        # gestire try except
        r = requests.post('http://localhost:5000/bot', json=data)
        # Ricevo ACK dal broker
        id = r.json()['id']
        # UI UPDATE
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
      
    def unsubBot(self):

        curItem = self.listBox.focus()
        col1 = self.listBox.item(curItem)['values'][0]
        col2 = self.listBox.item(curItem)['values'][1]
        col3 = self.listBox.item(curItem)['values'][2]
        col4 = self.listBox.item(curItem)['values'][3]

        botID = re.sub('[()]','',col1.split()[0])
        sector = col1.split()[2]
        topic = col4

        data = {}
        data['id'] = botID
        data['current_sector'] = sector
        data['topic'] = topic
        data['ipaddr'] = 'notneeded'

        r = requests.post('http://localhost:5000/unsubscribeBot', json=data)
        # check for ack
        # ...

    def heartBeatCallback(self):
        threading.Timer(6.0, self.heartBeatCallback).start()
        try:
            # substitute http://wbmqsystem-dev.us-east-2.elasticbeanstalk.com with http://localhost:5000 to work in localhost
            r = requests.get('http://localhost:5000/status')
            if r.json()['status'] == "alivectx":
                context = 1
                self.my_string_var.set("System is running\nin context-aware mode!")
            elif r.json()['status'] == "alive":
                self.my_string_var.set("System is running\nwithout context!")
            self.limg.configure(image=self.working)
            self.limg.image =self.working
            #master.after(6000, heartBeatCallback)
        except requests.exceptions.ConnectionError:
            self.my_string_var.set("System is down!")
            self.limg.configure(image=self.stopped)
            self.limg.image = self.stopped
            #master.after(6000, heartBeatCallback)

    def save(self):
        pass

    def main_form(self):

        self.root = Tk()
        
        self.e2_bot = ''
        self.e1_bot = ''
        self.e1_sens = ''
        self.e2_sens = ''
        # for random spawn and unsub
        self.topics = ['Humidity','Motion','Temperature']
        self.sectors = ['A1','A2','B1','B2','B3','C1','C2','D1','D2','D3']

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
        wrapper3 = LabelFrame(self.root, text="Bots operation")
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
        wrapper3.pack(side=BOTTOM, fill="both", expand="no", padx=0, pady=0)
        wrapper4.pack(side=BOTTOM, fill="both", expand="yes", padx=0, pady=0)
        wrapper2.pack(side=TOP, fill="both", expand="no", padx=0, pady=0)

        cols = ('Bot', 'Received value', 'Sensor', 'Topic')
        self.listBox = ttk.Treeview(myframe, columns=cols, show='headings', height=35)
        # set column headings
        for col in cols:
            self.listBox.heading(col, text=col)    
        #listBox.grid(row=1, column=0, columnspan=2)
        self.listBox.pack()

        B = Button(wrapper3, text="Subscribe a new bot", command=self.botsub_thread, width=25).pack()
        B3 = Button(wrapper3, text="Subscribe random bots", command=self.spawnRandomBots_thread, width=25).pack()
        
        # Lo facciamo con il doppio click sulla row della tabella?
        # se vogliamo provare il bottone bisogna rimuovere da botunsub_thread paramentro a
        Bremove = Button(wrapper3, text="Unsubscribe bot", command=self.botunsub_thread, width=25).pack()
        # Questo è per il doppio click!
        self.listBox.bind('<ButtonRelease-1>', self.botunsub_thread)
            
        B4 = Button(wrapper2, text="Publish a new value", command=self.sensorpub_thread, width=25).pack()
        B5 = Button(wrapper2, text="Publish random values", command=self.spawnRandomSensor_thread, width=25).pack()
        
        # Servono?
        #B45 = Button(wrapper3, text="Kill single bot", command=killSingleBot, width=25).pack()
        #B46 = Button(wrapper3, text="Kill random bots", command=killRandomBot, width=25).pack()
        #Bkill = Button(wrapper2, text="Kill single sensor", command=killSingleSensor, width=25).pack()
        #Bkillrand = Button(wrapper2, text="Kill random sensors", command=killRandomSensor, width=25).pack()

        # Figo da implementare switch context a runtime? 
        #B21 = Button(wrapper4, text="Context switch (?)", command=switchCallBack, width=25).pack()

        self.my_string_var = StringVar(value="Checking system status ...")

        # nabbata ---------------------------
        space = Label(wrapper4, text="")
        space.pack()
        space1 = Label(wrapper4, text="")
        space1.pack()
        space2 = Label(wrapper4, text="")
        space2.pack()
        # fine nabbata -----------------------

        self.limg = Label(wrapper4, image=self.load)
        self.limg.pack()
        my_label = Label(wrapper4, textvariable=self.my_string_var)
        my_label.pack()

        executor = ThreadPoolExecutor(50)
        future = executor.submit(self.task, ("Completed"))
        
        self.heartbeat_thread()
        self.root.update()
        self.root.mainloop()

    def task(self, message):
       app = Flask(__name__)
       hostname = socket.gethostname()    
       IPAddr = socket.gethostbyname(hostname)
       
       @app.route("/", methods = ['POST'])
       def wait_for_message():

            data = request.get_json()
            msg = data.get('msg', '')
            botId = data.get('botId', '')
            bot_cs = data.get('bot_cs', '')
            sensor = data.get('sensor', '')
            sensor_cs = data.get('sensor_cs', '')
           
            # UI UPDATE
            children = self.listBox.get_children('')
            for child in children:
                values = self.listBox.item(child, 'values')
                if values[0] == "["+botId+"]"+" in "+bot_cs:
                    self.listBox.set(child, column="Received value", value=msg)
                    self.listBox.set(child, column="Sensor", value="["+sensor+"]"+" in "+sensor_cs)
                    break

            data = {'id': botId,'message': msg}
            return jsonify(data)
                 
       app.run(debug=True, use_reloader=False, host=IPAddr, port=5001)
       

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

    def botunsub_thread(self,a):
        maincal = threading.Thread(target=self.unsubBot)
        maincal.start()
    
    def botsub_thread(self):
        maincal = threading.Thread(target=self.spawnBotCallBack)
        maincal.start()

    def sensorpub_thread(self):
        maincal = threading.Thread(target=self.spawnSensorCallBack)
        maincal.start()

    def heartbeat_thread(self):
        maincal = threading.Thread(target=self.heartBeatCallback)
        maincal.start()

co = class_one()
mainfz = threading.Thread(target=co.main_form)
mainfz.start() 