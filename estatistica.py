try:
    from tkinter import ttk, Treeview,Style   
except ImportError:  # Python 3
    from tkinter import *
    from tkinter.ttk import *
    
from tooltip import CreateToolTip
from tkinter.font import nametofont
import time
import csv
import pandas as pd
import matplotlib.pyplot as plt

def gerar_grafico():
    plt.close()
    label_grafico_gerar['text'] = 'Gerando gráfico...'
    d = {}
    str_tribunal = comboBox_grafico_tribunal.get().lower()
    str_cargo = search_grafico_cargo.get().lower()
    str_orgao = comboBox_grafico_orgao.get().lower()
    str_escolha = comboBox_grafico_valor.get().lower()

    if 'líquido' in str_escolha:
        str_escolha = 'rendimento_liquido'
        escolha = 'RL'

    elif 'descontos' in str_escolha:
        str_escolha = 'total_de_descontos'
        escolha = 'TdD'

    else:
        str_escolha = 'total_de_rendimentos'
        escolha = 'TdR'

    for x in lista_data[1::]:
        d[x] = 0
    
    for x in range(len(df)):
        if str_tribunal in (str(df['tribunal'][x]).lower(),'todos') and str_orgao in (str(df['orgao'][x]).lower(),'todos') and str_cargo in ( str(df['cargo'][x]).lower(), '') and not pd.isna(df[str_escolha][x]):
            d[df['mesano_de_referencia'][x]] += float(df[str_escolha][x])
        janela.update()
    l_x, l_y = [], []

    for x in d.items():
        l_x.append(x[0])
        l_y.append(x[1])

    label_grafico_gerar['text'] = 'Gráfico gerado com\nsucesso!'                                                                                                                           
    plt.plot(l_x,l_y,'go',color = 'blue')
    plt.plot(l_x,l_y,'k',color = 'black')
    plt.grid(True)
    plt.title("Gráfico de linhas")
    plt.xlabel('Datas')
    plt.ylabel(str_escolha)
    plt.legend([escolha], loc = 2)
    plt.show()
    
def criar_csv():
    colunas = ("Mes/ano de Referência", "Tribunal", "Lotacão", "Cargo", "Nome", "Total de Rendimentos",
                   "Total de Descontos", "Rendimento Líquido", "Órgão")
    label_info['text'] = "Aguarde um momento..."
    with open("Salário-Magistrados.csv",'w',newline = '', encoding = 'utf-8') as saida:
        escrever = csv.writer(saida)
        escrever.writerow(colunas)
        for i in table.get_children():
            aux = ''
            l = []
            tupla_text = table.item(i, "text")
            tupla_value = table.item(i, "values")
            for x in tupla_text:
                aux += x
            l.append(aux)
            for x in tupla_value:
                l.append(x)
           
            escrever.writerow(l)
            janela.update()

    label_info['text'] = "Arquivo criado com sucesso!"

def boton_filtrar ():
    label_info['text'] = ''
    progress_bar.set(0)
    janela.update()
    for i in table.get_children():
        table.delete(i)
    
    busca = search.get().lower()
    busca_nome = search_name.get().lower()
    busca_cargo = search_cargo.get().lower()
    cbx_tribunal = comboBox_tribunal.get().lower()
    cbx_orgao = comboBox_orgao.get().lower()
    cbx_data = comboBox_data.get().lower()
    p_b = 0.1
    tam = len(df)
    size_treeview = 0   
    for n in range (tam):
        if busca != '':
            if ( busca == df['tribunal'][n].lower() or busca == str(df['lotacao'][n]).lower() or busca == str(df['cargo'][n]).lower() or busca == df['nome'][n].lower() ):
                if(busca_nome in (df['nome'][n].lower(), '' ) and busca_cargo in (str(df['cargo'][n]).lower(),'') and cbx_tribunal in (df['tribunal'][n].lower(),'todos') and cbx_orgao in (df['orgao'][n].lower(),'todos') and cbx_data in (str(df['mesano_de_referencia'][n]).lower(),'todos')):
                     inserção(df,n)
                     size_treeview+=1
                        
        else:
            if (busca_nome in (df['nome'][n].lower(), '' ) and busca_cargo in (str(df['cargo'][n]).lower(),'') and cbx_tribunal in (df['tribunal'][n].lower(),'todos') and cbx_orgao in (df['orgao'][n].lower(),'todos') and cbx_data in (str(df['mesano_de_referencia'][n]).lower(),'todos')):
                inserção(df,n)
                size_treeview+=1
            
        if (int ((tam * p_b)/2) == n or n+1 == tam):
            p_b += 0.1
            progress_bar.set(n)
            janela.update()
    if (size_treeview == 0):
        table.insert('', 'end', text='Vazio')
        label_size['text'] = "0 - 0"
    else:
        label_size['text'] = ("1 - %d" %size_treeview)

