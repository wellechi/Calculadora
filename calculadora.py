import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from sympy import symbols, sympify, Eq, solveset, S, pretty, limit, diff, integrate, exp, simplify
from sympy.core.sympify import SympifyError
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import io
import threading
import re  # Importando o módulo re para expressões regulares

class CalculadoraCientifica:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora Científica")
        self.root.state('zoomed')  # Maximiza a janela
        self.root.configure(bg="#000813")  # Cor de fundo do root

        # Tema moderno escuro
        self.bg_color = "#000813"
        self.fg_color = "#EEEEEE"
        self.entry_bg = "#5D6674"
        self.btn_bg = "#00ADB5"
        self.btn_fg = "#EEEEEE"
        self.btn_active_bg = "#019ca1"
        self.font_main = ("Segoe UI", 16)  # Aumenta a fonte principal
        self.font_small = ("Segoe UI", 14)

        self.criar_widgets()
        self.atualizar_campos()

    def criar_widgets(self):
        padx = 20
        pady = 12

        # Frame principal (entrada e cálculo)
        frame_principal = tk.Frame(self.root, bg=self.bg_color)
        frame_principal.pack(side=tk.TOP, padx=padx, pady=pady, fill=tk.BOTH, expand=True)

        # Frame topo: entrada + operação + campos extras
        frame_topo = tk.Frame(frame_principal, bg=self.bg_color)
        frame_topo.pack(fill=tk.X, padx=padx, pady=pady)

        # Label e entrada da função
        tk.Label(frame_topo, text="Entrada de dados: ", bg=self.bg_color, fg=self.fg_color, font=self.font_main).grid(row=0, column=0, sticky="w")
        self.entrada_funcao = tk.Entry(frame_topo, width=72, font=self.font_main, bg=self.entry_bg, fg=self.fg_color, insertbackground=self.fg_color, relief=tk.FLAT)
        self.entrada_funcao.grid(row=0, column=1, columnspan=7, sticky="w")

        # Label e combobox operação
        tk.Label(frame_topo, text="Operação:", bg=self.bg_color, fg=self.fg_color, font=self.font_main).grid(row=1, column=0, sticky="w", pady=(10,0))
        operacoes = [
            "Função",
            "Limite",
            "Derivada",
            "Integral Indefinida",
            "Integral Definida",
            "Equação 1º Grau",
            "Equação 2º Grau",
            "Equação 3º Grau"
        ]
        self.combo_operacoes = ttk.Combobox(frame_topo, values=operacoes, state="readonly", width=50, font=self.font_main)
        self.combo_operacoes.current(0)
        self.combo_operacoes.grid(row=1, column=1, columnspan=7, sticky="w", pady=(10,0))
        self.combo_operacoes.bind("<<ComboboxSelected>>", lambda e: self.atualizar_campos())

        # Frame campos extras (ponto, limites)
        self.frame_extras = tk.Frame(frame_topo, bg=self.bg_color)
        self.frame_extras.grid(row=2, column=0, columnspan=8, sticky="w", pady=(10,0))

        # Novo campo para entrada do valor de x
        self.label_x = tk.Label(self.frame_extras, text="Valor de x:", bg=self.bg_color, fg=self.fg_color, font=self.font_main)
        self.entrada_x = tk.Entry(self.frame_extras, width=28, font=self.font_main, bg=self.entry_bg, fg=self.fg_color, insertbackground=self.fg_color, relief=tk.FLAT)

        self.label_ponto = tk.Label(self.frame_extras, text="Ponto (ex: 1, oo):", bg=self.bg_color, fg=self.fg_color, font=self.font_main)
        self.entrada_ponto = tk.Entry(self.frame_extras, width=28, font=self.font_main, bg=self.entry_bg, fg=self.fg_color, insertbackground=self.fg_color, relief=tk.FLAT)

        self.label_limite_inf = tk.Label(self.frame_extras, text="Limite inferior:", bg=self.bg_color, fg=self.fg_color, font=self.font_main)
        self.entrada_limite_inf = tk.Entry(self.frame_extras, width=28, font=self.font_main, bg=self.entry_bg, fg=self.fg_color, insertbackground=self.fg_color, relief=tk.FLAT)
        self.label_limite_sup = tk.Label(self.frame_extras, text="Limite superior:", bg=self.bg_color, fg=self.fg_color, font=self.font_main)
        self.entrada_limite_sup = tk.Entry(self.frame_extras, width=28, font=self.font_main, bg=self.entry_bg, fg=self.fg_color, insertbackground=self.fg_color, relief=tk.FLAT)

        # Frame teclado
        self.frame_teclado = tk.Frame(frame_principal, bg=self.bg_color)
        self.frame_teclado.pack(padx=padx, pady=(10,0), fill=tk.BOTH, expand=True)
        self.criar_teclado_cientifico()

        # Frame botoes calcular e limpar
        frame_botoes = tk.Frame(frame_principal, bg=self.bg_color)
        frame_botoes.pack(pady=20)
        self.botao_calcular = tk.Button(frame_botoes, text="Calcular", command=self.calcular_com_thread, width=20, font=self.font_main,
                                       bg="#FFA500", fg="black", activebackground="#FF8C00", relief=tk.FLAT, bd=0)  # Cor preta para a letra
        self.botao_calcular.pack(side=tk.LEFT, padx=15)
        self.botao_limpar = tk.Button(frame_botoes, text="Limpar", command=self.limpar_campos, width=20, font=self.font_main,
                                     bg=self.btn_bg, fg="black", activebackground="#019ca1", relief=tk.FLAT, bd=0)  # Cor preta para a letra
        self.botao_limpar.pack(side=tk.LEFT, padx=15)

        # Frame para resultados lado a lado
        frame_resultado = tk.Frame(self.root, bg=self.bg_color)
        frame_resultado.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=padx, pady=pady)

        # Parte 1: Resultado da expressão - em um lado
        self.text_resultado = scrolledtext.ScrolledText(frame_resultado, width=40, height=12, wrap=tk.WORD, font=("Consolas", 16),
                                                       bg=self.entry_bg, fg=self.fg_color, relief=tk.FLAT, insertbackground=self.fg_color)
        self.text_resultado.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        # Parte 2: Frame para o gráfico - do outro lado
        self.frame_grafico = tk.Frame(frame_resultado, bg=self.bg_color)
        self.frame_grafico.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        frame_resultado.grid_columnconfigure(0, weight=1)
        frame_resultado.grid_columnconfigure(1, weight=1)

    def criar_teclado_cientifico(self):
        # Define as teclas de maneira mais organizada, agora com a tecla "elevado a" (^) adicionada
        teclas = [
            ['7', '8', '9', '(', ')', 'sin(', 'cos(', 'tan('],
            ['4', '5', '6', '√', 'oo', 'asin(', 'acos(', 'atan('],
            ['1', '2', '3', '+', '-', 'log(', 'ln(', 'exp('],
            ['0', '.', 'π', 'e', 'x', '/', '*', '^'],  # Adiciona a tecla "elevado a" (^) aqui
            ['CE', 'DEL', '<', '>', 'abs(', 'sqrt(']
        ]

        for widget in self.frame_teclado.winfo_children():
            widget.destroy()  # Limpa o teclado antigo

        # Adiciona as teclas de forma organizada com espaçamento entre elas
        for r, linha in enumerate(teclas):
            for c, tecla in enumerate(linha):
                largura = 4  # Diminuindo a largura das teclas para compactar
                altura = 2
                cmd = None

                if tecla == 'CE':
                    cmd = self.limpar_entrada
                elif tecla == 'DEL':
                    cmd = self.apagar_ultimo
                elif tecla == '=':
                    cmd = self.calcular_com_thread
                else:
                    cmd = lambda t=tecla: self.inserir_texto(t)

                # Se a tecla for um número (0-9), a cor de fundo será branca e o texto será preto
                if tecla.isdigit():
                    btn = tk.Button(self.frame_teclado, text=tecla, width=largura, height=altura, font=("Segoe UI", 12),
                                    bg="white", fg="black", activebackground="#019ca1", relief=tk.RAISED, bd=1, command=cmd)
                else:
                    # Estilo das teclas com bordas retas e cor de fundo para outras teclas
                    btn = tk.Button(self.frame_teclado, text=tecla, width=largura, height=altura, font=("Segoe UI", 12),
                                    bg="#00ADB5", fg="#000000", activebackground="#019ca1", relief=tk.RAISED, bd=1, command=cmd)
                
                btn.grid(row=r, column=c, padx=5, pady=5, sticky="nsew")

        # Configura as linhas e colunas para esticar as teclas
        for i in range(len(teclas)):
            self.frame_teclado.grid_rowconfigure(i, weight=1)
        for i in range(len(teclas[0])):
            self.frame_teclado.grid_columnconfigure(i, weight=1)

    def inserir_texto(self, texto):
        pos = self.entrada_funcao.index(tk.INSERT)
        # Apenas insere o texto como está, sem modificar o "^" para "**"
        self.entrada_funcao.insert(pos, texto)
        self.entrada_funcao.focus()

    def limpar_entrada(self):
        self.entrada_funcao.delete(0, tk.END)
        self.entrada_funcao.focus()

    def apagar_ultimo(self):
        pos = self.entrada_funcao.index(tk.INSERT)
        if pos > 0:
            self.entrada_funcao.delete(pos - 1)
            self.entrada_funcao.icursor(pos - 1)
        self.entrada_funcao.focus()

    def atualizar_campos(self):
        for widget in self.frame_extras.winfo_children():
            widget.grid_forget()

        op = self.combo_operacoes.get()
        if op == "Limite":
            self.label_ponto.grid(row=0, column=0, sticky="w", padx=5, pady=5)
            self.entrada_ponto.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        elif op == "Integral Definida":
            self.label_limite_inf.grid(row=0, column=0, sticky="w", padx=5, pady=5)
            self.entrada_limite_inf.grid(row=0, column=1, sticky="w", padx=5, pady=5)
            self.label_limite_sup.grid(row=1, column=0, sticky="w", padx=5, pady=5)
            self.entrada_limite_sup.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        elif op == "Função":  # Exibe o campo para inserir x
            self.label_x.grid(row=0, column=0, sticky="w", padx=5, pady=5)
            self.entrada_x.grid(row=0, column=1, sticky="w", padx=5, pady=5)

    def limpar_campos(self):
        self.entrada_funcao.delete(0, tk.END)
        self.entrada_ponto.delete(0, tk.END)
        self.entrada_limite_inf.delete(0, tk.END)
        self.entrada_limite_sup.delete(0, tk.END)
        self.entrada_x.delete(0, tk.END)  # Limpa o campo de x
        self.text_resultado.delete("1.0", tk.END)  # Limpa a área de resultados

        # Remove qualquer gráfico existente
        for widget in self.frame_grafico.winfo_children():
            widget.destroy()

    def calcular_com_thread(self):
        # Executa o cálculo em um thread separado para evitar travar a interface
        thread = threading.Thread(target=self.calcular)
        thread.start()

    def calcular(self):
        funcao_str = self.entrada_funcao.get().strip()  # Obtém a expressão da entrada do usuário
        operacao = self.combo_operacoes.get()  # Verifica qual operação foi selecionada

        if not funcao_str:
            messagebox.showwarning("Atenção", "Informe a função para calcular.")
            return

        # Corrige a função de entrada para lidar com "^" como "**" e "√" como "sqrt"
        funcao_str_corrigida = funcao_str.replace(" ", "")  # Remove espaços
        funcao_str_corrigida = funcao_str_corrigida.replace('^', '**')  # Corrige "^" para "**"
        funcao_str_corrigida = funcao_str_corrigida.replace('√', 'sqrt')  # Substitui '√' por 'sqrt'
        funcao_str_corrigida = self.corrigir_multiplicacao(funcao_str_corrigida)  # Corrige multiplicação entre número e x

        try:
            # Definindo as variáveis que podem ser usadas nas expressões
            variaveis = [symbol for symbol in funcao_str_corrigida if symbol.isalpha()]
            variaveis = list(set(variaveis))  # Remover duplicatas
            variaveis = symbols(variaveis)  # Criando as variáveis

            funcao = sympify(funcao_str_corrigida, evaluate=True)  # Converte a string para uma expressão simbólica

            if "derivada" in operacao.lower():
                derivada = diff(funcao, variaveis[0])  # Calcula a derivada
                derivada_simplificada = simplify(derivada)  # Simplifica a derivada
                resultado = pretty(derivada_simplificada)

                # Não gera gráfico nas derivadas
                self.text_resultado.delete("1.0", tk.END)
                self.text_resultado.insert(tk.END, resultado)

                return  # Não gera gráfico para a derivada

            elif "limite" in operacao.lower():
                ponto_str = self.entrada_ponto.get().strip()
                if not ponto_str:
                    messagebox.showwarning("Atenção", "Informe o ponto onde calcular o limite.")
                    return

                ponto = sympify(ponto_str)  # Converte o ponto para um valor simbólico
                resultado = f"{limit(funcao, variaveis[0], ponto)}"  # Calcula o limite

                # Não gera gráfico para operação Limite
                self.text_resultado.delete("1.0", tk.END)
                self.text_resultado.insert(tk.END, resultado)

                return  # Não gera gráfico para o limite

            elif "integral indefinida" in operacao.lower():
                integral = integrate(funcao, variaveis[0])
                resultado = pretty(integral) + " + C"  # Adiciona a constante de integração

            elif "integral definida" in operacao.lower():
                limite_inf = sympify(self.entrada_limite_inf.get())
                limite_sup = sympify(self.entrada_limite_sup.get())
                integral_definida = integrate(funcao, (variaveis[0], limite_inf, limite_sup))  # Calcula a integral definida
                resultado = pretty(integral_definida)

            elif "função" in operacao.lower():  # Se for apenas uma função
                valor_x_str = self.entrada_x.get().strip()  # Obtém o valor de x
                if valor_x_str:
                    try:
                        # Converte o valor de x para um número decimal ou simbólico
                        valor_x = sympify(valor_x_str) if '.' in valor_x_str else float(valor_x_str)  # Verifica se é decimal
                        resultado = funcao.subs(variaveis[0], valor_x)  # Substitui na função e calcula o valor

                        # Formata o resultado com 2 casas decimais
                        resultado_formatado = round(resultado, 2)
                        resultado = f"f(x) = {resultado_formatado}"  # Exibe o valor da função em x
                    except Exception as e:
                        resultado = f"Erro ao calcular f(x) para x={valor_x}: {e}"
                else:
                    resultado = f"f(x) = {pretty(funcao)}"  # Exibe a função simbólica se x não for fornecido

            elif "equação 1º grau" in operacao.lower():  # Se for uma equação de 1º grau
                partes = funcao_str_corrigida.split("=")  # Divide a equação em dois lados
                if len(partes) == 2:
                    eq_lado_esquerdo = sympify(partes[0].strip())  # Expressão do lado esquerdo
                    eq_lado_direito = sympify(partes[1].strip())  # Expressão do lado direito

                    eq = Eq(eq_lado_esquerdo, eq_lado_direito)  # Cria a equação para resolver

                    solucao = solveset(eq, variaveis[0], domain=S.Reals)  # Resolve a equação para x

                    if solucao == S.EmptySet:
                        resultado = "Nenhuma solução encontrada."
                    else:
                        resultado = f"Solução: {solucao}"

            # Exibe o resultado no campo de texto antes do gráfico
            self.text_resultado.delete("1.0", tk.END)
            self.text_resultado.insert(tk.END, resultado)

            # Exclui qualquer gráfico anterior antes de plotar o novo
            for widget in self.frame_grafico.winfo_children():
                widget.destroy()

            if "derivada" not in operacao.lower() and "limite" not in operacao.lower():  # Não gerar gráfico nas derivadas e limites
                self.plotar_funcao(funcao)

        except SympifyError:
            messagebox.showerror("Erro", "Função inválida! Verifique a sintaxe.")
            return
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao calcular: {e}")

    def corrigir_multiplicacao(self, funcao_str):
        """
        Função para adicionar '*' entre números e variáveis onde falta a multiplicação.
        """
        funcao_str = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', funcao_str)
        funcao_str = re.sub(r'([a-zA-Z])(\d)', r'\1*\2', funcao_str)
        
        return funcao_str

    def plotar_funcao(self, funcao):
        # Gera um gráfico para a função fornecida
        x_vals = [i for i in range(-10, 11)]  # Gera x de -10 a 10
        y_vals = [funcao.subs(self.vars[0], x) for x in x_vals]

        fig, ax = plt.subplots(figsize=(3, 2))  # Aumenta ou diminui a largura e altura (em polegadas)

        ax.plot(x_vals, y_vals, label="f(x)")

        ax.set(xlabel='x', ylabel='f(x)', title="Gráfico de f(x)")
        ax.grid(True)
        ax.legend()

        # Exibe o gráfico na interface
        canvas = FigureCanvasTkAgg(fig, master=self.frame_grafico)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculadoraCientifica(root)
    root.mainloop()
