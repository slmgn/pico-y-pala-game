import reflex as rx

config = rx.Config(
    app_name="pico_y_pala_game",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ]
)