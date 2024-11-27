import sqlite3

conn = sqlite3.connect("eventos_sympla.db")
cursor = conn.cursor()

cursor.execute("""
SELECT e.nome, de.data, de.localizacao, e.tipo
FROM Eventos e
JOIN DadosEventos de ON e.id = de.evento_id
ORDER BY de.data ASC
LIMIT 2
""")

eventos_proximos = cursor.fetchall()
for evento in eventos_proximos:
    print("------------------------------")
    print(f"Nome: {evento[0]}\nData: {evento[1]}\nLocalização: {evento[2]}\nTipo: {evento[3]}")

conn.close()
