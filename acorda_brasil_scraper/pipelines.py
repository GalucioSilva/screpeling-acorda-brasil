from itemadapter import ItemAdapter
import json
import os


class AcordaBrasilScraperPipeline:
    def process_item(self, item, spider):
        # pipeline padrão (pode adicionar regras extras depois)
        return item


class PoliticosPipeline:
    def open_spider(self, spider):
        # só aplica em spiders de políticos
        if spider.name not in ["deputados", "senadores", "governadores"]:
            self.file = None
            return

        os.makedirs("data_output", exist_ok=True)
        self.file_path = "data_output/politicos.json"

        # Se o arquivo não existe ou está vazio → abre e inicia como lista
        if not os.path.exists(self.file_path) or os.stat(self.file_path).st_size == 0:
            self.file = open(self.file_path, "w", encoding="utf-8")
            self.file.write("[\n")
            self.first = True
        else:
            # Se já existe, remove o "]" final para continuar adicionando
            with open(self.file_path, "rb+") as f:
                f.seek(-1, os.SEEK_END)
                last_char = f.read(1)
                if last_char == b"]":
                    f.seek(-1, os.SEEK_END)
                    f.truncate()
            self.file = open(self.file_path, "a", encoding="utf-8")
            self.file.write("\n")
            self.first = False

    def close_spider(self, spider):
        if self.file:
            # Remove vírgula extra se tiver sobrado
            self.file.seek(self.file.tell() - 2, os.SEEK_SET)
            last_chars = self.file.read(2)
            if last_chars == ",\n":
                self.file.seek(self.file.tell() - 2, os.SEEK_SET)
                self.file.truncate()
            self.file.write("\n]")
            self.file.close()

    def process_item(self, item, spider):
        if self.file is None:
            return item  # ignora spiders que não são políticos

        # adiciona campo cargo fixo por tipo
        if spider.name == "deputados":
            item["cargo"] = "Deputado Federal"
        elif spider.name == "senadores":
            item["cargo"] = "Senador"
        elif spider.name == "governadores":
            item["cargo"] = "Governador"

        # escreve no JSON consolidado
        json.dump(dict(item), self.file, ensure_ascii=False, indent=2)
        self.file.write(",\n")

        return item
