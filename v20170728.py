
import random
import re
import sys
import time
from math import *

# import numpy as np
# import skimage
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
# from skimage import draw

import Distance
import DPP

# --- canvas ---
Width=600
Height=400
Color=('blue','blue','green','red','gray','orange','gold')



'''initialize procedure'''


'''each tuple denotes a polygon, (x1,y1,x2,y2 ...)'''
Polygons=(
    (30,0,0,40,-30,0,0,-40),
    (60,0,0,50,-60,0,-30,-40,30,-40),        
    (40,-40,-40,40,-15,80,15,80),
    (0,-30,30,0,-40,70),
    (40,-20,-40,-20,0,50),
    (40,0,20,34,-20,34,-40,0,-20,-34,20,-34),
    (30,30,30,-30,-30,-30,-30,30),    
    (0,-20,20,0,-20,40,-40,20)
)


''' each polygon has an atribute, the same number means the same class'''
# Groups=[]
# for i in range(0,len(Polygons)):
#     Groups.append(i)

Groups=[1,1,1,3,3,2,2,2]


''' center_vectors is a list of the translation of each polygon,
    [x1,y1,x2,y2,...]

    the initial state is generated by DPP'''

center_vectors=DPP.DPP(20,len(Polygons))

'''here is to make sure the initial state generated by DPP
    would not make polygons out of canvas bound'''
for i in range(0,len(Polygons)):
    x=list(Polygons[i])[0::2]
    y=list(Polygons[i])[1::2]
    center_vectors[2*i]*=Width
    center_vectors[2*i+1]*=Height
    shift_x=0
    shift_y=0

    if min(x)+center_vectors[2*i]<0:
        shift_x=abs(min(x)+center_vectors[2*i])
    if max(x)+center_vectors[2*i]>Width-1:
        shift_x=Width-1-max(x)-center_vectors[2*i]
    if min(y)+center_vectors[2*i+1]<0:
        shift_y=abs(min(y)+center_vectors[2*i+1])
    if max(y)+center_vectors[2*i+1]>Height-1:
        shift_y=Height-1-max(y)-center_vectors[2*i+1]
    
    center_vectors[2*i]+=shift_x
    center_vectors[2*i+1]+=shift_y


'''methods to draw the poltgons'''
class MyCanvas(QtGui.QWidget):
    
    # shapes=[]
    
    def __init__(self):
        super(MyCanvas, self).__init__()

        # default size
        self.setFixedSize(Width, Height)

        
    def paintEvent(self, event):

        qp = QtGui.QPainter()
        qp.begin(self)

        # white background
        qp.fillRect(event.rect(), QtGui.QBrush(QtGui.QColor('white')))



        for i in range(0,len(Polygons)):
            col=Color[Groups[i]%len(Color)]
            self.drawPolygonWithCenter(qp,center_vectors[i*2],center_vectors[i*2+1],Polygons[i],col)
            # print 'item',i

        

        # print "update"

                
        qp.end()
    

    def drawPolygonWithCenter(self,qp,x,y,polygon,col):
        new_polygon=[]
        for i in range(0,len(polygon)):
            if i%2==0:
                new_polygon.append(polygon[i]+x)
            else:
                new_polygon.append(polygon[i]+y)
        self.drawPolygon(qp,col,*tuple(new_polygon))

        
    def drawPolygon(self, qp,col, *points):     
        '''drawing polygon'''

        # set color                  
        qp.setBrush(QtGui.QColor(col))

        temp_list=[]
        # # create polygon
        num=points.__len__()/2
        for i in range(0,num):
            temp_list.append(QPoint(points[2*i],points[2*i+1]))        

        # draw
        qp.drawConvexPolygon(QPolygon(temp_list))
        






class App(QtGui.QWidget):

    def __init__(self):
        super(App, self).__init__()
        self.learning_rate=[2]*len(center_vectors)
        self.function_value=0

        self.initUI()
    def restart(self):  

        

        a=Distance.GridentDescent(center_vectors,Polygons,self.learning_rate,self.function_value,Groups)
        self.canvas.update()
        self.function_value=a
        print 'final',center_vectors,'\n'*3,'value',self.function_value,'\t','rate',self.learning_rate,'\n'*3,
        
        return a
    
    def test(self):
        for i in range(0,50):
            self.restart()
            # print i
        


    def initUI(self):      

        self.vbox = QtGui.QVBoxLayout(self)
        self.setLayout(self.vbox)

        #--- canvas - created to get tool list ---
        
        self.canvas = MyCanvas() 

        
        self.restart()
        # self.test()
            
               

        self.btn=QPushButton("next step")
        self.btn.setCheckable(True)
        self.btn.setAutoExclusive(True)
        self.btn.clicked.connect(self.restart)

        self.btn1=QPushButton("run 50 steps")
        self.btn1.setCheckable(True)
        self.btn1.setAutoExclusive(True)
        self.btn1.clicked.connect(self.test)

         #--- canvas - add to window ---
        self.vbox.addWidget(self.canvas)
        self.vbox.addWidget(self.btn)
        self.vbox.addWidget(self.btn1)
       
        
        #self.setGeometry(300, 300, 600, 170)
        self.setWindowTitle('MyCanvas')
        self.show()

        

        
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
