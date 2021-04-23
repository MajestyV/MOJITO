import numpy as np
# import scipy as sp
import matplotlib.pyplot as plt
from scipy.optimize import leastsq
from MOJITO import GetSpectra

pi = np.pi
def ln(x): return np.log(x)
def exp(x): return np.exp(x)

class anda:
    """ This class of functions is designed to help analysis the spectra. """
    #  为了单位尺度的统一，在这个函数包中，我们一律采用角频率w作为自变量以方便使用de Broglie relations进行角频率-能量转换(E=hbar*w)

    def __init__(self):
        self.name = anda

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
    gd = GetSpectra.geda()
    ad = anda()

    # data_directory = "D:/OneDrive/OneDrive - The Chinese University of Hong Kong/Desktop/Testing/GetData/B1-Raman.txt"
    data_directory = "D:/Projects/PhaseTransistor/DataGallery/2021-04-14-Characterizations/Raman_PL/2021-04-14/"
    data_file = 'D1-Raman.txt'
    data = gd.Extract(data_directory+data_file, output_mode='original data')
    data = gd.Range(data,340,450)
    data = gd.Rearrange(data)

    # print(gd.Extract(data_directory,output_mode='data'))
    # print(gd.Extract(data_directory,output_mode='original data'))
    # print(gd.Extract(data_directory,output_mode='testing parameters'))
    # print(gd.Range(data,350,450))
    #print(data)
    #print(gd.Visualize(data, xlim=(350, 450), ylim=(150, 250)))
    # print(ad.Fitting(data,num_peaks=2,param=[[380,1,1],[410,1,1]],mode='Lorentzian'))

    Para = ad.Fitting(data,num_peaks=2,param=[[380,10,90],[410,10,300]],mode='Lorentzian',baseline=50)
    print(Para)
    def FittedCurve(x):
        w1, gamma1, i1 = Para[0]
        w2, gamma2, i2 = Para[1]
        f1 = i1*(gamma1/2)/(pi*((x-w1)**2+(gamma1/2)**2))
        f2 = i2 * (gamma2 / 2) / (pi * ((x - w2) ** 2 + (gamma2 / 2) ** 2))
        # f3 = i3 * (gamma3 / 2) / (pi * ((x - w3) ** 2 + (gamma3 / 2) ** 2))
        return f1+f2
    x0 = np.linspace(340,450,500)
    y0 = ad.Fitted_curve(x0,Para,2,50,'Lorentzian')
    print(y0)
    plt.plot(x0,y0)


    # plt.plot(x0,FittedCurve(x0))
    #plt.plot(data[0],data[1])

