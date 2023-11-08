import tkinter as tk

# Create the main window
window = tk.Tk()
window.title("Text Display")

# Create a label widget to display text
text_label = tk.Label(window, text="Hello, this is a text display!")
text_label.pack()

# Start the main event loop
window.mainloop()