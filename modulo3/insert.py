import psycopg2

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

def insert_data(rg, apelido, crimes, conexoes):
    """Insere dados na tabela historico."""
    conn = connect_to_db()
    if conn is not None:
        try:
            cur = conn.cursor()
            
            # Comando SQL para inserção com aspas duplas
            insert_query = """
            INSERT INTO historico ("RG", "Apelido", "Crimes", "Conexoes")
            VALUES (%s, %s, %s, %s)
            """
            
            # Dados a serem inseridos
            data_to_insert = (rg, apelido, crimes, conexoes)
            
            # Executar o comando
            cur.execute(insert_query, data_to_insert)
            
            # Confirmar a inserção
            conn.commit()
            print("Dados inseridos com sucesso.")
            
            # Fechar o cursor
            cur.close()
        except Exception as error:
            print(f"Erro ao inserir dados: {error}")
        finally:
            conn.close()
            print("Conexão com o PostgreSQL fechada.")

# Dados de exemplo
rg = "1245"
apelido = "Francisco"
crimes = [ ]
conexoes = ['15346']

# Inserir dados
insert_data(rg, apelido, crimes, conexoes)
