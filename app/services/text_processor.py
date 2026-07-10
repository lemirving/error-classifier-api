# app/services/text_processor.py
import language_tool_python
from typing import List, Dict

class TextProcessor:
    def __init__(self):
        self.tool = language_tool_python.LanguageTool('pt-BR')

    def extrair_pares_erros(self, texto: str) -> List[Dict[str, str]]:
        """
        Analisa o texto e extrai os pares de palavras erradas e suas respectivas sugestões.
        Retorna no formato esperado pelo modelo do Thiago: [{'errada': '...', 'correta': '...'}]
        """
        if not texto:
            return []
            
        matches = self.tool.check(texto)
        pares_erros = []

        for match in matches:
            termo_errado = texto[match.offset:match.offset + match.errorLength]
            
            if match.replacements:
                termo_correto = match.replacements[0]
                
                if not any(e['errada'] == termo_errado and e['correta'] == termo_correto for e in pares_erros):
                    pares_erros.append({
                        "errada": termo_errado,
                        "correta": termo_correto
                    })
                    
        return pares_erros