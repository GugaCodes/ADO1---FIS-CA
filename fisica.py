import math


x0 = 0

def calcular_resultados(v0,angulo,y0,g):

    theta = math.radians(angulo)

    #pegando o v0 e o angulo e transformando em componentes horizontais e verticais
    vx = v0 * math.cos(theta) #VELOCIDADE HORIZONTAL
    vy = v0 * math.sin(theta) # VELOCIDADE VERTICAL
    #==========================================================
    #fazendo a formula que calcula o tempo de voo
    # vy² = vy ** 2
    # 2gy0 = 2 * g * y0
    #==========================================================

    tempo_voo = (vy + math.sqrt(vy ** 2 + 2 * g * y0)) / g

    #Calculando a altura máxima
    altura_maxima = y0 + (vy ** 2) / (2 * g)

    #Calculando o alcance horizontal


    alcance_horizontal = x0 + vx * tempo_voo

    return alcance_horizontal, altura_maxima, tempo_voo


def calcular_posicao(v0,angulo,y0,g,t):

    theta = math.radians(angulo)

    # pegando o v0 e o angulo e transformando em componentes horizontais e verticais
    vx = v0 * math.cos(theta)
    vy = v0 * math.sin(theta)

    #Calculadndo as formulas

    x = x0 + vx*t #minha função x(t)
    y = y0 + vy * t - 0.5 * g * t ** 2 # minha função y(t)

    return x,y

def calcular_trajetoria(v0, angulo, y0, g):
    _, _, tempo_voo = calcular_resultados(v0,angulo,y0,g)

    #Criando uma lista de tempos
    tempos = []
    t = 0

    #Criando loop para preecher a lista enquanto t <= tempo de voo
    while t<= tempo_voo:
        tempos.append(t)
        t += 0.1

    tempos.append(tempo_voo)

    xs = [] # posições horizontais
    ys = [] #posições verticais

    #loop em para cada tempo que está dentro da lista de tempos, calculamos o x e y
    for t in tempos:
        x,y = calcular_posicao(v0,angulo,y0,g,t)
        xs.append(x)
        ys.append(y)

    return xs,ys,tempos
#=============================
# FORA DAS FUNÇÕES - AREA DE TESTE
# ============================
'''alcance, altura, tempo_voo = calcular_resultados(
    v0=30,
    angulo=45,
    y0=5,
    g=9.81
)

x,y = calcular_posicao(
    v0 = 30,
    angulo=45,
    y0 = 5,
    g = 9.81,
    t = 2
)

xs, ys, tempos = calcular_trajetoria(
    v0=30,
    angulo=45,
    y0=5,
    g=9.81
)

print("X:", x)
print("Y:", y)

print("Quantidade de pontos:", len(xs))
print("Primeiro X:", xs[0])
print("Primeiro Y:", ys[0])
print("Último X:", xs[-1])
print("Último Y:", ys[-1])'''