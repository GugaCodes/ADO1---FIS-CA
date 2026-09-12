import customtkinter as ctk
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
from fisica import calcular_trajetoria

# ============================================================
# CONFIGURAÇÕES
# ============================================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class Aplicativo(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Lançamento de Projéteis — Física")
        self.geometry("1400x850")
        self.minsize(1150, 720)

        # Cores usadas na interface
        self.bg = "#202020"
        self.sidebar_bg = "#161616"
        self.panel = "#282828"
        self.panel_2 = "#303030"
        self.graph_bg = "#181818"
        self.border = "#404040"
        self.text_gray = "#A8A8A8"

        # Lista que guarda todas as trajetórias já lançadas
        self.trajetorias_comparadas = []

        # ========================================================
        # GRID PRINCIPAL
        # ========================================================

        self.grid_columnconfigure(0, weight=0, minsize=240)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ========================================================
        # SIDEBAR
        # ========================================================

        self.sidebar = ctk.CTkFrame(self, corner_radius=0, fg_color=self.sidebar_bg)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(6, weight=1)

        ctk.CTkLabel(
            self.sidebar,
            text="Lançamento\nde Projéteis",
            font=ctk.CTkFont(size=25, weight="bold"),
            justify="left"
        ).grid(row=0, column=0, padx=25, pady=(30, 6), sticky="w")

        ctk.CTkLabel(
            self.sidebar,
            text="Simulação 2D • Física ideal",
            text_color=self.text_gray,
            font=ctk.CTkFont(size=13)
        ).grid(row=1, column=0, padx=25, pady=(0, 28), sticky="w")

        self.btn_simulacao = ctk.CTkButton(
            self.sidebar, text="●  Simulação", anchor="w", height=42, corner_radius=8
        )
        self.btn_simulacao.grid(row=2, column=0, padx=15, pady=5, sticky="ew")

        self.btn_restaurar = ctk.CTkButton(
            self.sidebar,
            text="↻  Restaurar valores",
            anchor="w", height=40, corner_radius=8,
            fg_color="transparent", border_width=1,
            border_color=self.border, hover_color="#292929"
        )
        self.btn_restaurar.grid(row=3, column=0, padx=15, pady=5, sticky="ew")

        self.btn_comparar = ctk.CTkButton(
            self.sidebar,
            text="＋  Comparar trajetória",
            anchor="w", height=40, corner_radius=8,
            fg_color="transparent", border_width=1,
            border_color=self.border, hover_color="#292929",
            command=self.lancar_projetil
        )
        self.btn_comparar.grid(row=4, column=0, padx=15, pady=5, sticky="ew")

        self.btn_limpar = ctk.CTkButton(
            self.sidebar,
            text="×  Limpar comparações",
            anchor="w", height=40, corner_radius=8,
            fg_color="transparent", border_width=1,
            border_color=self.border, hover_color="#292929",
            command=self.limpar_comparacoes
        )
        self.btn_limpar.grid(row=5, column=0, padx=15, pady=5, sticky="ew")

        ctk.CTkLabel(
            self.sidebar,
            text="Física • Práticas Extensivas",
            text_color=self.text_gray,
            font=ctk.CTkFont(size=11)
        ).grid(row=7, column=0, padx=17, pady=(0, 4), sticky="w")

        ctk.CTkLabel(
            self.sidebar,
            text="Sem resistência do ar",
            text_color="#666666",
            font=ctk.CTkFont(size=11)
        ).grid(row=8, column=0, padx=17, pady=(0, 17), sticky="w")

        # ========================================================
        # CONTEÚDO
        # ========================================================

        self.conteudo = ctk.CTkFrame(self, corner_radius=0, fg_color=self.bg)
        self.conteudo.grid(row=0, column=1, sticky="nsew")
        self.conteudo.grid_columnconfigure(0, weight=0, minsize=310)
        self.conteudo.grid_columnconfigure(1, weight=1)
        self.conteudo.grid_rowconfigure(1, weight=1)

        # ========================================================
        # CABEÇALHO
        # ========================================================

        cabecalho = ctk.CTkFrame(self.conteudo, fg_color="transparent")
        cabecalho.grid(row=0, column=0, columnspan=2, padx=30, pady=(25, 16), sticky="ew")
        cabecalho.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            cabecalho, text="Simulação interativa",
            font=ctk.CTkFont(size=28, weight="bold")
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(
            cabecalho,
            text="Altere os parâmetros e acompanhe a trajetória em tempo real.",
            text_color=self.text_gray,
            font=ctk.CTkFont(size=13)
        ).grid(row=1, column=0, pady=(3, 0), sticky="w")

        status = ctk.CTkLabel(
            cabecalho, text="Simulação atualizada",
            fg_color="#252525", corner_radius=10,
            padx=15, pady=10, text_color="#D0D0D0"
        )
        status.grid(row=0, column=1, rowspan=2, padx=(20, 0), sticky="e")

        # ========================================================
        # PAINEL ESQUERDO
        # ========================================================

        self.controles = ctk.CTkScrollableFrame(
            self.conteudo, fg_color=self.panel, corner_radius=14
        )
        self.controles.grid(row=1, column=0, padx=(30, 15), pady=(0, 30), sticky="nsew")

        ctk.CTkLabel(
            self.controles, text="Parâmetros do lançamento",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(anchor="w", padx=20, pady=(20, 20))

        # --------------------------------------------------------
        # CONTROLES (sliders sem "command" — só os botões desenham)
        # --------------------------------------------------------

        self.slider_velocidade = self.criar_controle(
            "Velocidade inicial v₀", 30, 5, 150, "m/s"
        )
        self.slider_angulo = self.criar_controle(
            "Ângulo de lançamento ω", 45, 1, 89, "°"
        )
        self.slider_altura = self.criar_controle(
            "Altura inicial y₀", 5, 0, 50, "m"
        )
        self.slider_gravidade = self.criar_controle(
            "Aceleração da gravidade g", 9.81, 1.6, 24.8, "m/s²"
        )

        ctk.CTkLabel(
            self.controles, text="Preset de gravidade",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(anchor="w", padx=20, pady=(10, 7))

        self.planeta = ctk.CTkOptionMenu(
            self.controles,
            values=[
                "Personalizado",
                "Lua — 1,62 m/s²",
                "Marte — 3,71 m/s²",
                "Terra — 9,81 m/s²",
                "Júpiter — 24,79 m/s²"
            ],
            width=220
        )
        self.planeta.set("Personalizado")
        self.planeta.pack(anchor="w", padx=20)

        # --------------------------------------------------------
        # SEPARADOR
        # --------------------------------------------------------

        ctk.CTkFrame(self.controles, height=1, fg_color=self.border).pack(fill="x", padx=20, pady=20)

        # ========================================================
        # RESULTADOS
        # ========================================================

        ctk.CTkLabel(
            self.controles, text="Resultados",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(anchor="w", padx=20, pady=(0, 10))

        self.criar_resultado("Alcance horizontal R", "86,50 m")
        self.criar_resultado("Altura máxima yₘₐₓ", "27,94 m")
        self.criar_resultado("Tempo de voo tᵥₒₒ", "4,08 s")

        # --------------------------------------------------------
        # BOTÃO DE LANÇAMENTO
        # --------------------------------------------------------

        ctk.CTkFrame(self.controles, height=1, fg_color=self.border).pack(fill="x", padx=20, pady=20)

        self.btn_lancar = ctk.CTkButton(
            self.controles,
            text="▶  Lançar projétil",
            height=45, corner_radius=9,
            fg_color="#19A83B", hover_color="#13852F",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.lancar_projetil
        )
        self.btn_lancar.pack(fill="x", padx=20, pady=(0, 20))

        # ========================================================
        # PAINEL DO GRÁFICO
        # ========================================================

        self.grafico_painel = ctk.CTkFrame(self.conteudo, fg_color=self.panel, corner_radius=14)
        self.grafico_painel.grid(row=1, column=1, padx=(0, 30), pady=(0, 30), sticky="nsew")
        self.grafico_painel.grid_columnconfigure(0, weight=1)
        self.grafico_painel.grid_rowconfigure(1, weight=1)

        topo_grafico = ctk.CTkFrame(self.grafico_painel, fg_color="transparent")
        topo_grafico.grid(row=0, column=0, sticky="ew", padx=20, pady=(18, 5))
        topo_grafico.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            topo_grafico, text="Trajetória",
            font=ctk.CTkFont(size=18, weight="bold")
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(
            topo_grafico,
            text="Eixo X: distância (m)   •   Eixo Y: altura (m)",
            text_color=self.text_gray,
            font=ctk.CTkFont(size=11)
        ).grid(row=0, column=1, sticky="e")

        self.area_grafico = tk.Canvas(self.grafico_painel, bg=self.graph_bg, highlightthickness=0)
        self.area_grafico.grid(row=1, column=0, padx=18, pady=(5, 18), sticky="nsew")

        # Gráfico começa vazio
        self.figura, self.ax = plt.subplots()

        self.ax.set_xlabel("Distância horizontal (m)")
        self.ax.set_ylabel("Altura (m)")
        self.ax.set_title("Trajetória do Projétil")
        self.anim = None
        self.canvas = FigureCanvasTkAgg(self.figura, master=self.area_grafico)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    # ============================================================
    # CRIA CONTROLE
    # ============================================================

    def criar_controle(self, titulo, valor_inicial, minimo, maximo, unidade, comando=None):
        ctk.CTkLabel(
            self.controles, text=titulo,
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(anchor="w", padx=20, pady=(4, 7))

        linha = ctk.CTkFrame(self.controles, fg_color="transparent")
        linha.pack(fill="x", padx=20)
        linha.grid_columnconfigure(0, weight=1)

        slider = ctk.CTkSlider(linha, from_=minimo, to=maximo, height=18, command=comando)
        slider.set(valor_inicial)
        slider.grid(row=0, column=0, sticky="ew", padx=(0, 10))

        entrada = ctk.CTkEntry(linha, width=73, height=32, justify="center")
        entrada.insert(0, str(valor_inicial))
        entrada.grid(row=0, column=1)

        ctk.CTkLabel(
            self.controles, text=unidade,
            text_color=self.text_gray, font=ctk.CTkFont(size=10)
        ).pack(anchor="e", padx=24, pady=(1, 9))

        return slider

    # ============================================================
    # LANÇAR / COMPARAR PROJÉTIL
    # ============================================================

    def lancar_projetil(self):
        velocidade = self.slider_velocidade.get()
        angulo = self.slider_angulo.get()
        altura = self.slider_altura.get()
        gravidade = self.slider_gravidade.get()

        xs, ys, tempos = calcular_trajetoria(
            v0=velocidade,
            angulo=angulo,
            y0=altura,
            g=gravidade
        )

        self.trajetorias_comparadas.append((xs, ys, angulo))
        self.animar_trajetoria(xs, ys, angulo)

    # ============================================================
    # ANIMAÇÃO DO PROJÉTIL
    # ============================================================

    def animar_trajetoria(self, xs, ys, angulo):
        # Para animação anterior
        if self.anim is not None and self.anim.event_source is not None:
            self.anim.event_source.stop()

        self.ax.clear() ## Apaga o que está desenhado no gráfico

        # Redesenha as trajetórias anteriores
        for x_ant, y_ant, ang_ant in self.trajetorias_comparadas[:-1]:
            self.ax.plot(x_ant, y_ant, label=f"{ang_ant:.0f}°", alpha=0.6)

        todos_xs = [x for xs_i, ys_i, a in self.trajetorias_comparadas for x in xs_i]
        todos_ys = [y for xs_i, ys_i, a in self.trajetorias_comparadas for y in ys_i]
        self.ax.set_xlim(0, max(todos_xs) * 1.05)
        self.ax.set_ylim(0, max(todos_ys) * 1.15)

        self.ax.set_xlabel("Distância horizontal (m)")
        self.ax.set_ylabel("Altura (m)")
        self.ax.set_title("Trajetória do Projétil")

        # Objetos que serão animados
        linha, = self.ax.plot([], [], label=f"{angulo:.0f}°")
        ponto, = self.ax.plot([], [], 'o', color=linha.get_color())
        self.ax.legend()

        # Criando a animação
        def atualizar(frame):
            linha.set_data(xs[:frame], ys[:frame])
            ponto.set_data([xs[frame]], [ys[frame]])
            return linha, ponto

        self.anim = FuncAnimation(
            self.figura,
            atualizar,
            frames=len(xs),
            interval=20,
            blit=False,
            repeat=False
        )
        self.canvas.draw()

    def limpar_comparacoes(self):
        if self.anim is not None and self.anim.event_source is not None:
            self.anim.event_source.stop()
        self.anim = None

        self.trajetorias_comparadas = []

        self.ax.clear()
        self.ax.set_xlabel("Distância horizontal (m)")
        self.ax.set_ylabel("Altura (m)")
        self.ax.set_title("Trajetória do Projétil")
        self.canvas.draw()

    # ============================================================
    # RESULTADO
    # ============================================================

    def criar_resultado(self, titulo, valor):
        card = ctk.CTkFrame(self.controles, fg_color=self.panel_2, corner_radius=9)
        card.pack(fill="x", padx=20, pady=4)

        ctk.CTkLabel(
            card, text=titulo,
            text_color=self.text_gray, font=ctk.CTkFont(size=11)
        ).pack(anchor="w", padx=12, pady=(8, 0))

        ctk.CTkLabel(
            card, text=valor,
            font=ctk.CTkFont(size=19, weight="bold")
        ).pack(anchor="w", padx=12, pady=(0, 8))

# ================================================================
# EXECUÇÃO
# ================================================================

if __name__ == "__main__":
    app = Aplicativo()
    app.mainloop()