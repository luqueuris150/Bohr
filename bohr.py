# Vamos importar as bibliotecas necessárias
import matplotlib.pyplot as plt
import matplotlib.colors
import seaborn as sns
sns.set_theme()
import numpy as np

# vamos definir uma função bem legal que transforma comprimentos de onda em 'vetores' de RGB com a cor que o comprimento de onda apresenta
def wavelength_to_rgb(wavelength, gamma=0.8):
    wavelength = float(wavelength)
    if wavelength >= 380 and wavelength <= 750:
        A = 1.
    else:
        A=0.5
    if wavelength < 380:
        wavelength = 380.
    if wavelength >750:
        wavelength = 750.
    if wavelength >= 380 and wavelength <= 440:
        attenuation = 0.3 + 0.7 * (wavelength - 380) / (440 - 380)
        R = ((-(wavelength - 440) / (440 - 380)) * attenuation) ** gamma
        G = 0.0
        B = (1.0 * attenuation) ** gamma
    elif wavelength >= 440 and wavelength <= 490:
        R = 0.0
        G = ((wavelength - 440) / (490 - 440)) ** gamma
        B = 1.0
    elif wavelength >= 490 and wavelength <= 510:
        R = 0.0
        G = 1.0
        B = (-(wavelength - 510) / (510 - 490)) ** gamma
    elif wavelength >= 510 and wavelength <= 580:
        R = ((wavelength - 510) / (580 - 510)) ** gamma
        G = 1.0
        B = 0.0
    elif wavelength >= 580 and wavelength <= 645:
        R = 1.0
        G = (-(wavelength - 645) / (645 - 580)) ** gamma
        B = 0.0
    elif wavelength >= 645 and wavelength <= 750:
        attenuation = 0.3 + 0.7 * (750 - wavelength) / (750 - 645)
        R = (1.0 * attenuation) ** gamma
        G = 0.0
        B = 0.0
    else:
        R = 0.0
        G = 0.0
        B = 0.0
    return (R,G,B,A)

# Vamos definir as funções importantes, como da energia em função de n, da frequência e do comprimento de onda, bem como alguns vetores
# e constantes importantes
E = lambda n: -13.6/n**2
h = 4.136*1e-15
c = 299792458
nu = lambda n1,n2: (13.6/h)*np.abs(1/n1**2 - 1/n2**2)
f = []
lmbda = lambda f: float(c)/float(f)
wv = []
cores = []
lcl = []

# Criando os pontos para os gráficos
x = np.linspace(0, 16, 17)
n = np.linspace(1,5,5)
n = np.append(n, np.inf)

#Calculamos as energias para os valores de n anteriormente definidos
En = [E(ni) for ni in n]
En[5] = np.abs(En[5])
Enm = [En]*17
Emn = np.transpose(Enm)

# Criamos a primeira figura, que mostrará os estados de energia e as possíveis transições de estados
fig = plt.figure()
ax = fig.add_subplot()
k = 1

# Fazemos as operações para calcular cada comprimento de onda e plotar as transições na primeira figura
for j in range(len(n)):
    ax.plot(x, Emn[j][0:len(x)], c='k')
    if j == 5:
        ax.annotate('n = $\\infty$' % n[j], xy=[0.0,En[j]], textcoords='data')
    else:
        ax.annotate('n = %.0f' % n[j], xy=[0.0,En[j]], textcoords='data')
    ax.annotate('E = %.1f eV' % En[j], xy=[16.0,En[j]], textcoords='data')
    i = 0
    while n[i] < n[len(n) - j - 1]:
        nf = n[len(n) - j - 1]
        ni = n[i]
        v = nu(ni,nf)
        f.append(v)
        wl = lmbda(v)*1e9
        wv.append(wl)
        if (len(n) - j - 1 == 5):
            a = '\\infty'
        else:
            a = '%i'%(len(n) - j)
        b = '%i'%(i+1)
        lb = ('$\\lambda_{%s %s}$' % (a,b))
        if wl < 350:
            cor = 'xkcd:deep purple'
            legenda = ('%s $ = $ %.0f nm -> ultravioleta' % (lb,wl))
        elif wl > 750:
            cor = 'xkcd:dark red'
            legenda = ('%s $ = $ %.0f nm -> infravermelho' % (lb,wl))
        else:
            cor = wavelength_to_rgb(wl)
            legenda = ('%s $ = $ %.0f nm -> visível' % (lb,wl))
        cores.append(cor)
        lcl.append([wl, cor, lb])
        ax.arrow(x[k], En[len(n) - j - 1], 0, En[i] - En[len(n) - j - 1] + 0.2, head_width=0.1, head_length=0.2, fc=cor, ec=cor, label=legenda)
        i = i+1
        k = k+1

