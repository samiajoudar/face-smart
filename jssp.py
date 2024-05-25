import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import subprocess

def open_direction_window():
    try:
        subprocess.Popen(["python", "welcome.py"])
    except FileNotFoundError:
        messagebox.showerror("Erreur", "Le fichier welcome.py est introuvable.")

def open_add_employee_window():
    try:
        subprocess.Popen(["python", "employe.py"])
    except FileNotFoundError:
        messagebox.showerror("Erreur", "Le fichier employe.py est introuvable.")

def show_admin():
    user_frame.pack_forget()
    admin_frame.pack(fill='both', expand=True)

def show_user():
    admin_frame.pack_forget()
    user_frame.pack(fill='both', expand=True)

def quit_app():
    root.quit()

root = tk.Tk()
root.title("Interface Admin/Employé")
root.geometry("800x600")

# Charger l'image de fond
background_image = Image.open("resources/fond.png")
background_photo = ImageTk.PhotoImage(background_image)

# Afficher l'image de fond
background_label = tk.Label(root, image=background_photo)
background_label.place(relwidth=1, relheight=1)
background_label.lower()

# Charger le logo en le réduisant avec subsample
logo_img = tk.PhotoImage(file="resources/logo-emsi.png").subsample(3, 3)

# Cadre supérieur pour le logo
top_frame = tk.Frame(root, bg='#001f3f')
top_frame.pack(side='top', fill='x')

# Afficher le logo dans le cadre supérieur
logo_label = tk.Label(top_frame, image=logo_img, bg='#001f3f')
logo_label.pack(side='left', padx=10, pady=10)

# Cadres pour le contenu admin et user
admin_frame = tk.Frame(root, bg='#001f3f')
user_frame = tk.Frame(root, bg='#001f3f')

# Contenu pour les cadres
welcome_label_admin = tk.Label(admin_frame, text="Welcome There", bg='#001f3f', fg='white', font=('Arial', 40))
welcome_label_admin.place(relx=0.5, rely=0.5, anchor='center')

welcome_label_user = tk.Label(user_frame, text="Welcome There", bg='#001f3f', fg='white', font=('Arial', 40))
welcome_label_user.place(relx=0.5, rely=0.5, anchor='center')

# Cadre pour les boutons de navigation au bas de la fenêtre
button_frame = tk.Frame(root, bg='#001f3f')
button_frame.place(relx=0.5, rely=0.85, anchor='center')

admin_button = tk.Button(button_frame, text="Administration", command=open_direction_window, bg='green', fg='white', font=('Arial', 12))
admin_button.pack(side='left', padx=20)

user_button = tk.Button(button_frame, text="Employé", command=open_add_employee_window, bg='green', fg='white', font=('Arial', 12))
user_button.pack(side='left', padx=20)

quit_button = tk.Button(button_frame, text="Quitter", command=quit_app, bg='red', fg='white', font=('Arial', 12))
quit_button.pack(side='left', padx=20)

# Afficher le cadre employé par défaut
user_frame.pack(fill='both', expand=True)

root.mainloop()
