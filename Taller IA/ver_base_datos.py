import sqlite3

def ver_piezas():
    conn = sqlite3.connect('piezas.db')
    c = conn.cursor()

    # Ver todas las piezas
    c.execute("SELECT * FROM piezas")
    piezas = c.fetchall()
    
    print("=== TODAS LAS PIEZAS ===")
    for pieza in piezas:
        print(pieza)
    
    conn.close()

if __name__ == "__main__":
    ver_piezas()