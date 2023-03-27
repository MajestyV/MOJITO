import numpy as np
import pandas as pd
# import scipy as sp
import matplotlib.pyplot as plt
from scipy.optimize import leastsq
from MOJITO import Visualize

VI = Visualize.plot()

pi = np.pi
def ln(x): return np.log(x)
def exp(x): return np.exp(x)

class anda:
    """ This class of functions is designed to help analysis the spectra. """
    #  为了单位尺度的统一，在这个函数包中，我们一律采用角频率w作为自变量以方便使用de Broglie relations进行角频率-能量转换(E=hbar*w)

    def __init__(self):
        self.name = anda

    # 数据提取模块
    # 此函数可以利用pandas提取excel文件中的测试数据
    def GetExcelData(self, data_file, **kwargs):
        # 一些关于数据文件的参数
        header = kwargs['header'] if 'header' in kwargs else None  # 文件中的数据列，默认为没有列名，第一行作为数据读取
        # 设置sheet_name=None，可以读取全部的sheet，返回字典，key为sheet名字，value为sheet表内容
        sheet_name = kwargs['sheet_name'] if 'sheet_name' in kwargs else 'Sheet1'
        x_col = kwargs['x_col'] if 'x_col' in kwargs else 0  # 默认第一列为自变量所在列
        y_col = kwargs['y_col'] if 'y_col' in kwargs else 1  # 默认第二列为因变量所在列

        # 利用pandas提取数据，得到的结果为DataFrame格式
        data_DataFrame = pd.read_excel(data_file, header=header, sheet_name=sheet_name)
        # data_DataFrame = pd.read_csv(data_file, header=header)  # 若header=None的话，则设置为没有列名
        data_array = data_DataFrame.values  # 将DataFrame格式的数据转换为数组
        wavelength = data_array[:, x_col]  # 自变量所在列为波长
        intensity = data_array[:, y_col]  # 因变量所在列为强度

        return wavelength, intensity

    # 采用了跟粒子激发态寿命导致的自然致宽相关的洛伦兹分布：L(v) = (1/pi)*gamma/[4*pi**2*(v-v0)**2+(gamma/w)**2], w = 2*pi*v, tau = 1/gamma
    def Lorentzaian(self,w,param):
        w0, gamma, intensity = param  # w0是峰位，gamma是半峰全宽（FWHM），tau = 1/gamma是寿命
        return intensity*(gamma/2.0)/(pi*((w-w0)**2+(gamma/2.0)**2))

    # 跟粒子碰撞相关的多普勒致宽的高斯分布：G(v) = np.sqrt(ln(2)/pi)*exp(-(v-v0)**2/(2*sigma**2))/sigma, sigma是高斯分布的方差
    def Gaussian(self,w,param):
        w0, alpha, intensity = param  # w0是峰位，alpha是半峰全宽（FWHM），高斯分布的方差sigma = alpha/2*np.sqrt(2*ln(2))
        return np.array([intensity*np.sqrt(ln(2)/pi)*(2.0/alpha)*exp(-(2*pi*w[i]-2*pi*w0)**2*ln(2)*(2.0/alpha)**2) for i in range(len(w))])

    # Voigt函数是高斯分布跟洛伦兹分布的卷积，这条函数假设两种组分有着同样的峰位
    def Voigt(self,w,param):
        w0, gamma, alpha, intensity = param
        Lw = self.Lorentzaian(w,[w0,gamma])
        Gw = self.Gaussian(w,[w0,alpha])
        return np.convolve(Lw,Gw,'same')

    def function(self,function_name):
        function_dict = {'Lorentzian':self.Lorentzaian,
                         'Gaussian':self.Gaussian,
                         'Voigt':self.Voigt}
        nparam_dict = {'Lorentzian':3,
                       'Gaussian':3,
                       'Voigt':4}
        return function_dict[function_name],nparam_dict[function_name]

    # Fitting Module

    # 背景基线函数
    # def Baseline(self,x,baseline): return baseline

    def hypothesis_func(self,param_set,x,num_peaks,num_param,baseline,mode):
        func = baseline
        param_list = np.copy(param_set)
        param = np.zeros((num_param), dtype=float)  # num_param会比调用标准波形函数的参数个数多1个，因为最后一位是强度参数，而标准函数的强度固定，不考虑强度变化
        for i in range(num_peaks):
            for j in range(num_param):
                param[j] = param_list[i*num_param+j]
            func += self.function(mode)[0](x,param)
            # print(param)
        return func

    def Error(self,param_set,x,y,num_peaks,num_param,baseline,mode):
        return y-self.hypothesis_func(param_set,x,num_peaks,num_param,baseline,mode)

    # 计算拟合用的函数与测试结果的误差
    # def Error(self,x,y,num_peaks):
        # return

    # 需拟合的原始数据的输入形式应为：[[x0, x1, x2......], [y0, y1, y2......]]
    def Fitting(self,Datum,**kwargs):
        x, y = Datum

        if 'num_peaks' in kwargs:
            npeaks_range = [kwargs['num_peaks']]
        else:
            if 'num_peaks search range' in kwargs:
                npeaks_range = list(range(kwargs['num_peaks search range']))
            else:
                npeaks_range = list(range(0,10))

        mode = kwargs['mode'] if 'mode' in kwargs else 'Voigt'  # 决定用于拟合的函数线型
        num_param = self.function(mode)[1]  # 单个波形函数的参数个数
        baseline = kwargs['baseline'] if 'baseline' in kwargs else 0  # 函数的基线，用于数据在y轴方向有平移的情况

        fitted_param = None
        for n in range(len(npeaks_range)):
            num_peaks = npeaks_range[n]
            #print(num_peaks)
            # 输入应为[[函数1的参数1, 函数1的参数2], [函数2的参数1, 函数2的参数2], [函数3的参数1, 函数3的参数2]......]
            # nparam+1的1为强度参数，Intensity（因为所有预设函数都是分布函数的形式，积分为1）
            initial_param = kwargs['param'] if 'param' in kwargs else [[1]*(num_param)]*num_peaks
            initial_param = np.array([initial_param[i][j] for i in range(num_peaks) for j in range(num_param)])
            # 把出入参数解压成[函数1的参数1, 函数1的参数2, 函数2的参数1, 函数2的参数2, 函数3的参数1, 函数3的参数2......]形式方便拟合
            # initial_param = np.array(initial_param)  # 在最开头加上基线，并将数据类型转化为数组

            #print(initial_param[6])

            fitted_param = leastsq(self.Error,initial_param,args=(x,y,num_peaks,num_param,baseline,mode))

        num_peaks = int(len(fitted_param[0])/num_param)  # 计算最终确定的峰的个数
        fitted_result = fitted_param[0]
        fitted_result = [[fitted_result[i+j*num_param] for i in range(num_param)] for j in range(num_peaks)]

        return fitted_result

    # 用于从各个波的参数复原拟合函数的函数
    def Fitted_curve(self,x,fitted_result,num_peaks,baseline,mode):
        y_list = []
        for n in range(len(x)):
            y = baseline
            for m in range(num_peaks):
                y += self.function(mode)[0](x[n],fitted_result[m])
            y_list.append(y)

        return np.array(y_list)

