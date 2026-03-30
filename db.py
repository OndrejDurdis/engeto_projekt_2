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

def hlavni_menu():
    while True:
        print("\n--- SPRÁVCE ÚKOLŮ 2.0 ---")
        print("1. Přidat nový úkol.")
        print("2. Zobrazit všechny úkoly.")
        print("3. Aktualizovat úkol.")
        print("4. Odstranit úkol.")
        print("5. Konec programu.")
        
        volba = input("Vyberte možnost (1-5): ").strip()

        if volba == "1":
            pridat_ukol()
        elif volba == "2":
            zobrazit_ukoly()
        elif volba == "3":
            aktualizovat_ukol()
        elif volba == "4":
            odstranit_ukol()
        elif volba == "5":
            print("Konec programu.")
            break
        else:
            print("Neplatná volba.")

def pridat_ukol_db(nazev, popis, conn):
    if not nazev or not popis:
        return False

    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO ukoly (nazev, popis) VALUES (%s, %s)",
        (nazev, popis)
    )
    conn.commit()
    return True

def pridat_ukol():
    nazev = input("Zadejte název úkolu: ").strip()
    popis = input("Zadejte popis úkolu: ").strip()

    if not nazev or not popis:
        print("Název ani popis úkolu nesmí být prázdné.")
        return
    
    conn = pripojeni_db()
    if conn is None:
        return
    
    if pridat_ukol_db(nazev, popis, conn):
        print("Úkol byl přidán.")

    conn.close()

def zobrazit_ukoly():
    conn = pripojeni_db()
    if conn is None:
        return
    
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, nazev, popis, stav
        FROM ukoly
        WHERE stav IN ('Nezahájeno', 'Probíhá')
    """)

    ukoly = cursor.fetchall()

    if not ukoly:
        print("Žádné úkoly k zobrazení.")
    else:
        print("\nSeznam úkolů:")
        for ukol in ukoly:
            print(f"""{ukol[0]} 
{ukol[1]}
{ukol[2]}
{ukol[3]}
""")

    conn.close()

def aktualizovat_ukol_db(id_ukolu, novy_stav, conn):
    if novy_stav not in ["Nezahájeno", "Probíhá", "Hotovo"]:
        return False

    cursor = conn.cursor()
    cursor.execute(
        "UPDATE ukoly SET stav = %s WHERE id = %s",
        (novy_stav, id_ukolu)
    )

    if cursor.rowcount == 0:
        return False

    conn.commit()
    return True

def aktualizovat_ukol():
    zobrazit_ukoly()

    try:
        id_ukolu = int(input("Zadejte ID ukolu: "))
    except ValueError:
        print("Neplatné ID.")
        return
    
    print("Vyberte nový stav: ")
    print("1. Nezahájeno")
    print("2. Probíhá")
    print("3. Hotovo")

    volba = input("Volba: ").strip()

    if volba == "1":
        novy_stav = "Nezahájeno"
    elif volba == "2":
        novy_stav = "Probíhá"
    elif volba == "3":
        novy_stav = "Hotovo"
    else:
        print("Neplatná volba.")
        return
    
    conn = pripojeni_db()
    if conn is None:
        return

    if aktualizovat_ukol_db(id_ukolu, novy_stav, conn):
        print("Úkol byl aktualizován.")
    else:
        print("Úkol s tímto ID neexistuje nebo neplatný stav.")

    conn.close()

def odstranit_ukol_db(id_ukolu, conn):
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM ukoly WHERE id = %s",
        (id_ukolu,)
    )

    if cursor.rowcount == 0:
        return False

    conn.commit()
    return True

def odstranit_ukol():
    zobrazit_ukoly()

    try:
        id_ukolu = int(input("Zadejte ID ukolu k odstranění: "))
    except ValueError:
        print("Neplatné ID.")
        return
    
    conn = pripojeni_db()
    if conn is None:
        return

    # 🔥 místo SQL logiky voláš DB funkci
    if odstranit_ukol_db(id_ukolu, conn):
        print("Úkol byl odstraněn.")
    else:
        print("Úkol s tímto ID neexistuje.")

    conn.close()

if __name__ == "__main__":
    vytvoreni_tabulky()
    hlavni_menu()