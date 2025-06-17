Documentação da Calculadora Científica
Este projeto implementa uma Calculadora Científica interativa com interface gráfica utilizando Tkinter, processamento simbólico de expressões matemáticas com SymPy, e visualização gráfica das funções com Matplotlib. A aplicação permite realizar uma variedade de operações matemáticas, como cálculo de derivadas, integrais, limites e soluções de equações de 1º, 2º e 3º grau.

Funcionalidades
A calculadora oferece as seguintes funcionalidades:

Função: Avalia uma função matemática para um valor específico de 
𝑥
x.

Limite: Calcula o limite de uma função em um ponto determinado.

Derivada: Calcula a derivada simbólica de uma função.

Integral Indefinida: Calcula a integral indefinida de uma função.

Integral Definida: Calcula a integral definida de uma função, com limites inferior e superior.

Equação 1º Grau: Resolve equações do tipo 
𝑎
𝑥
+
𝑏
=
0
ax+b=0.

Equação 2º e 3º Grau: Resolve equações quadráticas e cúbicas.

Requisitos
Para executar a calculadora, você precisa instalar as seguintes bibliotecas:

tkinter: Interface gráfica.

sympy: Manipulação simbólica de expressões matemáticas.

matplotlib: Geração de gráficos das funções.

Instale as dependências com o seguinte comando:

bash
Copiar
pip install sympy matplotlib
Estrutura do Código
1. Interface Gráfica
A interface gráfica foi desenvolvida com Tkinter e é dividida nas seguintes seções:

Entrada de Dados: Área para inserção da função matemática.

Operações Matemáticas: Um Combobox para selecionar a operação desejada (Função, Limite, Derivada, etc.).

Teclado Científico: Teclado com números e funções matemáticas.

Área de Resultados: Exibe o resultado da operação.

Gráfico: Exibe o gráfico da função, caso aplicável.

2. Teclado Científico
O teclado da calculadora oferece uma interface amigável para a inserção de expressões matemáticas. Ele inclui botões para números, operadores aritméticos, funções matemáticas (como seno, cosseno, logaritmos) e operações especiais (como potência e radiciação). O teclado é organizado para facilitar a digitação de funções complexas.

3. Cálculos Realizados
O código é projetado para realizar uma variedade de operações matemáticas. Dependendo da operação selecionada, a calculadora realiza o cálculo correspondente.

3.1 Função
Descrição: Calcula o valor de uma função para um valor específico de 
𝑥
x.

Exemplo: Se a função for 
𝑓
(
𝑥
)
=
𝑥
2
+
3
𝑥
+
5
f(x)=x 
2
 +3x+5, insira o valor de 
𝑥
x e obtenha o resultado.

3.2 Limite
Descrição: Calcula o limite de uma função em um ponto.

Exemplo: Calcule o limite de 
1
𝑥
x
1
​
  quando 
𝑥
x se aproxima de 0.

3.3 Derivada
Descrição: Calcula a derivada de uma função simbólica em relação a uma variável.

Exemplo: Calcule a derivada de 
𝑓
(
𝑥
)
=
𝑥
3
+
2
𝑥
2
f(x)=x 
3
 +2x 
2
 .

3.4 Integral Indefinida
Descrição: Calcula a integral indefinida de uma função.

Exemplo: Calcule a integral indefinida de 
𝑓
(
𝑥
)
=
3
𝑥
2
f(x)=3x 
2
 .

3.5 Integral Definida
Descrição: Calcula a integral definida de uma função, com limites inferior e superior.

Exemplo: Calcule a integral definida de 
𝑓
(
𝑥
)
=
𝑥
2
f(x)=x 
2
  de 
0
0 a 
2
2.

3.6 Equações de 1º, 2º e 3º Grau
Descrição: Resolve equações lineares, quadráticas e cúbicas.

Exemplo: Resolva a equação 
3
𝑥
+
5
=
0
3x+5=0 ou 
𝑥
2
+
2
𝑥
−
8
=
0
x 
2
 +2x−8=0.

4. Geração de Gráficos
A calculadora pode gerar gráficos das funções inseridas, utilizando a biblioteca Matplotlib. O gráfico será exibido na interface ao lado do resultado da operação. Ele é gerado para todas as operações, exceto para as derivadas e limites, que não geram gráficos.

5. Execução em Threads
O cálculo das operações é realizado em um thread separado para garantir que a interface não trave durante o processamento de cálculos mais complexos, como integrais e equações de grau superior.

6. Correção de Sintaxe
A entrada do usuário é corrigida automaticamente antes do cálculo, transformando símbolos como ^ para ** e √ para sqrt, além de corrigir multiplicações entre números e variáveis que podem ser digitadas sem o operador * (ex: 2x se torna 2*x).

7. Exemplo de Uso
Inicie o programa.

Digite uma função matemática na área de entrada de dados.

Selecione a operação desejada no Combobox.

Clique em "Calcular".

O resultado será exibido na área de resultados, com o gráfico gerado ao lado, se aplicável.

Personalização
O código permite a personalização das cores e do layout da interface. As cores de fundo, texto, botões e fontes estão configuradas nas variáveis dentro da classe CalculadoraCientifica. Além disso, você pode ajustar o layout para se adequar às suas preferências.

Conclusão
Esta Calculadora Científica é uma ferramenta poderosa e interativa que combina uma interface gráfica intuitiva com cálculos simbólicos avançados e visualização gráfica de funções. Ela foi projetada para ser simples de usar, mas também flexível o suficiente para realizar uma ampla gama de operações matemáticas.