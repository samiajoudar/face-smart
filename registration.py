import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import subprocess
import mysql.connector

# Fonction pour basculer entre afficher/masquer le mot de passe
def toggle_password():
    if show_pass_var.get():
        password_entry.config(show="")
    else:
        password_entry.config(show="*")

# Fonction de gestion de la soumission du formulaire
def add():
    feedback_label.config(text="", fg="#a92121")
    pass_value = password_entry.get()

    if len(pass_value) < 8:
        feedback_label.config(text="Password Must Contain 8 Characters.")
        return
    
    lastname = name_entry.get()
    firstname = firstname_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    
    if not lastname or not firstname or not email or not password:
        feedback_label.config(text="All fields are required.", fg="#a92121")
        return

    # Connexion à la base de données
    try:
        print("Connecting to database...")
        conn = mysql.connector.connect(
            host="localhost",  
            user="root",
            password="",  # Remplacez par votre mot de passe MySQL si nécessaire
            database="employee_management"
        )
        cursor = conn.cursor()
        print("Inserting data...")
        cursor.execute("INSERT INTO admin (username, password, firstname, lastname, email) VALUES (%s, %s, %s, %s, %s)", (email, password, firstname, lastname, email))
        conn.commit()
        messagebox.showinfo("Inscription réussie", "Inscription réussie!")
        root.destroy()
        subprocess.Popen(["python", "gestion.py"])
    except mysql.connector.Error as err:
        feedback_label.config(text=f"Erreur: {err}", fg="#a92121")
        print(f"Erreur: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("Database connection closed.")

# Fonction pour ouvrir la page de connexion
def open_login_page():
    root.destroy()  # Fermer la fenêtre actuelle
    import login  # Importer le script de la page de connexion (login.py)

# Création de la fenêtre principale
root = tk.Tk()
root.title("S'enregistrer")

# Fond bleu nuit
background_color = "#001f3f"
root.configure(bg=background_color)

# Cadre pour le formulaire d'inscription
signup_frame = tk.Frame(root, padx=20, pady=20, bg=background_color)
signup_frame.pack()

# Charger et redimensionner l'image du logo
logo_image = Image.open("resources/logo-emsi.png")
logo_image = logo_image.resize((120, 120), Image.Resampling.LANCZOS)
logo_photo = ImageTk.PhotoImage(logo_image)

# Afficher le logo dans le coin supérieur gauche
logo_label = tk.Label(signup_frame, image=logo_photo, bg=background_color)
logo_label.grid(row=0, column=0, pady=10, padx=10, sticky="nw")

# Titre
tk.Label(signup_frame, text="SMART FACE", font=("Arial", 24), bg=background_color, fg="white").grid(row=0, column=1, columnspan=2, pady=10)

# Champ Nom
tk.Label(signup_frame, text="Nom :", bg=background_color, fg="white").grid(row=1, column=0, sticky="w")
name_entry = tk.Entry(signup_frame, width=30)
name_entry.grid(row=1, column=1, columnspan=2, padx=10, pady=10)

# Champ Prénom
tk.Label(signup_frame, text="Prénom :", bg=background_color, fg="white").grid(row=2, column=0, sticky="w")
firstname_entry = tk.Entry(signup_frame, width=30)
firstname_entry.grid(row=2, column=1, columnspan=2, padx=10, pady=10)

# Champ E-mail
tk.Label(signup_frame, text="E-mail :", bg=background_color, fg="white").grid(row=3, column=0, sticky="w")
email_entry = tk.Entry(signup_frame, width=30)
email_entry.grid(row=3, column=1, columnspan=2, padx=10, pady=10)

# Champ Mot de Passe
tk.Label(signup_frame, text="Mot de Passe :", bg=background_color, fg="white").grid(row=4, column=0, sticky="w")
password_entry = tk.Entry(signup_frame, width=30, show="*")
password_entry.grid(row=4, column=1, columnspan=2, padx=10, pady=10)

# Checkbox pour montrer le mot de passe
show_pass_var = tk.BooleanVar()
show_pass_checkbox = tk.Checkbutton(signup_frame, text="Afficher le mot de passe", variable=show_pass_var, command=toggle_password, bg=background_color, fg="white")
show_pass_checkbox.grid(row=5, column=0, columnspan=3, pady=5)

# Label pour les feedbacks
feedback_label = tk.Label(signup_frame, text="", bg=background_color, fg="#a92121")
feedback_label.grid(row=6, column=0, columnspan=3)

# Bouton de connexion
signup_button = tk.Button(signup_frame, text="S'enregistrer", command=add, bg="green", fg="white", width=15)
signup_button.grid(row=7, column=0, columnspan=3, pady=10)

# Lien pour se connecter
login_link = tk.Label(signup_frame, text="Se connecter si vous avez déjà un compte", fg="lightgreen", cursor="hand2", bg=background_color)
login_link.grid(row=8, column=0, columnspan=3, pady=5)
login_link.bind("<Button-1>", lambda e: open_login_page())

root.mainloop()
