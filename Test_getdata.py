from MOJITO import GetSpectra

gd = GetSpectra.geda()

data_directory = "D:/Projects/PhaseTransistor/DataGallery/2021-04-14-Characterizations/Raman_PL/2021-04-14/"
data_directory2 = "D:/Projects/PhaseTransistor/DataGallery/2021-04-14-Characterizations/XRD/2021-04-15 LSW/2021-04-15 LSW/"

file_list = ['E3-Raman.txt','D3-Raman.txt','E2-Raman.txt','D2-Raman.txt','E1-Raman.txt','D1-Raman.txt']
file_list2 = ['E4_Theta_2-Theta.txt', 'C5_Theta_2-Theta.txt','B5_Theta_2-Theta.txt','A5_Theta_2-Theta.txt','C4_Theta_2-Theta.txt','B4_Theta_2-Theta.txt','A4_Theta_2-Theta.txt']

data = []
for n in file_list:
    data.append(gd.Extract(data_directory+n))

data2 = []
for n in file_list2:
    data2.append(gd.Extract(data_directory2+n))

# data2 = gd.Extract(data_directory+"D1-Raman.txt")

# gd.Visualize(data,xlim=(370,420),ylim=(0,650),xlabel=r'Raman shift ($\mathregular{cm^-1}$)',ylabel='Intensity (a.u.)', title='Raman spectra of $\mathregular{LPE-MoS_2}$',
             # curve_label=['5l as-deposited', '5l annealing', '10l as-deposited', '10l annealing', '15l as-deposited', '15l annealing'],
             # Seperating='True',step=100,Fitting='True',num_peaks=2, param=[[380, 10, 90], [410, 10, 300]],mode='Lorentzian', baseline=[33,150,236,350,426,550])
# print(gd.Extract(data_directory+"D1-Raman.txt"))

gd.Visualize(data2,xlim=(15,25),ylim=(180,1100),xlabel=r'2$\theta$ (degree)',ylabel='Intensity (a.u.)', title='XRD of P(VDF-TrFE)',
             curve_label=['SiO2/Si', '10l', '20l', '30l', '10l annealed', '20l annealed','30l annealed'],
             Seperating='False')