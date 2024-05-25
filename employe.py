import tkinter as tk
from tkinter import messagebox
import mysql.connector
import subprocess

class EmployeApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Employé")
        self.master.geometry("400x400")
        self.master.configure(bg="#001f3f")

        # Connexion à la base de données MySQL
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="employee_management"
        )
        self.cursor = self.conn.cursor()

        self.label = tk.Label(master, text="Bienvenue, Employé", bg="#001f3f", fg="white", font=("Arial", 20))
        self.label.pack(pady=20)

        # Rubrique de saisie de l'ID
        self.id_label = tk.Label(master, text="Entrez l'ID :", bg="#001f3f", fg="white", font=("Arial", 12))
        self.id_label.pack(pady=5)
        self.id_entry = tk.Entry(master)
        self.id_entry.pack(pady=5)

        # Bouton "Afficher les employés"
        self.show_button = tk.Button(master, text="Afficher les employés", command=self.show_employee, bg="green", fg="white", font=("Arial", 12))
        self.show_button.pack(pady=10)

        # Bouton "Pointer l'arrivée"
        self.arrival_button = tk.Button(master, text="Pointer l'arrivée", command=self.pointer_arrivee, bg="blue", fg="white", font=("Arial", 12))
        self.arrival_button.pack(pady=5)

        # Bouton "Pointer le départ"
        self.departure_button = tk.Button(master, text="Pointer le départ", command=self.pointer_depart, bg="orange", fg="white", font=("Arial", 12))
        self.departure_button.pack(pady=5)

        self.quit_button = tk.Button(master, text="Quitter", command=self.quit_app, bg="red", fg="white", font=("Arial", 12))
        self.quit_button.pack(pady=10)

    def show_employee(self):
        employee_id = self.id_entry.get()
        if employee_id:
            # Récupérer les informations de l'employé à partir de la base de données
            self.cursor.execute("SELECT * FROM employees WHERE id = %s", (employee_id,))
            employee_info = self.cursor.fetchone()
            if employee_info:
                # Afficher les informations de l'employé
                self.display_info(employee_info)
            else:
                messagebox.showwarning("ID invalide", "Aucun employé trouvé avec cet ID.")
        else:
            messagebox.showwarning("ID manquant", "Veuillez entrer un ID.")

    def display_info(self, employee_info):
        # Afficher les informations de l'employé dans une boîte de dialogue
        messagebox.showinfo("Informations de l'employé", f"Informations pour l'employé avec l'ID: {employee_info[0]}\nNom: {employee_info[1]}\nPrénom: {employee_info[2]}\nPoste: {employee_info[3]}\nDépartement: {employee_info[4]}")

    def quit_app(self):
        # Fermer la connexion à la base de données et quitter l'application
        self.cursor.close()
        self.conn.close()
        self.master.quit()

    def pointer_arrivee(self):
        # Exécuter le script adminregistration.py
        subprocess.Popen(["python", "adminenregistration.py"])

    def pointer_depart(self):
        # Exécuter le script adminregistration.py
        subprocess.Popen(["python", "adminenregistration.py"])
    def afficher_profil(self):
        messagebox.showinfo("Profil de l'employé", "Voici les informations de votre profil.")

if __name__ == "__main__":
    root = tk.Tk()
    app = EmployeApp(root)
    root.mainloop()
