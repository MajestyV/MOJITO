import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from MOJITO import AnaData, VisualizeSCI

# AD = AnaData.anda()  # 调用AnaData模块
VI = VisualizeSCI.plot()  # 调用VisualizeSCI模块

class Test:
    ''' This is a class of test functions. '''
    def __init__(self):
        self.name = Test

    def Lorentzian(self,x,param):
        xc, w, A = param
        return (2*A/np.pi)*(w/(4.0*(x-xc)**2+w**2))

    def Lorentzian_sum(self,x,param_set):
        num_curve = len(param_set)
        Lorentzian_array = np.array([self.Lorentzian(x,param_set[i]) for i in range(num_curve)])
        print(Lorentzian_array)
        return np.sum(Lorentzian_array,axis=0)

if __name__ == '__main__':
    data_index = 2
    x_range = (610,900)
    y_range = (500,1300)

    tt = Test()  # 调用Test函数类

    data_directory = 'D:/OneDrive/OneDrive - The Chinese University of Hong Kong/Desktop/PL/Raw data/'
    file_name = ['0V', '15V', '40V']
    data_file = data_directory+file_name[data_index]+'.xlsx'  # 指定数据文件绝对地址

    ########################################################################################################
    # 提取实验测试数据
    data_DataFrame = pd.read_excel(data_file, header=None, sheet_name='Sheet1')
    data_array = data_DataFrame.values  # 将DataFrame格式的数据转换为数组
    wavelength, intensity = (data_array[:, 0], data_array[:, 1])  # 第一列为波长，第二列为发光强度

    ########################################################################################################
    # Origin拟合结果
    fitting_result = {'0V': [[624.65, 62.47, 89431.97],
                             [687.16, 22.90, 4605.55],
                             [707.31, 43.05, 10383.89],
                             [749.54, 152.33, 31419.87]],
                      '15V':[[624.24, 56.80, 63133.51],
                             [694.82, 47.39, 13223.57],
                             [745.69, 142.20, 27768.34]],
                      '40V':[[625.07, 55.67, 46403.03],
                             [693.93, 49.40, 12821.72],
                             [750.42, 146.88, 28900.64]]}
    baseline = {'0V': 598.82, '15V': 616.17, '40V': 619.60}

    ########################################################################################################
    # 画图模块
    color_list_data = [VI.MorandiColor('Pink'), VI.MorandiColor('Spring'), VI.MorandiColor('Lightblue')]
    color_list_fitting = [VI.MorandiColor('Redred'), VI.MorandiColor('Forrest'), VI.MorandiColor('Paris')]

    VI.GlobalSetting(x_major_tick=75, y_major_tick=200)  # 载入画图的全局变量

    plt.scatter(wavelength,intensity,c=color_list_data[data_index],s=0.1,label='Experimental result')  # 可视化实验结果

    # 可视化拟合结果
    fitting_param = fitting_result[file_name[data_index]]
    baseline = baseline[file_name[data_index]]

    x = np.linspace(x_range[0], x_range[1], 500)
    y = tt.Lorentzian_sum(x,fitting_param)+baseline
    plt.plot(x,y,c=color_list_fitting[data_index],label='Fitting result')  # 可视化拟合总和

    color_list_components = [np.array([255,0,255])/255.0, np.array([0,255,255])/255.0, np.array([0,0,255])/255.0, np.array([0,255,0])/255.0]
    for i in range(len(fitting_param)):
        y0 = tt.Lorentzian(x,fitting_param[i])+baseline
        plt.plot(x, y0, c=color_list_components[i])  # 可视化拟合组分

    VI.FigureSetting(legend='True', xlim=x_range, ylim=y_range,xlabel=r'Wavelength (nm)', ylabel='Intensity (a.u.)')
    #plt.xlim(x_range[0],x_range[1])
    #plt.ylim(y_range[0],y_range[1])

    saving_directory = 'D:/OneDrive/OneDrive - The Chinese University of Hong Kong/Desktop/PL/Result/'  # 宿舍电脑汇总
    VI.SavingFigure(saving_directory, filename='InSituPL_'+file_name[data_index], format='pdf')
    VI.SavingFigure(saving_directory, filename='InSituPL_'+file_name[data_index], format='eps')

