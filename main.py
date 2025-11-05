from nicegui import ui

@ui.page('/')
def index_page():
    ui.label('¡Hola desde NiceGUI!')

ui.run(host='0.0.0.0', port=8080)
