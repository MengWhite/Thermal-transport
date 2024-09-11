import sys
import os
import numpy as np
import ovito
sys.path.append("../..")
os.environ['OVITO_GUI_MODE'] = '1'
from PySide6.QtWidgets import QMainWindow
from GUI.MainWindow_GUI import Ui_MainWindow
from GUI.ChildWindow_1 import Ui_Form as Ui_Form_1
from GUI.ChildWindow_2 import Ui_Form as Ui_Form_2
from melolular_dynamics.lammps_calculation import Work
from output import lattice_set, render_3d, read_datafile
from output.plot_2d import plot_2d
from output.plot_2d import background
from output.plot_2d import fit_plot
from output.plot_2d import plot_scatter
from initial.create_eam import create_eam
from initial.vacf_pdos import find_pdos
import webbrowser
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.childwindow_1 = ChildMaindow_1()
        self.childwindow_2 = ChildMaindow_2()
        self.action_set_1.triggered.connect(self.childwindow_1.show)
        self.action_set_2.triggered.connect(self.childwindow_2.show)
        self.action_save.triggered.connect(self.save_file)
        self.setting()
        self.childwindow_1.exp1_arg_pushButton.clicked.connect(self.recommend_experiment_1)
        self.childwindow_2.exp2_arg_pushButton.clicked.connect(self.recommend_experiment_2)
        self.childwindow_1.finish.clicked.connect(self.start_main_1)
        self.childwindow_2.finish.clicked.connect(self.start_main_2)
        # self.gap_checkBox_2.clicked.connect(self.set_occupancy)
        # self.zon_tem_checkBox_2.clicked.connect(self.set_tempareture_display)
        # self.vacant_checkBox.clicked.connect(self.set_vacancy)
        # self.exp2_arg_pushButton_2.clicked.connect(self.save_file)
        # self.exp2_arg_pushButton_3.clicked.connect(self.help_doc)     

    def setting(self):
        self.atom_all = ["Cu", "Ag", "Au", "Ni", "Pd", "Pt", "Al", "Pb", "Fe", "Mo", "Ta", "W"]
        self.atomic_mass = ['63.546', '107.87', '196.97', '58.693', '106.42', '195.08', 
                            '26.982', '207.2', '55.845','95.95', '180.95', '183.84']
        # 子窗口一
        self.childwindow_1.exp1_ele1_comboBox.addItems(self.atom_all)
        self.childwindow_1.exp1_ele1_comboBox.setCurrentIndex(-1)
        self.childwindow_1.exp1_ele1x_lineEdit.setText('0')
        self.childwindow_1.exp1_ele1y_lineEdit.setText('0')
        self.childwindow_1.exp1_ele1z_lineEdit.setText('0')
        self.childwindow_1.rel_tem_lineEdit.setText('0')
        self.childwindow_1.rel_tem_lineEdit_2.setText('0')
        self.childwindow_1.rel_sys_comboBox.addItem('nvt')
        self.childwindow_1.rel_sys_comboBox.addItem('nve')
        self.childwindow_1.rel_tim_lineEdiT.setText('0')
        self.childwindow_1.Them_lineEdit.setText('0')
        self.childwindow_1.Them_sys_lineEdit.setText('nve')
        self.childwindow_1.defect_lineEdit.setText('0')
        self.childwindow_1.Them_tim_lineEdit.setText('0')
        self.childwindow_1.Them_sys_lineEdit.setText('nve')
        # 子窗口二
        self.childwindow_2.exp2_ele1_comboBox.addItems(self.atom_all)
        self.childwindow_2.exp2_ele1_comboBox.setCurrentIndex(-1)
        self.childwindow_2.exp2_ele1x_lineEdit.setText('0')
        self.childwindow_2.exp2_ele1y_lineEdit.setText('0')
        self.childwindow_2.exp2_ele1z_lineEdit.setText('0')
        self.childwindow_2.exp2_ele2_comboBox.addItems(self.atom_all)
        self.childwindow_2.exp2_ele2_comboBox.setCurrentIndex(-1)
        self.childwindow_2.exp2_ele2x_lineEdit.setText('0')
        self.childwindow_2.exp2_ele2y_lineEdit.setText('0')
        self.childwindow_2.exp2_ele2z_lineEdit.setText('0')
        self.childwindow_2.exp2_ele1_comboBox.setCurrentIndex(-1)
        self.childwindow_2.exp2_ele2_comboBox.setCurrentIndex(-1)
        self.childwindow_2.rel_tem_lineEdit.setText('0')
        self.childwindow_2.rel_tem_lineEdit_2.setText('0')
        self.childwindow_2.rel_sys_comboBox.addItem('nvt')
        self.childwindow_2.rel_sys_comboBox.addItem('nve')
        self.childwindow_2.rel_tim_lineEdiT.setText('0')
        self.childwindow_2.Them_lineEdit.setText('0')
        self.childwindow_2.Them_sys_lineEdit.setText('nve')
        self.childwindow_2.defect_lineEdit.setText('0')
        self.childwindow_2.Them_tim_lineEdit.setText('0')
        self.childwindow_2.Them_sys_lineEdit.setText('nve')
        cav = background('time/ps', 'num')
        self.verticalLayout_2.addWidget(cav)
        cav = background('time/ps', 'num')
        self.verticalLayout_3.addWidget(cav)
        cav = background('time/ps', 'num')
        self.verticalLayout_4.addWidget(cav)

    def recommend_experiment_1(self):
        self.childwindow_1.exp1_ele1_comboBox.setCurrentIndex(0)
        self.childwindow_1.exp1_ele1x_lineEdit.setText('100')
        self.childwindow_1.exp1_ele1y_lineEdit.setText('4')
        self.childwindow_1.exp1_ele1z_lineEdit.setText('4')
        self.childwindow_1.defect_lineEdit.setText('0')
        self.childwindow_1.rel_tem_lineEdit.setText('300')
        self.childwindow_1.rel_tem_lineEdit_2.setText('300')
        self.childwindow_1.rel_sys_comboBox.setCurrentIndex(0)
        self.childwindow_1.rel_tim_lineEdiT.setText('10')
        self.childwindow_1.Them_lineEdit.setText('1.64')
        self.childwindow_1.Them_tim_lineEdit.setText('25')

    def recommend_experiment_2(self):
        self.childwindow_2.exp2_ele1_comboBox.setCurrentIndex(0)
        self.childwindow_2.exp2_ele2_comboBox.setCurrentIndex(3)
        self.childwindow_2.exp2_ele1x_lineEdit.setText('30')
        self.childwindow_2.exp2_ele1y_lineEdit.setText('10')
        self.childwindow_2.exp2_ele1z_lineEdit.setText('10')
        self.childwindow_2.exp2_ele2x_lineEdit.setText('30')
        self.childwindow_2.exp2_ele2y_lineEdit.setText('10')
        self.childwindow_2.exp2_ele2z_lineEdit.setText('10')
        self.childwindow_2.defect_lineEdit.setText('0')
        self.childwindow_2.rel_tem_lineEdit.setText('300')
        self.childwindow_2.rel_tem_lineEdit_2.setText('300')
        self.childwindow_2.rel_sys_comboBox.setCurrentIndex(0)
        self.childwindow_2.rel_tim_lineEdiT.setText('10')
        self.childwindow_2.Them_lineEdit.setText('8')
        self.childwindow_2.Them_tim_lineEdit.setText('40')

    def start_main_1(self):
        self.childwindow_1.close()
        self.label.setText("材料热导率")
        self.label_2.setText("W*K-1*m-1")
        # 清除结果文件内容
        with open('result_iterate.txt', 'w') as f:
            f.truncate(0)
        with open('result_heat_1.txt', 'w') as f:
            f.truncate(0)
        with open('result_heat_2.txt', 'w') as f:
            f.truncate(0)
        with open('result_pdos.txt', 'w') as f:
            f.truncate(0)
        # 读取GUI数据
        self.element1 = self.childwindow_1.exp1_ele1_comboBox.currentText()
        defect_num = int(self.childwindow_1.defect_lineEdit.text())
        size1 = [int(self.childwindow_1.exp1_ele1x_lineEdit.text()), int(self.childwindow_1.exp1_ele1y_lineEdit.text()), int(self.childwindow_1.exp1_ele1z_lineEdit.text())]
        # 建立晶体数据文件
        lattice_set(element1=self.element1, size1=size1)
        render_3d.set_file('data\lattice.lmp')
        create_eam([self.element1])

        filepath = 'data\lattice.lmp'
        self.atom_num = read_datafile('data\lattice.lmp').atom_num
        temperature_set = float(self.childwindow_1.rel_tem_lineEdit_2.text())
        temperature_0 = float(self.childwindow_1.rel_tem_lineEdit.text())
        iterate_time = float(float(self.childwindow_1.rel_tim_lineEdiT.text()))
        ensemble_name = self.childwindow_1.rel_sys_comboBox.currentText()
        heat = float(self.childwindow_1.Them_lineEdit.text())
        self.iterate_time_heat = float(float(self.childwindow_1.Them_tim_lineEdit.text()))
        ensemble_name_1 = self.childwindow_1.Them_sys_lineEdit.text()
        self.t = Work(filepath, temperature_0, temperature_set,
                        iterate_time, ensemble_name, ensemble_name_1, heat, 
                        self.iterate_time_heat, defect_num, self.x, element1=self.element1)
        self.t.signal.connect(self.plot_1)
        self.t.start()
    
    def start_main_2(self):
        self.childwindow_2.close()
        self.label.setText("界面热导")
        self.label_2.setText("W*K-1*m-2")
        # 清除画布
        if self.verticalLayout_2.itemAt(0) != None:
            self.verticalLayout_2.itemAt(0).widget().deleteLater()
        if self.verticalLayout_3.itemAt(0) != None:
            self.verticalLayout_3.itemAt(0).widget().deleteLater()
        if self.verticalLayout_4.itemAt(0) != None:
            self.verticalLayout_4.itemAt(0).widget().deleteLater()
        # 清除结果文件内容
        with open('result_iterate.txt', 'w') as f:
            f.truncate(0)
        with open('result_heat_1.txt', 'w') as f:
            f.truncate(0)
        with open('result_heat_2.txt', 'w') as f:
            f.truncate(0)
        with open('result_pdos.txt', 'w') as f:
            f.truncate(0)
        # 读取GUI数据
        self.element2 = self.childwindow_2.exp2_ele1_comboBox.currentText()
        self.element3 = self.childwindow_2.exp2_ele2_comboBox.currentText()
        defect_num = int(self.childwindow_2.defect_lineEdit.text())
        size2 = [int(self.childwindow_2.exp2_ele1x_lineEdit.text()), int(self.childwindow_2.exp2_ele1y_lineEdit.text()), int(self.childwindow_2.exp2_ele1z_lineEdit.text())]
        size3 = [int(self.childwindow_2.exp2_ele2x_lineEdit.text()), int(self.childwindow_2.exp2_ele2y_lineEdit.text()), int(self.childwindow_2.exp2_ele2z_lineEdit.text())]
        # 建立晶体数据文件
        self.x = lattice_set(element2=self.element2, element3=self.element3, size2=size2, size3=size3)
        render_3d.set_file('data\lattice.lmp')
        # 体系参数填入
        create_eam([self.element2, self.element3])
        self.atom_num_1 = read_datafile('data\lattice_1.lmp').atom_num
        self.atom_num_2 = read_datafile('data\lattice_2.lmp').atom_num
        # 读取计算所需内容
        filepath = 'data\lattice.lmp'
        temperature0 = float(self.childwindow_2.rel_tem_lineEdit_2.text())
        temperature_set = float(self.childwindow_2.rel_tem_lineEdit.text())
        iterate_time = float(float(self.childwindow_2.rel_tim_lineEdiT.text()))
        ensemble_name = self.childwindow_2.rel_sys_comboBox.currentText()
        heat = float(self.childwindow_2.Them_lineEdit.text())
        self.iterate_time_heat = float(float(self.childwindow_2.Them_tim_lineEdit.text()))
        ensemble_name_1 = self.childwindow_2.Them_sys_lineEdit.text()
        self.t = Work(filepath, temperature0, temperature_set,
                        iterate_time, ensemble_name, ensemble_name_1, heat, 
                        self.iterate_time_heat, defect_num, self.x, element2=self.element2, element3=self.element3)
        self.t.signal.connect(self.plot_2)
        self.t.signal_2.connect(self.plot_2)
        self.t.start()
    
    def stop_main(self):
        self.t.terminate()
        self.t.wait()

    def help_doc(self):
        webbrowser.open('data\软件帮助手册.pdf', new=2)
    
    def plot_1(self):
        if self.verticalLayout_2.itemAt(0) != None: # 清空T-Time图像，防止暂停时重复绘图
            self.verticalLayout_2.itemAt(0).widget().deleteLater()
        if self.verticalLayout_3.itemAt(0) != None:
            self.verticalLayout_3.itemAt(0).widget().deleteLater()
        if self.verticalLayout_4.itemAt(0) != None:
            self.verticalLayout_4.itemAt(0).widget().deleteLater()
        self.clear_GUI()
        self.exp_res_lineEdit_2.setText(str(round(float(self.t.T_conduct), 1)))
        # 数据文件x轴最大值
        with open('data/lattice.lmp', 'r') as f:
            line = f.readline()
            while line.find('xlo') == -1:
                line = f.readline()
        data = line.split()
        lattice_x_max_1 = data[1]

        if os.path.isfile('data/' + self.element1 + '.eam.alloy'):
            os.remove('data/' + self.element1 + '.eam.alloy')

        # 绘制弛豫温度与三维坐标图
        self.iterate_x = []
        self.iterate_y = []
        with open('result_iterate.txt', 'r') as f:
            f.seek(0, 2)
            eof = f.tell()
            f.seek(0, 0)  #移到文件头
            line = f.readline()
            line = f.readline()
            while True:
                line = f.readline()
                data = line.split()
                self.iterate_x.append(float(data[0]))
                self.iterate_y.append(float(data[1]))
                if f.tell() >= eof:  #将当前位置与文件尾(eof)比较
                    break
        if len(self.iterate_x) != 0:
            cav = plot_2d(np.array(self.iterate_x) * 1e-2, np.array(self.iterate_y), 'Time/ps', 'Temperature/K')
            self.verticalLayout_2.addWidget(cav)
        render_3d.set_file('data\lattice.dump')

        # 绘制体系区域温度
        self.heat_x_1 = []
        self.heat_y_1 = []
        self.heat_x_2 = []
        self.heat_y_2 = []
        with open('result_heat_1.txt', 'r') as f:
            line = f.readlines()
            line_final = line[-20:][:]
            for i in range(len(line_final)):
                data = line_final[i].split()
                self.heat_x_1.append(float(data[0]) * float(lattice_x_max_1)/20)
                self.heat_y_1.append(float(data[3]))
        if len(self.heat_x_1) != 0:
            cav = fit_plot(np.array(self.heat_x_1), np.array(self.heat_y_1),  'X/Å', 'Temperature/K', bar='yes', ymin=min(self.heat_y_1), ymax=max(self.heat_y_1))
            self.verticalLayout_3.addWidget(cav)

        #绘制声子态密度曲线
        veclocity = np.zeros((int(self.iterate_time_heat*100), self.atom_num, 3))
        with open('result_pdos.txt', 'r') as f:
            for i in range(int(self.iterate_time_heat*100)):
                for j in range(9):
                    line = f.readline()
                for k in range(self.atom_num):
                    line = list(map(str, f.readline().split(' ')))
                    if line != ['']:
                        veclocity[i, k] = line.pop(0)
        omega = np.arange(1, 380.5, 0.5)
        vacf_output, pdos = find_pdos(veclocity, 100, dt = 0.001, omega = omega)
        self.pdos_x = omega
        self.pdos_y = pdos
        cav = plot_2d(self.pdos_x, self.pdos_y, 'Omega/THZ', 'PDOS')
        self.verticalLayout_4.addWidget(cav)

    def plot_2(self):
        if self.verticalLayout_2.itemAt(0) != None: # 清空T-Time图像，防止暂停时重复绘图
            self.verticalLayout_2.itemAt(0).widget().deleteLater()
        if self.verticalLayout_3.itemAt(0) != None:
            self.verticalLayout_3.itemAt(0).widget().deleteLater()
        if self.verticalLayout_4.itemAt(0) != None:
            self.verticalLayout_4.itemAt(0).widget().deleteLater()
        self.clear_GUI()
        self.exp_res_lineEdit_2.setText(str(round(float(self.t.T_conduct), 1)))
        # 数据文件x轴最大值
        with open('data/lattice.lmp', 'r') as f:
            line = f.readline()
            while line.find('xlo') == -1:
                line = f.readline()
        data = line.split()
        lattice_x_max_1 = data[1]
        if os.path.isfile('data/' + self.element2 + self.element3+ '.eam.alloy'):
            os.remove('data/' + self.element2 + self.element3+ '.eam.alloy')
        # 绘制弛豫温度与三维坐标图
        self.iterate_x = []
        self.iterate_y = []
        with open('result_iterate.txt', 'r') as f:
            f.seek(0, 2)
            eof = f.tell()
            f.seek(0, 0)  #移到文件头
            line = f.readline()
            line = f.readline()
            while True:
                line = f.readline()
                data = line.split()
                self.iterate_x.append(float(data[0]))
                self.iterate_y.append(float(data[1]))
                if f.tell() >= eof:  #将当前位置与文件尾(eof)比较
                    break
        if len(self.iterate_x) != 0:
            cav = plot_2d(np.array(self.iterate_x) * 1e-2, np.array(self.iterate_y), 'Time/ps', 'Temperature/K')
            self.verticalLayout_2.addWidget(cav)
        render_3d.set_file('data\lattice.dump')

        # 绘制体系区域温度
        self.heat_x_1 = []
        self.heat_y_1 = []
        self.heat_x_2 = []
        self.heat_y_2 = []
        with open('result_heat_2.txt', 'r') as f:
            line = f.readlines()
            line_final = line[-1:][:]
            data = line_final[0].split(" ")
            data.pop(0)
            for i in range(len(data)):
                if i <= 9:
                    self.heat_x_2.append((float(self.x)/10) * i)
                    self.heat_y_2.append(float(data[i]))
                if i > 9:
                    self.heat_x_2.append(((float(lattice_x_max_1) - float(self.x))/10) * (i - 9) + self.x)
                    self.heat_y_2.append(float(data[i]))
        if len(self.heat_x_2) != 0:
            cav = plot_scatter(np.array(self.heat_x_2[9:11]), np.array(self.heat_y_2[9:11]),np.array(self.heat_x_2), np.array(self.heat_y_2),  'X/Å', 'Temperature/K', bar='yes', ymin=min(self.heat_y_2), ymax=max(self.heat_y_2))
            self.verticalLayout_3.addWidget(cav)

        #绘制声子态密度曲线
        veclocity = np.zeros((int(self.iterate_time_heat*100), self.atom_num_1+self.atom_num_2, 3))
        with open('result_pdos.txt', 'r') as f:
            for i in range(int(self.iterate_time_heat*100)):
                for j in range(9):
                    line = f.readline()
                for k in range(self.atom_num_1+self.atom_num_2):
                    line = list(map(str, f.readline().split(' ')))
                    if line != ['']:
                        veclocity[i, k] = line.pop(0)
        omega = np.arange(1, 380.5, 0.5)
        vacf_output, pdos = find_pdos(veclocity, 100, dt = 0.001, omega = omega)
        self.pdos_x = omega
        self.pdos_y = pdos
        cav = plot_2d(self.pdos_x, self.pdos_y, 'Omega/THZ', 'PDOS')
        self.verticalLayout_4.addWidget(cav)

    def set_occupancy(self):
        self.zon_tem_checkBox_2.setChecked(False)
        self.vacant_checkBox.setChecked(False)
        if self.painting_zoom.itemAt(1) != None:
            self.painting_zoom.itemAt(1).widget().deleteLater() # 删除温度条
        if not self.gap_checkBox_2.isChecked():
            render_3d.clear_modifiers()
        else:
            render_3d.set_occupancy('data/lattice.lmp')
            
    def set_tempareture_display(self):
        from output.tempareture_color_bar import create_tem_color_bar
        self.gap_checkBox_2.setChecked(False)
        self.vacant_checkBox.setChecked(False)
        if self.zon_tem_checkBox_2.isChecked() == False:
            render_3d.clear_modifiers()
            if self.painting_zoom.itemAt(1) != None:
                self.painting_zoom.itemAt(1).widget().deleteLater()
        else:
            if self.heat_y_1 != []:
                render_3d.set_color_by_tempareture(self.heat_y_1)
                self.painting_zoom.addWidget(create_tem_color_bar(self.heat_y_1), 1)
            if self.heat_y_2 != []:
                render_3d.set_color_by_tempareture(self.heat_y_2)
                self.painting_zoom.addWidget(create_tem_color_bar(self.heat_y_2), 1)

    def set_vacancy(self):
        self.zon_tem_checkBox_2.setChecked(False)
        self.gap_checkBox_2.setChecked(False)
        if self.painting_zoom.itemAt(1) != None:
            self.painting_zoom.itemAt(1).widget().deleteLater() # 删除温度条
        if not self.gap_checkBox_2.isChecked():
            render_3d.clear_modifiers()
        if self.vacant_checkBox.isChecked() == False:
            render_3d.clear_modifiers()
        else:
            render_3d.set_occupancy('data/lattice.lmp',True)
            
    def save_file(self):
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk()
        root.withdraw()
        Folderpath = filedialog.askdirectory()
        self.element1 = self.childwindow_2.exp2_ele1_comboBox.currentText()
        self.element2 = self.childwindow_2.exp2_ele1_comboBox.currentText()
        self.element3 = self.childwindow_2.exp2_ele2_comboBox.currentText()
        if len(self.iterate_x) != 1 and self.element2 == '':
            cav = plot_2d(np.array(self.iterate_x) * 1e-3, np.array(self.iterate_y), 'Time/ps', 'Temperature/K', savename='体系温度曲线_单元素', save_path=Folderpath)
        else:
            if os.path.isfile(Folderpath + '/体系温度曲线_单元素.png'):
                os.remove(Folderpath + '/体系温度曲线_单元素.png')
                os.remove(Folderpath + '/体系温度曲线_单元素.txt')
        if len(self.iterate_x) != 1 and self.element1 == '':
            cav = plot_2d(np.array(self.iterate_x) * 1e-3, np.array(self.iterate_y), 'Time/ps', 'Temperature/K', savename='体系温度曲线_多元素', save_path=Folderpath)
        else:
            if os.path.isfile(Folderpath + '/体系温度曲线_多元素.png'):
                os.remove(Folderpath + '/体系温度曲线_多元素.png')
                os.remove(Folderpath + '/体系温度曲线_多元素.txt')
        if len(self.heat_x_1) != 0 and self.element2 == '':
            cav = fit_plot(np.array(self.heat_x_1), np.array(self.heat_y_1), 'X/Å', 'Temperature/K', bar='yes', ymin=min(self.heat_y_1), ymax=max(self.heat_y_1), savename='体系区域温度_单元素', save_path=Folderpath)
        else:
            if os.path.isfile(Folderpath + '/体系区域温度_单元素.png'):
                os.remove(Folderpath + '/体系区域温度_单元素.png')
                os.remove(Folderpath + '/体系区域温度_单元素.txt')
        if len(self.heat_x_2) != 0 and self.element1 == '':
            cav = plot_scatter(np.array(self.heat_x_2[9:11]), np.array(self.heat_y_2[9:11]),np.array(self.heat_x_2), np.array(self.heat_y_2), 'X/Å', 'Temperature/K', savename='体系区域温度_多元素', save_path=Folderpath, bar='yes')
        else:
            if os.path.isfile(Folderpath + '/体系区域温度_多元素.png'):
                os.remove(Folderpath + '/体系区域温度_多元素.png')
                os.remove(Folderpath + '/体系区域温度_多元素.txt')
        # if len(self.t.omega) != 0 and self.exp2_radioButton.isChecked():    # 保证暂停时不绘图
        #     cav = plot_2d(self.t.omega, self.t.pdos, 'Omega', 'Pdos', 'Pdos', '声子态密度曲线_多元素', Folderpath)
        # else:
        #     if os.path.isfile(Folderpath + '/声子态密度曲线_多元素.png'):
        #         os.remove(Folderpath + '/声子态密度曲线_多元素.png')
        #         os.remove(Folderpath + '/声子态密度曲线_多元素.txt')
        if self.heat_y_1 != []:
            render_3d.render_png(
                filename=Folderpath + '/晶体原子3D渲染图.png', 
                reference_file='data/lattice.lmp',
                tempareture=self.heat_y_1
                )
        else:
            render_3d.render_png(
                filename=Folderpath + '/晶体原子3D渲染图.png', 
                reference_file='data/lattice.lmp',
                tempareture=self.heat_y_2
                )

    def clear_GUI(self):
        self.childwindow_1.exp1_ele1_comboBox.setCurrentIndex(-1)
        self.childwindow_1.exp1_ele1x_lineEdit.setText('0')
        self.childwindow_1.exp1_ele1y_lineEdit.setText('0')
        self.childwindow_1.exp1_ele1z_lineEdit.setText('0')
        self.childwindow_1.rel_tem_lineEdit.setText('0')
        self.childwindow_1.rel_tem_lineEdit_2.setText('0')
        self.childwindow_1.rel_sys_comboBox.addItem('nvt')
        self.childwindow_1.rel_sys_comboBox.addItem('nve')
        self.childwindow_1.rel_tim_lineEdiT.setText('0')
        self.childwindow_1.Them_lineEdit.setText('0')
        self.childwindow_1.Them_sys_lineEdit.setText('nve')
        self.childwindow_1.defect_lineEdit.setText('0')
        self.childwindow_1.Them_tim_lineEdit.setText('0')
        self.childwindow_1.Them_sys_lineEdit.setText('nve')
        self.childwindow_2.exp2_ele1_comboBox.setCurrentIndex(-1)
        self.childwindow_2.exp2_ele1x_lineEdit.setText('0')
        self.childwindow_2.exp2_ele1y_lineEdit.setText('0')
        self.childwindow_2.exp2_ele1z_lineEdit.setText('0')
        self.childwindow_2.exp2_ele2_comboBox.setCurrentIndex(-1)
        self.childwindow_2.exp2_ele2x_lineEdit.setText('0')
        self.childwindow_2.exp2_ele2y_lineEdit.setText('0')
        self.childwindow_2.exp2_ele2z_lineEdit.setText('0')
        self.childwindow_2.exp2_ele1_comboBox.setCurrentIndex(-1)
        self.childwindow_2.exp2_ele2_comboBox.setCurrentIndex(-1)
        self.childwindow_2.rel_tem_lineEdit.setText('0')
        self.childwindow_2.rel_tem_lineEdit_2.setText('0')
        self.childwindow_2.rel_sys_comboBox.addItem('nvt')
        self.childwindow_2.rel_sys_comboBox.addItem('nve')
        self.childwindow_2.rel_tim_lineEdiT.setText('0')
        self.childwindow_2.Them_lineEdit.setText('0')
        self.childwindow_2.Them_sys_lineEdit.setText('nve')
        self.childwindow_2.defect_lineEdit.setText('0')
        self.childwindow_2.Them_tim_lineEdit.setText('0')
        self.childwindow_2.Them_sys_lineEdit.setText('nve')

class ChildMaindow_1(QMainWindow, Ui_Form_1):
    def __init__(self):
        super(ChildMaindow_1, self).__init__()
        self.setupUi(self)

class ChildMaindow_2(QMainWindow, Ui_Form_2):
    def __init__(self):
        super(ChildMaindow_2, self).__init__()
        self.setupUi(self)