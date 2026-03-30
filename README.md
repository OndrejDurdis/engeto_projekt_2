# engeto_projekt_2
Vylepšená verze správce úkolů, která ukládá data do MySQL databáze místo do paměti.
Aplikace umožňuje základní CRUD operace (Create, Read, Update, Delete) nad úkoly.
Součástí projektu jsou také automatizované testy pomocí knihovny pytest, které ověřují správnou funkčnost klíčových operací.

1. Instalace závislostí
   pip install mysql-connector-python pytest
2. Vytvoření databáze
   Spusťte SQL skript: database_task_manager.sql
3. Vytvoření testovací databáze
   Spusťte SQL skript: database_task_manager_test.sql