def inserção (df,n):
    table.insert('', 'end', text=df['mesano_de_referencia'][n], values=(df['tribunal'][n],
                                     str(df['lotacao'][n]).lower().title(), str(df['cargo'][n]).lower().title(),
                                      df['nome'][n].lower().title(), str(df['total_de_rendimentos'][n]),
                                       str(df['total_de_descontos'][n]), str(df['rendimento_liquido'][n]),df['orgao'][n] ))

def set_list(l):
    aux = []
    for x in l:
        aux.append(str(x).lower().title())
    aux.sort()
    aux.insert(0,'Todos')
    return aux
#########################################   INICIALIZANDO #########################################

df = pd.read_csv('S_Magistrado.csv', sep=',', error_bad_lines=False, index_col=False, dtype='unicode')

janela = Tk()
janela.title("Programa")
janela.resizable(0, 0)
janela.geometry("1225x500+400+200")

#########################################   PROGRESS BAR #########################################

progress_bar = DoubleVar()
my_progress_bar = Progressbar(janela,variable = progress_bar, maximum = len(df)-1)
my_progress_bar.place(x=42,y = 425,width = 1134)

frame = Frame(janela)
frame.place(x=43,y=184,height = 237, width = 1150)

#########################################   TREEVIEW   #############################################

style = Style(janela)
style.configure("Treeview.Heading", font=(None, 10))
style.configure("Treeview",rowheight=21)

table = Treeview(janela)

table['columns'] = ("column1", "column2", "column3", "column4", "column5","column6", "column7", "column8")
table.place(x=41,y=185)

table.heading("#0", text='Mês/ano')
table.column("#0", anchor="center",width=85)

table.heading('#1', text='Tribunal')
table.column('#1', anchor='center', width=157)

table.heading('#2', text='Lotacão')
table.column('#2', anchor='center', width=165)

table.heading('#3', text='Cargo')
table.column('#3', anchor='center', width=128)

table.heading('#4', text='Nome')
table.column('#4', anchor='center', width=204)

table.heading('#5', text='TdR')
table.column('#5', anchor='center', width=60)

table.heading('#6', text='TdD')
table.column('#6', anchor='center', width=60)

table.heading('#7', text='RL')
table.column('#7', anchor='center', width=60)

table.heading('#8', text='Órgão')
table.column('#8', anchor='center', width=213)

#########################################   SCROLL #########################################

scroll = Scrollbar(frame,orient = 'vertical', command = table.yview)
scroll.pack(side ="right", fill = "y")

table.config(yscrollcommand=scroll.set)

#########################################   ADICIONANDO TREEVIEW E COMBOBOX #########################################

for x in range(len(df)):
    inserção(df,x)

lista_data = set(list(df['mesano_de_referencia'].values))
lista_tribunal =  set(list(df['tribunal'].values))
lista_orgao =  set(list(df['orgao'].values))

lista_data = set_list(lista_data)
lista_tribunal = set_list(lista_tribunal)
lista_orgao = set_list(lista_orgao)

#########################################   CAIXAS DE BUSCA   #####################################

search = Entry(janela,width = 43)
search.place(x=41,y=22) 

