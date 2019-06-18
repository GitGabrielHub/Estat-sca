from tkinter import *
from tkinter import ttk
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
n = 0
def boton_click():
    #plt.plot( [10,5,3,4,6,8] )
    #plt.title("Muito Fácil")
    #plt.show()
    global n
    a = ['a','b\noi','c']
    fim = str(df['mesano_de_referencia'][n]) +'  '  + str(df['tribunal'][n]) +'|  ' + str(df['lotacao'][n]) +'|  ' + str(df['cargo'][n])+'|  ' + str(df['nome'][n]) +'|  ' + str(df['total_de_rendimentos'][n]) +'|  ' + str(df['total_de_descontos'][n]) +'|  ' + str(df['rendimento_liquido'][n]) + '|  ' + str(df['orgao'][n])
    list_box.insert(0,a)
    n+=1




#########################################   INICIALIZANDO #########################################

lista_tribunal = []
lista_orgao = []
lista_data = []
df = pd.read_csv('salarios-magistrados-0adef90a6f284ca69b23e919645b6e6b.csv', sep=',', error_bad_lines=False, index_col=False, dtype='unicode')


janela = Tk()
janela.title("Programa")
janela.geometry("1225x500+400+200")
#janela.configure(bg = "black")

frame = Frame(janela)
frame.place(x=44,y=185,height = 254, width = 1150)

#########################################   LISTBOX   #############################################

list_box = Listbox(janela,height = 21,width = 163) #58
list_box.place(x = 37, y = 185)

list_box.insert(0,"Vazio")

scroll = Scrollbar(frame,orient = 'vertical', command = list_box.yview)
scroll.pack(side ="right", fill = "y")


list_box.config(yscrollcommand=scroll.set)

for n in range(1000):
	list_box.insert(n,n+1)
list_box.delete(END)

#########################################   CAIXAS DE BUSCA   #####################################

search = Entry(janela,width = 27)
search.place(x=40,y=15) 

search_name = Entry(janela,width = 27)
search_name.place(x=40,y=85)

search_cargo = Entry(janela,width = 27)
search_cargo.place(x=250,y=85)

#########################################   BOTÃO   ###############################################

boton = Button(janela, width = 20, text = "Gerar gráfico",command = boton_click)
boton.place(x=40,y=455)

boton_filtrar = Button(janela, width = 20, text = "Filtrar",command = boton_click)
boton_filtrar.place(x=40,y=115)

#########################################   LABEL   ###############################################
									 #2017-12-01 | Superior Tribunal Militar|  3a AUD 1a CJM|  JUIZ-AUDITOR|  CARLOS HENRIQUE SILVA REINIGER FERREIRA|  73300.28|  18789.51|  54510.77|  Superior Tribunal Militar
label_list_box = Label(janela,text = "Mes/ano   |         Tribunal         |   Lotacão     |     Cargo    |                  Nome                   |     TR   |    TD    |     RL   | Órgão")
label_list_box.place(x=40,y = 150)

label_busca = Label(janela, text = "Busca")
label_busca.place(x=40,y=0)

label_tribunal = Label(janela, text = "Tribunal")
label_tribunal.place(x=249,y=0)

label_orgao = Label(janela, text = "Orgão")
label_orgao.place(x=40,y=35)

label_data = Label(janela, text = "Data")
label_data.place(x=249,y=35)

label_nome = Label(janela, text = "Nome")
label_nome.place(x=40,y=70)

label_cargo = Label(janela, text = "Cargo")
label_cargo.place(x=249,y=70)

#########################################   COMBOBOX   ############################################# 

comboBox_tribunal = ttk.Combobox(janela,values = lista_tribunal, width = 26)
comboBox_tribunal.place(x=250,y=15)
comboBox_tribunal.set("Todos")

comboBox_orgao = ttk.Combobox(janela,values = lista_orgao, width = 26)
comboBox_orgao.place(x=40,y=50)
comboBox_orgao.set("Todos")

comboBox_data = ttk.Combobox(janela,values = lista_data, width = 26)
comboBox_data.place(x=250,y=50)
comboBox_data.set("Todos")

######################################################################################################

janela.mainloop()


