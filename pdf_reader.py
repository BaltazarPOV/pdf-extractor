import fitz  # PyMuPDF
import os
from flask import Flask, request, send_file
import time

app = Flask(__name__)

@app.route('/extraer', methods=['POST'])
def extraer_texto():
    """ Extrae texto de un PDF y lo guarda en un archivo .txt único para descarga """
    try:
        data = request.json
        pdf_path = data.get("pdf_path")
        inicio = int(data.get("inicio"))
        fin = int(data.get("fin"))

        doc = fitz.open(pdf_path)
        texto_extraido = ""

        for num_pagina in range(inicio - 1, fin):
            texto_extraido += f"\n📄 Página {num_pagina + 1}:\n"
            texto_extraido += doc[num_pagina].get_text("text") + "\n"

        # Generar un archivo único con timestamp
        output_file = f"resultado_{int(time.time())}.txt"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(texto_extraido)

        return send_file(output_file, as_attachment=True)

    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
