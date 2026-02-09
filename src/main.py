from tkinter import filedialog, messagebox
import threading
import time

import customtkinter as ctk

from core.utils import resource_path
import fast_zip

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class ZipBruteForceGUI:

    def __init__(self, root: ctk.CTk):
        self.root = root
        self.root.title("ZIP Bruteforce")
        self.root.geometry("650x550")
        self.root.resizable(False, False)
        root.iconbitmap(resource_path("assets/icon.ico"))

        self.brute = None
        self.running = False
        self.start_time = 0

        self.setup_ui()
        self.update_stats()

    def setup_ui(self):
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill = "both", expand = True, padx = 20, pady = 20)

        title_label = ctk.CTkLabel(
            main_frame,
            text = "ZIP Password Cracker",
            font = ctk.CTkFont(size = 24, weight = "bold")
        )
        title_label.pack(pady = (10, 20))

        files_frame = ctk.CTkFrame(main_frame)
        files_frame.pack(fill = "x", padx = 10, pady = 10)

        zip_label = ctk.CTkLabel(files_frame, text = "ZIP File:", anchor="w")
        zip_label.grid(row = 0, column = 0, sticky = "w", padx=10, pady=10)

        self.zip_path = ctk.StringVar()
        self.zip_entry = ctk.CTkEntry(
            files_frame,
            textvariable = self.zip_path,
            width = 350,
            placeholder_text = "Select the ZIP file..."
        )
        self.zip_entry.grid(row = 0, column = 1, padx = 10, pady = 10)

        zip_button = ctk.CTkButton(
            files_frame,
            text = "Browse",
            command = self.browse_zip,
            width = 100
        )

        zip_button.grid(row = 0, column = 2, padx = 10, pady = 10)

        wordlist_label = ctk.CTkLabel(files_frame, text = "Wordlist:", anchor = "w")
        wordlist_label.grid(row = 1, column = 0, sticky = "w", padx = 10, pady = 10)

        self.wordlist_path = ctk.StringVar()
        self.wordlist_entry = ctk.CTkEntry(
            files_frame,
            textvariable=self.wordlist_path,
            width = 350,
            placeholder_text = "Select the wordlist..."
        )

        self.wordlist_entry.grid(row = 1, column = 1, padx = 10, pady = 10)

        wordlist_button = ctk.CTkButton(
            files_frame,
            text = "Browse",
            command = self.browse_wordlist,
            width = 100
        )

        wordlist_button.grid(row=1, column=2, padx=10, pady=10)

        stats_frame = ctk.CTkFrame(main_frame)
        stats_frame.pack(fill = "x", padx = 10, pady = 10)

        stats_title = ctk.CTkLabel(
            stats_frame,
            text = "Statistics",
            font = ctk.CTkFont(size = 16, weight = "bold")
        )

        stats_title.pack(pady=(10, 5))

        stats_grid = ctk.CTkFrame(stats_frame, fg_color = "transparent")
        stats_grid.pack(padx = 10, pady = 10)

        self.tries_label = ctk.CTkLabel(
            stats_grid,
            text = "Attempts: 0",
            font = ctk.CTkFont(size = 14)
        )

        self.tries_label.grid(row = 0, column = 0, padx = 20, pady = 5, sticky = "w")

        self.speed_label = ctk.CTkLabel(
            stats_grid,
            text = "Speed: 0 attempts/s",
            font = ctk.CTkFont(size = 14)
        )

        self.speed_label.grid(row = 1, column = 0, padx = 20, pady = 5, sticky = "w")

        self.time_label = ctk.CTkLabel(
            stats_grid,
            text = "Time: 0s",
            font = ctk.CTkFont(size = 14)
        )

        self.time_label.grid(row = 2, column = 0, padx = 20, pady = 5, sticky = "w")

        self.result_label = ctk.CTkLabel(
            main_frame,
            text = "",
            font = ctk.CTkFont(size = 16, weight = "bold"),
            text_color="green"
        )

        self.result_label.pack(pady = 10)

        button_frame = ctk.CTkFrame(main_frame, fg_color = "transparent")
        button_frame.pack(pady = 10)

        self.start_button = ctk.CTkButton(
            button_frame,
            text = "Start",
            command = self.start_bruteforce,
            width = 150,
            height = 40,
            font = ctk.CTkFont(size = 14, weight = "bold"),
            fg_color = "green",
            hover_color = "darkgreen"
        )

        self.start_button.grid(row = 0, column = 0, padx = 10)

        self.stop_button = ctk.CTkButton(
            button_frame,
            text = "Stop",
            command=self.stop_bruteforce,
            width = 150,
            height = 40,
            font = ctk.CTkFont(size = 14, weight = "bold"),
            fg_color = "red",
            hover_color = "darkred",
            state = "disabled"
        )
        self.stop_button.grid(row = 0, column = 1, padx = 10)

    def browse_zip(self):
        filename = filedialog.askopenfilename(
            title = "Select ZIP file",
            filetypes = [("ZIP files", "*.zip"), ("All files", "*.*")]
        )

        if filename:
            self.zip_path.set(filename)

    def browse_wordlist(self):
        filename = filedialog.askopenfilename(
            title = "Select wordlist",
            filetypes = [("Text files", "*.txt"), ("All files", "*.*")]
        )

        if filename:
            self.wordlist_path.set(filename)

    def update_stats(self):
        if self.running and self.brute:
            tries = self.brute.get_tries()
            elapsed = time.time() - self.start_time
            speed = tries / elapsed if elapsed > 0 else 0

            self.tries_label.configure(text = f"Attempts: {tries:,}")
            self.speed_label.configure(text = f"Speed: {speed:,.0f} attempts/s")
            self.time_label.configure(text = f"Time: {elapsed:.1f}s")

        self.root.after(100, self.update_stats)

    def bruteforce_thread(self):
        try:
            result = self.brute.crack(
                zip_path = self.zip_path.get(),
                wordlist_path = self.wordlist_path.get(),
                batch_size = 50000
            )

            self.root.after(0, lambda: self.handle_completion(result, None))

        except Exception as e:
            self.root.after(0, lambda: self.handle_completion(None, str(e)))

    def handle_completion(self, result, error):
        self.running = False

        if error:
            self.result_label.configure(text = "Process error", text_color = "red")
            messagebox.showerror("Error", error)

        elif result:
            self.result_label.configure(text = f"Password: {result}", text_color = "green")
            messagebox.showinfo("Success", f"Password found:\n\n{result}")

        else:
            self.result_label.configure(text = "Password not found", text_color = "orange")
            messagebox.showwarning("No results", "The password was not found in the wordlist")

        self.start_button.configure(state = "normal")
        self.stop_button.configure(state = "disabled")

    def start_bruteforce(self):
        if not self.zip_path.get() or not self.wordlist_path.get():
            messagebox.showerror(
                "Error",
                "Please select both the ZIP file and the wordlist"
            )

            return

        self.brute = fast_zip.BruteForce(src=self.wordlist_path.get())
        self.running = True
        self.start_time = time.time()

        self.result_label.configure(text = "")
        self.start_button.configure(state = "disabled")
        self.stop_button.configure(state = "normal")

        self.tries_label.configure(text = "Attempts: 0")
        self.speed_label.configure(text = "Speed: 0 attempts/s")
        self.time_label.configure(text = "Time: 0s")

        thread = threading.Thread(target = self.bruteforce_thread, daemon = True)
        thread.start()

    def stop_bruteforce(self):
        if self.running:
            self.running = False

            self.result_label.configure(
                text = "Process stopped by user",
                text_color = "orange"
            )

            self.start_button.configure(state = "normal")
            self.stop_button.configure(state = "disabled")

if __name__ == "__main__":
    root = ctk.CTk()
    app = ZipBruteForceGUI(root)
    root.mainloop()
