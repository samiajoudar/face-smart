import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
import subprocess


def open_add_employee_window():
    global add_employee_window
    add_employee_window = tk.Toplevel(root)
    add_employee_window.title("Ajouter Employé")
    add_employee_window.configure(bg="#001f3f")  # Définir le fond en bleu nuit

    tk.Label(add_employee_window, text="ID :", bg="#001f3f", fg="white").grid(row=0, column=0, padx=5, pady=5)
    tk.Label(add_employee_window, text="Nom :", bg="#001f3f", fg="white").grid(row=1, column=0, padx=5, pady=5)
    tk.Label(add_employee_window, text="Prénom :", bg="#001f3f", fg="white").grid(row=2, column=0, padx=5, pady=5)
    tk.Label(add_employee_window, text="Poste :", bg="#001f3f", fg="white").grid(row=5, column=0, padx=5, pady=5)
    tk.Label(add_employee_window, text="Département :", bg="#001f3f", fg="white").grid(row=6, column=0, padx=5, pady=5)

    id_entry = tk.Entry(add_employee_window)
    nom_entry = tk.Entry(add_employee_window)
    prenom_entry = tk.Entry(add_employee_window)
    poste_entry = tk.Entry(add_employee_window)
    departement_entry = tk.Entry(add_employee_window)

    id_entry.grid(row=0, column=1, padx=5, pady=5)
    nom_entry.grid(row=1, column=1, padx=5, pady=5)
    prenom_entry.grid(row=2, column=1, padx=5, pady=5)
    poste_entry.grid(row=5, column=1, padx=5, pady=5)
    departement_entry.grid(row=6, column=1, padx=5, pady=5)

    # Bouton "Ajouter"
    add_button = tk.Button(add_employee_window, text="Ajouter", command=lambda: add_employee(id_entry.get(), nom_entry.get(), prenom_entry.get(), poste_entry.get(), departement_entry.get()), bg="green", fg="white")
    add_button.grid(row=7, column=0, columnspan=2, pady=10)

def add_employee(id, nom, prenom, poste, departement):
    try:
        # Connexion à la base de données
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="", 
            database="employee_management"
        )
        if conn.is_connected():
            cursor = conn.cursor()

            # Requête pour insérer un nouvel employé
            query = """
            INSERT INTO employees (id, nom, prenom, poste, departement)
            VALUES (%s, %s, %s, %s, %s)
            """
            values = (id, nom, prenom, poste, departement)
            
            cursor.execute(query, values)
            conn.commit()

            messagebox.showinfo("Succès", "L'employé a été ajouté avec succès!")
            add_employee_window.destroy()  # Ferme uniquement la fenêtre d'ajout d'employé
    
    except Error as e:
        messagebox.showerror("Erreur", f"Erreur: {e}")
    
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def open_modify_employee_window():
    modify_employee_window = tk.Toplevel(root)
    modify_employee_window.title("Modifier Employé")
    modify_employee_window.configure(bg="#001f3f")  # Définir le fond en bleu nuit
    tk.Label(modify_employee_window, text="ID de l'employé à modifier :", bg="#001f3f", fg="white").grid(row=0,column=0,padx=5, pady=5)
    id_entry = tk.Entry(modify_employee_window)
    id_entry.grid(row=0, column=1, padx=5, pady=5)
    fetch_button = tk.Button(modify_employee_window, text="Rechercher", command=lambda: fetch_employee_data(id_entry.get(), modify_employee_window), bg="green",fg="white")
    fetch_button.grid(row=1, column=0, columnspan=2, pady=10)
    
def fetch_employee_data_from_database(employee_id):
    try:
        conn = mysql.connector.connect(
            host="localhost",  
            user="root",
            password="",  
            database="employee_management"
        )
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM employees WHERE id = %s", (employee_id,))
        employee = cursor.fetchone()
        cursor.close()
        conn.close()
        return employee
    except mysql.connector.Error as err:
        print(f"Erreur lors de la récupération des données de l'employé : {err}")
        return None
 
