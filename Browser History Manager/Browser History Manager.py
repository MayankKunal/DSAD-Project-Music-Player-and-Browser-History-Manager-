import tkinter as tk
from tkinter import messagebox


class Page:
    def __init__(self, url):
        self.url = url
        self.next = None
        self.prev = None

    def __str__(self):
        return self.url


class History:
    def __init__(self):
        self.current = None
        self.head = None

    def visit_page(self, url):
        new_page = Page(url)
        if self.current is None:  # First page visit
            self.head = new_page
        else:
            self.current.next = None  # Remove forward history
            new_page.prev = self.current
        self.current = new_page

    def go_back(self):
        if self.current and self.current.prev:
            self.current = self.current.prev
            return self.current.url
        else:
            return None

    def go_forward(self):
        if self.current and self.current.next:
            self.current = self.current.next
            return self.current.url
        else:
            return None

    def view_history(self):
        pages = []
        current = self.head
        while current:
            pages.append((current.url, current == self.current))
            current = current.next
        return pages

    def clear_history(self):
        self.current = None
        self.head = None


class BrowserHistoryManager:
    def __init__(self, root):
        self.history = History()

        # Set up root window with dark theme
        self.root = root
        self.root.title("Browser History Manager")
        self.root.geometry("500x400")
        self.root.config(bg="#2b2b2b")

        self.create_widgets()

    def create_widgets(self):
        # Entry for URL input
        self.url_entry = tk.Entry(self.root, width=50, font=("Helvetica", 12), bg="#4e4e4e", fg="#ffffff")
        self.url_entry.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 5))

        # Visit button
        self.visit_button = tk.Button(self.root, text="Visit Page", command=self.visit_page, bg="#333333",
                                      fg="#ffffff", font=("Helvetica", 10, "bold"))
        self.visit_button.grid(row=0, column=2, padx=10, pady=(10, 5))

        # Back and Forward buttons
        self.back_button = tk.Button(self.root, text="Back", command=self.go_back, bg="#333333",
                                     fg="#ffffff", font=("Helvetica", 10, "bold"))
        self.back_button.grid(row=1, column=0, padx=10, pady=5)

        self.forward_button = tk.Button(self.root, text="Forward", command=self.go_forward, bg="#333333",
                                        fg="#ffffff", font=("Helvetica", 10, "bold"))
        self.forward_button.grid(row=1, column=1, padx=10, pady=5)

        # Clear History button
        self.clear_button = tk.Button(self.root, text="Clear History", command=self.clear_history, bg="#333333",
                                      fg="#ffffff", font=("Helvetica", 10, "bold"))
        self.clear_button.grid(row=1, column=2, padx=10, pady=5)

        # History Display Box (Listbox)
        self.history_listbox = tk.Listbox(self.root, width=50, height=15, bg="#4e4e4e", fg="#ffffff",
                                          selectbackground="#1f77b4", font=("Helvetica", 10))
        self.history_listbox.grid(row=2, column=0, columnspan=3, padx=10, pady=(10, 10))

    def visit_page(self):
        url = self.url_entry.get().strip()
        if url:
            self.history.visit_page(url)
            self.update_history_listbox()
            self.url_entry.delete(0, tk.END)

    def go_back(self):
        url = self.history.go_back()
        if url:
            self.update_history_listbox()
        else:
            messagebox.showinfo("Navigation", "Already at the first page in history.")

    def go_forward(self):
        url = self.history.go_forward()
        if url:
            self.update_history_listbox()
        else:
            messagebox.showinfo("Navigation", "Already at the most recent page.")

    def clear_history(self):
        self.history.clear_history()
        self.update_history_listbox()
        messagebox.showinfo("History", "History cleared.")

    def update_history_listbox(self):
        self.history_listbox.delete(0, tk.END)
        for url, is_current in self.history.view_history():
            display_text = f"{url} {'<- Current' if is_current else ''}"
            self.history_listbox.insert(tk.END, display_text)


# Run the Application
root = tk.Tk()
app = BrowserHistoryManager(root)
root.mainloop()
