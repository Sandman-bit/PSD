# -*- coding: utf-8 -*-
"""untitled4.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/gist/Sandman-bit/8830403bdb01d49f6285d6d965fb1da5/untitled4.ipynb
"""

#importing statments
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import matplotlib.patches as mpatches
import os


#plt.rcParams['figure.figsize'] = 16, 11
##################controling fontsize
SMALL_SIZE = 20
MEDIUM_SIZE = 25
BIGGER_SIZE = 30

plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
#plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title
plt.rcParams['figure.figsize'] = 16, 11
fig, axes = plt.subplots(1,1,constrained_layout = True)
from itertools import cycle
lines = ["-","--"]
linecycler = cycle(lines)


###############plot dados históricos

path = r""
file  = "2024_01_27_Data_granulometria_hue"

data = (f"{file}.csv")
#data = (f"{path}"+r"\\"+rf"{file}.csv")
df = pd.read_csv(data, sep='\;', decimal='.' ,engine='python')
#first_df = pd.read_csv(data,na_filter=True)
print(df.head())
#df.columns
#df.dtypes
df = first_df.dropna(thresh=2)
"""Selecione a linha de dados para aberturas das peneiras"""

PSD_data_col = 6 ###selecione a coluna dos dados de granulometria
j = 0 ###selecione a linha dos dados
x = [float(element) for element in df.columns.tolist()[PSD_data_col:]]
#for num in range(14):
#   x.append(float(df.iloc[j,num+PSD_data_col]))

#print(x)
#df.columns
#plt.semilogx(x, x)
###############Fitting data to distributions
lb=0
#df.plot.line()
data_groups = df.groupby(df.columns.tolist())
size = data_groups.size().reset_index()
plotsize=size[size[0] > 1]        # DATAFRAME OF DUPLICATES

plotlen=len(size[size[0] > 1])   # NUMBER OF DUPLICATES
#print(plotsize,plotlen)
for dates, grp in df.groupby(['ID']):
    #plt.style.use("bmh")

    y = []
    for num in range(14):
        try:
            k = float(str(df.iloc[df.index[df.ID == dates],num+PSD_data_col]).split()[1])
        except: print('Not possible to float', str(df.iloc[df.index[df.date == dates]+1,num+1]).split()[1])
        y.append(k)


    d = {'xtp':x,'ytp':y}
    print (d)
    try:
        to_plot = pd.DataFrame(data = d)
        to_plot = to_plot.dropna()
    except: continue

    ytp = np.array(to_plot['ytp'])
    xtp = np.array(to_plot['xtp'])

#"""Find erros"""
#    for num in range(14):
#        for i in range(14):
#            try:
#                if (i<num):
#                    if (ytp[num]<ytp[num-i]):
#                        print(dates)
#            except: continue

    #print(y)
    try:
        axes.plot(xtp, ytp,linewidth=1, color = "grey", alpha = 0.5, label = 'Registros históricos', zorder=0)
        lb = lb+1
    except: continue


###############plot dados históricos filtrados
print('###############plot dados históricos filtrados############################################################\n##########################################################')

#path = r"C:\Users\gld_pvcastro\Golder Associates\21495547, Lundin. EOR Miner. Maraca - Project Files\5 Technical Work\4-Acompanhamento Golder\02-Granulometria"
file  = "2024_01_27_Data_granulometria_hue"

data = (f"{file}.csv")
#data = (f"{path}"+r"\\"+rf"{file}.csv")
#df = pd.read_csv(data, sep='\;', decimal=',')
first_df = pd.read_csv(data,na_filter=True, sep='\;')
df = first_df.dropna(thresh=1)
#print(df.head())
df.columns
# df.dtypes

"""
Selecione a linha de dados para aberturas das peneiras"""



x = [float(element) for element in df.columns.tolist()[PSD_data_col:]]

#x = []
#for num in range(14):
#    x.append(float(df.iloc[j,num+PSD_data_col]))

#print(x)
#df.columns
#plt.semilogx(x, x)