def fetch_employee_data(employee_id, window):
    employee = fetch_employee_data_from_database(employee_id)
    if employee:
        tk.Label(window, text="Nom :", bg="#001f3f", fg="white").grid(row=2, column=0, padx=5, pady=5)
        tk.Label(window, text="Prénom :", bg="#001f3f", fg="white").grid(row=3, column=0, padx=5, pady=5)
        tk.Label(window, text="Poste :", bg="#001f3f", fg="white").grid(row=6, column=0, padx=5, pady=5)
        tk.Label(window, text="Département :", bg="#001f3f", fg="white").grid(row=7, column=0, padx=5, pady=5)
        nom_entry = tk.Entry(window)
        prenom_entry = tk.Entry(window)
        poste_entry = tk.Entry(window)
        departement_entry = tk.Entry(window)
        nom_entry.grid(row=2, column=1, padx=5, pady=5)
        prenom_entry.grid(row=3, column=1, padx=5, pady=5)
        poste_entry.grid(row=6, column=1, padx=5, pady=5)
        departement_entry.grid(row=7, column=1, padx=5, pady=5)
        nom_entry.insert(0, employee["nom"])
        prenom_entry.insert(0, employee["prenom"])
        poste_entry.insert(0, employee["poste"])
        departement_entry.insert(0, employee["departement"])
        update_button = tk.Button(window, text="Mettre à jour", command=lambda: update_employee(employee["id"], nom_entry.get(), prenom_entry.get(), poste_entry.get(), departement_entry.get()), bg="green", fg="white")
        update_button.grid(row=8, column=0, columnspan=2, pady=10)
    else:
        messagebox.showerror("Erreur", f"L'employé avec l'ID {employee_id} est introuvable.")

def update_employee(employee_id, nom, prenom, poste, departement):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  
            database="employee_management"
        )
        cursor = conn.cursor()

        # Requête SQL pour mettre à jour les informations de l'employé
        update_query = "UPDATE employees SET nom = %s, prenom = %s, poste = %s, departement = %s WHERE id = %s"
        cursor.execute(update_query, (nom, prenom, poste, departement, employee_id))

        conn.commit()
        cursor.close()
        conn.close()

        messagebox.showinfo("Succès", "Les informations de l'employé ont été mises à jour avec succès.")
    except mysql.connector.Error as err:
        messagebox.showerror("Erreur", f"Erreur lors de la mise à jour des informations de l'employé : {err}")
    
def open_delete_employee_window():
    global delete_employee_window  # Indiquer que vous utilisez la variable globale
    delete_employee_window = tk.Toplevel(root)
    delete_employee_window.title("Supprimer Employé")
    delete_employee_window.configure(bg="#001f3f")  # Définir le fond en bleu nuit
    tk.Label(delete_employee_window, text="ID de l'employé à supprimer :", bg="#001f3f", fg="white").grid(row=0, column=0, padx=5, pady=5)
    id_entry = tk.Entry(delete_employee_window)
    id_entry.grid(row=0, column=1, padx=5, pady=5)
    delete_button = tk.Button(delete_employee_window, text="Supprimer", command=lambda: delete_employee(id_entry.get()), bg="red", fg="white")
    delete_button.grid(row=1, column=0, columnspan=2, pady=10)

def delete_employee(id):
    try:
        # Connexion à la base de données
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="employee_management"
        )
        cursor = conn.cursor()

        # Exécution de la requête SQL DELETE pour supprimer l'employé avec l'ID spécifié
        cursor.execute("DELETE FROM employees WHERE id = %s", (id,))
        conn.commit()

        # Afficher un message de succès
        messagebox.showinfo("Suppression réussie", f"L'employé avec l'ID {id} a été supprimé avec succès.")
        delete_employee_window.destroy()
    except mysql.connector.Error as err:
        # En cas d'erreur, afficher un message d'erreur
        messagebox.showerror("Erreur de suppression", f"Erreur lors de la suppression de l'employé : {err}")
    finally:
        # Fermer le curseur et la connexion à la base de données
        if conn.is_connected():
            cursor.close()
            conn.close()

