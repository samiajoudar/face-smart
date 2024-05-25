import tkinter as tk
from tkinter import messagebox
import subprocess

# Fonction pour ouvrir la page d'inscription
def open_signup_page():
    try:
        subprocess.Popen(["python", "registration.py"])  # Ouvrir le script registration.py
    except FileNotFoundError:
        messagebox.showerror("Erreur", "Le fichier registration.py est introuvable.")

# Fonction pour ouvrir la page de connexion
def open_login_page():
    try:
        subprocess.Popen(["python", "login.py"])  # Ouvrir le script login.py
    except FileNotFoundError:
        messagebox.showerror("Erreur", "Le fichier login.py est introuvable.")

# Création de la fenêtre principale
root = tk.Tk()
root.title("Bienvenue")
root.configure(bg="#001f3f")  # Fond bleu nuit

# Cadre principal pour le contenu
main_frame = tk.Frame(root, padx=20, pady=20, bg="#001f3f")
main_frame.pack(expand=True)

# Titre
title = tk.Label(main_frame, text="Bienvenue chez FACESMART  administration ", font=("Arial", 24), bg="#001f3f", fg="white")
title.pack(pady=10)

# Bouton S'inscrire
signup_button = tk.Button(main_frame, text="S'inscrire", command=open_signup_page, bg="green", fg="white", width=15)
signup_button.pack(pady=10)

# Bouton Se Connecter
login_button = tk.Button(main_frame, text="Se Connecter", command=open_login_page, bg="blue", fg="white", width=15)
login_button.pack(pady=10)

root.mainloop()
