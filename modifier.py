import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error

# Exemple de données d'employés (à remplacer par vos propres données)
employees_data = [
    {"id": 1, "nom": "Doe", "prenom": "John", "heure_arrivee": "09:00", "heure_sortie": "17:00", "poste": "Ingénieur", "departement": "Informatique"},
    {"id": 2, "nom": "Smith", "prenom": "Jane", "heure_arrivee": "08:30", "heure_sortie": "16:30", "poste": "Analyste", "departement": "Ressources Humaines"},
    {"id": 3, "nom": "Brown", "prenom": "Michael", "heure_arrivee": "09:15", "heure_sortie": "17:15", "poste": "Développeur", "departement": "Informatique"}
]

def find_employee_by_id(employee_id):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # Remplacez par votre mot de passe MySQL si nécessaire
            database="employee_management"
        )
        if conn.is_connected():
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM employees WHERE id = %s", (employee_id,))
            employee = cursor.fetchone()
            return employee
    except Error as e:
        messagebox.showerror("Erreur", f"Erreur: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
    return None

def modify_employee(employee_id, new_data):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # Remplacez par votre mot de passe MySQL si nécessaire
            database="employee_management"
        )
        if conn.is_connected():
            cursor = conn.cursor()
            query = """
            UPDATE employees SET nom = %s, prenom = %s, heure_arrivee = %s, heure_sortie = %s, poste = %s, departement = %s WHERE id = %s
            """
            values = (new_data["nom"], new_data["prenom"], new_data["heure_arrivee"], new_data["heure_sortie"], new_data["poste"], new_data["departement"], new_data["id"])
            cursor.execute(query, values)
            conn.commit()
            messagebox.showinfo("Modification réussie", "Les informations de l'employé ont été modifiées avec succès.")
    except Error as e:
        messagebox.showerror("Erreur", f"Erreur: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def open_modify_employee_window(employee_id):
    employee = find_employee_by_id(employee_id)
    if employee:
        modify_employee_window = tk.Toplevel(root)
        modify_employee_window.title(f"Modifier Employé - ID: {employee['id']}")
        modify_employee_window.configure(bg="#001f3f")

        # Labels et Entries pour afficher les informations actuelles de l'employé
        tk.Label(modify_employee_window, text="Nom :", bg="#001f3f", fg="white").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(modify_employee_window, text="Prénom :", bg="#001f3f", fg="white").grid(row=1, column=0, padx=5, pady=5)
        tk.Label(modify_employee_window, text="Heure d'arrivée :", bg="#001f3f", fg="white").grid(row=2, column=0, padx=5, pady=5)
        tk.Label(modify_employee_window, text="Heure de sortie :", bg="#001f3f", fg="white").grid(row=3, column=0, padx=5, pady=5)
        tk.Label(modify_employee_window, text="Poste :", bg="#001f3f", fg="white").grid(row=4, column=0, padx=5, pady=5)
        tk.Label(modify_employee_window, text="Département :", bg="#001f3f", fg="white").grid(row=5, column=0, padx=5, pady=5)

        nom_entry = tk.Entry(modify_employee_window)
        prenom_entry = tk.Entry(modify_employee_window)
        heure_arrivee_entry = tk.Entry(modify_employee_window)
        heure_sortie_entry = tk.Entry(modify_employee_window)
        poste_entry = tk.Entry(modify_employee_window)
        departement_entry = tk.Entry(modify_employee_window)

        nom_entry.insert(0, employee["nom"])
        prenom_entry.insert(0, employee["prenom"])
        heure_arrivee_entry.insert(0, employee["heure_arrivee"])
        heure_sortie_entry.insert(0, employee["heure_sortie"])
        poste_entry.insert(0, employee["poste"])
        departement_entry.insert(0, employee["departement"])

        nom_entry.grid(row=0, column=1, padx=5, pady=5)
        prenom_entry.grid(row=1, column=1, padx=5, pady=5)
        heure_arrivee_entry.grid(row=2, column=1, padx=5, pady=5)
        heure_sortie_entry.grid(row=3, column=1, padx=5, pady=5)
        poste_entry.grid(row=4, column=1, padx=5, pady=5)
        departement_entry.grid(row=5, column=1, padx=5, pady=5)

        # Bouton "Enregistrer les modifications"
        save_button = tk.Button(modify_employee_window, text="Enregistrer les modifications", command=lambda: save_modifications(employee_id, nom_entry.get(), prenom_entry.get(), heure_arrivee_entry.get(), heure_sortie_entry.get(), poste_entry.get(), departement_entry.get()), bg="green", fg="white")
        save_button.grid(row=6, column=0, columnspan=2, pady=10)
    else:
        messagebox.showerror("Erreur", f"Aucun employé trouvé avec l'ID {employee_id}")

def save_modifications(employee_id, nom, prenom, heure_arrivee, heure_sortie, poste, departement):
    new_data = {
        "id": int(employee_id),
        "nom": nom,
        "prenom": prenom,
        "heure_arrivee": heure_arrivee,
        "heure_sortie": heure_sortie,
        "poste": poste,
        "departement": departement
    }
    modify_employee(employee_id, new_data)

# Création de la fenêtre principale
root = tk.Tk()
root.title("Gestion des Employés")

# Pour tester la modification, passez un ID valide dans open_modify_employee_window
employee_id_to_modify = 1  # Remplacez par un ID valide
open_modify_employee_window(employee_id_to_modify)

root.mainloop()
