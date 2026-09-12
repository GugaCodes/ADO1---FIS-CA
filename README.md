Markdown(1).md colado
Arquivo
n funcionou


Markdown(2).md colado
Arquivo
Continua sem funcionar

a4665c7b-84df-45a4-9fef-09211db7b829.png
Markdown(3).md colado
Arquivo
aparece esse erro quando aperta em lançar

a9ebb94f-5cd8-41c7-b71b-860d80be1ef0.png
deu esse erro

AEEEE 😎🔥

Agora a comparação já está funcionando.

Vamos para a segunda parte: fazer o botão “Limpar comparações” apagar somente as curvas que foram salvas, sem apagar a trajetória atual.

A lógica será simples:

self.comparacoes
      ↓
guarda cada linha criada pelo botão Comparar
      ↓
Limpar comparações
      ↓
remove cada linha da lista
      ↓
gráfico volta a ficar limpo

No seu __init__, você já tem:

self.comparacoes = []

Então agora precisamos apenas ligar o botão:

self.btn_limpar = ctk.CTkButton(
    self.sidebar,
    text="×  Limpar comparações",
    anchor="w",
    height=40,
    corner_radius=8,
    fg_color="transparent",
    border_width=1,
    border_color=self.border,
    hover_color="#292929",
    command=self.limpar_comparacoes
)

Depois crie, dentro da classe:

def limpar_comparacoes(self):

    for linha in self.comparacoes:
        linha.remove()

    self.comparacoes.clear()

    self.canvas.draw()

O que cada parte faz?

for linha in self.comparacoes:

Passa por todas as curvas que você salvou.

linha.remove()

Remove aquela curva do Matplotlib.

self.comparacoes.clear()

Esvazia a lista para podermos fazer novas comparações.

self.canvas.draw()

Atualiza o gráfico na tela.
Teste

Faça:

    comparação com 45°;

    mude para 60°;

    compare novamente;

    mude para 30°;

    compare de novo;

    clique em Limpar comparações.

As curvas comparativas devem desaparecer.

A trajetória/esboço atual não deve ser apagada, porque ela não está dentro de self.comparacoes.

Depois disso, a gente pode melhorar uma coisa bem legal: fazer cada comparação ter uma legenda com os parâmetros usados (por exemplo v₀=30, θ=45°, g=9,81), que deixaria a apresentação muito mais profissional.

funcionando

BOAAAA 😎🔥

Agora vocês já têm a parte de comparação funcionando também. O projeto está ficando bem completo.

Eu faria agora uma última melhoria importante na comparação: colocar uma legenda identificando cada trajetória com os parâmetros usados. Assim, durante a apresentação, dá para olhar o gráfico e saber qual curva corresponde a cada lançamento.

Por exemplo:

Trajetória 1 → v₀=30 m/s | θ=45° | g=9,81
Trajetória 2 → v₀=30 m/s | θ=60° | g=9,81

Isso também deixaria o recurso de comparação muito mais claro visualmente.

agr faça o read me desse projeto pf

Boa! Montei um README.md já estruturado com:

    descrição do projeto;

    funcionalidades;

    fórmulas da Física;

    tecnologias utilizadas;

    estrutura dos arquivos;

    instalação e execução;

    instruções de uso;

    tratamento de entradas;

    objetivo acadêmico.

Baixar README.md
README.mdDocumento
Melhore a precisão em tarefas técnicas
Assine o Plus e use raciocínio ampliado para depurar código, analisar sistemas e resolver problemas de matemática ou ciências.
Voltar ao Plus


Lançamento de Projéteis — Física

Interface gráfica interativa para simulação de lançamento de projéteis em 2D, desenvolvida em Python para a disciplina de Física.

O projeto permite alterar os principais parâmetros do lançamento e visualizar, em tempo real, a trajetória do projétil e os resultados físicos calculados.
📌 Sobre o projeto

A aplicação simula um lançamento de projétil considerando um modelo ideal, sem resistência do ar.

Os parâmetros podem ser alterados diretamente pela interface:

    Velocidade inicial (v₀): de 5 a 150 m/s

    Ângulo de lançamento (θ): de 1° a 89°

    Altura inicial (y₀): de 0 a 50 m

    Aceleração da gravidade (g): de 1,6 a 24,8 m/s²

