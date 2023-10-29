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
        price=data['price'],
    )
    movie_data.append(movie)

# Membuat folder "images" jika belum ada
if not os.path.exists("images"):
    os.makedirs("images")

def order_ticket(movie_info):
    root = tk.Tk()
    root.title(f"Available Seats for {movie_info.title}")
    root.geometry("600x400")

    available_seats = movie_info.available_seats
    booked_seats = movie_info.booked_seats

    selected_seats = set()  # Store selected seats in a set

    def seat_click(seat, label):
        if seat not in booked_seats:
            if label.cget("bg") == "green":
                # If the seat is already highlighted (green), unhighlight it by restoring the default background color
                label.configure(bg=label.master.cget("bg"))  # Use the background color of the parent frame
                status_label.config(text="Selected Seat: None")
                selected_seats.discard(seat)  # Remove the seat from the selected seats
            else:
                # Highlight the seat by changing the background color to green
                label.configure(bg="green")
                status_label.config(text=f"Selected Seat: {seat} (Available)")
                selected_seats.add(seat)  # Add the seat to the selected seats
        else:
            status_label.config(text=f"Selected Seat: {seat} (Not Available)")

    def order_selected_seats():
        if selected_seats:
            total_price = 0
            for seat in selected_seats:
                # Hitung harga berdasarkan kursi yang dipilih (misalnya, 10000 per kursi)
                total_price += movie_info.price  # Gantilah ini dengan formula harga yang sesuai

            # Buat tampilan check-out baru
            checkout_window = tk.Toplevel()
            checkout_window.title("Checkout")
            checkout_window.geometry("400x200")

            # Tampilkan informasi pesanan
            movie_title_label = Label(checkout_window, text=f"Film: {movie_info.title}")
            movie_title_label.pack()
        
        selected_seats_label = Label(checkout_window, text=f"Kursi yang Dipilih: {', '.join(selected_seats)}")
        selected_seats_label.pack()
        
        total_price_label = Label(checkout_window, text=f"Total Harga: Rp {total_price}00")
        total_price_label.pack()

        # Tombol "Confirm Order"
        confirm_button = Button(checkout_window, text="Confirm Order", command=checkout_window.destroy)
        confirm_button.pack()

        # Tutup jendela check-out setelah selesai
        checkout_window.mainloop()

    seat_label = tk.Label(root, text="Available Seats:")
    seat_label.pack()

    # Create a frame to hold the seat labels
    seat_frame = tk.Frame(root)
    seat_frame.pack()

    rows = ["A", "B", "C", "D", "E"]

    # Dictionary to store references to seat labels
    seat_labels = {}

    for row in rows:
        for seat_num in range(1, 11):
            seat = f"{row}{seat_num}"
            if seat in available_seats:
                label = tk.Label(seat_frame, text=seat, borderwidth=2, relief="solid", padx=10, pady=5, cursor="hand2")
                if seat in booked_seats:
                    label.configure(bg="red", fg="white")
                else:
                    label.bind("<Button-1>", lambda event, seat=seat, label=label: seat_click(seat, label))
                label.grid(row=ord(row) - ord('A'), column=seat_num - 1, padx=5, pady=5)
                seat_labels[seat] = label
            else:
                label = tk.Label(seat_frame, text="", padx=10, pady=5)  # Empty label for unavailable seats
                label.grid(row=ord(row) - ord('A'), column=seat_num - 1, padx=5, pady=5)
                seat_labels[seat] = label

    status_label = tk.Label(root, text="Selected Seat: None")
    status_label.pack()

    order_button = tk.Button(root, text="Order Selected Seats", command=order_selected_seats)
    order_button.pack()

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
        
        duration_label = Label(frame, text=f"Harga: Rp {movie_info.price}00")
        duration_label.grid(row=3, column=0, sticky="w")
        

        # Tombol "Order Ticket"
        order_button = Button(frame, text="Order Ticket", command=lambda movie_info=movie_info: order_ticket(movie_info))
        order_button.grid(row=4, column=0, pady=5)

    root.mainloop()

# Menampilkan detail film menggunakan Tkinter
display_movie_details(movie_data)
