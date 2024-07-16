import os
from PyPDF2 import PdfReader, PdfWriter

def split_and_merge_pdfs(input_pdf_path, output_dir, merge_dir, acuse_dir, merge_names):
    pdf_reader = PdfReader(input_pdf_path)
    total_pages = len(pdf_reader.pages)

    merged_pdfs = []

    for i in range(0, total_pages, 2):
        # Crear un PdfWriter para el PDF combinado
        pdf_writer = PdfWriter()
        
        merge_name = merge_names[i // 2]

        # Buscar el PDF correspondiente en merge_dir
        merge_pdf_path = None
        for file in os.listdir(merge_dir):
            if merge_name in file:
                merge_pdf_path = os.path.join(merge_dir, file)
                break
        
        # Buscar el PDF correspondiente en acuse_dir
        acuse_pdf_path = None
        for file in os.listdir(acuse_dir):
            if merge_name in file:
                acuse_pdf_path = os.path.join(acuse_dir, file)
                break
        
        if merge_pdf_path:
            # Agregar las páginas del PDF de merge primero
            merge_reader = PdfReader(merge_pdf_path)
            for page in merge_reader.pages:
                pdf_writer.add_page(page)

            # Agregar las páginas del PDF base
            for j in range(2):
                if i + j < total_pages:
                    pdf_writer.add_page(pdf_reader.pages[i + j])

            # Agregar las páginas del PDF de acuse si existe
            if acuse_pdf_path:
                acuse_reader = PdfReader(acuse_pdf_path)
                for page in acuse_reader.pages:
                    pdf_writer.add_page(page)

            # Generar el nombre de archivo combinado
            output_pdf_path = os.path.join(output_dir, f"MEMORANDO_{merge_name}.pdf")

            # Escribir el PDF combinado
            with open(output_pdf_path, 'wb') as output_pdf:
                pdf_writer.write(output_pdf)

            merged_pdfs.append(output_pdf_path)
            print(f"Combinado: {merge_pdf_path}" +
                  f", {input_pdf_path} páginas {i}-{i+1}" +
                  (f", {acuse_pdf_path}" if acuse_pdf_path else "") +
                  f" -> {output_pdf_path}")
        else:
            print(f"No se encontró PDF para {merge_name} en FACTURAS")

    return merged_pdfs

input_pdf_path = "C:/Users/ACER/Desktop/tarifas/src/memo_ica04.pdf"
output_directory = "C:/Users/ACER/Desktop/tarifas/src/merged"
merge_directory = "C:/Users/ACER/Desktop/tarifas/src/FACTURAS"  # Carpeta con los PDFs a unir
acuse_directory = "C:/Users/ACER/Desktop/tarifas/src/ACUSE DIAN"  # Carpeta con los PDFs adicionales

merge_names = [
    "5000060132","FE12206","FE7050", "FE5876"
]

if not os.path.exists(output_directory):
    os.makedirs(output_directory)

merged_pdfs = split_and_merge_pdfs(input_pdf_path, output_directory, merge_directory, acuse_directory, merge_names)

# Imprimir los PDFs combinados
for pdf in merged_pdfs:
    print(f"PDF combinado creado: {pdf}")
