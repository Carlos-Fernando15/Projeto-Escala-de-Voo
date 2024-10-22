# Blibiotecas para cirar tela e interação com os dados 
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
from itertools import cycle

class Voo:
    def __init__(self, numero_voo, origem, destino, duracao, custo, horario):
        self.numero_voo = numero_voo
        self.origem = origem
        self.destino = destino
        self.duracao = duracao
        self.custo = custo
        self.horario = horario

class Tripulacao:
    def __init__(self, nome, funcao):
        self.nome = nome
        self.funcao = funcao

class Escala:
    def __init__(self, voo, tripulacao):
        self.voo = voo
        self.tripulacao = tripulacao

    def exibir_escala(self):
        escala_text = f"Voo {self.voo.numero_voo}: {self.voo.origem} -> {self.voo.destino} | Horário: {self.voo.horario}\n"
        escala_text += f"Duração: {self.voo.duracao} horas | Custo: R${self.voo.custo}\n"
        escala_text += "Tripulação:\n"
        for membro in self.tripulacao:
            escala_text += f" - {membro.nome}, {membro.funcao}\n"
        escala_text += "-" * 30 + "\n"
        return escala_text

# Função para puxar as informações dos dados do Voo pelo arquivo .csv
def carregar_voos(arquivo_csv):
    try:
        voos_df = pd.read_csv(arquivo_csv)
        voos = []
        for _, row in voos_df.iterrows():
            voo = Voo(row['numero_voo'], row['origem'], row['destino'], row['duracao'], row['custo'], row['horario'])
            voos.append(voo)
        return voos
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao carregar voos: {e}")

# Função para puxar as informações dos dados da tripulação do arquivos .csv
def carregar_tripulacao(arquivo_csv):
    try:
        tripulacao_df = pd.read_csv(arquivo_csv)
        tripulacoes = []
        for _, row in tripulacao_df.iterrows():
            tripulacao = Tripulacao(row['nome'], row['funcao'])
            tripulacoes.append(tripulacao)
        return tripulacoes
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao carregar tripulação: {e}")

# Função para organizar as tripulações por cada voo, sendo assim deve seguir um padrão de tripulantes por cada voo, se nao ocorre erro por não ter tripulantes suficientes 
def organizar_tripulacao_por_voo():
    if len(voos) > len(tripulacoes) // 3:
        messagebox.showerror("Erro", "Não há tripulantes suficientes para cada voo.")
        return None
    
    tripulacoes_por_voo = []
    tripulantes_ciclo = cycle([tripulacoes[i:i+3] for i in range(0, len(tripulacoes), 3)])
    
    for voo in voos:
        tripulacoes_por_voo.append(next(tripulantes_ciclo))
    
    return tripulacoes_por_voo

#Função para selecionar o arquivo de voo no modelo csv. Estando tudo certo ele exibe uma mensagem de dados carregados com sucesso
def carregar_dados_voo():
    arquivo_voos = filedialog.askopenfilename(title="Selecione o arquivo de voos", filetypes=[("CSV files", "*.csv")])
    if arquivo_voos:
        global voos
        voos = carregar_voos(arquivo_voos)
        messagebox.showinfo("Sucesso", "Dados dos voos carregados com sucesso!")

# Função para selecionar o arquivo de tripulação nop modelo csv. Estando tudo certo ele exibe uma mensagem de dados carregados com sucesso
def carregar_dados_tripulacao():
    arquivo_tripulacao = filedialog.askopenfilename(title="Selecione o arquivo de tripulação", filetypes=[("CSV files", "*.csv")])
    if arquivo_tripulacao:
        global tripulacoes
        tripulacoes = carregar_tripulacao(arquivo_tripulacao)
        messagebox.showinfo("Sucesso", "Dados da tripulação carregados com sucesso!")

# Função para exibir as escalas, se não for importado as informações ele aparece uma mensagem de erro informado que tem que importar os dados antes de exibir 
def exibir_escalas():
    if not voos or not tripulacoes:
        messagebox.showerror("Erro", "Por favor, carregue os dados dos voos e da tripulação antes.")
        return

    resultado_texto.delete(1.0, tk.END)  # Limpar área de texto
    
    tripulacoes_por_voo = organizar_tripulacao_por_voo()
    
    if tripulacoes_por_voo is None:
        return
    
    for i, voo in enumerate(voos):
        escala = Escala(voo, tripulacoes_por_voo[i])
        resultado_texto.insert(tk.END, escala.exibir_escala())

# Interface Gráfica com Tkinter
app = tk.Tk()
app.title("Escalas de Voo")
app.geometry("1000x600")

# Botão para o usuario carregar os dados do voo
btn_carregar_voo = tk.Button(app, text="Carregar Dados do Voo", command=carregar_dados_voo)
btn_carregar_voo.pack(pady=10)

# Função para o usuario carregar os dados da tripulação
btn_carregar_tripulacao = tk.Button(app, text="Carregar Dados da Tripulação", command=carregar_dados_tripulacao)
btn_carregar_tripulacao.pack(pady=10)

#Botão para o usuario exibir as escalas 
btn_exibir_escalas = tk.Button(app, text="Exibir Escalas", command=exibir_escalas)
btn_exibir_escalas.pack(pady=10)

# Texto para exibir resultados
resultado_texto = tk.Text(app, height=20, width=90)
resultado_texto.pack(pady=10)

# Variáveis globais para armazenar voos e tripulação
voos = []
tripulacoes = []

# Executar a interface
app.mainloop()
