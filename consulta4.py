import sqlite3

conn = sqlite3.connect("eventos_sympla.db")
cursor = conn.cursor()

cursor.execute("""
SELECT e.nome, de.data, de.localizacao, e.tipo
FROM Eventos e
JOIN DadosEventos de ON e.id = de.evento_id
WHERE de.localizacao LIKE '%ao ar livre%' OR de.localizacao LIKE '%aberto%'
""")

# Seguindo a mesma lógica do exercício passado acredito que não tenha nenhum evento ao ar livre no meu Scrap portanto sem resultados.

eventos_ao_ar_livre = cursor.fetchall()
for evento in eventos_ao_ar_livre:
    print("------------------------------")
    print(f"Nome: {evento[0]}\nData: {evento[1]}\nLocalização: {evento[2]}\nTipo: {evento[3]}")

conn.close()
