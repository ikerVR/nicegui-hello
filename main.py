import os
from datetime import datetime
from nicegui import ui, app
from sqlalchemy import create_engine, text

# --- DB ---
DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL, pool_pre_ping=True) if DATABASE_URL else None

def db_exec(sql, **params):
    if not engine:
        return None
    with engine.begin() as conn:
        return conn.execute(text(sql), params)

# --- Healthz (útil para Coolify/monitor) ---
@app.get('/healthz')
def healthz():
    try:
        if engine:
            db_exec('SELECT 1')
        return {'ok': True, 'ts': datetime.utcnow().isoformat()}
    except Exception as e:
        return {'ok': False, 'error': str(e)}

# --- Layout base ---
def layout(title: str):
    with ui.header().classes('items-center justify-between'):
        ui.label('My NiceGUI App').classes('text-lg font-bold')
        with ui.row().classes('gap-4'):
            ui.link('Inicio', '/')
            ui.link('Admin', '/admin')
    ui.separator()
    ui.label(title).classes('text-xl font-semibold mt-2')
    ui.separator()

# --- Página principal ---
@ui.page('/')
def index_page():
    layout('Inicio')
    ui.label('¡Hola desde NiceGUI!')
    if engine:
        db_exec('CREATE TABLE IF NOT EXISTS hello (id SERIAL PRIMARY KEY, msg TEXT NOT NULL)')
        db_exec("INSERT INTO hello (msg) VALUES ('desde Neon')")
        msg = db_exec("SELECT msg FROM hello ORDER BY id DESC LIMIT 1").scalar()
        ui.label(f'DB dice: {msg}')

# --- Página admin ---
@ui.page('/admin')
def admin_page():
    layout('Admin')
    ui.label('Solo para admins (ejemplo).')

ui.run(host='0.0.0.0', port=int(os.getenv('PORT', '8080')))
