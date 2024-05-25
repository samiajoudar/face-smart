import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector
import subprocess

# Fonction pour basculer entre afficher/masquer le mot de passe
def toggle_password():
    if show_pass_var.get():
        password_entry.config(show="")
    else:
        password_entry.config(show="*")

# Fonction de gestion de la soumission du formulaire
def submit_form():
    username = email_entry.get()
    password = password_entry.get()

    if not username or not password:
        messagebox.showerror("Erreur de connexion", "Veuillez entrer votre nom d'utilisateur et votre mot de passe.")
        return

    # Connexion à la base de données et vérification des informations d'identification
    try:
        print("Connecting to database...")
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="", 
            database="employee_management"
        )
        cursor = conn.cursor()
        print("Executing query...")
        cursor.execute("SELECT * FROM admin WHERE email = %s AND password = %s", (username, password))
        result = cursor.fetchone()

        if result:
            messagebox.showinfo("Connexion réussie", "Connexion réussie!")
            root.destroy()  # Fermer la fenêtre actuelle
            subprocess.Popen(["python", "gestion.py"])  # Ouvrir le script gestion.py
        else:
            messagebox.showerror("Erreur de connexion", "Nom d'utilisateur ou mot de passe incorrect.")
    
    except mysql.connector.Error as err:
        print(f"Erreur: {err}")
        messagebox.showerror("Erreur de connexion", f"Erreur: {err}")
    
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("Database connection closed.")

# Fonction pour ouvrir la page d'inscription
def open_signup_page():
    root.destroy()  # Fermer la fenêtre actuelle
    subprocess.Popen(["python", "registration.py"])  # Ouvrir le script registration.py

# Création de la fenêtre principale
root = tk.Tk()
root.title("Se connecter")

# Fond bleu nuit
background_color = "#001f3f"
root.configure(bg=background_color)

# Cadre pour le formulaire de connexion
login_frame = tk.Frame(root, padx=20, pady=20, bg=background_color)
login_frame.pack()

# Charger et redimensionner l'image du logo
logo_image = Image.open("resources/logo-emsi.png")
logo_image = logo_image.resize((200, 200), Image.LANCZOS)  # Redimensionner l'image à 200x200 pixels avec Image.LANCZOS
logo_photo = ImageTk.PhotoImage(logo_image)

# Afficher le logo dans le coin supérieur gauche avec un padding ajusté
logo_label = tk.Label(login_frame, image=logo_photo, bg=background_color)
logo_label.grid(row=0, column=0, padx=20, pady=20, sticky="nw")  # sticky="nw" pour aligner le logo en haut à gauche

# Titre
tk.Label(login_frame, text="Face SMART", font=("Arial", 24), bg=background_color, fg="white").grid(row=0, column=1, columnspan=2, pady=10)

# Champ E-mail
tk.Label(login_frame, text="E-mail :", bg=background_color, fg="white").grid(row=1, column=0, sticky="w")
email_entry = tk.Entry(login_frame, width=30)
email_entry.grid(row=1, column=1, columnspan=2, padx=10, pady=10)

# Champ Mot de Passe
tk.Label(login_frame, text="Mot de Passe :", bg=background_color, fg="white").grid(row=2, column=0, sticky="w")
password_entry = tk.Entry(login_frame, width=30, show="*")
password_entry.grid(row=2, column=1, columnspan=2, padx=10, pady=10)

# Checkbox pour montrer le mot de passe
show_pass_var = tk.BooleanVar()
show_pass_checkbox = tk.Checkbutton(login_frame, text="Afficher le mot de passe", variable=show_pass_var, command=toggle_password, bg=background_color, fg="white")
show_pass_checkbox.grid(row=3, column=0, columnspan=3, pady=5)

# Bouton de connexion
login_button = tk.Button(login_frame, text="Connecter", command=submit_form, bg="green", fg="white", width=15)
login_button.grid(row=4, column=0, columnspan=3, pady=10)

# Lien pour s'inscrire
signup_link = tk.Label(login_frame, text="S'inscrire", fg="blue", cursor="hand2", bg=background_color)
signup_link.grid(row=5, column=0, columnspan=3, pady=5)
# bind event to function
signup_link.bind("<Button-1>", lambda e: open_signup_page())

root.mainloop()
