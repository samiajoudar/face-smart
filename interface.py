import tkinter as tk
from tkinter import ttk


def open_direction_window():
    direction_window = tk.Toplevel(root)
    direction_window.title("Actions Direction")

    # Création des boutons pour les différentes actions
    add_button = ttk.Button(direction_window, text="Ajouter Employé", command=open_add_employee_window)
    modify_button = ttk.Button(direction_window, text="Modifier Employé", command=lambda: print("Modifier Employé"))
    delete_button = ttk.Button(direction_window, text="Supprimer Employé", command=lambda: print("Supprimer Employé"))
    view_button = ttk.Button(direction_window, text="Consulter Informations Employé", command=lambda: print("Consulter Informations Employé"))
    filter_dept_button = ttk.Button(direction_window, text="Filtrer Par Département", command=lambda: print("Filtrer Par Département"))
    filter_post_button = ttk.Button(direction_window, text="Filtrer Par Poste", command=lambda: print("Filtrer Par Poste"))
    filter_perf_button = ttk.Button(direction_window, text="Filtrer Par Performances", command=lambda: print("Filtrer Par Performances"))

    # Placement des boutons dans la fenêtre
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

#Création de la fenêtre principale
root = tk.Tk()
root.title("FaceSmart - Gestion des Employés")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

canvas = tk.Canvas(root, width=screen_width, height=screen_height)
canvas.pack(fill="both", expand=True)

background_image = tk.PhotoImage(file="resources/fond.png")
canvas.create_image(0, 0, anchor="nw", image=background_image)

logo_img = tk.PhotoImage(file="resources/logo-emsi.png").subsample(2, 2)
logo_label = tk.Label(canvas, image=logo_img)
logo_label.place(relx=0.5, rely=0.1, anchor="n")

style = ttk.Style()
style.map("Red.TButton",
          background=[('active', 'red'), ('pressed', '!disabled', 'red')],
          foreground=[('!active', 'red'), ('pressed', 'red')])

direction_button = ttk.Button(canvas, text="Administation", style="Red.TButton", command=open_direction_window)
employer_button = ttk.Button(canvas, text="Employé", command=open_add_employee_window)
exit_button = ttk.Button(canvas, text="Quitter", command=root.quit)

canvas.create_window(screen_width * 0.25, screen_height * 0.8, anchor="nw", window=direction_button)
canvas.create_window(screen_width * 0.5, screen_height * 0.8, anchor="nw", window=employer_button)
canvas.create_window(screen_width * 0.75, screen_height * 0.8, anchor="nw", window=exit_button)

root.mainloop()
