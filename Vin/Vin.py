import sqlite3

# Connexion à ta base existante
conn = sqlite3.connect("C:\Sharepoint GIP\OneDrive - Gestion Indépendante de patrimoines GIP SA\Bureau\Database\Vin")
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(Vin)")
columns = cursor.fetchall()
print("Colonnes actuelles de la table 'Vin' :")
for column in columns:
    print(column)


# Données à insérer
nom_du_vin = "Margaux"  # Vous pouvez généraliser ou automatiser la saisie

# Insertion
cursor.execute("""
INSERT INTO Vin (Nom_du_vin) VALUES (?)
""", (nom_du_vin,))

# Sauvegarde et fermeture
conn.commit()
conn.close()