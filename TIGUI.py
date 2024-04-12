import tkinter as tk
from tkinter import ttk
from ImgScriper import *
import threading


class SimpleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ImgScriper")
        # Frame
        frame = ttk.Frame(self.root, padding="10")
        frame.grid(row=0, column=0, sticky="nsew")

        # Text input for URL
        ttk.Label(frame, text="URL:").grid(row=0, column=0, sticky="w")
        self.url_input = ttk.Entry(frame)
        self.url_input.grid(row=0, column=1, sticky="ew")

        # Text input for path
        ttk.Label(frame, text="Path To Save:").grid(row=1, column=0, sticky="w")
        self.path_input = ttk.Entry(frame)
        self.path_input.grid(row=1, column=1, sticky="ew")

        # Checkbox
        self.checked = tk.BooleanVar()
        self.checkbox = ttk.Checkbutton(
            frame, text="Send To Telegram?", variable=self.checked
        )
        self.checkbox.grid(row=2, column=0, columnspan=2, sticky="w")

        # Button
        download_button = ttk.Button(frame, text="Download", command=self.download)
        download_button.grid(row=3, column=0, columnspan=2, sticky="ew")

    def download(self):
        url = self.url_input.get()
        path = self.path_input.get()
        checked = self.checked.get()

        # Perform download logic using the values of url, path, and checked
        threading.Thread(target=start_download(url=url,folder_path=path,save_path=path,send_telegram=checked), args=(url, path, path, checked))


def main():
    root = tk.Tk()
    app = SimpleApp(root)
    root.iconbitmap("./icon.ico")
    root.mainloop()


if __name__ == "__main__":
    main()
