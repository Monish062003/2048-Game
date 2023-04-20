import random
import re
import sqlite3
from kivy.app import App
from kivy.core.window import Window
from kivymd.app import MDApp
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.layout import Layout
from kivy.properties import StringProperty
from kivy.graphics import Color
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager,Screen

global openonrefresh
openonrefresh=0
sm=ScreenManager()


def sqlstart():
    try:
        global jackdaw
        conn=sqlite3.connect('scoredata')
        cur=conn.cursor()
        cur.execute("""
            create table score(
            highscore int
            );
            """)

    except Exception:
        print()
    finally:
        cur.execute("""Select*from score""")
        jackdaw=cur.fetchall()
        # print("You START at {}".format(jackdaw))
        conn.commit()
        conn.close()

#at the starting stage it imports 2 random values
def startrandom():
    for i in range(0,2):
        position=[2,4,8]
        num1=random.randint(0,2)
        rnum1=random.randint(0,3)
        rnum2=random.randint(0,3)

        for num,row in enumerate(rows_sum):
            if num==rnum1:
                for i in range(0,len(rows_sum)):
                    if i==rnum2:
                        if(row[i]==0):
                            row[i]=position[num1]
                        else:
                            if i==len(rows_sum)-1:
                                row[i-1]=position[num1]
                            elif i==0:
                                row[i+1]=position[num1]
                            else:
                                row[i+1]=position[num1]

#it inserts all the zero i.e empty elements in the array zeroexistent so we can further use it to import random values
def insert():
    for num,row in enumerate(rows_sum):
        for i in range(0,len(rows_sum)):
            if row[i]==0:
                zeroexistent.append([num,i])


#After each swipe it adds a random number in the grid
def aftersort():
    position=[2,4,8]
    num1=random.randint(0,2)
    rnum3=random.randint(0,len(zeroexistent)-1)
    rnum4=zeroexistent[rnum3]
    for num,row in enumerate(rows_sum):
        if num==rnum4[0]:
            for i in range(0,len(rows_sum)):
                if i==rnum4[1]:
                    row[i]=position[num1]
    zeroexistent.clear()


def sqlend():
    global currentscore
    global jackdaw

    conn=sqlite3.connect('scoredata')
    cur=conn.cursor()
    try:
        cur.execute("""
            create table score(
            highscore int
            );
            """)
    except Exception:
        print()
    finally:
        cur.execute("""Insert into score values(?)""",(currentscore))
        # cur.execute("""Update score SET highscore=""",jackdaw,""" Where highscore=(?)""",highscore)
        cur.execute("Select*from score")
        conn.commit()
        conn.close()



#in the end it checks if all are non zero and non of the closeby elements are common, so it can end the game


def save():
    global currentscore
    conn=sqlite3.connect('scoredata')
    cur=conn.cursor()
    jackdaw.append(currentscore)
    cur.execute("""Insert into score VALUES (?)""",jackdaw)
    cur.execute("""Select*from score""")
    currentscore=0
    jackdaw.clear()
    conn.commit()
    conn.close()

def repeat():
    firstclass=First()


def highscorelogic():
    global highscore
    try:
        highscore = re.findall(r'\d+',str(jackdaw[len(jackdaw)-1]))
        highscore=int(highscore[0])

    except Exception:
        highscore=0
    jackdaw.clear()


class First(Screen):


    global currentscore,highscore,rows_sum,rev_rows_sum,zeroexistent,row1,row2,row3,row4,jackdaw,lament
    currentscore=0
    sqlstart()

    highscorelogic()

    row1=[0,0,0,0]
    row2=[0,0,0,0]
    row3=[0,0,0,0]
    row4=[0,0,0,0]

    lament=[]

    rows_sum=[row1,row2,row3,row4]
    rev_rows_sum=rows_sum[::-1]
    zeroexistent=[]
    jackdaw=[]


    def display(self):
        if openonrefresh==0:
            for row in rows_sum:
                for elements in row:
                    if elements==0:
                        lament.append(" ")
                    else:
                        lament.append(str(elements))

        else:
            sqlstart()

            highscorelogic()

            for row in rows_sum:
                for elements in row:
                    lament.append(str(elements))

            global currentscore
            currentscore=0

        try:
            self.ids.twoo.text=str(currentscore)
            self.ids.fourr.text=str(highscore)
        except Exception:
            self.ids.highscore.text=str(highscore)
            self.ids.currscore.text=str(currentscore)
            self.ids.zero.text=lament[0]
            self.ids.one.text=lament[1]
            self.ids.two.text=lament[2]
            self.ids.three.text=lament[3]
            self.ids.four.text=lament[4]
            self.ids.five.text=lament[5]
            self.ids.six.text=lament[6]
            self.ids.seven.text=lament[7]
            self.ids.eight.text=lament[8]
            self.ids.nine.text=lament[9]
            self.ids.ten.text=lament[10]
            self.ids.eleven.text=lament[11]
            self.ids.twelve.text=lament[12]
            self.ids.thirteen.text=lament[13]
            self.ids.fourteen.text=lament[14]
            self.ids.fifteen.text=lament[15]

        lament.clear()

    def exit(self):
        App.get_running_app().stop()
        Window.close()

    def start(self):
        startrandom()
        insert()
        self.display()

    def change(self):
        self.ids.twoo.text=str(currentscore)
        self.ids.fourr.text=str(highscore)

    def endcheck(self):
        zeroexistent=[]
        condition="True"
        for num,row in enumerate(rows_sum):
            for i in range(len(rows_sum)):
                if row[i]==0:
                    zeroexistent.append([num,i])

        if len(zeroexistent)==0:

            if condition=="True":
                for i in range(len(rows_sum)):
                    for num,row in enumerate(rows_sum):
                        for num1,rows in enumerate(rows_sum):
                            if num+1!=len(rows_sum):
                                if num+1==num1:
                                    if row[i]==rows[i]:
                                        condition="False"

            if condition=="True":
                self.booltru()
    def booltru(self):
        popups=MyPopup()
        popups.open()
        try:
            MyPopup.open()
        except Exception:
            pass

        if(currentscore>highscore):
            save()