#df.plot.line()
new_df = pd.DataFrame(columns=['date','estaca','xtp','ytp'])
for ID, grp in df.groupby(['ID']):
    #plt.style.use("bmh")

    y = []
    dt = []
    dt_mm_yyy = []
    dt_raw = []
    estacas = []
    CY_ = []
    for num in range(14):
        try:
            k = float(str(df.iloc[df.index[df.ID == ID],num+PSD_data_col]).split()[1])
            #print(k)
            dates = str(df.iloc[df.index[df.ID == ID],1]).split()[1]
            estaca = (str(df.iloc[df.index[df.ID == ID],3])).split()[1]

        except: print('Not possible to float', (str(df.iloc[df.index[df.ID == ID],3])).split()[1] )
        y.append(k)
        dt.append(str(dates)[-4:])
        dt_mm_yyy.append(str(dates)[-7:])
        dt_raw.append(dates)
        estacas.append(estaca)
        #print(estacas)


        d = {'date':dt,'estaca':estacas,'xtp':x,'ytp':y}
        #print(d)

        try:
            to_plot = pd.DataFrame(data = d)
            to_plot = to_plot.dropna()
            #print(to_plot)
        except: continue
        new_df = new_df.append(to_plot, ignore_index=True)
        ytp = np.array(to_plot['ytp'])
        xtp = np.array(to_plot['xtp'])
#print (new_df.head())
new_df.columns
palette = sns.color_palette("ch:s=.25,rot=-.25",3)
ax = sns.lineplot(ax=axes, data=new_df,
        x="xtp", y="ytp",hue='estaca',style='estaca',#,palette = palette
        hue_order=['60.0', '90.0', '120.0'],
        style_order=['60.0', '90.0', '120.0'],
        zorder=20)

'''####getting data out of specification 20 fines
fines_dates=[]
for i, row in new_df.iterrows():
    if new_df.at[i,"xtp"] > 0.075:continue
    elif new_df.at[i,"ytp"] > 20 and  new_df.at[i,"date_raw"] not in fines_dates:
        print(new_df.at[i,"date_raw"],1,row)
        fines_dates.append(new_df.at[i,"date_raw"])
fines_dates = pd.DataFrame(data = fines_dates)'''


#"""Find erros"""
#    for num in range(14):
#        for i in range(14):
#            try:
#                if (i<num):
#                    if (ytp[num]<ytp[num-i]):
#                        print(dates)
#            except: continue
#####Creating output folder
try:
    os.mkdir(f"{path}"+r"\\Output\\")
except: pass


############Layout setup
axes.set_xscale('log')
axes.grid(axis='x', which = 'both', color = '0.95')
axes.grid(axis='y', which = 'major', color = '0.8')
axes.legend(loc = 'center right')#, bbox_to_anchor = (.7,.5))
axes.axis(ymin=0,ymax=100,xmin=0.0009)
axes.set(xlabel = "Abertura da malha [mm]",ylabel ="% passante a aculmulada" )
axes.vlines(x=[0.002,0.06, .2, .6], ymin=0, ymax=100, colors='black', ls='--', lw=1, zorder=200)
axes.vlines(x=.075, ymin=0, ymax=100, colors='red', ls='--', lw=1, label='Limite de finos em 20%', zorder=2)
axes.text(0.001, 0.2, 'Argila',style='italic',size='x-small')
axes.text(0.008, 0.2, 'Silte',style='italic',size='x-small')
axes.text(.08, 0.2, 'Areia fina',style='italic',size='x-small')
axes.text(.25, 0.2, 'Areia Média',style='italic',size='x-small')
axes.text(1, 0.2, 'Areia Grossa',style='italic',size='x-small')


    ##botton bar
#pcm =
#fig.colorbar(pcm, ax=axes, cax=cax)
#ax.xlabel("Abertura da malha [mm]")
#ax.ylabel("porcentagem passante [%]")
#ax.set_facecolor("white")


######legenda
handles, labels = ax.get_legend_handles_labels()
display = (lb-1,lb, lb+1,lb +2,lb+3)
ax.legend([handle for i,handle in enumerate(handles) if i in display],
         [label for i,label in enumerate(labels) if i in display])


##############Saving results:

fig.savefig(f"{path}"+r"\\Output\\"+rf"{file}_filter95.jpeg", dpi=250)




#########Saving df
with pd.ExcelWriter(f"{path}"+r"\\Output\\"+rf"{file}_new_df.xlsx") as writer:
    new_df.to_excel(writer, sheet_name='Dados')
 #   fines_dates.to_excel(writer, sheet_name='Dates with more than 20% fines')