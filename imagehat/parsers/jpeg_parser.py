from imagehat.parsers.base_parser import BaseParser

class JPEGParser(BaseParser):
    def parse(self):
        return f"Parsing JPEG metadata from {self.file_path}"
