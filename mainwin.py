# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/mnt/hgfs/tmpcode/pyqt-http/untitled.ui'
#
# Created: Fri Jun  5 10:59:33 2015
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import socket
import signal
import errno
import sys
import os
import platform
import time
#from sendfile import sendfile

class Worker(QtCore.QThread): 
    trigger = QtCore.pyqtSignal(int, int, str)


    def __init__(self,parent=None): 
        super(Worker,self).__init__(parent) 

    def __del__(self): 
        self.wait() 


    def set(self, strHost, port, httpheader, fullFileName, totalLen):
        self.ip = strHost
        self.p = port
        self.hdr = httpheader
        self.fn = fullFileName
        self.fileLen = totalLen

    def run(self): 
        #signal.signal(signal.SIGUSR1,sigHander)
        global lisfd
        lisfd = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        lisfd.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        lisfd.bind((self.ip, self.p))
        lisfd.listen(10)

        

        self.runflag = True
        lisfd.setblocking(0)
        while self.runflag:
            if self.runflag == False:
                break
            try:
                confd,addr = lisfd.accept()
            except socket.error, msg:
                if msg.errno == errno.EINTR or msg.errno == errno.EAGAIN or msg.errno == errno.EWOULDBLOCK:
                    print msg
                else:
                    raise
                time.sleep(1)
                continue

            print "connect by ",addr
            ip = addr[0]
            port = addr[1]
            addrStr = "%s:%d"%(ip, port)
            confd.settimeout(10)
            try:
                #print "recving"
                #data = confd.recv(1024, socket.MSG_DONTWAIT)
                data = confd.recv(1024)
            except socket.error, msg:
                #print msg
                confd.close()
                continue

            #print "recv end"
            if not data:
                break
            print(data)
            confd.send(self.hdr)
            print addrStr

            self.trigger.emit(0, self.fileLen, addrStr)
                
            file = open(self.fn, "rb")

            #offset = 0
            #totalSent = long(0);
            while True:
                if self.runflag == False:
                    return 
                chunk = file.read(65536)
                if not chunk:
                    break  # EOF
                try:
                    confd.sendall(chunk)
                except socket.error, msg:
                    print msg
                    lisfd.close() 
                    return
                #totalSent += 65536
                self.trigger.emit(65536, self.fileLen, addrStr)
    
            #confd.send('\n\n')
            confd.close()
            self.trigger.emit(self.fileLen, self.fileLen, addrStr)
            print "send fin"
        else:
            lisfd.close()
            print "stop"


def GetFileSize(filename):
        len = os.path.getsize(filename)
        return len

def HttpResponse(header,filename):
        f = open(filename, "rb")
        contxtlist = f.readlines()
        size=os.path.getsize(filename)
        context = ''.join(contxtlist)
        response = "%s %d\n\n%s\n\n" % (header,size,context) 
        return response 

def TestPlatform():
        print ("----------Operation System--------------------------")
        #Windows will be : (32bit, WindowsPE)
        #Linux will be : (32bit, ELF)
        print(platform.architecture())

        #Windows will be : Windows-XP-5.1.2600-SP3 or Windows-post2008Server-6.1.7600
        #Linux will be : Linux-2.6.18-128.el5-i686-with-redhat-5.3-Final
        print(platform.platform())

        #Windows will be : Windows
        #Linux will be : Linux
        print(platform.system())

        print ("--------------Python Version-------------------------")
        #Windows and Linux will be : 3.1.1 or 3.1.3
        print(platform.python_version())

def WhichPlatform():
        sysstr = platform.system()
        if(sysstr =="Windows"):
            print ("Call Windows tasks")
            return "windows"
        elif(sysstr == "Linux"):
            print ("Call Linux tasks")
            return "linux"
        else:
            print ("Other System tasks")
            return "others"

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

from PyQt4 import QtGui, QtCore
from PIL import ImageQt
import qrcode


class Image(qrcode.image.base.BaseImage):
    def __init__(self, border, width, box_size):
        self.border = border
        self.width = width
        self.box_size = box_size
        size = (width + border * 2) * box_size
        self._image = QtGui.QImage(
            size, size, QtGui.QImage.Format_RGB16)
        self._image.fill(QtCore.Qt.white)

    def pixmap(self):
        return QtGui.QPixmap.fromImage(self._image)

    def drawrect(self, row, col):
        painter = QtGui.QPainter(self._image)
        painter.fillRect(
            (col + self.border) * self.box_size,
            (row + self.border) * self.box_size,
            self.box_size, self.box_size,
            QtCore.Qt.black)

    def save(self, stream, kind=None):
        pass

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(800, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))


        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(650, 220, 100, 50))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))


        self.linkLabel = QtGui.QLabel(self.centralwidget)
        self.linkLabel.setGeometry(QtCore.QRect(450, 0, 300, 160))
        self.linkLabel.setObjectName(_fromUtf8("label"))

        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(455, 160, 200, 60))
        self.label.setObjectName(_fromUtf8("label"))
        self.label.setWordWrap(True)

        self.addr = QtGui.QLabel(self.centralwidget)
        self.addr.setGeometry(QtCore.QRect(450, 105, 150, 30))
        self.addr.setObjectName(_fromUtf8("addr"))
        self.addr.setWordWrap(True)
        self.addr.setText("remoteaddr");


        self.ratio = QtGui.QLabel(self.centralwidget)
        self.ratio.setGeometry(QtCore.QRect(610, 105, 250, 30)) 
        self.ratio.setObjectName(_fromUtf8("ratio")) 
        self.ratio.setWordWrap(True)
        self.ratio.setText("ratio");


        self.textEdit = QtGui.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(680, 180, 50, 30))
        self.textEdit.setObjectName(_fromUtf8("textEdit"))


        self.pushButton_2 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(450, 220, 100, 50))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))


        self.pb = QtGui.QProgressBar(self.centralwidget)
        self.pb.setGeometry(QtCore.QRect(450, 130, 300, 20))
        self.pb.setObjectName(_fromUtf8("pb"))
        self.pb.setRange(0, 0)
        self.pb.setRange(0, 100)
        self.pb.setValue(0)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.qrLabel = QtGui.QLabel(self.centralwidget)
        self.qrLabel.setGeometry(QtCore.QRect(20, 2, 300, 300))
        self.qrLabel.setObjectName(_fromUtf8("label"))
