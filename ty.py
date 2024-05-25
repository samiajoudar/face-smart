import tkinter as tk

def action():
    print("Bouton cliqué !")

# Créer la fenêtre principale
root = tk.Tk()

# Créer un cadre
frame = tk.Frame(root)

# Créer un bouton
button = tk.Button(frame, text="Cliquez ici", command=action)

# Placer le bouton dans le cadre
button.pack()

# Placer le cadre dans la fenêtre principale
frame.pack()

# Démarrer la boucle principale
root.mainloop()
