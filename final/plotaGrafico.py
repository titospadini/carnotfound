from constants import *
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


df = pd.read_csv(DATA_PATH + ARQUIVO_CSV)
plt.figure()
df.plot()

#caso esteja rodando por ssh, mostrar a imagem dará erro
try:
	plt.show()
except:
	pass
	
#salva imagem
plt.savefig(fname = DATA_PATH + ARQUIVO_GRAFICO)