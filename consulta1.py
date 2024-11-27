import sqlite3

conn = sqlite3.connect("eventos_sympla.db")
cursor = conn.cursor()

cursor.execute("""
SELECT e.nome, de.data, de.localizacao, e.tipo
FROM Eventos e
JOIN DadosEventos de ON e.id = de.evento_id
""")

# Exibir os resultados
eventos = cursor.fetchall()
for evento in eventos:
    print("------------------------------")
    print(f"Nome: {evento[0]}\nData: {evento[1]}\nLocalização: {evento[2]}\nTipo: {evento[3]}")

# Fechar a conexão
conn.close()