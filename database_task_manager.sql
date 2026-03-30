CREATE DATABASE task_manager;
USE task_manager;

CREATE TABLE ukoly (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nazev VARCHAR(255) NOT NULL,
    popis TEXT NOT NULL,
    stav ENUM('Nezahájeno', 'Probíhá', 'Hotovo') DEFAULT 'Nezahájeno',
    datum_vytvoreni TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);