def open_consult_employee_window():
    consult_employee_window = tk.Toplevel(root)
    consult_employee_window.title("Consulter Employés")
    consult_employee_window.configure(bg="#001f3f")  # Définir le fond en bleu nuit

    # Création d'une frame pour organiser les données des employés
    frame = tk.Frame(consult_employee_window, bg="#001f3f")
    frame.pack(padx=20, pady=20)

    # Labels pour les titres des colonnes
    tk.Label(frame, text="ID", bg="#001f3f", fg="white", padx=10, pady=5).grid(row=0, column=0, sticky="w")
    tk.Label(frame, text="Nom", bg="#001f3f", fg="white", padx=10, pady=5).grid(row=0, column=1, sticky="w")
    tk.Label(frame, text="Prénom", bg="#001f3f", fg="white", padx=10, pady=5).grid(row=0, column=2, sticky="w")
    tk.Label(frame, text="Poste", bg="#001f3f", fg="white", padx=10, pady=5).grid(row=0, column=5, sticky="w")
    tk.Label(frame, text="Département", bg="#001f3f", fg="white", padx=10, pady=5).grid(row=0, column=6, sticky="w")

    # Récupérer les données des employés depuis la base de données et les afficher dans la table
    employees_data = fetch_employees_data_from_database()
    if employees_data:
        for idx, employee in enumerate(employees_data, start=1):
            tk.Label(frame, text=employee["id"], bg="#001f3f", fg="white", padx=10, pady=5).grid(row=idx, column=0, sticky="w")
            tk.Label(frame, text=employee["nom"], bg="#001f3f", fg="white", padx=10, pady=5).grid(row=idx, column=1, sticky="w")
            tk.Label(frame, text=employee["prenom"], bg="#001f3f", fg="white", padx=10, pady=5).grid(row=idx, column=2, sticky="w")
            tk.Label(frame, text=employee["poste"], bg="#001f3f", fg="white", padx=10, pady=5).grid(row=idx, column=5, sticky="w")
            tk.Label(frame, text=employee["departement"], bg="#001f3f", fg="white", padx=10, pady=5).grid(row=idx, column=6, sticky="w")
    else:
        tk.Label(frame, text="Aucun employé trouvé", bg="#001f3f", fg="white", padx=10, pady=5).grid(row=1, column=0, columnspan=7)

def fetch_employees_data_from_database():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  
            database="employee_management"
        )
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM employees")
        employees_data = cursor.fetchall()
        cursor.close()
        conn.close()
        return employees_data
    except mysql.connector.Error as err:
        print(f"Erreur lors de la récupération des données des employés : {err}")
        return None

def open_filter_department_window():
    # Fonction pour ouvrir la fenêtre de filtrage par département
    filter_department_window = tk.Toplevel(root)
    filter_department_window.title("Filtrer par Département")
    filter_department_window.configure(bg="#001f3f")

    tk.Label(filter_department_window, text="Département :", bg="#001f3f", fg="white").grid(row=0, column=0, padx=5, pady=5)

    department_entry = tk.Entry(filter_department_window)
    department_entry.grid(row=0, column=1, padx=5, pady=5)

    # Bouton "Filtrer"
    filter_button = tk.Button(filter_department_window, text="Filtrer", command=lambda: filter_employees_by_department(department_entry.get(), filter_department_window), bg="green", fg="white")
    filter_button.grid(row=1, column=0, columnspan=2, pady=10)

def filter_employees_by_department(department, filter_department_window):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  
            database="employee_management"
        )
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM employees WHERE departement = %s", (department,))
        rows = cursor.fetchall()
        conn.close()

        # Création d'une nouvelle fenêtre pour afficher les résultats
        result_window = tk.Toplevel(filter_department_window)
        result_window.title("Résultats du Filtrage")
        result_window.configure(bg="#001f3f")

        if rows:
            for idx, employee in enumerate(rows, start=1):
                tk.Label(result_window, text=f"ID: {employee['id']}", bg="#001f3f", fg="white").grid(row=idx, column=0, padx=5, pady=5, sticky="w")
                tk.Label(result_window, text=f"Nom: {employee['nom']}", bg="#001f3f", fg="white").grid(row=idx, column=1, padx=5, pady=5, sticky="w")
                tk.Label(result_window, text=f"Prénom: {employee['prenom']}", bg="#001f3f", fg="white").grid(row=idx, column=2, padx=5, pady=5, sticky="w")
                tk.Label(result_window, text=f"Poste: {employee['poste']}", bg="#001f3f", fg="white").grid(row=idx, column=3, padx=5, pady=5, sticky="w")
                tk.Label(result_window, text=f"Département: {employee['departement']}", bg="#001f3f", fg="white").grid(row=idx, column=4, padx=5, pady=5, sticky="w")
        else:
            tk.Label(result_window, text="Aucun employé trouvé pour ce département.", bg="#001f3f", fg="white").grid(row=1, column=0, padx=5, pady=5)

    except mysql.connector.Error as err:
        print(f"Erreur lors de la connexion à la base de données : {err}")

