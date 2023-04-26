import tkinter as tk
from tkinter import ttk
from datetime import datetime
import time
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def download_stock_data(ticker, start_date, end_date):
    """Baixa dados históricos de uma ação do Yahoo Finance."""
    data = yf.download(ticker, start=start_date, end=end_date)
    return data


def plot_stock_data(data, ticker):
    """Plota um gráfico de linhas dos dados históricos da ação."""
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(data['Close'])
    ax.set(
        title=f'Histórico de preços de {ticker}', xlabel='Data', ylabel='Preço (R$)')
    plt.xticks(rotation=45)
    plt.grid()
    return fig


def show_table(data):
    """Mostra os dados históricos da ação em uma tabela."""
    root = tk.Tk()
    # root.geometry("400x150")
    root.title("Dados históricos da ação")
    table = ttk.Treeview(root)
    table.pack(side='left', fill='both', expand=True)

    # Adiciona a coluna de data aos dados históricos da ação
    data = data.reset_index()

    # Cria as colunas
    table['columns'] = data.columns.tolist()
    table.heading('Date', text='Data')  # adiciona a coluna de data à tabela
    for column in table['columns']:
        table.heading(column, text=column)

    # Preenche as linhas
    for row in data.itertuples(index=False):
        table.insert('', 'end', values=list(row))

    # Cria a barra de rolagem
    scrollbar = ttk.Scrollbar(root, orient='vertical', command=table.yview)
    scrollbar.pack(side='right', fill='y')
    table.configure(yscroll=scrollbar.set)

 # Posiciona a tabela abaixo do gráfico
    table.pack(side='top', fill='both', expand=True)


if __name__ == '__main__':
    # Define o ticker, data de início
    ticker = "^BVSP"
    start_date = "2023-01-01"

    # Cria a janela principal
    root = tk.Tk()
    root.title("Stock Data")
    root.geometry("1080x720")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    # Cria o frame para o gráfico
    graph_frame = ttk.Frame(root)
    graph_frame.grid(row=0, column=0, sticky='NSEW')

    # Faz o download dos dados históricos da ação
    end_date = datetime.now().strftime("%Y-%m-%d")
    data = download_stock_data(ticker, start_date, end_date)

    # remove a coluna 'Unnamed: 0'
    # data = data.reset_index()
    # data = data.drop('Unnamed', axis=1)
    data = data.drop('High', axis=1)
    data = data.drop('Low', axis=1)

    # remove a coluna 'volume'
    data = data.drop('Volume', axis=1)

    # Plota o gráfico de linhas dos dados históricos da ação
    fig = plot_stock_data(data, ticker)

    # Cria o canvas para exibir o gráfico na janela
    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.get_tk_widget().pack(side='top', fill='both', expand=True)
    # canvas.get_tk_widget().configure(width=500, height=700)

    # Cria o frame para a tabela
    table_frame = ttk.Frame(root)
    table_frame.grid(row=1, column=0, sticky='NSEW', pady=3)
    table_frame.columnconfigure(0, weight=1)
    # Cria o botão para exibir a tabela
    table_button = ttk.Button(
        table_frame, text='Exibir tabela', command=lambda: show_table(data))
    table_button.pack(side='bottom', pady=5)

    root.mainloop()

    # Atraso de 1 hora antes da próxima iteração
    time.sleep(60 * 60)
