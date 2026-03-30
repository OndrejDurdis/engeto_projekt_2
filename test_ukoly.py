import sys
print(sys.executable)
import pytest
import mysql.connector
from db import pridat_ukol_db, aktualizovat_ukol_db, odstranit_ukol_db

def get_test_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Kohoutek-1",
        database="task_manager_test"
    )

def test_pridat_ukol_pozitivni():
    conn = get_test_db()
    
    result = pridat_ukol_db("Testovací úkol", "Toto je testovací úkol.", conn)

    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM ukoly WHERE nazev = %s",
        ('Testovací úkol',)
    )
    data = cursor.fetchone()

    assert result == True
    assert data is not None
    
    cursor.execute(
        "DELETE FROM ukoly WHERE nazev = %s", 
        ('Testovací úkol',)
    )
    conn.commit()
    conn.close()

def test_pridat_ukol_negativni():
    conn = get_test_db()
    
    result = pridat_ukol_db("", "", conn)

    assert result == False
    
    conn.close()

def test_aktualizovat_ukol_pozitivni():
    conn = get_test_db()
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT INTO ukoly (nazev, popis) VALUES (%s, %s)",
        ("Aktualizační úkol", "Toto je úkol pro aktualizaci.")
    )
    conn.commit()

    id_ukolu = cursor.lastrowid

    result = aktualizovat_ukol_db(id_ukolu, "Hotovo", conn)

    cursor.execute(
        "SELECT stav FROM ukoly WHERE id = %s",
        (id_ukolu,)
    )
    stav = cursor.fetchone()[0]

    assert result == True
    assert stav == "Hotovo"

    cursor.execute(
        "DELETE FROM ukoly WHERE id = %s",
        (id_ukolu,)
    )
    conn.commit()
    conn.close()

def test_aktualizovat_ukol_negativni():
    conn = get_test_db()
    
    fake_id = 9999
    
    result = aktualizovat_ukol_db(fake_id, "Hotovo", conn)

    assert result == False
    
    conn.close()

def test_odstranit_ukol_pozitivni():
    conn = get_test_db()
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT INTO ukoly (nazev, popis) VALUES (%s, %s)",
        ("Odstraňovací úkol", "Toto je úkol pro odstranění.")
    )
    conn.commit()

    id_ukolu = cursor.lastrowid

    result = odstranit_ukol_db(id_ukolu, conn)

    cursor.execute(
        "SELECT * FROM ukoly WHERE id = %s",
        (id_ukolu,)
    )
    data = cursor.fetchone()

    assert result == True
    assert data is None
    
    conn.close()

def test_odstranit_ukol_negativni():
    conn = get_test_db()
    
    fake_id = 9999
    
    result = odstranit_ukol_db(fake_id, conn)

    assert result == False
    
    conn.close()