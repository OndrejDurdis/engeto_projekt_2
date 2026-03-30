import mysql.connector

def pripojeni_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Kohoutek-1",
            database="task_manager"
        )
        print("Připojení k databázi bylo úspěšné.")
        return conn
    except mysql.connector.Error as err:
        print(f"Chyba při připojování k DB: {err}")
        return None
    
def vytvoreni_tabulky():
    conn = pripojeni_db()

    if conn is None:
        print("Nepodařilo se připojit k DB")
        return

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ukoly (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nazev VARCHAR(255) NOT NULL,
            popis TEXT NOT NULL,
            stav ENUM('Nezahájeno', 'Probíhá', 'Hotovo') DEFAULT 'Nezahájeno',
            datum_vytvoreni TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

    print("Tabulka připravena.")

def pridat_ukol():
    nazev = input("Zadej název úkolu: ").strip()
    popis = input("Zadej popis úkolu: ").strip()

    # validace
    if not nazev or not popis:
        print("Název i popis jsou povinné!")
        return

    conn = pripojeni_db()
    if conn is None:
        return

    cursor = conn.cursor()

    sql = "INSERT INTO ukoly (nazev, popis) VALUES (%s, %s)"
    cursor.execute(sql, (nazev, popis))

    conn.commit()
    conn.close()

    print("Úkol byl přidán.")

    if __name__ == "__main__":
        pridat_ukol()