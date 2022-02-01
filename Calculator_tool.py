# coding:gbk
# *******************************************
# ����: �Җ|
# mail:wodong526@dingtalk.com
# time:2022/2/1
# �汾��V1.2
# ******************************************

from PySide2 import QtGui
from PySide2 import QtCore
from PySide2 import QtWidgets
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import os
from functools import partial
import re

edition = 'V1.2'    #�汾��

def maya_main_window():
    main_window_par = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_par), QtWidgets.QWidget)


class MyTextEdit(QtWidgets.QTextEdit):
    '''
    ��дtextEdit�ؼ��ļ��̻س��źţ�����С���̻س�
    '''
    enter_pressed = QtCore.Signal(str)

    def keyPressEvent(self, e):
        super(MyTextEdit, self).keyPressEvent(e)

        if e.key() == QtCore.Qt.Key_Enter:
            self.enter_pressed.emit(u'����Ϊ��')

        elif e.key() == QtCore.Qt.Key_Return:
            self.enter_pressed.emit(u'����Ϊ��')


class Calculator(QtWidgets.QDialog):
    def __init__(self, parent = maya_main_window()):
        super(Calculator, self).__init__(parent)

        self.setWindowTitle(u'�|�Ƽ����.{}'.format(edition))
        self.setMinimumWidth(330)
        self.setMinimumHeight(640)

        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)  # ȥ�������ϵ��ʺ�
        self.setFixedSize(self.width(), self.height())

        self.crea_widgets()
        self.crea_layouts()
        self.crea_connections()

    def crea_widgets(self):
        self.input_tex = MyTextEdit()
        self.input_tex.setFixedSize(310, 100)
        self.input_tex.setFont(QtGui.QFont('����', 30))

        self.output_tex = QtWidgets.QTextEdit()
        self.output_tex.setFixedSize(310, 60)
        self.output_tex.setFont(QtGui.QFont('����', 30))
        self.output_tex.setReadOnly(True)#����������������ֶ�����

        #ѭ������0��9�İ�ť
        for inf in range(10):
            exec('self.but_{} = QtWidgets.QPushButton(u"{}")'.format(inf, inf))
            exec('self.but_{}.setFixedSize(70, 70)'.format(inf))
            exec('self.but_{}.setFont(QtGui.QFont("����", 60))'.format(inf))

        #ѭ����������������Ű�ť
        self.operator_dir = {'plus'     : '+',
                             'reduce'   : '-',
                             'ride'     : '*',
                             'except'   : '/',
                             'decimal'  : '.',
                             'bracket_f': '(',
                             'bracket_b': ')'}
        for inf in self.operator_dir:
            exec('self.but_{} = QtWidgets.QPushButton(u"{}")'.format(inf, self.operator_dir[inf]))
            exec('self.but_{}.setFixedSize(70, 70)'.format(inf))
            exec('self.but_{}.setFont(QtGui.QFont("����", 60))'.format(inf))

        self.but_run = QtWidgets.QPushButton(u'=')
        self.but_run.setFixedSize(150, 70)
        self.but_run.setFont(QtGui.QFont('����', 60))

        self.but_clos = QtWidgets.QPushButton(u'�رռ�����')
        self.but_clos.setFixedHeight(40)
        self.but_clos.setFont(QtGui.QFont('����', 15))
        self.but_copy = QtWidgets.QPushButton(u'���Ƶ���')
        self.but_copy.setFixedHeight(40)
        self.but_copy.setFont(QtGui.QFont('����', 15))
        self.but_clear = QtWidgets.QPushButton(u'���')
        self.but_clear.setFixedHeight(70)
        self.but_clear.setFont(QtGui.QFont('����', 20))

    def crea_layouts(self):
        but_top_layout = QtWidgets.QHBoxLayout()
        but_top_layout.addWidget(self.but_clear)
        but_top_layout.addWidget(self.but_bracket_f)
        but_top_layout.addWidget(self.but_bracket_b)
        but_top_layout.addWidget(self.but_ride)

        but_up_layout = QtWidgets.QHBoxLayout()
        but_up_layout.addWidget(self.but_7)
        but_up_layout.addWidget(self.but_8)
        but_up_layout.addWidget(self.but_9)
        but_up_layout.addWidget(self.but_except)

        but_well_layout = QtWidgets.QHBoxLayout()
        but_well_layout.addWidget(self.but_4)
        but_well_layout.addWidget(self.but_5)
        but_well_layout.addWidget(self.but_6)
        but_well_layout.addWidget(self.but_plus)

        but_lower_layout = QtWidgets.QHBoxLayout()
        but_lower_layout.addWidget(self.but_1)
        but_lower_layout.addWidget(self.but_2)
        but_lower_layout.addWidget(self.but_3)
        but_lower_layout.addWidget(self.but_reduce)

        but_end_layout = QtWidgets.QHBoxLayout()
        but_end_layout.addWidget(self.but_0)
        but_end_layout.addWidget(self.but_decimal)
        but_end_layout.addWidget(self.but_run)
        but_end_layout.addWidget(self.but_decimal)

        but_other_layout = QtWidgets.QHBoxLayout()
        but_other_layout.addWidget(self.but_clos)
        but_other_layout.addWidget(self.but_copy)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(self.input_tex)
        main_layout.addWidget(self.output_tex)
        main_layout.addLayout(but_top_layout)
        main_layout.addLayout(but_up_layout)
        main_layout.addLayout(but_well_layout)
        main_layout.addLayout(but_lower_layout)
        main_layout.addLayout(but_end_layout)
        main_layout.addLayout(but_other_layout)

    def crea_connections(self):
        #ѭ������ͬһ���ۣ������봰������������
        for inf in range(10):
            exec('self.but_{}.clicked.connect(partial(self.crea_tex, {}))'.format(inf, inf))

        for inf in self.operator_dir:
            exec('self.but_{}.clicked.connect(partial(self.crea_tex, "{}"))'.format(inf, self.operator_dir[inf]))

        #�ڴ��ںͼ����ϰ��µ��źŶ����ӵ��������
        self.but_run.clicked.connect(self.crea_run)
        self.input_tex.enter_pressed.connect(self.crea_run)

        self.but_copy.clicked.connect(self.crea_clipboard)
        self.but_clear.clicked.connect(self.crea_clear)
        self.but_clos.clicked.connect(self.wnd_close)

    def crea_tex(self, tex):
        old_tex = self.input_tex.toPlainText()

        cursor = self.input_tex.textCursor()
        cru_pos = cursor.position()  # ��ȡ���λ��

        self.input_tex.setText(old_tex[:cru_pos] + str(tex) + old_tex[cru_pos:])#�ڹ�괦���������������

        cursor.setPosition(cru_pos + 1)
        self.input_tex.setTextCursor(cursor)  # �ƶ���굽��������ַ����

    def crea_run(self, *inf):
        number_str = self.input_tex.toPlainText()#��ȡ���봰������
        if number_str:#��������ݾͼ�������
            number_str = self.brackets(number_str)
            self.output_tex.setText(str(number_str))#�������������������
        else:#���û�����ݾ��׳���ʾ
            print u'����������û��ʽ�ӡ�'
            return False

        if inf:#����Ǽ��̻س��ź�
            cursor = self.input_tex.textCursor()
            cursor.clearSelection()
            cursor.deletePreviousChar()#ʹ���λ�ò���
            print u"{}{}".format(inf[0], number_str)
        else:#����Ǵ��ڰ�ť��=�����ź�
            print '����Ϊ:{}'.format(number_str)

    def atom_seek(self, seek_str):
        # �㵥���˳�����������˳����ʽ�ӣ�ͨ����ֳ˳������ߵ��������¼������
        if "*" in seek_str:
            s1, s2 = seek_str.split("*")
            return str(float(s1) * float(s2))
        elif "/" in seek_str:
            s1, s2 = seek_str.split("/")
            return str(float(s1) / float(s2))

    def mulOrDiv(self, exp):
        #�˳���
        while True:
            exp_res = re.search(r"\d+(\.\d+)?[*/]-?\d+(\.\d+)?", exp)
            if exp_res:
                atom_exp = exp_res.group()
                res = self.atom_seek(atom_exp)
                exp = exp.replace(atom_exp, res)
            else:
                return str(exp)

    def addOrSub(self, exp):
        #�Ӽ���
        exp_sum = 0
        while True:
            exp_res = re.findall(r"-?\d+(?:\.\d+)?", exp)
            if exp_res:
                for i in exp_res:
                    exp_sum += float(i)
                return exp_sum

    def brackets(self, exp):
        #ѭ�������Ƿ�������
        while True:
            exp_res = re.search(r"\([^()]+\)", exp)#����û������,�������е����������
            if exp_res:#��������ʱ
                exp_group = exp_res.group()#���ŵ����ݣ���������
                new_num = self.mulOrDiv(exp_group)
                new_num = self.addOrSub(new_num)
                exp = exp.replace(exp_group, str(new_num))#����������ַ�����������������������
            else:#���û������ ��ֱ���׳�������
                num = self.mulOrDiv(exp)
                num = self.addOrSub(num)
                return num

    def crea_clear(self):
        #�������������˫�������������д��ť�����߸������ε��ʱ���ж��Ƿ�˫��������ûд
        self.input_tex.clear()

    def crea_clipboard(self):
        #��osģ��ѵ���ճ����windows��ճ����
        tex = self.output_tex.toPlainText()
        com = 'echo | set /p unl = ' + tex.strip() + '| clip'
        os.system(com)
        print '����{}�Ѹ��Ƶ�ճ���塣'.format(tex)

    def wnd_close(self):
        self.close()
        print '�������رա�'
        self.deleteLater()


if __name__ == '__main__':
    try:
        a.wnd_close()
    except:
        pass

    a = Calculator()
    a.show()