if __name__ == '__main__':
    def Rearrange(Parameters):
        param_array = np.array(Parameters)
        order = param_array[:,0]
        order.sort()
        print(order)

        param_rearranged = []
        for i in range(len(Parameters)):
            label = order[i]
            for j in range(len(Parameters)):
                if Parameters[j][0] == label:
                    param_rearranged.append(Parameters[j])
                else:
                    pass

        return np.array(param_rearranged)


    ad = anda()

    # data_directory = "D:/Projects/PhaseTransistor/Data/Figures/Photoluminescence (PL)/PL_InSitu/Data/filtered/"  # 办公室数据文件地址
    # data_directory = 'D:/Projects/PhaseTransistor/Data/PL/PL_InSitu/Data/filtered/'  # 宿舍数据文件夹地址
    data_directory = '/Users/liusongwei/InSituPL/'

    file_name = ['0V.xlsx', '15V.xlsx', '40V.xlsx']
    # file_name = ['0V.xlsx','40V.xlsx']

    data_file = data_directory+file_name[0]
    data = ad.GetExcelData(data_file)

    # wmin, wmax = (610,650)
    # wmin, wmax = (675, 725)
    wmin, wmax = (610,900)

    w, l = [[],[]]
    for i in range(len(data[0])):
        if data[0][i] >= wmin and data[0][i] <=wmax:
            w.append(data[0][i])
            l.append(data[1][i])
    data = np.array([w,l])

    wavelength, intensity = data

    plt.plot(wavelength,intensity,c=VI.MorandiColor('Redred'))

    #wavelength, intensity = [[], []]
    #for n in file_name:
        #data_file = data_directory + n
        #x, y = ad.GetExcelData(data_file)
        #wavelength.append(x)
        #intensity.append(y)

    # print(wavelength,intensity)


    baseline = 660
    num_peaks = 5
    mode = 'Lorentzian'
    # Para = ad.Fitting(data, num_peaks=num_peaks, param=[[627,50,1600],[685,50,900]], mode='Lorentzian', baseline=baseline)  # 2 components
    # Para = ad.Fitting(data, num_peaks=num_peaks, param=[[627, 50, 1600],[640, 50, 1400],[685, 50, 900]], mode='Lorentzian',baseline=baseline)  # 3 components
    # Para = ad.Fitting(data, num_peaks=num_peaks, param=[[627, 50, 1600],[640, 50, 1400],[660, 50, 1200],[685, 50, 900]], mode=mode,baseline=baseline)  # 4 components
    Para = ad.Fitting(data, num_peaks=num_peaks,param=[[627, 50, 1600], [640, 50, 1400], [660, 50, 1200], [800, 50, 400], [700, 50, 800]], mode='Lorentzian',baseline=baseline)  # 5 components
    # Para = ad.Fitting(data, num_peaks=num_peaks, param=[[627, 50, 1600], [685, 50, 900]], mode='Gaussian', baseline=baseline)
    # Para = ad.Fitting(data, num_peaks=num_peaks, param=[[627, 50, 50, 1600], [685, 50, 50, 900]], mode='Voigt', baseline=baseline)
    # Para = ad.Fitting(data,num_peaks=1,param=[[627,1600,70]],mode='Lorentzian',baseline=baseline)
    # Para = ad.Fitting(data, num_peaks=1, param=[[685, 900, 70]], mode='Lorentzian', baseline=baseline)
    #print(Para)

    # a = np.array(Para)[:,0]
    Para_reaaranged = Rearrange(Para)
    #print(Para_reaaranged)


    x0 = np.linspace(wmin,wmax,500)
    y0 = ad.Fitted_curve(x0,Para,num_peaks,baseline,mode)
    # print(y0)
    # plt.plot(x0,y0+baseline)
    plt.plot(x0,y0,c='#17becf')
    for i in range(len(Para_reaaranged)):
        # print(Para_reaaranged[i])
        #y0_sep = ad.Fitted_curve(x0,Para_reaaranged[i],1,baseline,mode)
        y0_sep = ad.Lorentzaian(x0, Para_reaaranged[i])
        # print(y0_sep)
        plt.plot(x0,y0_sep)

    # plt.xlim((wmin,wmax))


    # plt.plot(x0,FittedCurve(x0))
    #plt.plot(data[0],data[1])

