import reflex as rx
import random

# Definimos la clase para el historial fuera del State
class Intento(rx.Base):
    numero: str
    pico_pala: str

class State(rx.State):
    ganador: bool = False
    game_started: bool = False
    intentos: int = 0
    numero_secreto: list[int] = []
    historial: list[Intento] = []

    @rx.event
    def start_game(self):
        self.game_started = True
        # Generamos el número secreto (4 dígitos únicos)
        self.numero_secreto = random.sample(range(0, 10), 4)

    @rx.event
    def reset_game(self):
        self.game_started = False
        self.ganador = False
        self.intentos = 0
        self.historial = []
        self.numero_secreto = []

    @rx.event
    def verificar_numero(self, form_data: dict):
        valor_string = form_data.get("numero_input", "")
        
        # Validación básica
        if len(valor_string) != 4:
            return rx.window_alert("Deben ser 4 números")

        # Conversión a lista de enteros
        numero_usuario = [int(d) for d in valor_string]
        
        # Lógica de Pico y Pala optimizada
        pala = sum(1 for u, s in zip(numero_usuario, self.numero_secreto) if u == s)
        comunes = len(set(numero_usuario) & set(self.numero_secreto))
        pico = comunes - pala

        self.intentos += 1
        resultado_texto = f"{pico} Pico / {pala} Pala"

        # AGREGAR AL HISTORIAL: Guardamos el número y su resultado específico
        self.historial.insert(0, Intento(numero=valor_string, pico_pala=resultado_texto))

        if pala == 4:
            self.ganador = True

def render_fila(item: Intento):
    """Función separada para renderizar cada fila (Evita el error de la tabla)"""
    return rx.table.row(
        rx.table.cell(item.numero),
        rx.table.cell(item.pico_pala),
    )

def tabla_historial():
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                rx.table.column_header_cell("Número"),
                rx.table.column_header_cell("Resultado"),
            )
        ),
        rx.table.body(
            # Usamos la referencia a la función render_fila
            rx.foreach(State.historial, render_fila),
        ),
        variant="surface",
        width="100%",
    )

def form_numero():
    return rx.form(
        rx.hstack(
            rx.input(name="numero_input", placeholder="Ej. 4586", max_length=4, required=True),
            rx.button("Verificar", color_scheme="green", type="submit"),
        ),
        on_submit=State.verificar_numero,
        reset_on_submit=True,
    )

def index() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.heading("Juego de Pico y Pala", size="9", margin_bottom="1em"),
            rx.cond(
                ~State.game_started,
                rx.button("Start Game", on_click=State.start_game, color_scheme="blue", size="4"),
                rx.vstack(
                    rx.cond(
                        State.ganador,
                        rx.vstack(
                            rx.heading("¡FELICITACIONES!", size="8", color="green"),
                            rx.text(f"Lo lograste en {State.intentos} intentos."),
                            spacing="2",
                        ),
                        rx.vstack(
                            form_numero(),
                            rx.text(f"Intentos: {State.intentos}", font_weight="bold"),
                        )
                    ),
                    rx.divider(),
                    tabla_historial(),
                    rx.button(
                        rx.cond(State.ganador, "Jugar de nuevo", "Reset Game"),
                        on_click=State.reset_game,
                        color_scheme="red",
                        variant="soft",
                    ),
                    spacing="4",
                    width="100%",
                )
            ),
            padding="5em",
            max_width="400px",
        )
    )

app = rx.App()
app.add_page(index,title="Juego de Pico y Pala")