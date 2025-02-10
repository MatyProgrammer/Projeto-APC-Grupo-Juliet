import tkinter as tk
from tkinter import ttk, messagebox

historico_calculos = []

# Funções de cálculo (sem mudanças)
def EmissaoMilho(QuantidadeHectares, ProduçãoPorHectare, QuantidadeDesmatada):
    return (QuantidadeHectares * (875 * (ProduçãoPorHectare / 1000))) + (QuantidadeDesmatada * 85000)

def EmissaoSoja(QuantidadeHectares, ProduçãoPorHectare, QuantidadeDesmatada):
    return (QuantidadeHectares * (1237 * (ProduçãoPorHectare / 1000))) + (QuantidadeDesmatada * 85000)

def EmissaoCarne(QuantidadeRuminantes, LitrosDiesel, QuantidadeDesmatada):
    return (QuantidadeRuminantes * (130 * 84)) + (LitrosDiesel * 2.64) + (QuantidadeDesmatada * 85000)

# Interface Gráfica
root = tk.Tk()
root.title("Calculadora de Emissões de CO2")
root.geometry("500x400")
root.resizable(False, False)

# Estilo customizado para botões
style = ttk.Style(root)
style.theme_use('clam')
style.configure("Green.TButton",
                background="green",
                foreground="white",
                font=("Arial", 10, "bold"),
                padding=5)

# Mudança de cor quando o botão estiver presionado
style.map("Green.TButton",
          background=[("active", "dark green")])

# Frames para organização
frame_principal = ttk.Frame(root, padding="10")
frame_principal.pack(fill="both", expand=True)

frame_campos = ttk.LabelFrame(frame_principal, text="Dados da Produção", padding="10")
frame_campos.pack(fill="both", expand=True, pady=5)

frame_botoes = ttk.Frame(frame_principal)
frame_botoes.pack(fill="x", pady=10)

frame_resultado = ttk.LabelFrame(frame_principal, text="Resultado", padding="10")
frame_resultado.pack(fill="x", pady=5)

# Variáveis
produto_var = tk.StringVar()
uso_maquinas_var = tk.StringVar(value="não")

# Widgets dentro do Frame
ttk.Label(frame_campos, text="Produto Cultivado:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
ttk.Combobox(frame_campos, textvariable=produto_var, values=["Milho", "Soja", "Carne"], state="readonly").grid(row=0, column=1, padx=5, pady=5)

ttk.Label(frame_campos, text="Hectares Totais:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
quantidade_hectares_entry = ttk.Entry(frame_campos)
quantidade_hectares_entry.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(frame_campos, text="Área Desmatada:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
quantidade_desmatada_entry = ttk.Entry(frame_campos)
quantidade_desmatada_entry.grid(row=2, column=1, padx=5, pady=5)

producao_por_hectare_label = ttk.Label(frame_campos, text="Produção por Hectare (kg):")
producao_por_hectare_entry = ttk.Entry(frame_campos)

quantidade_ruminantes_label = ttk.Label(frame_campos, text="Número de Ruminantes:")
quantidade_ruminantes_entry = ttk.Entry(frame_campos)

uso_maquinas_label = ttk.Label(frame_campos, text="Usa Máquinas?")
uso_maquinas_sim = ttk.Radiobutton(frame_campos, text="Sim", variable=uso_maquinas_var, value="sim")
uso_maquinas_nao = ttk.Radiobutton(frame_campos, text="Não", variable=uso_maquinas_var, value="não")

litros_diesel_label = ttk.Label(frame_campos, text="Litros de Diesel:")
litros_diesel_entry = ttk.Entry(frame_campos)

# Resultado
resultado_label = ttk.Label(frame_resultado, text="", font=("Arial", 10, "bold"))
resultado_label.pack()

# Função para exibir coisas específicas
def mostrar_campos():
    produto = produto_var.get().lower()
    for widget in [producao_por_hectare_label, producao_por_hectare_entry, quantidade_ruminantes_label, 
                   quantidade_ruminantes_entry, uso_maquinas_label, uso_maquinas_sim, uso_maquinas_nao, 
                   litros_diesel_label, litros_diesel_entry]:
        widget.grid_forget()
    
    if produto in ["milho", "soja"]:
        producao_por_hectare_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        producao_por_hectare_entry.grid(row=3, column=1, padx=5, pady=5)
    elif produto == "carne":
        quantidade_ruminantes_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        quantidade_ruminantes_entry.grid(row=3, column=1, padx=5, pady=5)
        uso_maquinas_label.grid(row=4, column=0, padx=5, pady=5, sticky="w")
        uso_maquinas_sim.grid(row=4, column=1, padx=5, pady=5)
        uso_maquinas_nao.grid(row=4, column=2, padx=5, pady=5)
        litros_diesel_label.grid(row=5, column=0, padx=5, pady=5, sticky="w")
        litros_diesel_entry.grid(row=5, column=1, padx=5, pady=5)

produto_var.trace_add("write", lambda *args: mostrar_campos())

# Função para cálculo
def calcular_emissao():
    produto = produto_var.get().lower()
    try:
        hectares = float(quantidade_hectares_entry.get())
        desmatada = float(quantidade_desmatada_entry.get())
    except ValueError:
        messagebox.showerror("Erro", "Insira valores numéricos válidos.")
        return

    if produto in ["milho", "soja"]:
        try:
            producao = float(producao_por_hectare_entry.get())
        except ValueError:
            messagebox.showerror("Erro", "Insira um valor válido para produção por hectare.")
            return
        emissao = EmissaoMilho(hectares, producao, desmatada) if produto == "milho" else EmissaoSoja(hectares, producao, desmatada)

    elif produto == "carne":
        try:
            ruminantes = int(quantidade_ruminantes_entry.get())
            litros_diesel = float(litros_diesel_entry.get()) if uso_maquinas_var.get() == "sim" else 0
        except ValueError:
            messagebox.showerror("Erro", "Insira valores válidos para ruminantes e diesel.")
            return
        emissao = EmissaoCarne(ruminantes, litros_diesel, desmatada)

    else:
        messagebox.showerror("Erro", "Escolha um produto válido.")
        return

    resultado_label.config(text=f"Emissão: {emissao:.2f} kg CO2")
    historico_calculos.append(f"{produto.capitalize()} - {emissao:.2f} kg CO2")

# Histórico
def exibir_historico():
    historico_texto = "\n".join(historico_calculos) if historico_calculos else "Nenhum cálculo realizado."
    messagebox.showinfo("Histórico de Cálculos", historico_texto)

# Botões
ttk.Button(frame_botoes, text="Calcular", command=calcular_emissao, style="Green.TButton").pack(side="left", padx=10)
ttk.Button(frame_botoes, text="Histórico", command=exibir_historico, style="Green.TButton").pack(side="left", padx=10)


root.mainloop()