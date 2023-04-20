import random

row1=[0,0,2,0]
row2=[2,0,2,0]
row3=[0,0,0,2]
row4=[2,2,0,0]

rows_sum=[row1,row2,row3,row4]
rev_rows_sum=rows_sum[::-1]

position=[2,4,8]

num1=random.randint(0,2)
# direction=int(input("1: Up\n2: Down\n3: Left\n4: Right\nType the number accordingly :"))

direction=7

def left():
    for row in rows_sum:
        for i in range(len(row)-1,-1,-1):
            if(row[i]!=0):
                for j in range(i-1,-1,-1):
                    if(row[j]==0):
                        row[j]=row[i]
                        row[i]=0

def right():
    for pos,row in enumerate(rows_sum):
        for i in range(len(row)):
            if(row[i]!=0):
                for j in range(i+1,len(row)):
                    if(row[j]==0):
                        row[j]=row[i]
                        row[i]=0

def down():
    for i in range(len(rows_sum)):
        for num,row in enumerate(rev_rows_sum):
            if(row[i]!=0):
                for num2,rows in enumerate(rev_rows_sum):
                    if num2<=num-1:
                        if rows[i]==0:
                            rows[i]=row[i]
                            row[i]=0


def up():
    for i in range(len(rows_sum)):
        for num,row in enumerate(rows_sum):
            if(row[i]!=0):
                for num2,rows in enumerate(rows_sum):
                    if num2<=num+1:
                        if rows[i]==0:
                            rows[i]=row[i]
                            row[i]=0

up()
match(direction):
    case 1:up()
    case 2:down()
    case 3:left()
    case 4:right()


for row in rows_sum:
    print(row)