Também é possível selecionar presets de gravidade para Lua, Marte, Terra e Júpiter.
✨ Funcionalidades
Simulação em tempo real

Ao alterar os parâmetros pelos sliders ou pelos campos numéricos, a trajetória e os resultados são recalculados automaticamente.
Resultados físicos

A aplicação apresenta:

    Alcance horizontal (R)

    Altura máxima (yₘₐₓ)

    Tempo de voo (tᵥₒₒ)

Animação do lançamento

Ao clicar em Lançar projétil, o ponto que representa o projétil percorre a trajetória calculada enquanto a linha da curva é desenhada progressivamente.

Também existe a opção de Parar animação.
Comparação de trajetórias

A aplicação permite salvar trajetórias para comparação. É possível alterar os parâmetros e adicionar novas curvas ao mesmo gráfico.

As comparações podem ser removidas pelo botão Limpar comparações.
Restaurar valores

O botão Restaurar valores retorna os parâmetros para:

    v₀ = 30 m/s

    θ = 45°

    y₀ = 5 m

    g = 9,81 m/s²

🧮 Física utilizada

A aplicação utiliza as equações do lançamento oblíquo sem resistência do ar.
Componentes da velocidade

vₓ = v₀ · cos(θ)
vᵧ = v₀ · sen(θ)

Posição horizontal

x(t) = x₀ + vₓ · t

Posição vertical

y(t) = y₀ + vᵧ · t − (g · t²)/2

Tempo de voo

Considerando o retorno do projétil ao nível do solo:

tᵥₒₒ = (vᵧ + √(vᵧ² + 2gy₀)) / g

Altura máxima

yₘₐₓ = y₀ + vᵧ² / (2g)

Alcance horizontal

R = x₀ + vₓ · tᵥₒₒ

🖥️ Tecnologias utilizadas

    Python

    CustomTkinter — interface gráfica

    Tkinter — integração com a interface

    Matplotlib — gráficos e visualização da trajetória

    Math — cálculos matemáticos

📁 Estrutura do projeto

PROJETO/
│
├── layout.py
├── fisica.py
└── README.md

layout.py

Responsável pela interface gráfica, controles, resultados, gráfico, animação e interação do usuário.
fisica.py

Responsável pelos cálculos físicos da simulação, mantendo a lógica da Física separada da interface.

Principais funções:

calcular_resultados()
calcular_posicao()
calcular_trajetoria()

⚙️ Como executar
1. Instale o Python

Utilize Python 3.
2. Instale as bibliotecas

No terminal:

pip install customtkinter matplotlib

3. Execute o projeto

Na pasta do projeto:

python layout.py

🎮 Como utilizar

    Abra a aplicação.

    Ajuste a velocidade, o ângulo, a altura inicial e a gravidade.

    Observe a atualização da trajetória e dos resultados.

    Utilize os presets para alterar a gravidade rapidamente.

    Clique em Lançar projétil para visualizar a animação.

    Use Parar animação para interromper o lançamento.

    Utilize Comparar trajetória para adicionar a trajetória atual ao gráfico.

    Use Limpar comparações para remover as trajetórias salvas.

    Clique em Restaurar valores para voltar aos parâmetros padrão.

⚠️ Tratamento de entradas

Os campos numéricos possuem validação de faixa.

Valores fora dos limites definidos ou entradas inválidas são rejeitados e o valor anterior é restaurado.

Também é possível utilizar vírgula como separador decimal nos campos de entrada, por exemplo:

9,81

🎯 Objetivo acadêmico

O projeto foi desenvolvido com o objetivo de unir os conceitos de lançamento de projéteis, programação em Python e desenvolvimento de interfaces gráficas interativas.

Além dos cálculos físicos, a aplicação demonstra a utilização de:

    funções e modularização;

    manipulação de eventos;

    atualização de componentes gráficos;

    animação;

    integração entre bibliotecas;

    validação de entradas;

    visualização gráfica.

👨‍💻 Autores

Projeto acadêmico desenvolvido para a disciplina de Física.
