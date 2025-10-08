import customtkinter as ctk
import tkinter as tk
from tkinter import simpledialog, messagebox
import base64

DAYS = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
HOURS = [f"{h}:00" for h in range(24)]

class UserManager:
    def __init__(self):
        self.users = {}  # username -> {"password": ..., "calendar": ...}

    def encrypt(self, password):
        return base64.b64encode(password.encode("utf-8")).decode("utf-8")

    def decrypt(self, enc_password):
        return base64.b64decode(enc_password.encode("utf-8")).decode("utf-8")

    def add_user(self, username, password):
        self.users[username] = {
            "password": self.encrypt(password),
            "calendar": [["Kein Termin!"] * 24 for _ in range(7)]
        }

    def user_exists(self, username):
        return username in self.users

    def check_password(self, username, password):
        enc_pw = self.users.get(username, {}).get("password")
        if enc_pw is None:
            return False
        return self.decrypt(enc_pw) == password

    def get_calendar(self, username):
        return self.users[username]["calendar"]

    def get_usernames(self):
        return list(self.users.keys())

class UserLoginDialog(simpledialog.Dialog):
    def __init__(self, parent, user_manager):
        self.user_manager = user_manager
        self.selected_user = ctk.StringVar()
        super().__init__(parent, "Benutzeranmeldung")

    def body(self, frame):
        usernames = self.user_manager.get_usernames()
        ctk.CTkLabel(frame, text="Benutzername:").grid(row=0, column=0)
        if usernames:
            self.username_menu = ctk.CTkOptionMenu(frame, variable=self.selected_user, values=usernames)
            self.selected_user.set(usernames[0])
            self.username_menu.grid(row=0, column=1)
            self.username_entry = None
        else:
            self.username_entry = ctk.CTkEntry(frame)
            self.username_entry.grid(row=0, column=1)
            self.selected_user.set("")
        ctk.CTkLabel(frame, text="Passwort:").grid(row=1, column=0)
        self.password_entry = ctk.CTkEntry(frame, show="*")
        self.password_entry.grid(row=1, column=1)

    def apply(self):
        usernames = self.user_manager.get_usernames()
        if usernames:
            username = self.selected_user.get().strip()
        else:
            username = self.username_entry.get().strip()
        password = self.password_entry.get()
        if not username or not password:
            messagebox.showerror("Fehler", "Benutzername und Passwort dürfen nicht leer sein!")
            self.result = None
            return
        if self.user_manager.user_exists(username):
            if self.user_manager.check_password(username, password):
                self.result = username
            else:
                messagebox.showerror("Fehler", "Falsches Passwort!")
                self.result = None
        else:
            if messagebox.askyesno("Registrieren", f"Benutzer '{username}' existiert nicht. Registrieren?"):
                self.user_manager.add_user(username, password)
                self.result = username
            else:
                self.result = None

