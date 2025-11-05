import os
from nicegui import ui
from sqlalchemy import create_engine, text

DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL, pool_pre_ping=True) if DATABASE_URL else None

@ui.page('/')
def index_page():
    ui.label('¡Hola desde NiceGUI!')
    if engine:
        with engine.connect() as conn:
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS hello (
                    id SERIAL PRIMARY KEY,
                    msg TEXT NOT NULL
                )
            """))
            conn.execute(text("INSERT INTO hello (msg) VALUES ('desde Neon')"))
            conn.commit()
            msg = conn.execute(text("SELECT msg FROM hello ORDER BY id DESC LIMIT 1")).scalar()
        ui.label(f'DB dice: {msg}')

ui.run(host='0.0.0.0', port=8080)
