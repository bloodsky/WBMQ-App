import requests
import time
from flask import Flask
import random
import threading
from functools import partial
from tkinter import *


class class_one:

    def runBackground(self, th_data): 
        first_request = True
        final_id = ""
        
        data = {}
        data['current_sector'] = th_data['e1']
        data['type'] = th_data['e2']
        ack = ""
        while True:    
            
            data['msg'] = str(random.uniform(25.5, 50.9))
            data['pbrtx'] = False
            
            
            data['id'] = final_id
            
            try: 
                # Happy scenario
                self.Console.insert(INSERT, "\n BEFORE REQUEST...\n")
                r = requests.post('http://localhost:5000/sensor', json=data, timeout=5)
                if final_id =="":
                    final_id = r.json()['id']
                ack = r.json()['msg']

                self.Console.insert(INSERT, "\n")
                self.Console.insert(INSERT, ack + "\n")
                time.sleep(5)
            except requests.exceptions.ConnectionError:
                self.Console.insert(INSERT, "\n")
                self.Console.insert(INSERT, "Error requesting backend!")
            except requests.exceptions.Timeout:

                while ack != "Ack on message : " +  data['msg'] + " on sensorn :" + final_id:
                    
                    try:
                        data['pbrtx'] = True
                        self.Console.insert(INSERT, "\n BEFORE REQUEST RETRASMIT...\n")
                        r = requests.post('http://localhost:5000/sensor', json=data, timeout=5)
                        if final_id =="":
                            final_id = r.json()['id']

                        ack = r.json()['msg']

                        self.Console.insert(INSERT, "\n RETRANSMITTING...\n")
                        self.Console.insert(INSERT, ack + "\n")
                    except requests.exceptions.ConnectionError:
                        self.Console.insert(INSERT, "\n")
                        self.Console.insert(INSERT, "Error requesting backend!")
                    except requests.exceptions.Timeout:
                        self.Console.insert(INSERT, "\n CE STAMO POPO A RIPROVA...\n")
                        continue



    def spawnsensor(self,e1, e2, newWin):
        th_data = {}
        th_data['e1'] = e1.get()
        th_data['e2'] = e2.get()
        newWin.destroy()
        maincal = threading.Thread(target=self.runBackground, args=(th_data,))
        maincal.start()
       

    def spawnSensorCallBack(self):
        newWindow = Toplevel(self.root)
        newWindow.title("Spawing sensor")

        x_cor = int((self.screen_width / 2) - (236 / 2))
        y_cor = int((self.screen_height / 2) - (67 / 2))

        newWindow.geometry("{}x{}+{}+{}".format(236, 67, x_cor, y_cor))

        Label(newWindow,
              text="Sector").grid(row=0, column=0)
        Label(newWindow,
              text="Type").grid(row=1, column=0)

        e1 = Entry(newWindow, width=18)
        e2 = Entry(newWindow, width=18)

        e1.grid(row=0, column=1)
        e2.grid(row=1, column=1)

        action_with_arg = partial(self.spawnsensor, e1, e2, newWindow)
        B7 = Button(newWindow, text="Spawn", command=action_with_arg, width=18).grid(row=2, column=0)
        Be = Button(newWindow, text="Close", command=newWindow.destroy, width=18).grid(row=2, column=1)


    def bot_task_Background(self, th_data):
        
        # Richiedo la sub
        
        data = {}
        data['id'] = ""
        data['current_sector'] = th_data['e1']
        data['topic'] = th_data['e2']
        # gestire try except
        r = requests.post('http://localhost:5000/bot', json=data)
        
        # Ricevo ACK dal broker
        id = r.json()['id']

        app = Flask(__name__)
        app.run(host='0.0.0.0', port=5001)
        
        @app.route("/")
        def wait_for_message():
            # if id == id che mi manda il broker
            # allora il messaggio riguarda me e quindi me lo storo
            print("ok")


    def spawnbot(self, e1, e2, newWin):
        
        th_data = {}
        th_data['e1'] = e1.get()
        th_data['e2'] = e2.get()
        newWin.destroy()
        maincal = threading.Thread(target=self.bot_task_Background, args=(th_data,))
        maincal.start()

    def spawnBotCallBack(self):
        newWindow = Toplevel(self.root)
        newWindow.title("Spawing bot")

        x_cor = int((self.screen_width / 2) - (236 / 2))
        y_cor = int((self.screen_height / 2) - (67 / 2))

        newWindow.geometry("{}x{}+{}+{}".format(236, 67, x_cor, y_cor))

        Label(newWindow,
              text="Sector").grid(row=0, column=0)
        Label(newWindow,
              text="Topic").grid(row=1, column=0)

        e1 = Entry(newWindow, width=18)
        e2 = Entry(newWindow, width=18)

        e1.grid(row=0, column=1)
        e2.grid(row=1, column=1)

        action_with_arg = partial(self.spawnbot, e1, e2, newWindow)
        B2 = Button(newWindow, text="Spawn", command=action_with_arg, width=18).grid(row=2, column=0)
        Be = Button(newWindow, text="Close", command=newWindow.destroy, width=18).grid(row=2, column=1)


    def unsub(self, e1):
        id = e1.get();
        print("-------- ", id)
        r = requests.post('http://localhost:5000/unsubscribeBot', json=id)
        insertedId = r.json()['id']
        # cs = r.json()['current_sector']
        tp = r.json()['topic']

        self.Console.insert(INSERT, "\n")
        self.Console.insert(INSERT, "Unsubscribing ...\n")
        self.Console.insert(INSERT, "* ID: " + insertedId + "\n")
        self.Console.insert(INSERT, "* Bot was unsubscribed from topic: " + tp)
        self.Console.insert(INSERT, "\n")

    def unsubSingleBot(self):

        newWindow = Toplevel(self.root)
        newWindow.title("Unsubscribe bot")

        x_cor = int((screen_width / 2) - (236 / 2))
        y_cor = int((screen_height / 2) - (67 / 2))

        newWindow.geometry("{}x{}+{}+{}".format(236, 67, x_cor, y_cor))

        Label(newWindow,
              text="Insert bot ID:").grid(row=0, column=0)

        e1 = Entry(newWindow, width=18)
        e1.grid(row=0, column=1)

        action_with_arg = partial(self.unsub, e1)
        B12 = Button(newWindow, text="Unsubscribe", command=action_with_arg, width=18).grid(row=2, column=0)
        Be = Button(newWindow, text="Close", command=newWindow.destroy, width=18).grid(row=2, column=1)

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
        
        self.root.resizable(False, False)
        self.window_height = 600
        self.window_width = 800

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

        self.Console = Text(myframe, width=75, height=35)
        # Console.config(state=DISABLED)
        self.Console.pack()
        
        B = Button(wrapper3, text="Subscribe a new bot", command=self.botsub_thread, width=25).pack()
        #B3 = Button(wrapper3, text="Subscribe random bots", command=spawnRandomBots, width=25).pack()
        Bremove = Button(wrapper3, text="Unsubscribe single bot", command=self.botunsub_thread, width=25).pack()
        #Bremoverand = Button(wrapper3, text="Unsubscribe random bots", command=unsubRandomBots, width=25).pack()
        #B45 = Button(wrapper3, text="Kill single bot", command=killSingleBot, width=25).pack()
        #B46 = Button(wrapper3, text="Kill random bots", command=killRandomBot, width=25).pack()
        #B1 = Button(wrapper3, text="List all bots", command=listBotsCallBack, width=25).pack()

        B4 = Button(wrapper2, text="Publish a new value", command=self.sensorpub_thread, width=25).pack()
        #B5 = Button(wrapper2, text="Publish random values", command=spawnRandomSensor, width=25).pack()
        #Bkill = Button(wrapper2, text="Kill single sensor", command=killSingleSensor, width=25).pack()
        #Bkillrand = Button(wrapper2, text="Kill random sensors", command=killRandomSensor, width=25).pack()
        #B6 = Button(wrapper2, text="List all sensors", command=listSensorsCallBack, width=25).pack()

        #B21 = Button(wrapper4, text="Context switch (?)", command=switchCallBack, width=25).pack()
        #B21 = Button(wrapper4, text="Timestamp report", command=listSensorsCallBack, width=25).pack()
        #B21 = Button(wrapper4, text="Track work", command=consoleRequest, width=25).pack()

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

        self.heartbeat_thread()
        self.root.update()
        self.root.mainloop()


    def botunsub_thread(self):
        maincal = threading.Thread(target=self.unsubSingleBot)
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