from flask import Flask, render_template, request
from PyPDF2 import PdfReader, PdfWriter
import os
import glob

app = Flask(__name__)

def split_pdf(base_folder, order):
    user_folders = [f for f in os.listdir(base_folder) if os.path.isdir(os.path.join(base_folder, f))]
    
    if not user_folders:
        return {}
    
    processed_files = {}

    for user_folder in user_folders:
        user_path = os.path.join(base_folder, user_folder)
        pdf_files = glob.glob(os.path.join(user_path, "img*.pdf"))
        
        if not pdf_files:
            continue
        
        processed_files[user_folder] = []  # Simpan daftar file hasil pemisahan
        
        for pdf_path in pdf_files:
            reader = PdfReader(pdf_path)
            total_pages = len(reader.pages)
            all_pages = [reader.pages[i] for i in range(total_pages)]
            
            pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
            
            for i, name in enumerate(order):
                if i < len(all_pages):
                    writer = PdfWriter()
                    writer.add_page(all_pages[i])
                    
                    output_filename = os.path.join(user_path, f"{name}.pdf")
                    with open(output_filename, "wb") as output_pdf:
                        writer.write(output_pdf)
                    
                    processed_files[user_folder].append(output_filename)  # Simpan path file hasil
                    
            # Hapus file PDF asli setelah diproses
            try:
                os.remove(pdf_path)
            except Exception as e:
                print(f"Error menghapus file {pdf_path}: {e}")
    
    return processed_files

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Ambil inputan user dari form
        folder_path = request.form.get("folder_path")
        order_input = request.form.get("order")
        
        if not os.path.exists(folder_path):
            return render_template("index.html", error="Path folder tidak valid!")
        
        order_list = [x.strip() for x in order_input.split(",")]  # Konversi ke list
        
        processed_files = split_pdf(folder_path, order_list)
        return render_template("index.html", processed_files=processed_files)
    
    return render_template("index.html", processed_files={}, error="")

if __name__ == "__main__":
    app.run(debug=True)
