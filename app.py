from flask import Flask, render_template, request
from PIL import Image
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    # Mendapatkan file gambar yang diunggah
    uploaded_image = request.files['image']
    
    # Menyimpan file gambar sementara
    image_path = 'static/uploaded_image.jpg'
    uploaded_image.save(image_path)

    return render_template('crop.html', image_path=image_path)

@app.route('/crop', methods=['POST'])
def crop():
    # Mendapatkan path file gambar yang diunggah
    image_path = request.form.get('image_path')
    
    # Memuat gambar menggunakan PIL
    image = Image.open(image_path)

    # Mendapatkan data form untuk ukuran dan posisi crop
    size = request.form.get('size')
    position = request.form.get('position')

    # Memastikan nilai yang diambil tidak bernilai None
    if size is not None and position is not None:
        size = int(size)

        if size > image.width or size > image.height:
            return "Size melebihi ukuran asli"

        # Mengubah posisi menjadi koordinat x dan y berdasarkan pilihan
        if position == 'top left':
            x = 0
            y = 0
        elif position == 'top center':
            x = (image.width - size) // 2
            y = 0
        elif position == 'top right':
            x = image.width - size
            y = 0
        elif position == 'center left':
            x = 0
            y = (image.height - size) // 2
        elif position == 'center':
            x = (image.width - size) // 2
            y = (image.height - size) // 2
        elif position == 'center right':
            x = image.width - size
            y = (image.height - size) // 2
        elif position == 'bottom left':
            x = 0
            y = image.height - size
        elif position == 'bottom center':
            x = (image.width - size) // 2
            y = image.height - size
        elif position == 'bottom right':
            x = image.width - size
            y = image.height - size

        # Memotong gambar sesuai dengan koordinat yang diberikan
        cropped_image = image.crop((x, y, x + size, y + size))

        # Menyimpan gambar yang dipotong
        cropped_image_path = 'static/cropped_image.jpg'
        cropped_image.save(cropped_image_path)

        # Menghapus file gambar sementara
        os.remove(image_path)

        return render_template('result.html', cropped_image_path=cropped_image_path)

    # Jika nilai yang diambil kosong, tampilkan pesan kesalahan
    return "Invalid input"


if __name__ == '__main__':
    app.run(debug=True, port=8000)
