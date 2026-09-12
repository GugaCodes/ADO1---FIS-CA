import customtkinter as ctk
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from fisica import calcular_trajetoria, calcular_resultados


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

        # Guarda o ID da animação
        self.animacao_id = None
        self.comparacoes = []

        # ========================================================
        # GRID PRINCIPAL
        # ========================================================

        self.grid_columnconfigure(0, weight=0, minsize=240)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ========================================================
        # SIDEBAR
        # ========================================================

        self.sidebar = ctk.CTkFrame(
            self,
            corner_radius=0,
            fg_color=self.sidebar_bg
        )
        self.sidebar.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        self.sidebar.grid_rowconfigure(6, weight=1)

        ctk.CTkLabel(
            self.sidebar,
            text="Lançamento\nde Projéteis",
            font=ctk.CTkFont(size=25, weight="bold"),
            justify="left"
        ).grid(
            row=0,
            column=0,
            padx=25,
            pady=(30, 6),
            sticky="w"
        )

        ctk.CTkLabel(
            self.sidebar,
            text="Simulação 2D • Física ideal",
            text_color=self.text_gray,
            font=ctk.CTkFont(size=13)
        ).grid(
            row=1,
            column=0,
            padx=25,
            pady=(0, 28),
            sticky="w"
        )



        self.btn_restaurar = ctk.CTkButton(
            self.sidebar,
            text="↻  Restaurar valores",
            anchor="w",
            height=40,
            corner_radius=8,
            fg_color="transparent",
            border_width=1,
            border_color=self.border,
            hover_color="#292929",
            command=self.restaurar_valores
        )
        self.btn_restaurar.grid(
            row=3,
            column=0,
            padx=15,
            pady=5,
            sticky="ew"
        )

        self.btn_comparar = ctk.CTkButton(
            self.sidebar,
            text="＋  Comparar trajetória",
            anchor="w",
            height=40,
            corner_radius=8,
            fg_color="transparent",
            border_width=1,
            border_color=self.border,
            hover_color="#292929",
            command=self.comparar_trajetoria
        )
        self.btn_comparar.grid(
            row=4,
            column=0,
            padx=15,
            pady=5,
            sticky="ew"
        )

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
        self.btn_limpar.grid(
            row=5,
            column=0,
            padx=15,
            pady=5,
            sticky="ew"
        )

        ctk.CTkLabel(
            self.sidebar,
            text="Física • Práticas Extensivas",
            text_color=self.text_gray,
            font=ctk.CTkFont(size=11)
        ).grid(
            row=7,
            column=0,
            padx=17,
            pady=(0, 4),
            sticky="w"
        )

        ctk.CTkLabel(
            self.sidebar,
            text="Sem resistência do ar",
            text_color="#666666",
            font=ctk.CTkFont(size=11)
        ).grid(
            row=8,
            column=0,
            padx=17,
            pady=(0, 17),
            sticky="w"
        )

        # ========================================================
        # CONTEÚDO
        # ========================================================

        self.conteudo = ctk.CTkFrame(
            self,
            corner_radius=0,
            fg_color=self.bg
        )
        self.conteudo.grid(
            row=0,
            column=1,
            sticky="nsew"
        )

        self.conteudo.grid_columnconfigure(
            0,
            weight=0,
            minsize=310
        )

        self.conteudo.grid_columnconfigure(
            1,
            weight=1
        )

        self.conteudo.grid_rowconfigure(
            1,
            weight=1
        )

        # ========================================================
        # CABEÇALHO
        # ========================================================

        cabecalho = ctk.CTkFrame(
            self.conteudo,
            fg_color="transparent"
        )
        cabecalho.grid(
            row=0,
            column=0,
            columnspan=2,
            padx=30,
            pady=(25, 16),
            sticky="ew"
        )

        cabecalho.grid_columnconfigure(
            0,
            weight=1
        )

        ctk.CTkLabel(
            cabecalho,
            text="Simulação interativa",
            font=ctk.CTkFont(size=28, weight="bold")
        ).grid(
            row=0,
            column=0,
            sticky="w"
        )

        ctk.CTkLabel(
            cabecalho,
            text="Altere os parâmetros e acompanhe a trajetória em tempo real.",
            text_color=self.text_gray,
            font=ctk.CTkFont(size=13)
        ).grid(
            row=1,
            column=0,
            pady=(3, 0),
            sticky="w"
        )

        status = ctk.CTkLabel(
            cabecalho,
            text="Simulação atualizada",
            fg_color="#252525",
            corner_radius=10,
            padx=15,
            pady=10,
            text_color="#D0D0D0"
        )
        status.grid(
            row=0,
            column=1,
            rowspan=2,
            padx=(20, 0),
            sticky="e"
        )

        # ========================================================
        # PAINEL ESQUERDO
        # ========================================================

        self.controles = ctk.CTkScrollableFrame(
            self.conteudo,
            fg_color=self.panel,
            corner_radius=14
        )
        self.controles.grid(
            row=1,
            column=0,
            padx=(30, 15),
            pady=(0, 30),
            sticky="nsew"
        )

        ctk.CTkLabel(
            self.controles,
            text="Parâmetros do lançamento",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 20)
        )

        # ========================================================
        # CONTROLES
        # ========================================================

        self.slider_velocidade, self.entrada_velocidade = self.criar_controle(
            "Velocidade inicial v₀",
            30,
            5,
            150,
            "m/s",
            comando=self.atualizar_grafico
        )

        self.slider_angulo, self.entrada_angulo = self.criar_controle(
            "Ângulo de lançamento ω",
            45,
            1,
            89,
            "°",
            comando=self.atualizar_grafico
        )

        self.slider_altura, self.entrada_altura = self.criar_controle(
            "Altura inicial y₀",
            5,
            0,
            50,
            "m",
            comando=self.atualizar_grafico
        )

        self.slider_gravidade, self.entrada_gravidade = self.criar_controle(
            "Aceleração da gravidade g",
            9.81,
            1.6,
            24.8,
            "m/s²",
            comando=self.atualizar_grafico
        )

        # ========================================================
        # PRESET DE GRAVIDADE
        # ========================================================

        ctk.CTkLabel(
            self.controles,
            text="Preset de gravidade",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(
            anchor="w",
            padx=20,
            pady=(10, 7)
        )

        self.planeta = ctk.CTkOptionMenu(
            self.controles,
            values=[
                "Personalizado",
                "Lua — 1,62 m/s²",
                "Marte — 3,71 m/s²",
                "Terra — 9,81 m/s²",
                "Júpiter — 24,79 m/s²"
            ],
            width=220,
            command=self.selecionar_planeta
        )

        self.planeta.set("Personalizado")

        self.planeta.pack(
            anchor="w",
            padx=20
        )

        # ========================================================
        # SEPARADOR
        # ========================================================

        ctk.CTkFrame(
            self.controles,
            height=1,
            fg_color=self.border
        ).pack(
            fill="x",
            padx=20,
            pady=20
        )

        # ========================================================
        # RESULTADOS
        # ========================================================

        ctk.CTkLabel(
            self.controles,
            text="Resultados",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 10)
        )

        self.resultado_alcance = self.criar_resultado(
            "Alcance horizontal R",
            "86,50 m"
        )

        self.resultado_altura = self.criar_resultado(
            "Altura máxima yₘₐₓ",
            "27,94 m"
        )

        self.resultado_tempo = self.criar_resultado(
            "Tempo de voo tᵥₒₒ",
            "4,08 s"
        )

        # ========================================================
        # BOTÕES
        # ========================================================

        ctk.CTkFrame(
            self.controles,
            height=1,
            fg_color=self.border
        ).pack(
            fill="x",
            padx=20,
            pady=20
        )

        self.btn_lancar = ctk.CTkButton(
            self.controles,
            text="▶  Lançar projétil",
            height=45,
            corner_radius=9,
            fg_color="#19A83B",
            hover_color="#13852F",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.lancar
        )

        self.btn_lancar.pack(
            fill="x",
            padx=20,
            pady=(0, 20)
        )

        self.btn_parar = ctk.CTkButton(
            self.controles,
            text="■  Parar animação",
            height=40,
            corner_radius=9,
            fg_color="transparent",
            border_width=1,
            border_color=self.border,
            hover_color="#303030",
            command=self.parar_animacao
        )

        self.btn_parar.pack(
            fill="x",
            padx=20,
            pady=(0, 20)
        )

        # ========================================================
        # PAINEL DO GRÁFICO
        # ========================================================

        self.grafico_painel = ctk.CTkFrame(
            self.conteudo,
            fg_color=self.panel,
            corner_radius=14
        )

        self.grafico_painel.grid(
            row=1,
            column=1,
            padx=(0, 30),
            pady=(0, 30),
            sticky="nsew"
        )

        self.grafico_painel.grid_columnconfigure(
            0,
            weight=1
        )

        self.grafico_painel.grid_rowconfigure(
            1,
            weight=1
        )

        # ========================================================
        # TÍTULO DO GRÁFICO
        # ========================================================

        topo_grafico = ctk.CTkFrame(
            self.grafico_painel,
            fg_color="transparent"
        )

        topo_grafico.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=20,
            pady=(18, 5)
        )

        topo_grafico.grid_columnconfigure(
            0,
            weight=1
        )

        ctk.CTkLabel(
            topo_grafico,
            text="Trajetória",
            font=ctk.CTkFont(size=18, weight="bold")
        ).grid(
            row=0,
            column=0,
            sticky="w"
        )

        ctk.CTkLabel(
            topo_grafico,
            text="Eixo X: distância (m)   •   Eixo Y: altura (m)",
            text_color=self.text_gray,
            font=ctk.CTkFont(size=11)
        ).grid(
            row=0,
            column=1,
            sticky="e"
        )

        # ========================================================
        # ÁREA DO GRÁFICO
        # ========================================================

        self.area_grafico = tk.Canvas(
            self.grafico_painel,
            bg=self.graph_bg,
            highlightthickness=0
        )

        self.area_grafico.grid(
            row=1,
            column=0,
            padx=18,
            pady=(5, 18),
            sticky="nsew"
        )

        # ========================================================
        # MATPLOTLIB
        # ========================================================

        self.figura, self.ax = plt.subplots()

        xs, ys, tempos = calcular_trajetoria(
            v0=30,
            angulo=45,
            y0=5,
            g=9.81
        )

        # Linha da animação
        self.trajetoria_animada, = self.ax.plot(
            [],
            [],
            linewidth=2
        )

        # Linha de esboço
        self.trajetoria_esboco, = self.ax.plot(
            xs,
            ys,
            linestyle="--",
            linewidth=1.5,
            alpha=0.5
        )

        # Ponto do projétil
        self.ponto_projetil, = self.ax.plot(
            [],
            [],
            "o",
            markersize=8
        )

        self.ax.set_xlabel(
            "Distância horizontal (m)"
        )

        self.ax.set_ylabel(
            "Altura (m)"
        )

        self.ax.set_title(
            "Trajetória do projétil"
        )

        self.ax.set_xlim(
            0,
            max(xs) * 1.05
        )

        self.ax.set_ylim(
            0,
            max(ys) * 1.10
        )

        # ========================================================
        # CANVAS MATPLOTLIB
        # ========================================================

        self.canvas = FigureCanvasTkAgg(
            self.figura,
            master=self.area_grafico
        )

        self.canvas.draw()

        self.canvas.get_tk_widget().pack(
            fill="both",
            expand=True
        )

    # ============================================================
    # CRIA CONTROLE
    # ============================================================

    def criar_controle(
        self,
        titulo,
        valor_inicial,
        minimo,
        maximo,
        unidade,
        comando=None
    ):
        ctk.CTkLabel(
            self.controles,
            text=titulo,
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(
            anchor="w",
            padx=20,
            pady=(4, 7)
        )

        linha = ctk.CTkFrame(
            self.controles,
            fg_color="transparent"
        )

        linha.pack(
            fill="x",
            padx=20
        )

        linha.grid_columnconfigure(
            0,
            weight=1
        )

        # Campo de entrada
        entrada = ctk.CTkEntry(
            linha,
            width=73,
            height=32,
            justify="center"
        )

        entrada.insert(
            0,
            str(valor_inicial)
        )

        entrada.grid(
            row=0,
            column=1
        )

        # Slider
        slider = ctk.CTkSlider(
            linha,
            from_=minimo,
            to=maximo,
            height=18
        )

        slider.set(
            valor_inicial
        )

        slider.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(0, 10)
        )

        # Slider atualiza o campo e a física
        slider.configure(
            command=lambda valor: self.atualizar_valor(
                valor,
                entrada,
                comando
            )
        )

        # Enter no campo atualiza o slider e a física
        entrada.bind(
            "<Return>",
            lambda event: self.atualizar_pelo_campo(
                entrada,
                slider,
                minimo,
                maximo
            )
        )

        # Unidade
        ctk.CTkLabel(
            self.controles,
            text=unidade,
            text_color=self.text_gray,
            font=ctk.CTkFont(size=10)
        ).pack(
            anchor="e",
            padx=24,
            pady=(1, 9)
        )

        return slider, entrada

    # ============================================================
    # ATUALIZA VALOR PELO SLIDER
    # ============================================================

    def atualizar_valor(
        self,
        valor,
        entrada,
        comando
    ):
        entrada.delete(
            0,
            "end"
        )

        entrada.insert(
            0,
            f"{float(valor):.2f}"
        )

        if comando is not None:
            comando(valor)

    # ============================================================
    # ATUALIZA VALOR PELO CAMPO
    # ============================================================

    def atualizar_pelo_campo(
        self,
        entrada,
        slider,
        minimo,
        maximo
    ):
        try:
            valor = float(
                entrada.get().replace(",", ".")
            )

        except ValueError:
            entrada.delete(0, "end")
            entrada.insert(
                0,
                f"{slider.get():.2f}"
            )
            return

        if valor < minimo or valor > maximo:
            entrada.delete(0, "end")
            entrada.insert(
                0,
                f"{slider.get():.2f}"
            )
            return

        slider.set(valor)

        self.atualizar_grafico()

    # ============================================================
    # ATUALIZA SLIDER + CAMPO + GRÁFICO
    # ============================================================

    def atualizar_controle(
        self,
        slider,
        entrada,
        valor
    ):
        slider.set(valor)

        entrada.delete(
            0,
            "end"
        )

        entrada.insert(
            0,
            f"{valor:.2f}"
        )

        self.atualizar_grafico()

    # ============================================================
    # ATUALIZA GRÁFICO E RESULTADOS
    # ============================================================

    def atualizar_grafico(self, valor=None):

        velocidade = self.slider_velocidade.get()
        angulo = self.slider_angulo.get()
        altura = self.slider_altura.get()
        gravidade = self.slider_gravidade.get()

        # Calcula resultados
        alcance, altura_maxima, tempo_voo = calcular_resultados(
            v0=velocidade,
            angulo=angulo,
            y0=altura,
            g=gravidade
        )

        # Atualiza resultados na interface
        self.resultado_alcance.configure(
            text=f"{alcance:.2f} m"
        )

        self.resultado_altura.configure(
            text=f"{altura_maxima:.2f} m"
        )

        self.resultado_tempo.configure(
            text=f"{tempo_voo:.2f} s"
        )

        # Calcula nova trajetória
        xs, ys, tempos = calcular_trajetoria(
            v0=velocidade,
            angulo=angulo,
            y0=altura,
            g=gravidade
        )

        # Atualiza esboço
        self.trajetoria_esboco.set_data(
            xs,
            ys
        )

        # Limpa animação anterior
        self.trajetoria_animada.set_data(
            [],
            []
        )

        self.ponto_projetil.set_data(
            [],
            []
        )

        # Atualiza limites
        self.ax.set_xlim(
            0,
            max(xs) * 1.05
        )

        self.ax.set_ylim(
            0,
            max(ys) * 1.10
        )

        self.canvas.draw()

    # ============================================================
    # LANÇAR PROJÉTIL
    # ============================================================

    def lancar(self):

        self.parar_animacao()

        xs, ys, tempos = calcular_trajetoria(
            v0=self.slider_velocidade.get(),
            angulo=self.slider_angulo.get(),
            y0=self.slider_altura.get(),
            g=self.slider_gravidade.get()
        )

        # Esconde o esboço
        self.trajetoria_esboco.set_data(
            [],
            []
        )

        # Reinicia animação
        self.trajetoria_animada.set_data(
            [],
            []
        )

        self.ponto_projetil.set_data(
            [],
            []
        )

        self.canvas.draw()

        self.animar_projetil(
            xs,
            ys,
            0
        )

    # ============================================================
    # ANIMAÇÃO
    # ============================================================

    def animar_projetil(
        self,
        xs,
        ys,
        indice
    ):

        if indice >= len(xs):
            self.animacao_id = None
            return

        # Desenha a trajetória até o ponto atual
        self.trajetoria_animada.set_data(
            xs[:indice + 1],
            ys[:indice + 1]
        )

        # Posiciona o projétil
        self.ponto_projetil.set_data(
            [xs[indice]],
            [ys[indice]]
        )

        self.canvas.draw()

        indice += 1

        self.animacao_id = self.after(
            50,
            self.animar_projetil,
            xs,
            ys,
            indice
        )

    # ============================================================
    # PARAR ANIMAÇÃO
    # ============================================================

    def parar_animacao(self):

        if self.animacao_id is not None:
            self.after_cancel(
                self.animacao_id
            )

            self.animacao_id = None

    # ============================================================
    # RESTAURAR VALORES
    # ============================================================

    def restaurar_valores(self):

        self.atualizar_controle(
            self.slider_velocidade,
            self.entrada_velocidade,
            30
        )

        self.atualizar_controle(
            self.slider_angulo,
            self.entrada_angulo,
            45
        )

        self.atualizar_controle(
            self.slider_altura,
            self.entrada_altura,
            5
        )

        self.atualizar_controle(
            self.slider_gravidade,
            self.entrada_gravidade,
            9.81
        )

        self.planeta.set(
            "Personalizado"
        )

    # =============================================================
    # COMPARANDO A TRAJETORIA
    # ============================================================

    def comparar_trajetoria(self):

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
        linha, = self.ax.plot(
            xs,
            ys,
            linestyle="--",
            linewidth=1.5
        )

        self.comparacoes.append(linha)

        self.canvas.draw()

    # ==========================================================
    # LIMPANDO AS COMPARAÇÕES
    # ==========================================================

    def limpar_comparacoes(self):

        for linha in self.comparacoes:
            linha.remove()

        self.comparacoes.clear()

        self.canvas.draw()

    # ============================================================
    # PRESETS DE GRAVIDADE
    # ============================================================

    def selecionar_planeta(self, escolha):

        if escolha == "Lua — 1,62 m/s²":

            self.atualizar_controle(
                self.slider_gravidade,
                self.entrada_gravidade,
                1.62
            )

        elif escolha == "Marte — 3,71 m/s²":

            self.atualizar_controle(
                self.slider_gravidade,
                self.entrada_gravidade,
                3.71
            )

        elif escolha == "Terra — 9,81 m/s²":

            self.atualizar_controle(
                self.slider_gravidade,
                self.entrada_gravidade,
                9.81
            )

        elif escolha == "Júpiter — 24,79 m/s²":

            self.atualizar_controle(
                self.slider_gravidade,
                self.entrada_gravidade,
                24.79
            )

    # ============================================================
    # RESULTADO
    # ============================================================

    def criar_resultado(
        self,
        titulo,
        valor
    ):
        card = ctk.CTkFrame(
            self.controles,
            fg_color=self.panel_2,
            corner_radius=9
        )

        card.pack(
            fill="x",
            padx=20,
            pady=4
        )

        ctk.CTkLabel(
            card,
            text=titulo,
            text_color=self.text_gray,
            font=ctk.CTkFont(size=11)
        ).pack(
            anchor="w",
            padx=12,
            pady=(8, 0)
        )

        resultado = ctk.CTkLabel(
            card,
            text=valor,
            font=ctk.CTkFont(
                size=19,
                weight="bold"
            )
        )

        resultado.pack(
            anchor="w",
            padx=12,
            pady=(0, 8)
        )

        return resultado


# ================================================================
# EXECUÇÃO
# ================================================================

if __name__ == "__main__":
    app = Aplicativo()
    app.mainloop()