import tkinter as tk
from tkinter import messagebox, filedialog
import random


# Song and Playlist classes (including shuffle method)
class Song:
    def __init__(self, title, artist, duration):
        self.title = title
        self.artist = artist
        self.duration = duration
        self.next = None  # Points to the next song in the playlist

    def __str__(self):
        return f"{self.title} by {self.artist} ({self.duration})"


class Playlist:
    def __init__(self):
        self.head = None  # First song in the playlist

    def add_song(self, title, artist, duration, position=None):
        new_song = Song(title, artist, duration)
        if position is None or position <= 0:
            if not self.head:
                self.head = new_song
            else:
                current = self.head
                while current.next:
                    current = current.next
                current.next = new_song
        else:
            if position == 1:
                new_song.next = self.head
                self.head = new_song
            else:
                current = self.head
                prev = None
                current_position = 1
                while current and current_position < position:
                    prev = current
                    current = current.next
                    current_position += 1
                new_song.next = current
                if prev:
                    prev.next = new_song
                else:
                    self.head = new_song

    def remove_song(self, title):
        if not self.head:
            return False
        if self.head.title == title:
            self.head = self.head.next
            return True
        current = self.head
        prev = None
        while current and current.title != title:
            prev = current
            current = current.next
        if current is None:
            return False
        else:
            prev.next = current.next
            return True

    def display_playlist(self):
        playlist = []
        current = self.head
        while current:
            playlist.append(f"{current.title} by {current.artist} ({current.duration})")
            current = current.next
        return playlist

    def shuffle_playlist(self):
        if not self.head or not self.head.next:
            print("Not enough songs to shuffle.")
            return

        songs_list = []
        current = self.head
        while current:
            songs_list.append(current)
            current = current.next

        random.shuffle(songs_list)

        self.head = songs_list[0]
        current = self.head
        for song in songs_list[1:]:
            current.next = song
            current = current.next
        current.next = None
        print("Playlist has been shuffled!")

    def save_playlist(self, filename):
        with open(filename, 'w') as file:
            current = self.head
            while current:
                file.write(f"{current.title},{current.artist},{current.duration}\n")
                current = current.next

    def load_playlist(self, filename):
        try:
            with open(filename, 'r') as file:
                self.head = None
                for line in file:
                    title, artist, duration = line.strip().split(',')
                    self.add_song(title, artist, duration)
        except FileNotFoundError:
            print(f"The file {filename} does not exist.")


