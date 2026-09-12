from fisica import calcular_trajetoria
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

xs, ys, tempos = calcular_trajetoria(20, 35, 5, 9.81)

print("Primeiros X:", xs[:10])
print("Primeiros Y:", ys[:10])

print("Últimos X:", xs[-10:])
print("Últimos Y:", ys[-10:])

# Criando o gráfico
fig, ax = plt.subplots()

ax.set_xlim(min(xs), max(xs))
ax.set_ylim(min(ys), max(ys))

ax.set_xlabel("Distância horizontal (m)")
ax.set_ylabel("Altura (m)")
ax.set_title("Trajetória do Projétil")
ax.grid()

# Animação

linha, = ax.plot([], [])
ponto, = ax.plot([], [], 'o')

# Função que atualiza a animação
def atualizar(i):
    # Desenha a trajetória até o ponto atual
    linha.set_data(xs[:i + 1], ys[:i + 1])
    # Move o projétil para o ponto atual
    ponto.set_data([xs[i]], [ys[i]])
    return linha, ponto

# Criando a animação
anim = FuncAnimation(
    fig,
    atualizar,
    frames=len(xs),
    interval=50,
    repeat=False
)

plt.show()