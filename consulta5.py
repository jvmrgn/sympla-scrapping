import sqlite3

conn = sqlite3.connect("eventos_sympla.db")
cursor = conn.cursor()

cursor.execute("""
SELECT e.nome, m.metadado
FROM Eventos e
JOIN Metadados m ON e.id = m.evento_id
""")

metadados = cursor.fetchall()
for metadado in metadados:
    print("------------------------------")
    print(f"Evento: {metadado[0]}, Metadado: {metadado[1]}")

# Fechar a conexão
conn.close()
