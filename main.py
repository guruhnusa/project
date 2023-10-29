import tkinter as tk
from tkinter import Label, Frame, Button
import os
import requests
from PIL import Image, ImageTk
from model import Movie  # Import model Movie dari file model.py
import json

# Membaca data film dari file JSON
with open('movie_data.json', 'r') as json_file:
    json_data = json.load(json_file)

# List untuk menyimpan objek Movie
movie_data = []

# Konversi data JSON ke objek Movie
for data in json_data:
    movie = Movie(
        title=data['title'],
        duration=data['duration'],
        poster_path=data['poster_path'],
        available_seats=data['available_seats'],
        booked_seats=data['booked_seats'],
    )
    movie_data.append(movie)

# Membuat folder "images" jika belum ada
if not os.path.exists("images"):
    os.makedirs("images")

def order_ticket(movie_info):
    root = tk.Tk()
    root.title(f"Available Seats for {movie_info.title}")

    available_seats = movie_info.available_seats
    
    seat_label = tk.Label(root, text="Available Seats:")
    seat_label.pack()

    # Create a frame to hold the seat labels
    seat_frame = tk.Frame(root)
    seat_frame.pack()

    rows = ["A", "B", "C", "D", "E"]  # Define the rows

    for idx, row in enumerate(rows):
        for seat_num in range(1, 11):
            seat = f"{row}{seat_num}"  # Format seat as "A1", "A2", ... "E10"
            seat_label = tk.Label(seat_frame, text=seat, borderwidth=2, relief="solid", padx=10, pady=5)
            seat_label.grid(row=idx, column=seat_num + 1, padx=5, pady=10)

    root.mainloop()


def display_movie_details(movie_data):
    root = tk.Tk()
    root.title("Detail Film")

    for idx, movie_info in enumerate(movie_data):
        # Membuat frame untuk setiap film
        frame = Frame(root)
        frame.grid(row=0, column=idx, padx=10, pady=10, sticky="w")
        
        # URL gambar poster
        poster_url = movie_info.poster_path

        # Unduh gambar poster
        poster_response = requests.get(poster_url)
        poster_filename = f"images/{movie_info.title.replace(' ', '_')}_poster.jpg"  # Simpan gambar dalam folder "images"
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
        title_label = Label(frame, text=f"Judul: {movie_info.title}")
        title_label.grid(row=1, column=0, sticky="w")

        # Durasi
        duration_label = Label(frame, text=f"Durasi: {movie_info.duration} menit")
        duration_label.grid(row=2, column=0, sticky="w")
        

        # Tombol "Order Ticket"
        order_button = Button(frame, text="Order Ticket", command=lambda movie_info=movie_info: order_ticket(movie_info))
        order_button.grid(row=3, column=0, pady=5)

    root.mainloop()

# Menampilkan detail film menggunakan Tkinter
display_movie_details(movie_data)