#this functions is used to swipe left
    def left(self):
        global currentscore
        incrementnumber=1
        approved=0
        lock=[]
        for num,row in enumerate(rows_sum):
            for i in range(len(row)):

                if(row[i]!=0):
                    for j in range(i-1,-1,-1):
                        if(row[j]==0):
                            row[j]=row[j+1]
                            row[j+1]=0

                        else:
                            condition=True
                            for lockchecks in lock:
                                if lockchecks[0]==num:
                                    if lockchecks[1]==j+incrementnumber:
                                        condition=False
                                        approved=1
                                        break

                            if condition==True:
                                if row[j]==row[j+1]:
                                    row[j]+=row[j]
                                    currentscore+=row[j]
                                    row[j+1]=0
                                    lock.append([num,j])

            if approved==1:
                incrementnumber-=1



        insert()
        aftersort()
        self.display()
        self.endcheck()

#this functions is used to swipe right
    def right(self):
        global currentscore
        lock=[]
        for num,row in enumerate(rows_sum):
            for i in range(len(row)-1,-1,-1):
                if(row[i]!=0):
                    for j in range(i+1,len(row)):
                        if(row[j]==0):
                            row[j]=row[j-1]
                            row[j-1]=0

                        else:
                            condition=True
                            for lockchecks in lock:
                                if lockchecks[0]==num:
                                    if lockchecks[1]==j-1:
                                        condition=False
                                        break

                            if condition==True:
                                if row[j]==row[j-1]:
                                    row[j]+=row[j]
                                    currentscore+=row[j]
                                    row[j-1]=0
                                    lock.append([num,j])

        insert()
        aftersort()
        self.display()
        self.endcheck()


#this functions is used to swipe down
    def down(self):
        global currentscore
        lock=[]
        for i in range(len(rows_sum)):
            for num,row in enumerate(rev_rows_sum):
                if(row[i]!=0):
                    for num2,rows in enumerate(rev_rows_sum):
                        if num2<=num-1:
                            if rows[i]==0:
                                rows[i]=row[i]
                                row[i]=0

            for num,row in enumerate(rev_rows_sum):
                if(row[i]!=0):
                    for num2,rows in enumerate(rows_sum):
                        if num2==len(rows_sum)-num:
                            condition=True
                            for lockchecks in lock:
                                if lockchecks[0]==num2:
                                    if lockchecks[1]==i:
                                        condition=False
                                        break

                            if condition==True:
                                if rows[i]==row[i]:
                                    rows[i]+=rows[i]
                                    currentscore+=row[i]
                                    row[i]=0
                                    lock.append([num2,i])

            for num,row in enumerate(rev_rows_sum):
                if(row[i]!=0):
                    for num2,rows in enumerate(rev_rows_sum):
                        if num2<=num-1:
                            if rows[i]==0:
                                rows[i]=row[i]
                                row[i]=0

        lock.clear()
        insert()
        aftersort()
        self.display()
        self.endcheck()

#this functions is used to swipe up
    def up(self):
        global currentscore
        lock=[]
        for i in range(len(rows_sum)):
            for num,row in enumerate(rows_sum):
                if(row[i]!=0):
                    for num2,rows in enumerate(rows_sum):
                        if num2<=num-1:
                            if rows[i]==0:
                                rows[i]=row[i]
                                row[i]=0

            for num,row in enumerate(rows_sum):
                if(row[i]!=0):
                    for num2,rows in enumerate(rev_rows_sum):
                        if num2==len(rows_sum)-num:
                            condition=True
                            for lockchecks in lock:
                                if lockchecks[0]==num2:
                                    if lockchecks[1]==i:
                                        condition=False
                                        break

                            if condition==True:
                                if rows[i]==row[i]:
                                    rows[i]+=rows[i]
                                    currentscore+=row[i]
                                    row[i]=0
                                    lock.append([num2,i])

            for num,row in enumerate(rows_sum):
                if(row[i]!=0):
                    for num2,rows in enumerate(rows_sum):
                        if num2<=num-1:
                            if rows[i]==0:
                                rows[i]=row[i]
                                row[i]=0

        lock.clear()
        insert()
        aftersort()
        self.display()
        self.endcheck()

    def restart(self):
        for row in rows_sum:
            for num,elements in enumerate(row):
                row[num]=0

    def currentscorevaluebypopup(self):
        return currentscore

    def highscorevaluebypopup(self):
        return highscore

    def callbyPopuponrestart(self):
        if currentscore>highscore:
            save()
        self.restart()
        global openonrefresh
        openonrefresh=1
        self.display()
        openonrefresh=0

class MyPopup(Popup):
    def on_kv_post(self, base_widget):
        repeat()
        self.ids.twoo.text=f"{currentscore}"
        self.ids.fourr.text=f"{highscore}"
    def callbyPopuponexit(self):
        repeat()
        if currentscore>highscore:
            save()
        App.get_running_app().stop()
        Window.close()


sm.add_widget(First(name="first"))


kv=Builder.load_file('game.kv')
class Games(MDApp):
    def build(self):
        self.theme_cls.theme_style= "Dark"
        return kv

Games().run()