# GUI Class using Tkinter with dark theme
class MusicPlayerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Mayank Music Player")
        self.root.geometry("600x600")

        self.playlist = Playlist()

        # Set dark theme
        self.root.configure(bg="black")
        self.text_color = "red"
        self.bg_color = "black"
        self.button_bg = "#333"

        # Current Song Frame
        current_song_frame = tk.LabelFrame(root, text="Currently Playing", fg=self.text_color, bg=self.bg_color,
                                           padx=10,
                                           pady=10)
        current_song_frame.grid(row=0, column=0, columnspan=3, padx=20, pady=20, sticky="ew")
        self.current_song_label = tk.Label(current_song_frame, text="No song playing", fg=self.text_color,
                                           bg=self.bg_color, width=50, height=2)
        self.current_song_label.pack(padx=10, pady=10)

        # Playlist Box

        # Playlist Label
        self.playlist_label = tk.Label(root, text="My Playlist", fg=self.text_color, bg=self.bg_color,
                                       font=("Helvetica", 12, "bold"))
        self.playlist_label.grid(row=1, column=0, columnspan=3, padx=20, pady=(20, 5))

        # Playlist Box
        self.playlist_box = tk.Listbox(root, width=70, height=12, selectmode=tk.SINGLE, bg=self.button_bg,
                                       fg=self.text_color)
        self.playlist_box.grid(row=2, column=0, columnspan=3, padx=20, pady=10)

        # playlist Button

        player_button_frame = tk.LabelFrame(root,text="Control Buttons", fg=self.text_color, bg=self.bg_color, padx=10, pady=10)
        player_button_frame.grid(row=3, column=0, columnspan=3, pady=10)

        # Control Buttons
        self.play_button = tk.Button(player_button_frame, text="Play", command=self.play_song, width=15,
                                     fg=self.text_color, bg=self.button_bg)
        self.play_button.grid(row=0, column=0, padx=5, pady=5)

        self.pause_button = tk.Button(player_button_frame, text="Pause", command=self.pause_song, width=15,
                                      fg=self.text_color, bg=self.button_bg)
        self.pause_button.grid(row=0, column=1, padx=5, pady=5)

        self.next_button = tk.Button(player_button_frame, text="Next", command=self.next_song, width=15,
                                     fg=self.text_color, bg=self.button_bg)
        self.next_button.grid(row=0, column=2, padx=5, pady=5)
        # Song Inputs Frame
        input_frame = tk.LabelFrame(root, text="Add a New Song", fg=self.text_color, bg=self.bg_color, padx=10, pady=10)
        input_frame.grid(row=4, column=0, columnspan=3, padx=20, pady=20, sticky="ew")

        self.title_label = tk.Label(input_frame, text="Title", fg=self.text_color, bg=self.bg_color)
        self.title_label.grid(row=0, column=0, padx=10, pady=5)
        self.title_entry = tk.Entry(input_frame, width=40)
        self.title_entry.grid(row=0, column=1, padx=10, pady=5)

        self.artist_label = tk.Label(input_frame, text="Artist", fg=self.text_color, bg=self.bg_color)
        self.artist_label.grid(row=1, column=0, padx=10, pady=5)
        self.artist_entry = tk.Entry(input_frame, width=40)
        self.artist_entry.grid(row=1, column=1, padx=10, pady=5)

        self.duration_label = tk.Label(input_frame, text="Duration (mm:ss)", fg=self.text_color, bg=self.bg_color)
        self.duration_label.grid(row=2, column=0, padx=10, pady=5)
        self.duration_entry = tk.Entry(input_frame, width=40)
        self.duration_entry.grid(row=2, column=1, padx=10, pady=5)

        self.position_label = tk.Label(input_frame, text="Position (optional)", fg=self.text_color, bg=self.bg_color)
        self.position_label.grid(row=3, column=0, padx=10, pady=5)
        self.position_entry = tk.Entry(input_frame, width=40)
        self.position_entry.grid(row=3, column=1, padx=10, pady=5)



        # Control Buttons Frame
        player_controls_frame = tk.Frame(root, bg=self.bg_color, padx=10, pady=10)
        player_controls_frame.grid(row=5, column=0, columnspan=3, pady=10)

        # Control Buttons


        self.add_button = tk.Button(player_controls_frame, text="Add Song", command=self.add_song, width=15,
                                    fg=self.text_color, bg=self.button_bg)
        self.add_button.grid(row=1, column=0, padx=5, pady=5)

        self.remove_button = tk.Button(player_controls_frame, text="Remove Song", command=self.remove_song, width=15,
                                       fg=self.text_color, bg=self.button_bg)
        self.remove_button.grid(row=1, column=1, padx=5, pady=5)

        self.save_button = tk.Button(player_controls_frame, text="Save Playlist", command=self.save_playlist, width=15,
                                     fg=self.text_color, bg=self.button_bg)
        self.save_button.grid(row=1, column=2, padx=5, pady=5)

        self.load_button = tk.Button(player_controls_frame, text="Load Playlist", command=self.load_playlist, width=15,
                                     fg=self.text_color, bg=self.button_bg)
        self.load_button.grid(row=2, column=0, padx=5, pady=5)

        self.shuffle_button = tk.Button(player_controls_frame, text="Shuffle", command=self.shuffle_playlist, width=15,
                                        fg=self.text_color, bg=self.button_bg)
        self.shuffle_button.grid(row=2, column=1, padx=5, pady=5)

        self.display_button = tk.Button(player_controls_frame, text="Refresh", command=self.display_playlist, width=15,
                                        fg=self.text_color, bg=self.button_bg)
        self.display_button.grid(row=2, column=2, padx=5, pady=5)



    def play_song(self):
        self.current_song_label.config(text=f"Playing: {self.playlist.head}")

    def pause_song(self):
        self.current_song_label.config(text="No song playing")

    def next_song(self):
        if self.playlist.head and self.playlist.head.next:
            current_song = self.playlist.head
            self.playlist.head = self.playlist.head.next
            current = self.playlist.head
            while current.next:
                current = current.next
            current.next = current_song
            current_song.next = None
            self.display_playlist()
            self.current_song_label.config(text=f"Playing: {self.playlist.head}")
        else:
            messagebox.showinfo("Next Song", "No next song available")

    def add_song(self):
        title = self.title_entry.get()
        artist = self.artist_entry.get()
        duration = self.duration_entry.get()
        position = self.position_entry.get()
        position = int(position) if position.isdigit() else None
        if title and artist and duration:
            self.playlist.add_song(title, artist, duration, position)
            self.display_playlist()
            self.clear_inputs()
        else:
            messagebox.showwarning("Input Error", "Please fill in all fields")

    def remove_song(self):
        selection = self.playlist_box.curselection()
        if selection:
            song_info = self.playlist_box.get(selection[0])
            title = song_info.split(" by ")[0]
            if self.playlist.remove_song(title):
                messagebox.showinfo("Remove Song", f"{title} has been removed")
                self.display_playlist()
            else:
                messagebox.showwarning("Remove Song", "Failed to remove song")

    def save_playlist(self):
        filename = filedialog.asksaveasfilename(defaultextension=".txt",
                                                filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if filename:
            self.playlist.save_playlist(filename)
            messagebox.showinfo("Save Playlist", f"Playlist saved to {filename}")

    def load_playlist(self):
        filename = filedialog.askopenfilename(defaultextension=".txt",
                                              filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if filename:
            self.playlist.load_playlist(filename)
            self.display_playlist()
            messagebox.showinfo("Load Playlist", f"Playlist loaded from {filename}")

    def shuffle_playlist(self):
        self.playlist.shuffle_playlist()
        self.display_playlist()

    def display_playlist(self):
        self.playlist_box.delete(0, tk.END)
        for song in self.playlist.display_playlist():
            self.playlist_box.insert(tk.END, song)

    def clear_inputs(self):
        self.title_entry.delete(0, tk.END)
        self.artist_entry.delete(0, tk.END)
        self.duration_entry.delete(0, tk.END)
        self.position_entry.delete(0, tk.END)


# Main program
root = tk.Tk()
app = MusicPlayerGUI(root)
root.mainloop()