# Configuramos o gráfico para que seja exibido de acordo com o que queremos
ax.legend(bbox_to_anchor=(-0.21, 0.19, 0.5, 0.5))
ax.set_title("Gráfico da Energia versus n")
ax.set_ylabel("Energia")
ax.yaxis.set_label_position("right")
ax.yaxis.tick_right()
ax.set_ylim([-13.7,0.1])
ax.set_xticklabels([])
ax.set_yticklabels([])

# Mudamos as configurações do gráfico e criamos uma nova figura, além de novos pontos. Nesta, exibiremos o espectro de emissão.
#sns.set(style="ticks", context="talk")
#plt.style.use("dark_background")

y = np.linspace(0, 17, 18)
lcl.sort()
fig2 = plt.figure()
ax2 = fig2.add_subplot()
infra = [750]*18
ultra = [350]*18

# Plotamos o espectro de emissão
for j in range(len(lcl)):
    ax2.plot([lcl[j][0]]*18, y, c=lcl[j][1], label='%s $ = $ %.0f nm' %(lcl[j][2],lcl[j][0]))
    if j < 6:
        continue
    elif j > 10:
        if (j%2)==1:
            ax2.annotate('%s $ = $ %.0f nm'%(lcl[j][2],lcl[j][0]), xy=[lcl[j][0], 17.0], xytext=[lcl[j][0]+100.0, 17.0], textcoords="data", va="top", c=lcl[j][1], rotation=90)
        else:
            ax2.annotate('%s $ = $ %.0f nm'%(lcl[j][2],lcl[j][0]), xy=[lcl[j][0], 5.0], xytext=[lcl[j][0]+100.0, 5.0], textcoords="data", va="top", c=lcl[j][1], rotation=90)
    elif j == 6:
        ax2.annotate('%s $ = $ %.0f nm'%(lcl[j][2],lcl[j][0]), xy=[lcl[j][0], 0.0], xytext=[lcl[j][0]+300.0, -0.5], textcoords="data", va="top", c=lcl[j][1])
    else:
        if (j%2)==1:
            ax2.annotate('%s $ = $ %.0f nm'%(lcl[j][2],lcl[j][0]), xy=[lcl[j][0], 17.0], xytext=[lcl[j][0]+100.0, 17.0], textcoords="data", va="top", c=lcl[j][1], rotation=90)
        else:
            ax2.annotate('%s $ = $ %.0f nm'%(lcl[j][2],lcl[j][0]), xy=[lcl[j][0], 5.0], xytext=[lcl[j][0]+100.0, 5.0], textcoords="data", va="top", c=lcl[j][1], rotation=90)

# Configuramos o final do gráfico, em especial adicionando as linhas lambda_infravermelho e lambda_ultravioleta para delimitar até onde vai a região do visível
ax2.plot(infra, y, c='xkcd:dark red', label='$\\lambda_{infravermelho} = $ %.0f nm' %(750.0))
ax2.annotate('$\\lambda_{infravermelho} = $ %.0f nm' %(750.0), xy=[750.0, 13.0], xytext=[1200.0, 18.0], textcoords="data", va="top", c='xkcd:dark red')
ax2.plot(ultra, y, c='xkcd:deep purple', label='$\\lambda_{ultravioleta} = $ %.0f nm' %(350.0))
ax2.annotate('$\\lambda_{ultravioleta} = $ %.0f nm' %(350.0), xy=[350.0, 13.0], xytext=[340.0, 12.0], textcoords="data", va="top", c='xkcd:deep purple',rotation=90)
ax2.set_title("Espectro de Emissão do Átomo de Hidrogênio segundo Modelo de Bohr")
ax2.set_xlabel("Comprimento de Onda")
plt.gca().invert_xaxis()
ax2.set_ylim([-0.2,20])
ax2.set_xticklabels([])
ax2.set_yticklabels([])

# Por fim, mostramos as figuras criadas
plt.show()