def open_filter_position_window():
    # Fonction pour ouvrir la fenêtre de filtrage par poste
    filter_position_window = tk.Toplevel(root)
    filter_position_window.title("Filtrer par Poste")
    filter_position_window.configure(bg="#001f3f")

    tk.Label(filter_position_window, text="Poste :", bg="#001f3f", fg="white").grid(row=0, column=0, padx=5, pady=5)

    position_entry = tk.Entry(filter_position_window)
    position_entry.grid(row=0, column=1, padx=5, pady=5)

    # Bouton "Filtrer"
    filter_button = tk.Button(filter_position_window, text="Filtrer", command=lambda: filter_employees_by_position(position_entry.get(), filter_position_window), bg="green", fg="white")
    filter_button.grid(row=1, column=0, columnspan=2, pady=10)

def filter_employees_by_position(position, filter_position_window):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  
            database="employee_management"
        )
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM employees WHERE poste = %s", (position,))
        rows = cursor.fetchall()
        conn.close()

        # Création d'une nouvelle fenêtre pour afficher les résultats
        result_window = tk.Toplevel(filter_position_window)
        result_window.title("Résultats du Filtrage par Poste")
        result_window.configure(bg="#001f3f")

        if rows:
            for idx, employee in enumerate(rows, start=1):
                tk.Label(result_window, text=f"ID: {employee['id']}", bg="#001f3f", fg="white").grid(row=idx, column=0, padx=5, pady=5, sticky="w")
                tk.Label(result_window, text=f"Nom: {employee['nom']}", bg="#001f3f", fg="white").grid(row=idx, column=1, padx=5, pady=5, sticky="w")
                tk.Label(result_window, text=f"Prénom: {employee['prenom']}", bg="#001f3f", fg="white").grid(row=idx, column=2, padx=5, pady=5, sticky="w")
                tk.Label(result_window, text=f"Poste: {employee['poste']}", bg="#001f3f", fg="white").grid(row=idx, column=3, padx=5, pady=5, sticky="w")
                tk.Label(result_window, text=f"Département: {employee['departement']}", bg="#001f3f", fg="white").grid(row=idx, column=4, padx=5, pady=5, sticky="w")
        else:
            tk.Label(result_window, text="Aucun employé trouvé pour ce poste.", bg="#001f3f", fg="white").grid(row=1, column=0, padx=5, pady=5)

    except mysql.connector.Error as err:
        print(f"Erreur lors de la connexion à la base de données : {err}")



root = tk.Tk()
root.title("Droit Administrateur")
root.geometry("800x600")

# Fond bleu nuit
background_color = "#001f3f"
root.configure(bg=background_color)

# Libellé "Droit Administrateur"
admin_label = tk.Label(root, text="Droit Administrateur", bg=background_color, fg="white", font=("Arial", 20))
admin_label.pack(pady=10)

# Boutons pour les actions d'administration
add_button = tk.Button(root, text="Ajouter Employé", command=open_add_employee_window, bg="green", fg="white")
add_button.pack(pady=5)

modify_button = tk.Button(root, text="Modifier Employé", command=open_modify_employee_window, bg="green", fg="white")
modify_button.pack(pady=5)

delete_button = tk.Button(root, text="Supprimer Employé", command=open_delete_employee_window, bg="green", fg="white")
delete_button.pack(pady=5)

consult_button = tk.Button(root, text="Consulter Employés", command=open_consult_employee_window, bg="green", fg="white")
consult_button.pack(pady=5)

filter_dept_button = tk.Button(root, text="Filtrer Par Département", command=open_filter_department_window, bg="green", fg="white")
filter_dept_button.pack(pady=5)

filter_post_button = tk.Button(root, text="Filtrer Par Poste", command=open_filter_position_window, bg="green", fg="white")
filter_post_button.pack(pady=5)

root.mainloop()
