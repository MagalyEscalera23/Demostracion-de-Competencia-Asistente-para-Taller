import sqlite3

def crear_base_datos():
    conn = sqlite3.connect('piezas.db')
    c = conn.cursor()
    
    # Tabla de piezas
    c.execute('''CREATE TABLE IF NOT EXISTS piezas
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  nombre TEXT NOT NULL,
                  descripcion TEXT,
                  categoria TEXT,
                  vehiculos_compatibles TEXT,
                  ubicacion_taller TEXT,
                  imagen_url TEXT)''')
    
    # Insertar datos de ejemplo
    piezas_ejemplo = [
        ('Bujía', 'Pieza para encendido del motor, produce chispa eléctrica', 'Motor', 'Toyota Corolla 2010-2015, Honda Civic 2012-2016', 'Estante A - Nivel 2', 'bujia.jpg'),
        ('Filtro de Aceite', 'Filtra impurezas del aceite del motor, forma cilíndrica metálica', 'Filtros', 'Todos los modelos 2000-2020', 'Estante B - Nivel 1', 'filtro_aceite.jpg'),
        ('Disco de Freno', 'Disco metálico para sistema de frenado delantero, circular', 'Frenos', 'Nissan Sentra 2015-2018, Ford Focus 2014-2017', 'Estante C - Nivel 3', 'disco_freno.jpg'),
        ('Correa de Distribución', 'Correa de goma con dientes, sincroniza motor', 'Motor', 'Chevrolet Aveo 2008-2012, Kia Rio 2010-2015', 'Estante A - Nivel 1', 'correa.jpg'),
        ('Amortiguador', 'Pieza larga con resorte, para suspensión', 'Suspensión', 'VW Jetta 2005-2010, Hyundai Elantra 2013-2018', 'Estante D - Nivel 2', 'amortiguador.jpg')
    ]
    
    c.executemany('''INSERT OR IGNORE INTO piezas 
                     (nombre, descripcion, categoria, vehiculos_compatibles, ubicacion_taller, imagen_url) 
                     VALUES (?,?,?,?,?,?)''', piezas_ejemplo)
    
    conn.commit()
    conn.close()
    print("✅ Base de datos creada exitosamente!")

if __name__ == '__main__':
    crear_base_datos()