import anthropic
import pathlib
import csv

client = anthropic.Anthropic(api_key="sk-ant-...")

def clasificar_ejercicios(tema: str, enunciados: list[dict]) -> list[dict]:
    """
    enunciados: lista de dicts con keys año, convocatoria, ejercicio, texto
    retorna:    lista de dicts con keys año, convocatoria, ejercicio, tema, tipo_ejercicio
    """

    # Carga el markdown con los criterios del tema
    prompt_sistema = pathlib.Path(f"prompts/{tema}.md").read_text()

    # Formatea los enunciados como texto para el mensaje
    contenido = ""
    for e in enunciados:
        contenido += f"\n---\nAño: {e['año']} | {e['convocatoria']} | {e['ejercicio']}\n{e['texto']}\n"

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=2048,
        system=prompt_sistema,
        messages=[
            {"role": "user", "content": contenido}
        ]
    )

    # Parsear la respuesta CSV
    resultado = []
    for linea in response.content[0].text.strip().splitlines():
        partes = linea.split(",")
        if len(partes) == 5:
            resultado.append({
                "año":             partes[0].strip(),
                "convocatoria":    partes[1].strip(),
                "ejercicio":       partes[2].strip(),
                "tema":            partes[3].strip(),
                "tipo_ejercicio":  partes[4].strip(),
            })
    return resultado