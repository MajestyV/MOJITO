import codecs
import re
import matplotlib.pyplot as plt

class geda:
    """ This class of functions is designed for the extraction and analysis of spectrums gathered from materials characterization. """
    # eg. X-ray Diffraction (XRD), Raman, UV-vis absorption and photoluminescence (PL)

    def __init__(self):
        self.name = geda

    # The word "Datum" (with capital "D") indicates the data list of one curves, and "Data" is data lists of multiple curves.
    # 抽取某一段范围(x_start, x_end)内的数据，输入的数据列表形式应为[[x0,y0],[x1,y1],[x2,y2]......]
    def Range(self,Datum,x_start,x_end):
        sampled_data = []
        for n in range(len(Datum)):
            if Datum[n][0] >= x_start and Datum[n][0] <= x_end:
                sampled_data.append(Datum[n])
        return sampled_data

    # 通过逐行读取txt文件中的信息得到的数据形式为[[x0,y0],[x1,y1],[x2,y2]......]，此函数可以将其重排为[[x0,x1,x2......],[y0,y1,y2......]]
    def Rearrange(self,Datum):
        return [[Datum[i][0] for i in range(len(Datum))],[Datum[j][1] for j in range(len(Datum))]]

    def Extract(self,DataFile, title_pattern="#", output_mode='data'):
        testing_parameters = []
        data = []

        file = codecs.open(DataFile, 'rb', 'utf-8', 'ignore')  # Open file, using codecs to uniform coding type
        line = file.readline()  # Read the first line
        while line:
            if re.search(title_pattern, line):
                testing_parameters.append(line)
            else:
                pattern = re.compile(r'-?\d+\.?\d+')  # 用于匹配浮点数的正则表达式
                datum = pattern.findall(line)  # 寻找这一行中所有的浮点数并提取，应注意得到的浮点数将是字符串形式
                datum = list(map(float,datum))  # 利用map函数对所有的字符串转化为浮点数，但是由于python3中map返回的是iterators类型（eg. <map object at 0x0000024897344700>）， 所以还要用list函数将其转换回列表
                data.append(datum)  # map函数十分强大，可以对序列中的所有元素调用某一函数，eg. list(map(function, iterable))可以得到[function(iterable[0]),function(iterable[1]),function(iterable[2])......]

            line = file.readline()  # Read the next line before ending the loop, keeping the loop functioning until finishing reading the whole file
        file.close()  # Closing file

        result = {'original data': data, 'data': self.Rearrange(data), 'testing parameters': testing_parameters}
        return result[output_mode]

    # Visualize module
    def Color(self,num_curves):  # 颜色序列
        color_dict = {'line_1':'#800080','line_2':'#8000ff','line_3':'#8080ff','line_4':'#00407f','line_5':'#0000ff',
                      'line_6':'#0080ff','line_7':'#00cbff','line_8':'#00c957','line_9':'#fad925','line_10':'#fe7f00',
                      'line_11':'#ff0080','line_12':'#ff0000'}
        color_sequence = list(color_dict.keys())
        return [color_dict[color_sequence[n%len(color_sequence)]] for n in range(num_curves)]

    def Seperate(self,Data,step):
        for n in range(len(Data)):
            shift = n*step
            for m in range(len(Data[n][1])):
                Data[n][1][m] = Data[n][1][m]+shift
        return Data

    # 输入形式为：Data = [测试数据列表1，测试数据列表2，测试数据列表3......]
    def Visualize(self,Data,**kwargs):
        if not isinstance(Data[0][0],list):  # 对于单个测试的数据，如果没有写成[测试数据列表]这样的形式，则对其进行格式修正
            Data = [Data]
        num_curves = len(Data)  # number of curves in the plot

        curve_label = kwargs['curve label'] if 'curve label' in kwargs else [None]*num_curves  # 默认设定不对曲线进行标注
        linewidth = kwargs['linewidth'] if 'linewidth' in kwargs else 1.0      # 曲线线宽
        linestyle = kwargs['linestyle'] if 'linestyle' in kwargs else '-'      # 曲线线型
        marker = kwargs['marker'] if 'marker' in kwargs else [None]*num_curves  # 默认设定不显示数据点
        markersize = kwargs['markersize'] if 'markersize' in kwargs else 5.0   # 控制数据点的大小
        color = kwargs['color'] if 'color' in kwargs else self.Color(num_curves)  # 曲线的颜色
        xlabel = kwargs['xlabel'] if 'xlabel' in kwargs else 'X'
        ylabel = kwargs['ylabel'] if 'ylabel' in kwargs else 'Y'
        fontsize = kwargs['fontsize'] if 'fontsize' in kwargs else 16
        title_fontsize = kwargs['title fontsize'] if 'title fontsize' in kwargs else 18
        xlim = kwargs['xlim'] if 'xlim' in kwargs else (min(Data[0][0]),max(Data[0][0]))
        ylim = kwargs['ylim'] if 'ylim' in kwargs else (min(Data[0][1]),max(Data[0][1]))

        step = kwargs['step'] if kwargs['Seperated'] == 'True' else 0
        Data = self.Seperate(Data,step)

        plt.rcParams['xtick.direction'] = 'in'
        plt.rcParams['ytick.direction'] = 'in'

        for n in range(num_curves):
            x, y = Data[n]
            plt.plot(x,y,label=curve_label[n],linewidth=linewidth,linestyle=linestyle,color=color[n],marker=marker[n],markersize=markersize)

        plt.xlabel(xlabel,fontsize=fontsize)
        plt.ylabel(ylabel,fontsize=fontsize)
        plt.xlim(xlim[0],xlim[1])
        plt.ylim(ylim[0],ylim[1])
        plt.title(kwargs['title'],fontsize=title_fontsize) if 'title' in kwargs else None

        return xlim

if __name__ == '__main__':
    gd = geda()
    data_directory = "D:/OneDrive/OneDrive - The Chinese University of Hong Kong/Desktop/Testing/GetData/D1-Raman.txt"
    data = gd.Extract(data_directory,output_mode='data')
    #print(gd.Extract(data_directory,output_mode='data'))
    #print(gd.Extract(data_directory,output_mode='original data'))
    #print(gd.Extract(data_directory,output_mode='testing parameters'))
    #print(gd.Range(data,350,450))
    print(data)
    print(gd.Visualize(data,xlim=(350,450),ylim = (150,250)))
