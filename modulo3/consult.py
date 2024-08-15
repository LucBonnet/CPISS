import psycopg2
import csv

# Defina suas credenciais de conexão
host = "localhost"
database = "TCC3"
user = "agent1"
password = "12"
port = "5432"

def connect_to_db():
    """Estabelece uma conexão com o banco de dados PostgreSQL."""
    conn = None
    try:
        conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=port
        )
        conn.set_client_encoding('UTF8')
        return conn
    except Exception as error:
        print(f"Erro ao conectar ao PostgreSQL: {error}")
        return None

def query_and_save_to_csv(rg, filename):
    """Consulta dados na tabela historico pelo RG e salva em um arquivo CSV."""
    conn = connect_to_db()
    if conn is not None:
        try:
            cur = conn.cursor()
            
            # Comando SQL para consulta
            query = """
            SELECT "RG", "Apelido", "Crimes", "Conexoes" FROM historico WHERE "RG" = %s;
            """
            
            # Executar a consulta
            cur.execute(query, (rg,))
            
            # Buscar todos os resultados
            rows = cur.fetchall()
            
            # Salvar em um arquivo CSV
            with open(filename, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                # Escrever os dados
                writer.writerows(rows)
            
            print(f"Dados salvos em {filename}.")
            
            # Fechar o cursor
            cur.close()
        except Exception as error:
            print(f"Erro ao consultar dados ou salvar em CSV: {error}")
        finally:
            conn.close()
            print("Conexão com o PostgreSQL fechada.")

# Consultar pelo RG e salvar os dados em um arquivo CSV
rg = "123456789"
filename = "historico_dados.csv"
query_and_save_to_csv(rg, filename)
