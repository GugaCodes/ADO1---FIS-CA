from fisica import calcular_trajetoria
import matplotlib.pyplot as plt

xs,ys,tempos = calcular_trajetoria(30,45,5,9.81)

print("Primeiros X:", xs[:10])
print("Primeiros Y:", ys[:10])

print("Últimos X:", xs[-10:])
print("Últimos Y:", ys[-10:])

#desenhando uma linha usando xs como X e ys como Y
plt.plot(xs,ys)
#Coloacando nome dos eixos
plt.xlabel("Distânica horizontal (m)")
plt.ylabel("Altura (m)")
#Colocando titulo do gáfico
plt.title("Trajetoria do Projétil")
#Colocando em uma grade para melhor vizualização
plt.grid()
#Mostrando o Gráfico
plt.show()

