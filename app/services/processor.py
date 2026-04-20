import re
import language_tool_python


import nltk
from nltk.corpus import words

nltk.download('words')
nltk.download('punkt') 
nltk.download('stopwords') 
nltk.download('rslp') 


tool = language_tool_python.LanguageTool('pt-BR')
print("Setup! Concluído")

def process_and_classify(texto: str):
    matches = tool.check(texto)
    results = []
    
    for match in matches:
        if match.replacements:
            incorrect = texto[match.offset : match.offset + match.errorLength]
            correct = match.replacements[0]
            
            # --- INTEGRAÇÃO COM MODELO ---
            # Exemplo genérico:
            classification = classify_error_model(incorrect, correct)
            
            
            results.append({
                "incorreta": incorrect,
                "correta": correct,
                "classification": classification
            })
            
    return results

# SERÁ IMPLEMENTADA APÓS CONSEGUIR O MODELO TREINADO
# def classify_error_model(incorreta: str, correta: str):
#     # Lógica temporária enquanto carrega o modelo
#     # No futuro: return modelo.predict([[incorreta, correta]])
#     return "ortografia" # Mock (exemplo)


# apenas uma função pra testar o endpoint


# # processor.py    
# def processar_teste_manual(texto_do_estudante: str):
#     matches = tool.check(texto_do_estudante)
#     resultados = []
    
#     for match in matches:
#         if match.replacements:
#             incorreta = texto_do_estudante[match.offset : match.offset + match.error_length]
#             correta = match.replacements[0]
            
#             resultados.append({
#                 "incorreta": incorreta,
#                 "correta": correta,
#                 "classificacao": "pendente_ia" 
#             })
            
#     return resultados