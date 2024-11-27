import requests
from bs4 import BeautifulSoup
import sqlite3
import re

def obter_descricao_evento(link):
    try:
        response = requests.get(link, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            descricao_elemento = soup.find("div", class_="sc-537fdfcb-0 bdUbUp")
            if descricao_elemento:
                descricao_texto = " ".join([p.get_text(strip=True) for p in descricao_elemento.find_all("p")])
                return descricao_texto
            else:
                return "Descrição não encontrada"
        else:
            return "Erro ao acessar o link"
    except Exception as e:
        return f"Erro: {e}"

def atribuir_tipo_evento(descricao):
    tipos_evento = []

    palavras_chave = {
        "Cultural": ["artes", "cultura", "música", "teatro", "dança", "exposição", "festival"],
        "Alimentação": ["gastronomia", "comida", "culinária", "alimentos", "restaurante", "food"],
        "Automobilismo": ["corrida", "carro", "automobilismo", "fórmula", "motocross", "rally"],
        "Tecnologia": ["tecnologia", "inovação", "startup", "software", "programação", "gaming"],
        "Esportes": ["futebol", "basquete", "corrida", "fitness", "esporte", "olimpíada", "vôlei"],
        "Negócios": ["empreendedorismo", "negócios", "empresas", "startups", "marketing"],
        "Saúde": ["saúde", "bem-estar", "medicina", "fitness", "saúde mental", "terapia"],
        "Educação": ["educação", "curso", "palestra", "workshop", "aprendizado", "capacitação"]
    }

    descricao_lower = descricao.lower()

    for tipo, palavras in palavras_chave.items():
        if any(palavra in descricao_lower for palavra in palavras):
            tipos_evento.append(tipo)

    if not tipos_evento:
        tipos_evento.append("Outro")

    return ", ".join(tipos_evento)

# Acredito que este link possa quebrar com o tempo mas para arrumar ele basta ir nesse site e pegar o link mais atualizado: https://www.sympla.com.br/eventos/este-fim-de-semana
url = "https://www.sympla.com.br/eventos/este-fim-de-semana?d=2024-11-30%2C2024-12-01"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    print("Requisição bem-sucedida!")
else:
    print(f"Erro na requisição: {response.status_code}")

soup = BeautifulSoup(response.content, "html.parser")

eventos_html = soup.find_all("a", class_="sympla-card pn67h10 pn67h11")

if not eventos_html:
    print("Nenhum evento encontrado na página.")
else:
    print(f"Total de eventos encontrados: {len(eventos_html)}")

eventos = []

conn = sqlite3.connect("eventos_sympla.db")
cursor = conn.cursor()

def evento_existe(link):
    cursor.execute("SELECT 1 FROM Eventos WHERE link = ?", (link,))
    return cursor.fetchone() is not None

cursor.execute(""" 
CREATE TABLE IF NOT EXISTS Eventos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    tipo TEXT,
    link TEXT NOT NULL UNIQUE,
    descricao TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS DadosEventos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    evento_id INTEGER,
    data TEXT,
    localizacao TEXT,
    FOREIGN KEY (evento_id) REFERENCES Eventos(id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Metadados (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    evento_id INTEGER,
    metadado TEXT,
    FOREIGN KEY (evento_id) REFERENCES Eventos(id)
)
""")

for evento_html in eventos_html:
    try:
        titulo_elemento = evento_html.find("h3", class_="pn67h18")
        localizacao_elemento = evento_html.find("p", class_="pn67h1a")
        data_elemento = evento_html.find("div", class_="qtfy413 qtfy414")
        
        nome = titulo_elemento.text.strip() if titulo_elemento else "Título não encontrado"
        localizacao = localizacao_elemento.text.strip() if localizacao_elemento else "Localização não encontrada"
        data = data_elemento.text.strip() if data_elemento else "Data não encontrada"
        
        link = evento_html["href"] if evento_html else "Link não encontrado"
        
        if evento_existe(link):
            print(f"Evento {nome} já existe no banco de dados, pulando...")
            continue
        
        descricao = obter_descricao_evento(link)
        
        tipo_evento = atribuir_tipo_evento(descricao)
        
        eventos.append((nome, tipo_evento, localizacao, data, link, descricao))
        
        print(f"Salvando evento no banco: {nome}")
        cursor.execute("INSERT INTO Eventos (nome, tipo, link, descricao) VALUES (?, ?, ?, ?)", 
                       (nome, tipo_evento, link, descricao))
        
        evento_id = cursor.lastrowid
        
        cursor.execute("INSERT INTO DadosEventos (evento_id, data, localizacao) VALUES (?, ?, ?)", 
                       (evento_id, data, localizacao))
        
        cursor.execute("INSERT INTO Metadados (evento_id, metadado) VALUES (?, ?)", 
                       (evento_id, link))

    except Exception as e:
        print(f"Erro ao processar evento: {e}")

conn.commit()

cursor.execute("SELECT COUNT(*) FROM Eventos")
total_eventos = cursor.fetchone()[0]
print(f"Total de eventos armazenados no banco de dados: {total_eventos}")

conn.close()
print("Dados armazenados no banco de dados SQLite com sucesso!")
