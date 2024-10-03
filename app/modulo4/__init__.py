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
    def main(self, facts_file_path=None):
        print("Módulo 4")

        facts = get_data_from_file(facts_file_path)

        Fact.update(facts)