#self.refreshQRCode()

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def refreshQRCode(self, port):
        global localIP 
        text = unicode("http://%s:%d"%(localIP, port))
        self.linkLabel.setText("Please visit: %s"%text);
        print text
        self.qrLabel.setPixmap(
            qrcode.make(text, image_factory=Image).pixmap())


    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.pushButton.setText(_translate("MainWindow", "run", None))
        self.label.setText(_translate("MainWindow", "choose a file", None))
        self.textEdit.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">1234</p></body></html>", None))
        self.pushButton_2.setText(_translate("MainWindow", "choose file", None))



class Window( QtGui.QMainWindow ):
    def __init__( self ):
        super( Window, self ).__init__()
        self.setWindowTitle( "hello" )
        self.resize( 200, 300 )
        self.uiWin = Ui_MainWindow() 
        self.uiWin.setupUi(self)
        self.fullFileName = ""
        self.fileName = ""
        self.thread=Worker()

        self.connect(self.uiWin.pushButton,
                QtCore.SIGNAL('clicked()'),
                self.runHttpSvr) 

        self.connect(self.uiWin.pushButton_2,
                QtCore.SIGNAL('clicked()'),
                self.chooseFile) 
        self.running = False

        self.thread.trigger.connect(self.updatePb)

    def updatePb(self, sent2, total2, addr):
        if sent2 == 0:
            self.sentLen = 0
        #print sent
        #print total2 
        self.sentLen += sent2
        total = self.fileLen
        #print total 
        val = self.sentLen/float(total)*100
        if val <= 100:
            self.uiWin.pb.setValue(val)
            self.uiWin.addr.setText(addr)
            self.uiWin.ratio.setText("%d/%d"%(self.sentLen, total))
        else:
            self.uiWin.pb.setValue(100)
            self.uiWin.addr.setText(addr)
            self.uiWin.ratio.setText("%d/%d"%(total, total))


    def runHttpSvr(self):
        if self.running :
            #global lisfd
            #lisfd.close()
            self.thread.runflag = False
            self.running = False
            #self.uiWin.label.setText("svr is not running") 
            self.uiWin.pushButton.setText("run") 
            #os.kill(1234, signal.SIGUSR1)
            return

        
        if len(self.fullFileName) == 0 or len(self.fileName) == 0: 
            msgBox = QtGui.QMessageBox(QtGui.QMessageBox.Warning,
            "error", "not choose file", 
            QtGui.QMessageBox.NoButton, self)      

            msgBox.show()
            return
            

        if self.fileName and os.path.exists(self.fullFileName):
            print 'OK, the "%s" file exists.'%self.fullFileName
        else:
            msgBox = QtGui.QMessageBox(QtGui.QMessageBox.Warning,
            "error", "Sorry, I cannot find the '%s' file."%self.fullFileName, 
            QtGui.QMessageBox.NoButton, self)      

            msgBox.show()
            return

        port = int(self.uiWin.textEdit.toPlainText())
        if port < 1 or port > 65535:
                msgBox = QtGui.QMessageBox(QtGui.QMessageBox.Warning,
                "error", "port[%s] error"%self.uiWin.textEdit.toPlainText(), 
                QtGui.QMessageBox.NoButton, self)      

                msgBox.show()
                return
            
        strHost = "0.0.0.0"

        
        self.fileLen = GetFileSize(self.fullFileName)

        httpheader = '''\
HTTP/1.1 200 OK
Context-Type: bin;charset=UTF-8
Server: Python-slp version 1.0
'''
        
        httpheader += "Content-Disposition: attachment;filename=%s\n" % self.fileName
        httpheader += 'Context-Length: %d\n\n'% self.fileLen

        print httpheader
        self.sentLen = 0
        self.thread.set(strHost, port, httpheader, self.fullFileName, self.fileLen)
        self.thread.start() 
        self.running = True
        self.uiWin.refreshQRCode(port)
        #self.uiWin.label.setText("svr is running") 
        self.uiWin.pushButton.setText("stop") 

    def chooseFile(self):     
        #self.uiWin.label.setText("choosefile") 
        name = QtGui.QFileDialog.getOpenFileName(self) 
        if name:
            self.fullFileName = unicode(name , "utf8")
            saperator = '/' 
            self.fileName = self.fullFileName.split(saperator)[-1]
            #print self.fullFileName
            #print self.fileName
            self.uiWin.label.setText(self.fullFileName)

import socket

if WhichPlatform() == "linux":
    import fcntl

import struct
  
def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])



if __name__ == '__main__':

    global localIP
    #localIP = socket.gethostbyname(socket.gethostname())
    if WhichPlatform() != "windows":
        localIP = get_ip_address("eth0")

    print "local ip:%s "%localIP

    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())

