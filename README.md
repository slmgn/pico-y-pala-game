# pico-y-pala-game
Juego que consiste en adivinar un numero de 4 dígitos en la menor cantidad de intentos posibles

Se usa reflex para crear el frontend y el backend en python
debemos instalar un entorno virtual, vamos a usar UV
como mi maquina es una apple silicon debo instalar rosseta 2
#/usr/sbin/softwareupdate --install-rosetta --agree-to-license
Luego intalamos uv
curl -LsSf https://astral.sh/uv/install.sh | sh
para iniciar uv usamos dentro de la carpeta del proyecto
uv init
Agregamos reflex al archivo pyproject.toml
uv add reflex
Inizializamos el reflex del proyecto
uv run reflex init
Para correr el proyecto usamos
uv run reflex run  
