from app.database.database import db

class Connection():
  # @staticmethod
  # def __saveConnectionFindPerson(conn):
  #   code_p_a, code_p_b, desc, weight, graph_id = conn

  #   person_a = UP.findByCode(code_p_a)
  #   if not person_a:
  #     raise Exception(f"Erro ao criar conexão\nPessoa {code_p_a} não encontrada")

  #   person_b = UP.findByCode(code_p_b)
  #   if not person_b:
  #     raise Exception(f"Erro ao criar conexão\nPessoa {code_p_b} não encontrada")

  #   return person_a.up_id, person_b.up_id, desc, weight, graph_id

  # @staticmethod
  # def createWithPersonCode(connectionData):
  #   connections = []
  #   if type(connectionData) is list:
  #     for conn in connectionData:
  #       connections.append(Connection.__saveConnectionFindPerson(conn))

  #     sql_insert_connection = f"INSERT OR REPLACE INTO conexoes (id_pessoa_A, id_pessoa_B, descricao, peso, id_grafo) VALUES (?,?,?,?,?)"
  #     db.connect()
  #     db.insert(sql_insert_connection, connections)
  #     db.close()
        
  #   elif type(connectionData) is tuple:
  #     connections.append(Connection.__saveConnectionFindPerson(connectionData))

  #     sql_insert_connection = f"INSERT OR REPLACE INTO conexoes (id_pessoa_A, id_pessoa_B, descricao, peso, id_grafo) VALUES (?,?,?,?,?)"
  #     db.connect()
  #     db.insert(sql_insert_connection, connections)
  #     db.close()

  #   return connections
  
  def create(connectionData):
    sql_insert_connection = f"INSERT OR REPLACE INTO conexoes (id_pessoa_A, id_pessoa_B, descricao, peso, id_grafo) VALUES (?,?,?,?,?)"
    
    connections = []
    if type(connectionData) is list:
      for conn in connectionData:
        connections.append(conn) 
        
    elif type(connectionData) is tuple:
      connections.append(connectionData)

    else: 
      return []
    
    db.connect()
    db.insert(sql_insert_connection, connections)
    db.close()

    return connections