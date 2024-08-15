import psycopg2

# Defina suas credenciais de conexão
host = "localhost"          # Endereço do servidor PostgreSQL
database = "TCC3"           # Nome do banco de dados
user = "agent1"            # Nome de usuário do PostgreSQL
password = "12"            # Senha do usuário PostgreSQL
port = "5432"             # Porta padrão para PostgreSQL

conn = None  # Inicializar a variável conn

try:
    # Estabelecer a conexão
    conn = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password,
        port=port
    )

    # Definir a codificação da conexão
    conn.set_client_encoding('UTF8')

    # Criar um cursor
    cur = conn.cursor()

    # Executar uma consulta de teste
    cur.execute("SELECT version();")

    # Obter o resultado
    db_version = cur.fetchone()
    print(f"Versão do PostgreSQL: {db_version}")

    # Fechar o cursor
    cur.close()

except Exception as error:
    print(f"Erro ao conectar ao PostgreSQL: {error}")

finally:
    # Verificar se a conexão foi estabelecida antes de tentar fechá-la
    if conn is not None:
        conn.close()
        print("Conexão com o PostgreSQL fechada.")
