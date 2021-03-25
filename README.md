# MOJITO
**M**aterials pr**OJ**ect on analyz**I**ng spec**T**r**O**scopy

## I. Introduction
The name *MOJITO* stands for materials project on analyzing spectroscopy. Though this abbreviation might not be favourable to everyone, this project is actually aiming to solve the problems of analyzing spectrums for anyone who works in materials science and related areas.

To begin with, let's consider some useful characterization techniques that we use in these areas. The first few ones that come up to me are X-ray Diffraction (XRD), Raman, UV-vis absorption and photoluminescence, and these will be the starting point of our project.

To under stand why the characterization results come in the form that we see. The first thing we need to do is to figure out how light is interacting with our materials. So, we will first talk about the mechanism of interaction between light and our materials.

## II. Interactions Between Electromagnetic Radiation and Materials
In this part, we are going to talk about the interactions between light and materials. This will give us a glimpse on the origin of the shape of spectrums that we can get from characterizations. Only spherical chicken in vacuum (真空中的球形鸡) will appear in the form of a seies of $\delta$-functions. There are more profound knowledge that drives the real world that we live in. The first thing that we will talk about in this section, is broadening. 

### A. Natural Line Broadening （自然致宽）
The origin of natrual line broadening is the energy-time uncertainty principle （能量-时间不确定性原理）. Let's consider a scene of a light is exciting electrons to higher states.

![1](https://user-images.githubusercontent.com/53797732/112113087-525ae580-8bf1-11eb-8186-20c7765e5607.png)

*Figure 1. Absorption and emission process between states m and n*[<sup>[1]</sup>](#reference-1)
:---------:

When the excitation is withdrawn, the excited particles will give out the excessive energy and drop back to the state *m* (eg. ground state, 基态), and the excessive energy might turn into heat or light. If the energy comes out in the form of light, we might be able to measure the energy difference between state *n* (eg. excited state, 激发态) and state *m* by measuring the frequency of this light, which is actually part of the principles of UV-vis absorption and photoluminescence and we will have deeper look into them in latter discussion. 

Assuming light is coming out in this process, why there a broadening? Wouldn't the output light possess the energy of exactly *E*<sub>*n*</sub>-*E*<sub>*m*</sub>? The answer is negative! Because the population of electrons staying in state *n* is reducing, the corresponding energy level will decay as the population of the electrons decreases. And this decay is a first-order process:

$$ -\frac{dN_{n}}{dt} = kN_{n} $$

where *N*<sub>*n*</sub> is the number of electron at state *n*, k is the first-order rate conbstant that $k=1/\tau$.[<sup>[1]</sup>](#reference-1) It should be emphasized that $\tau$ is the so-called lifetime of states ($\tau$ 就是人们一直提到的量子态的寿命). How exactly did this decay connected with the broadening of spectrums?

If we are having a state that has a stationary, accurate energy *E* and the corresponding wavefunctions is $\Psi$, then this state is a stationary state. (在这种情况下，体系的势能与时间无关，只是一个关于位置的函数，*U* = *U*(***r***)。因此在解薛定谔方程的时候，我们可以分离变量，即最后求得的波函数可以写成位置分量与时间分量的相乘。) We could seperate our wavefunction into two terms, time-depending term and position-depending term:

$$ {\Psi} = {\psi}(\pmb{r}){\phi}(t) = {\psi}(\pmb{r})e^{-i{\omega}t} = {\psi}(\pmb{r})e^{-iEt/{\hbar}} $$

where ***r*** is position and $\omega$ is the angular velocity of this wave (The de Brogile equation: $E = h{\nu} = {\hbar}{\omega}$, ${\nu} = {\omega}/2{\pi}$ is the frequency).[<sup>[2,3]</sup>](#reference-2) If this state is decaying through the process mentioned above instead of being stationary, it should follow the below relation:

$$ |{\Psi}|^2 = |{\psi}|^2e^{-t/{\tau}} $$，

$\tau$ is exactly the lifetime discussed above. Then the whole wavefunction could be rewritten as:

$$ {\Psi} = {\psi}(\pmb{r})e^{-iEt/{\hbar}-t/2{\tau}}    \Longrightarrow    {\phi}(t) = e^{-iEt/{\hbar}-t/2{\tau}} $$.

If we applied Fourier transform (对时域函数宝具：傅里叶变换) to the time-dependent term ${\phi}(t)$, we will then have

$$ g({\varepsilon}) = {\int}{\phi}(t)e^{i{\varepsilon}t/{\hbar}}dt $$

and as a result

$$ g({\varepsilon}) = \frac{{\hbar}/2{\pi}{\tau}}{({\varepsilon}-E)^2+({\hbar}/2{\tau})^2} $$.

This is a Lorentzian. **In conclusion, the lineshape of spectrum induced by natural broadening is Lorentzian.** The energy distribution of the above formula is

$$ {\Delta}E = {\theta}_{HWHM} = {\hbar}/2{\tau}    \Longrightarrow    {\Delta}E{\Delta}t {\geq} {\Delta}E{\tau} = {\hbar}/2 $$,

and this is the energy-time uncertainty principle (HWHM, half width at half maximum, 半峰半宽).[<sup>[4]</sup>](#reference-4)

### B. Doppler Broadening （多普勒致宽）

### C. Pressure Broadening （压力致宽）

### D. Power, or saturation, broadening （功率，或饱和致宽）

## III. Principles of Characterization Techniques
In this part, we will have a deep look at the working principles of the characterizations we usually carry out in materials science and related areas. To fully understand our testing results, knowing only the mechanism dicting the interactions between light and materials is insufficient. The situation changes from time to time as we always try to characterize our device from different perspectives. To understand the properties of our samples, we need to have a comprehensive understanding about the testing tools we used. So, let's take a look at the common characterization methods we used. 
### A. X-ray Diffraction (XRD)
### B. Raman
### C. UV-vis Absorption and Photoluminescence


## References
[1] [J. Michael Hollas (2004). *MODERN SPECTROSCOPY*, 4th ed. West Sussex, England: John Wiley & Sons Ltd. 452 pp.](http://www.chemistry.uoc.gr/lapkin/Hollas_ModernSpectroscopy.pdf)<div id="reference-1"></div>
[2] [David J. Griffiths (2005). *Introduction to Quantum Mechanics*. Upper Saddle River, NJ: Pearson Prentice Hall.](http://gr.xjtu.edu.cn/c/document_library/get_file?p_l_id=21699&folderId=2383652&name=DLFE-82647.pdf)<div id="reference-2"></div>
[3] [周世勋 (2009). *量子力学教程*, 第二版. 北京, 中国: 高等教育出版社.](https://books.google.com.hk/books/about/%E9%87%8F%E5%AD%90%E5%8A%9B%E5%AD%A6%E6%95%99%E7%A8%8B.html?id=bV6OQwAACAAJ&redir_esc=y)<div id="reference-3"></div>
[4] [Luyao Zou. 能量-时间的不确定关系如何导出光谱自然展宽？](https://www.zhihu.com/question/33565055/answer/75944534)<div id="reference-4"></div>
[5] [

