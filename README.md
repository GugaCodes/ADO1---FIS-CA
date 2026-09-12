# 🚀 Lançamento de Projéteis — Física

Interface gráfica interativa desenvolvida em **Python** para simulação de **lançamento de projéteis em 2D**, utilizando os conceitos de Física e programação.

O projeto permite alterar os principais parâmetros do lançamento e acompanhar a trajetória do projétil e os resultados físicos em tempo real.

---

## 📌 Sobre o projeto

A aplicação simula um lançamento de projétil considerando um modelo ideal, **sem resistência do ar**.

Os parâmetros podem ser alterados diretamente pela interface:

- **Velocidade inicial (v₀):** de 5 a 150 m/s
- **Ângulo de lançamento (θ):** de 1° a 89°
- **Altura inicial (y₀):** de 0 a 50 m
- **Aceleração da gravidade (g):** de 1,6 a 24,8 m/s²

Também é possível utilizar presets de gravidade para diferentes corpos celestes:

- 🌙 Lua — 1,62 m/s²
- 🔴 Marte — 3,71 m/s²
- 🌎 Terra — 9,81 m/s²
- 🪐 Júpiter — 24,79 m/s²

---

## ✨ Funcionalidades

### 🎛️ Simulação em tempo real

Ao alterar os parâmetros pelos sliders ou pelos campos numéricos, a trajetória e os resultados são recalculados automaticamente.

### 📊 Resultados físicos

A aplicação apresenta:

- **Alcance horizontal (R)**
- **Altura máxima (yₘₐₓ)**
- **Tempo de voo (tᵥₒₒ)**

### ▶️ Animação do lançamento

Ao clicar em **Lançar projétil**, um ponto representa o projétil e percorre a trajetória calculada.

A curva também é desenhada progressivamente durante a animação.

É possível interromper o lançamento utilizando o botão **Parar animação**.

### 📈 Comparação de trajetórias

A aplicação permite adicionar trajetórias ao mesmo gráfico para facilitar a comparação entre diferentes lançamentos.

Por exemplo:

- diferentes velocidades;
- diferentes ângulos;
- diferentes alturas iniciais;
- diferentes valores de gravidade.

As trajetórias adicionadas podem ser removidas utilizando o botão **Limpar comparações**.

### ↻ Restaurar valores

O botão **Restaurar valores** retorna os parâmetros para os valores padrão:

```text
v₀ = 30 m/s
θ = 45°
y₀ = 5 m
g = 9,81 m/s²