class Terminkalender:
    def __init__(self, master):
        self.master = master
        self.master.title("Terminkalender (Multi-User)")
        ctk.set_appearance_mode("system")  # "dark" or "light" for forced mode
        ctk.set_default_color_theme("blue")
        self.user_manager = UserManager()
        self.users = {}  # username -> calendar data
        self.current_user = None
        self.ter = None
        self.login()
        self.create_widgets()

    def login(self):
        dialog = UserLoginDialog(self.master, self.user_manager)
        self.current_user = dialog.result
        if self.current_user:
            self.ter = self.user_manager.get_calendar(self.current_user)
        else:
            self.master.quit()

    def switch_user(self):
        dialog = UserLoginDialog(self.master, self.user_manager)
        new_user = dialog.result
        if new_user and new_user != self.current_user:
            self.current_user = new_user
            self.ter = self.user_manager.get_calendar(self.current_user)
            self.user_label.configure(text=f"Benutzer: {self.current_user}")  # changed
            self.show_termin()

    def add_user(self):
        # Dialog for new user registration
        class AddUserDialog(simpledialog.Dialog):
            def __init__(self, parent, user_manager):
                self.user_manager = user_manager
                super().__init__(parent, "Neuen Benutzer hinzufügen")

            def body(self, frame):
                ctk.CTkLabel(frame, text="Benutzername:").grid(row=0, column=0)
                self.username_entry = ctk.CTkEntry(frame)
                self.username_entry.grid(row=0, column=1)
                ctk.CTkLabel(frame, text="Passwort:").grid(row=1, column=0)
                self.password_entry = ctk.CTkEntry(frame, show="*")
                self.password_entry.grid(row=1, column=1)

            def apply(self):
                username = self.username_entry.get().strip()
                password = self.password_entry.get()
                if not username or not password:
                    messagebox.showerror("Fehler", "Benutzername und Passwort dürfen nicht leer sein!")
                    self.result = None
                    return
                if self.user_manager.user_exists(username):
                    messagebox.showerror("Fehler", "Benutzer existiert bereits!")
                    self.result = None
                else:
                    self.user_manager.add_user(username, password)
                    messagebox.showinfo("Erfolg", f"Benutzer '{username}' wurde hinzugefügt.")
                    self.result = username

        dialog = AddUserDialog(self.master, self.user_manager)
        # Optionally, switch to new user after adding
        if dialog.result:
            self.current_user = dialog.result
            self.ter = self.user_manager.get_calendar(self.current_user)
            self.user_label.configure(text=f"Benutzer: {self.current_user}")  # changed
            self.show_termin()

    def create_widgets(self):
        self.day_var = ctk.StringVar(value=DAYS[0])
        self.hour_var = ctk.StringVar(value=HOURS[0])

        main_frame = ctk.CTkFrame(self.master, corner_radius=15)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        title_label = ctk.CTkLabel(main_frame, text="Terminkalender", font=ctk.CTkFont(size=20, weight="bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))

        user_frame = ctk.CTkFrame(main_frame, corner_radius=10)
        user_frame.grid(row=1, column=0, columnspan=3, sticky="ew", pady=(0, 10))
        user_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self.user_label = ctk.CTkLabel(user_frame, text=f"Benutzer: {self.current_user}", font=ctk.CTkFont(size=12, weight="bold"))
        self.user_label.grid(row=0, column=0, sticky="w", padx=2, pady=2)
        ctk.CTkButton(user_frame, text="Benutzer wechseln", command=self.switch_user).grid(row=0, column=1, sticky="ew", padx=2, pady=2)
        ctk.CTkButton(user_frame, text="Benutzer hinzufügen", command=self.add_user).grid(row=0, column=2, sticky="ew", padx=2, pady=2)

        cal_frame = ctk.CTkFrame(main_frame, corner_radius=10)
        cal_frame.grid(row=2, column=0, columnspan=3, sticky="ew", pady=(0, 10))
        cal_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(cal_frame, text="Tag:").grid(row=0, column=0, sticky="w", padx=2, pady=2)
        self.day_menu = ctk.CTkOptionMenu(cal_frame, variable=self.day_var, values=DAYS)
        self.day_menu.grid(row=0, column=1, sticky="ew", padx=2, pady=2)

        ctk.CTkLabel(cal_frame, text="Stunde:").grid(row=1, column=0, sticky="w", padx=2, pady=2)
        self.hour_menu = ctk.CTkOptionMenu(cal_frame, variable=self.hour_var, values=HOURS)
        self.hour_menu.grid(row=1, column=1, sticky="ew", padx=2, pady=2)

        btn_frame = ctk.CTkFrame(main_frame, corner_radius=10)
        btn_frame.grid(row=3, column=0, columnspan=3, sticky="ew", pady=(0, 10))
        btn_frame.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkButton(btn_frame, text="Ansehen", command=self.show_termin, width=120).grid(row=0, column=0, sticky="ew", padx=2, pady=2)
        ctk.CTkButton(btn_frame, text="Bearbeiten", command=self.edit_termin, width=120).grid(row=0, column=1, sticky="ew", padx=2, pady=2)
        ctk.CTkButton(btn_frame, text="Löschen", command=self.delete_termin, width=120).grid(row=1, column=0, sticky="ew", padx=2, pady=2)
        ctk.CTkButton(btn_frame, text="Alle Termine löschen", command=self.clear_day, width=120).grid(row=1, column=1, sticky="ew", padx=2, pady=2)
        ctk.CTkButton(btn_frame, text="Beenden", command=self.master.quit, width=250).grid(row=2, column=0, columnspan=2, sticky="ew", padx=2, pady=2)

        display_frame = ctk.CTkFrame(main_frame, corner_radius=10)
        display_frame.grid(row=4, column=0, columnspan=3, sticky="nsew")
        main_frame.grid_rowconfigure(4, weight=1)
        main_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self.display = ctk.CTkTextbox(display_frame, width=500, height=250, state="disabled", wrap="word")
        self.display.grid(row=0, column=0, sticky="nsew")
        display_frame.grid_rowconfigure(0, weight=1)
        display_frame.grid_columnconfigure(0, weight=1)

        self.show_termin()

    def get_indices(self):
        day_idx = DAYS.index(self.day_var.get())
        hour_idx = HOURS.index(self.hour_var.get())
        return day_idx, hour_idx

    def show_termin(self):
        day_idx, _ = self.get_indices()
        self.display.configure(state=tk.NORMAL)  # changed
        self.display.delete("1.0", tk.END)
        self.display.insert(tk.END, f"{DAYS[day_idx]} ({self.current_user}):\n")
        for h, termin in enumerate(self.ter[day_idx]):
            self.display.insert(tk.END, f"{h}:00 - {termin}\n")
        self.display.configure(state=tk.DISABLED)  # changed

    def edit_termin(self):
        day_idx, hour_idx = self.get_indices()
        termin = simpledialog.askstring("Termin bearbeiten", "Beschreibung des Termins:")
        if termin is not None:
            self.ter[day_idx][hour_idx] = termin
            self.show_termin()

    def delete_termin(self):
        day_idx, hour_idx = self.get_indices()
        self.ter[day_idx][hour_idx] = "Kein Termin!"
        self.show_termin()

    def clear_day(self):
        day_idx, _ = self.get_indices()
        self.ter[day_idx] = ["Kein Termin!"] * 24
        self.show_termin()

if __name__ == "__main__":
    root = ctk.CTk()
    app = Terminkalender(root)
    root.mainloop()