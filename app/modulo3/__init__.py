import networkx as nx
import matplotlib.pyplot as plt
import psycopg2  # Biblioteca responsável por usar o PostgreSQL no Python
import app.database.database as db

# Credenciais de conexão
host = "localhost"
database = "TCC3"  # Banco de dados
user = "agent1"  # Pessoa que vai modificar
password = "12"  # Senha do Banco de Dados
port = "5432"

class Modulo3:

    def connect_to_db(self):
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

    def create_graph_for_rg(self, rg, visited_rg, all_conexoes):
        """Cria um grafo de conexões e crimes para um RG específico e armazena conexões para futuros grafos."""
        conn = self.connect_to_db()
        if conn is not None:
            try:
                cur = conn.cursor()

                # Comando SQL para consultar o RG, suas conexões e crimes
                query_rg = """
                SELECT "RG", "Apelido" , "Conexoes", "Crimes" FROM historico WHERE "RG" = %s;
                """

                # Executar a consulta para o RG específico
                cur.execute(query_rg, (rg,))
                result = cur.fetchone()

                if result:
                    rg, apelido, conexoes, crimes = result

                    # Contagem de crimes e conexões
                    num_crimes = len(crimes) if crimes else 0
                    num_conexoes = len(conexoes) if conexoes else 0
                    
                    # Salvar crimes e conexões em vetores
                    crime_vetor = crimes if crimes else []
                    conexao_vetor = conexoes if conexoes else []

                    # Imprimir as informações do RG principal
                    print(f"RG Principal: {rg}")
                    print(f"Crimes ({num_crimes}): {crimes}")
                    print(f"Conexões ({num_conexoes}): {conexoes}")
                    print("-" * 50)
                    db.connect()
                    sql = """INSERT INTO grafo (etapa) VALUES (?)"""
                    db.execute(sql, "2")
        
                    # salva a pessoa no banco de dados da pessoa
                    sql = """INSERT INTO pessoas (id, nome, nivel_participacao, importancia) VALUES (?,?,?,?)"""
                    array_of_tuples = (rg, apelido,1,0)
                    db.execute(sql, array_of_tuples)
                    
                    # salva os fatos no banco de dados das pessoa_fato
                    for i in range(num_crimes):
                        print(crime_vetor[i])
                        sql = """INSERT INTO pessoa_fato (id_pessoa, id_fato) VALUES (?,?)"""
                        array_of_tuples = (rg, crime_vetor[i])
                        db.execute(sql, array_of_tuples)
                    
                    # salva as conexões no banco de dados das conexões
                    for i in range(num_conexoes):
                        print(conexao_vetor[i])
                        sql = """INSERT INTO conexoes (id_pessoa_A, id_pessoa_B, peso, id_grafo) VALUES (?,?,?,?)"""
                        array_of_tuples = (rg, conexao_vetor[i],1,2)
                        db.execute(sql, array_of_tuples)
                    db.close()

                    # Criar um grafo direcionado para o RG
                    G = nx.DiGraph()

                    # Adicionar o nó principal (RG) com os crimes como parte do rótulo
                    crime_labels = ', '.join(crimes) if crimes else 'Nenhum crime'
                    rg_label = f'{rg}\nCrimes: {crime_labels}'
                    G.add_node(rg, label=rg_label)

                    # Adicionar as conexões e seus crimes como nós e arestas
                    if conexoes:
                        for conexao in conexoes:
                            if conexao not in visited_rg:
                                all_conexoes.add(conexao)

                            # Comando SQL para buscar crimes e conexões da conexão
                            query_conexao = """
                            SELECT "Crimes", "Conexoes" FROM historico WHERE "RG" = %s;
                            """

                            cur.execute(query_conexao, (conexao,))
                            result_conexao = cur.fetchone()

                            if result_conexao:
                                conexao_crimes, conexao_conexoes = result_conexao
                                conexao_crimes_label = ', '.join(
                                    conexao_crimes) if conexao_crimes else 'Nenhum crime'

                                # Adicionar nó para cada conexão com rótulo
                                G.add_node(
                                    conexao, label=f'{conexao}\nCrimes: {conexao_crimes_label}')
                                # Adicionar aresta do RG para a conexão
                                G.add_edge(rg, conexao)

                                # Adicionar conexões para futuros grafos
                                for sub_conexao in conexao_conexoes:
                                    if sub_conexao not in visited_rg:
                                        all_conexoes.add(sub_conexao)

                    # Ajuste do layout para o grafo
                    pos = nx.spring_layout(G, seed=42)
                    plt.figure(figsize=(12, 10))

                    # Desenhar o grafo
                    nx.draw(
                        G,
                        pos,
                        with_labels=True,
                        labels=nx.get_node_attributes(G, 'label'),
                        node_size=3000,
                        node_color='lightblue',
                        font_size=10,
                        font_weight='bold',
                        arrows=True,  # Usar setas
                        edge_color='black',
                        width=2
                    )
                    plt.title(f'Grafo de Conexões e Crimes para RG {rg}')
                    plt.show()

                    # Atualizar a lista de RGs a serem visitados
                    visited_rg.add(rg)
                    # Retornar uma lista das conexões encontradas
                    return list(all_conexoes)
                else:
                    print(f"RG {rg} não encontrado na tabela historico.")
                    return []

                # Fechar o cursor
                cur.close()
            except Exception as error:
                print(f"Erro ao consultar dados ou criar o grafo: {error}")
                return []
            finally:
                conn.close()
                print("Conexão com o PostgreSQL fechada.")

    def main(self):
        start_rg = "1"  # Substituir pelo RG desejado
        """Função principal para iniciar a criação dos grafos e iteração das conexões."""
        visited_rg = set()  # Conjunto para rastrear RGs visitados
        to_visit = [start_rg]  # Lista de RGs a serem visitados
        all_conexoes = set()  # Conjunto para rastrear todas as conexões

        while to_visit:
            current_rg = to_visit.pop(0)
            if current_rg not in visited_rg:
                new_conexoes = self.create_graph_for_rg(
                    current_rg, visited_rg, all_conexoes)

                # Atualizar a lista de RGs a serem visitados com novas conexões
                to_visit.extend(
                    conexao for conexao in new_conexoes if conexao not in visited_rg)

        print("Todos os grafos foram desenhados.")


# Teste da classe Modulo3
if __name__ == "__main__":
    m3 = Modulo3()
    m3.main()
