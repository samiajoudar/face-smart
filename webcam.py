import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

def open_direction_window():
    direction_window = tk.Toplevel(root)
    direction_window.title("Actions Direction")

    add_button = ttk.Button(direction_window, text="Ajouter Employé", command=open_add_employee_window)
    modify_button = ttk.Button(direction_window, text="Modifier Employé", command=lambda: print("Modifier Employé"))
    delete_button = ttk.Button(direction_window, text="Supprimer Employé", command=lambda: print("Supprimer Employé"))
    view_button = ttk.Button(direction_window, text="Consulter Informations Employé", command=lambda: print("Consulter Informations Employé"))
    filter_dept_button = ttk.Button(direction_window, text="Filtrer Par Département", command=lambda: print("Filtrer Par Département"))
    filter_post_button = ttk.Button(direction_window, text="Filtrer Par Poste", command=lambda: print("Filtrer Par Poste"))
    filter_perf_button = ttk.Button(direction_window, text="Filtrer Par Performances", command=lambda: print("Filtrer Par Performances"))

    add_button.grid(row=0, column=0, padx=10, pady=5, sticky="ew")
    modify_button.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
    delete_button.grid(row=2, column=0, padx=10, pady=5, sticky="ew")
    view_button.grid(row=3, column=0, padx=10, pady=5, sticky="ew")
    filter_dept_button.grid(row=4, column=0, padx=10, pady=5, sticky="ew")
    filter_post_button.grid(row=5, column=0, padx=10, pady=5, sticky="ew")
    filter_perf_button.grid(row=6, column=0, padx=10, pady=5, sticky="ew")


def open_add_employee_window():
    add_employee_window = tk.Toplevel(root)
    add_employee_window.title("Ajouter Employé")

    # Création des labels et des champs de saisie pour le formulaire
    tk.Label(add_employee_window, text="Nom :").grid(row=0, column=0, padx=5, pady=5)
    tk.Label(add_employee_window, text="Prénom :").grid(row=1, column=0, padx=5, pady=5)
    tk.Label(add_employee_window, text="Coordonnées :").grid(row=2, column=0, padx=5, pady=5)
    tk.Label(add_employee_window, text="Département :").grid(row=3, column=0, padx=5, pady=5)
    tk.Label(add_employee_window, text="Poste :").grid(row=4, column=0, padx=5, pady=5)

    nom_entry = tk.Entry(add_employee_window)
    prenom_entry = tk.Entry(add_employee_window)
    coord_entry = tk.Entry(add_employee_window)
    dept_entry = tk.Entry(add_employee_window)
    poste_entry = tk.Entry(add_employee_window)

    nom_entry.grid(row=0, column=1, padx=5, pady=5)
    prenom_entry.grid(row=1, column=1, padx=5, pady=5)
    coord_entry.grid(row=2, column=1, padx=5, pady=5)
    dept_entry.grid(row=3, column=1, padx=5, pady=5)
    poste_entry.grid(row=4, column=1, padx=5, pady=5)

    # Ajouter le bouton Enregistrer
    def save_employee():
        # Ici vous pouvez ajouter le code pour sauvegarder les informations de l'employé
        nom = nom_entry.get()
        prenom = prenom_entry.get()
        coord = coord_entry.get()
        dept = dept_entry.get()
        poste = poste_entry.get()
        print(f"Enregistré: {nom}, {prenom}, {coord}, {dept}, {poste}")
        # Vous pouvez également ajouter la logique pour enregistrer les données dans une base de données ou un fichier

    save_button = ttk.Button(add_employee_window, text="Enregistrer", command=save_employee)
    save_button.grid(row=5, column=0, columnspan=2, padx=5, pady=10, sticky="ew")


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
background_label.lower()  # Envoyer l'image de fond à l'arrière-plan

# Charger le logo en le réduisant avec subsample
logo_img = tk.PhotoImage(file="resources/logo-emsi.png").subsample(3, 3)  # Ajuster le subsample pour changer la taille

# Cadre supérieur pour le logo
top_frame = tk.Frame(root, bg='#001f3f')  # Utilisez une couleur de fond similaire
top_frame.pack(side='top', fill='x')

# Afficher le logo dans le cadre supérieur
logo_label = tk.Label(top_frame, image=logo_img, bg='#001f3f')  # Utilisez la même couleur de fond
logo_label.pack(side='left', padx=10, pady=10)

# Cadres pour le contenu admin et user
admin_frame = tk.Frame(root, bg='#001f3f')  # Utilisez la même couleur de fond
user_frame = tk.Frame(root, bg='#001f3f')  # Utilisez la même couleur de fond

# Contenu pour le cadre administrateur
admin_label = tk.Label(admin_frame, text="Bienvenue, Administrateur", bg='#001f3f', fg='white', font=('Arial', 20))
admin_label.place(relx=0.5, rely=0.6, anchor='center')  # Centre la phrase de bienvenue

# Contenu pour le cadre employé
user_label = tk.Label(user_frame, text="Bienvenue, Employé", bg='#001f3f', fg='white', font=('Arial', 20))
user_label.place(relx=0.5, rely=0.6, anchor='center')  # Centre la phrase de bienvenue

# Cadre pour les boutons de navigation au bas de la fenêtre
button_frame = tk.Frame(root, bg='#001f3f')
button_frame.place(relx=0.5, rely=0.85, anchor='center')  # Positionner au centre vers le bas

admin_button = tk.Button(button_frame, text="Administrateur", command=open_direction_window, bg='green', fg='white', font=('Arial', 12))
admin_button.pack(side='left', padx=20)

user_button = tk.Button(button_frame, text="Employé", command=open_add_employee_window, bg='green', fg='white', font=('Arial', 12))
user_button.pack(side='left', padx=20)

quit_button = tk.Button(button_frame, text="Quitter", command=quit_app, bg='red', fg='white', font=('Arial', 12))
quit_button.pack(side='left', padx=20)



# Afficher le cadre employé par défaut
user_frame.pack(fill='both', expand=True)

root.mainloop()
