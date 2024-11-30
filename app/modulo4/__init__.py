from app.models.Fact import Fact


def get_data_from_file(file_path):
    facts = []
    if file_path:
        with open(file_path, 'r', encoding="utf-8") as facts_file:
            for fact in facts_file.readlines():
                fact_type, value = fact.split(";")
                facts.append((fact_type.strip(), float(value.strip())))

    return facts


class Modulo4:
    def __init__(self, print_data=True) -> None:
        self.print_data = print_data

    def main(self, facts_file_path=None):
        print("Módulo 4\n")

        facts = get_data_from_file(facts_file_path)
        
        if len(facts) > 0:
            print("Valores dos fatos")
            for fact in facts:
                print(fact)
            Fact.update(facts)
            print()
