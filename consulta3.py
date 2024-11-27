import sqlite3

conn = sqlite3.connect("eventos_sympla.db")
cursor = conn.cursor()

cursor.execute("""
SELECT e.nome, de.data, de.localizacao, e.tipo
FROM Eventos e
JOIN DadosEventos de ON e.id = de.evento_id
WHERE de.localizacao LIKE '%São Paulo%'
""")

# Para fazer o WebScrap do RJ Basta mudar de "São Paulo" para "Rio de Janeiro"
# Como aonde eu estava fazendo WebScrap não havia nenhum dado do RJ na hora eu troquei para São Paulo apenas para exemplificar

eventos_rj = cursor.fetchall()
for evento in eventos_rj:
    print("------------------------------")
    print(f"Nome: {evento[0]}\nData: {evento[1]}\nLocalização: {evento[2]}\nTipo: {evento[3]}")


conn.close()