import tkinter as tk
from tkinter import Label, Frame, Button
from model import Movie  # Import model Movie dari file model.py
import json
import os  # Modul untuk mengelola sistem file
import requests
from PIL import Image, ImageTk

# Membuat folder "images" jika belum ada
if not os.path.exists("images"):
    os.makedirs("images")

# Baca data film dari file JSON
with open('movie_data.json', 'r') as json_file:
    movie_list = json.load(json_file)

def order_ticket(movie_title):
    # Tambahkan logika untuk memesan tiket di sini
    print(f"Anda memesan tiket untuk film: {movie_title}")

def display_movie_details(movie_data):
    root = tk.Tk()
    root.title("Detail Film")

    for idx, movie_info in enumerate(movie_data):
        # Membuat frame untuk setiap film
        frame = Frame(root)
        frame.grid(row=0, column=idx, padx=10, pady=10, sticky="w")

        # URL gambar poster
        poster_url = movie_info['poster_path']

        # Unduh gambar poster
        poster_response = requests.get(poster_url)
        poster_filename = f"images/{movie_info['title'].replace(' ', '_')}_poster.jpg"  # Simpan gambar dalam folder "images"
        with open(poster_filename, "wb") as poster_file:
            poster_file.write(poster_response.content)

        # Mengubah ukuran gambar menggunakan Pillow
        poster_image = Image.open(poster_filename)
        new_width = 100  # Lebar gambar yang diinginkan
        poster_image.thumbnail((new_width, new_width))

        poster_image = ImageTk.PhotoImage(poster_image)

        # Menampilkan gambar poster di sisi kanan
        poster_label = Label(frame, image=poster_image)
        poster_label.image = poster_image
        poster_label.grid(row=0, column=0, padx=10)

        # Judul
        title_label = Label(frame, text=f"Judul: {movie_info['title']}")
        title_label.grid(row=1, column=0, sticky="w")

        # Durasi
        duration_label = Label(frame, text=f"Durasi: {movie_info['duration']} menit")
        duration_label.grid(row=2, column=0, sticky="w")

        # Tombol "Order Ticket"
        order_button = Button(frame, text="Order Ticket", command=lambda title=movie_info['title']: order_ticket(title))
        order_button.grid(row=3, column=0, pady=5)

    root.mainloop()

# Menampilkan detail film menggunakan Tkinter
display_movie_details(movie_list)
