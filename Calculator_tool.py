#coding:gbk
#*******************************************
#作者: 我東
#mail:wodong526@dingtalk.com
#time:2022/2/1
#版本：V1.1
#******************************************

from PySide2 import QtGui
from PySide2 import QtCore
from PySide2 import QtWidgets
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import os
from functools import partial

def maya_main_window():
    main_window_par = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_par), QtWidgets.QWidget)

class MyPushButton(QtWidgets.QPushButton):
    enter_pressed = QtCore.Signal(str)
    
    def keyPressEvent(self, e):
        super(MyPushButton, self).keyPressEvent(e)
        
        if e.key() == QtCore.Qt.Key_Enter:
            self.enter_pressed.emit(u'得数为：')
            
        elif e.key() == QtCore.Qt.Key_Return:
            self.enter_pressed.emit(u'得数为：')

class OpenImportDialog(QtWidgets.QDialog):
    def __init__(self, parent = maya_main_window()):
        super(OpenImportDialog, self).__init__(parent)
        
        self.setWindowTitle(u'東牌计算机.V1.1')
        self.setMinimumWidth(330)
        self.setMinimumHeight(560)
        
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)#去除窗口上的问号
        self.setFixedSize(self.width(), self.height())
        
        self.crea_widgets()
        self.crea_layouts()
        self.crea_connections()
        
        
    def crea_widgets(self):
        self.input_tex  = QtWidgets.QTextEdit()
        self.input_tex.setFixedSize(310, 100)
        self.input_tex.setFont(QtGui.QFont('黑体', 30))
        
        self.output_tex = QtWidgets.QTextEdit()
        self.output_tex.setFixedSize(310, 60)
        self.output_tex.setFont(QtGui.QFont('黑体', 30))
        self.output_tex.setReadOnly(True)
        
        for inf in range(10):
            exec('self.but_{} = QtWidgets.QPushButton(u"{}")'.format(inf, inf))
            exec('self.but_{}.setFixedSize(70, 70)'.format(inf))
            exec('self.but_{}.setFont(QtGui.QFont("黑体", 60))'.format(inf))
        
        self.operator_dir = {'plus'   : '+',
                        'reduce' : '-',
                        'ride'   : '*',
                        'except' : '/',}
        for inf in self.operator_dir:
            exec('self.but_{} = QtWidgets.QPushButton(u"{}")'.format(inf, self.operator_dir[inf]))
            exec('self.but_{}.setFixedSize(70, 70)'.format(inf))
            exec('self.but_{}.setFont(QtGui.QFont("黑体", 60))'.format(inf))
            
        self.but_run = MyPushButton()
        self.but_run.setText(u'=')
        self.but_run.setFixedSize(150, 70)
        self.but_run.setFont(QtGui.QFont('黑体', 60))
        
        self.but_clos = QtWidgets.QPushButton(u'关闭计算器')
        self.but_clos.setFixedHeight(40)
        self.but_clos.setFont(QtGui.QFont('黑体', 15))
        self.but_copy = QtWidgets.QPushButton(u'复制得数')
        self.but_copy.setFixedHeight(40)
        self.but_copy.setFont(QtGui.QFont('黑体', 15))
        self.but_clear = QtWidgets.QPushButton(u'清除')
        self.but_clear.setFixedHeight(40)
        self.but_clear.setFont(QtGui.QFont('黑体', 15))
        
    def crea_layouts(self):
        but_up_layout = QtWidgets.QHBoxLayout()
        but_up_layout.addWidget(self.but_7)
        but_up_layout.addWidget(self.but_8)
        but_up_layout.addWidget(self.but_9)
        but_up_layout.addWidget(self.but_ride)
        
        but_well_layout = QtWidgets.QHBoxLayout()
        but_well_layout.addWidget(self.but_4)
        but_well_layout.addWidget(self.but_5)
        but_well_layout.addWidget(self.but_6)
        but_well_layout.addWidget(self.but_except)
        
        but_lower_layout = QtWidgets.QHBoxLayout()
        but_lower_layout.addWidget(self.but_1)
        but_lower_layout.addWidget(self.but_2)
        but_lower_layout.addWidget(self.but_3)
        but_lower_layout.addWidget(self.but_plus)
        
        but_end_layout = QtWidgets.QHBoxLayout()
        but_end_layout.addWidget(self.but_0)
        but_end_layout.addWidget(self.but_run)
        but_end_layout.addWidget(self.but_reduce)
        
        but_other_layout = QtWidgets.QHBoxLayout()
        but_other_layout.addWidget(self.but_clos)
        but_other_layout.addWidget(self.but_copy)
        but_other_layout.addWidget(self.but_clear)
        
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(self.input_tex)
        main_layout.addWidget(self.output_tex)
        main_layout.addLayout(but_up_layout)
        main_layout.addLayout(but_well_layout)
        main_layout.addLayout(but_lower_layout)
        main_layout.addLayout(but_end_layout)
        main_layout.addLayout(but_other_layout)
        
    
    def crea_connections(self):
        for inf in range(10):
            exec('self.but_{}.clicked.connect(partial(self.crea_tex, {}))'.format(inf, inf))
        
        for inf in self.operator_dir:
            exec('self.but_{}.clicked.connect(partial(self.crea_tex, "{}"))'.format(inf, self.operator_dir[inf]))
        
        self.but_run.clicked.connect(self.crea_run)
        self.but_run.enter_pressed.connect(self.crea_run)
        
        self.but_copy.clicked.connect(self.crea_clipboard)
        self.but_clear.clicked.connect(self.crea_clear)
        self.but_clos.clicked.connect(self.wnd_close)
    
    def crea_tex(self, tex):
        old_tex = self.input_tex.toPlainText()
        
        cursor = self.input_tex.textCursor()
        cru_pos = cursor.position()#获取光标位置
        
        self.input_tex.setText(old_tex[:cru_pos] + str(tex) + old_tex[cru_pos:])
        
        cursor.setPosition(cru_pos + 1)
        self.input_tex.setTextCursor(cursor)#移动光标到输入的字符身后
        
    def crea_run(self, *inf):
        number_str = self.input_tex.toPlainText()
        number_str = self.mulOrDiv(number_str)
        number_str = self.addOrSub(number_str)
        self.output_tex.setText(str(number_str))
        if inf == True:
            print "{}{}".format(inf, number_str)
        else:
            print '得数为{}'.format(number_str)
    
    def atom_seek(self, seek_str):
        #算单个乘除并返回这个乘除后的式子
        if "*" in seek_str:
            s1,s2 = seek_str.split("*")
            return str(float(s1) * float(s2))
        elif "/" in seek_str:
            s1,s2 = seek_str.split("/")
            return str(float(s1)/float(s2))
    
    def mulOrDiv(self, exp):
        while True:
            exp_res = re.search(r"\d+(\.\d+)?[*/]-?\d+(\.\d+)?", exp)
            if exp_res:
                atom_exp = exp_res.group()
                res = self.atom_seek(atom_exp)
                exp = exp.replace(atom_exp, res)
            else:
                return str(exp)
    
    def addOrSub(self, exp):
        exp_sum = 0
        while True:
            exp_res = re.findall(r"-?\d+(?:\.\d+)?", exp)
            if exp_res:
                for i in exp_res:
                    exp_sum += float(i)
                return exp_sum
    
    def crea_clear(self):
        self.input_tex.clear()
        
    def crea_clipboard(self):
        tex = self.output_tex.toPlainText()
        com = 'echo | set /p unl = ' + tex.strip() + '| clip'
        os.system(com)
        print '得数{}已复制到粘贴板。'.format(tex)
                
    def wnd_close(self):
        self.close()
        print '计算器关闭。'
        self.deleteLater()
        
     
        
if __name__ == '__main__':
    try:
        a.wnd_close()
    except:
        pass
    
    a = OpenImportDialog()
    a.show()