search_name = Entry(janela,width = 43)
search_name.place(x=41,y=106)

search_cargo = Entry(janela,width = 43)
search_cargo.place(x=340,y=106)

search_grafico_cargo = Entry(janela,width = 43)
search_grafico_cargo.place(x=920,y=64)

#########################################   BOTÃO   ###############################################

bonton_tooltip = Button(janela, width = 20, text = "Dúvida (?)")
bonton_tooltip.place(x = 815, y = 150)
button1_ttp = CreateToolTip(bonton_tooltip, "TdR = Total de Rendimentos\nTdD = Total de Descontos\nRL = Rendimento Líquido")

boton = Button(janela, width = 20, text = "Criar .csv",command = criar_csv)
boton.place(x=41,y=455)

boton_filtrar = Button(janela, width = 20, text = "Filtrar",command = boton_filtrar)
boton_filtrar.place(x=40,y=136)

boton_gerar_grafico = Button(janela, width = 20, text = "Gerar gráfico",command = gerar_grafico)
boton_gerar_grafico.place(x = 920, y = 104)

#########################################   LABEL   ###############################################

label_size = Label(janela, text = "1 - %d" %(len(df)))
label_size.place (x = 1120, y = 165)

label_busca = Label(janela, text = "Busca")
label_busca.place(x=40,y=0)

label_tribunal = Label(janela, text = "Tribunal")
label_tribunal.place(x=338,y=0)

label_orgao = Label(janela, text = "Órgão")
label_orgao.place(x=40,y=43)

label_data = Label(janela, text = "Data")
label_data.place(x=338,y=42)

label_nome = Label(janela, text = "Nome")
label_nome.place(x=40,y=84)

label_cargo = Label(janela, text = "Cargo")
label_cargo.place(x=338,y=84)

label_info = Label(janela, text = "")
label_info.place(x = 180, y = 460)

label_grafico =  Label(janela, text = "Opções de variáveis para gerar gráfico de linhas" ,font='Helvetica 8 bold')
label_grafico.place(x=638,y=18)

label_grafico_tribunal = Label(janela, text = "Tribunal")
label_grafico_tribunal.place(x = 638, y = 42)

label_grafico_orgao = Label(janela, text = "Órgão")
label_grafico_orgao.place(x = 638, y = 84)

label_grafico_cargo = Label(janela, text = "Cargo")
label_grafico_cargo.place(x = 918, y = 42)

label_grafico_valor =Label(janela, text = "Valor")
label_grafico_valor.place(x = 918, y = 0 )

label_grafico_gerar = Label(janela, text ='')
label_grafico_gerar.place(x = 1060, y = 100)

#########################################   COMBOBOX   ############################################# 

comboBox_tribunal = ttk.Combobox(janela,values = lista_tribunal, width = 40)
comboBox_tribunal.place(x=340,y=22)
comboBox_tribunal.set("Todos")

comboBox_grafico_tribunal = ttk.Combobox(janela,values = lista_tribunal, width = 40)
comboBox_grafico_tribunal.place(x=640,y=64)
comboBox_grafico_tribunal.set("Todos")

comboBox_grafico_orgao = ttk.Combobox(janela,values = lista_orgao, width = 40)
comboBox_grafico_orgao.place(x=640,y=106)
comboBox_grafico_orgao.set("Todos")

comboBox_orgao = ttk.Combobox(janela,values = lista_orgao, width = 40)
comboBox_orgao.place(x=41,y=64)
comboBox_orgao.set("Todos")

comboBox_data = ttk.Combobox(janela,values = lista_data, width = 40)
comboBox_data.place(x=340,y=64)
comboBox_data.set("Todos")

comboBox_grafico_valor = ttk.Combobox(janela,values = ['Rendimento Líquido', 'Total de Rendimentos', 'Total de Descontos'], width = 40)
comboBox_grafico_valor.place( x = 920 , y = 18)
comboBox_grafico_valor.set("Rendimento Líquido")
######################################################################################################

janela.mainloop()

