from transformers import pipeline
import sys
import PyPDF2

translator = pipeline("translation_en_to_es", model="Helsinki-NLP/opus-mt-en-es")

# Función para extraer texto de un PDF
def extract_text_from_pdf(file_path):
    pdf_file = open(file_path, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in range(len(pdf_reader.pages)):
        pageObj = pdf_reader.pages[page]
        text += pageObj.extract_text() + "\n"
    pdf_file.close()
    return text

# Función para traducir texto
def translate_text(source_text, longitud_fragmento=400):
    texto_traducido = ""
    for i in range(0, len(source_text), longitud_fragmento):
        fragmento = source_text[i:i+longitud_fragmento]
        resultado_fragmento = translator(fragmento)
        texto_traducido += resultado_fragmento[0]['translation_text']
    return texto_traducido

if __name__ == '__main__':
    input_pdf_path = sys.argv[1] if len(sys.argv) > 1 else "input.pdf"
    output_file_path = sys.argv[2] if len(sys.argv) > 2 else "output.txt"

    text = extract_text_from_pdf(input_pdf_path)
    translated_text = translate_text(text)

    output_file = open(output_file_path, 'w', encoding='utf-8') if len(sys.argv) > 2 else sys.stdout
    print("\nTexto Original:\n") or print(text)
    print("\nTexto Traducido:\n") or output_file.write(translated_text)
    output_file.close()