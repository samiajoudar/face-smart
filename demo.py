import tkinter as tk


def main():
    # Create the main application window
    root = tk.Tk()

    # Set the title of the window
    root.title("Hello Tkinter")

    # Create a label widget
    label = tk.Label(root, text="Hello, Tkinter!")

    # Pack the label widget into the window
    label.pack()

    # Run the Tkinter event loop
    root.mainloop()


if __name__ == "__main__":
    main()