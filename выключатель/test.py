import tkinter as tk
from PIL import Image, ImageTk

class LampApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lamp Switch")

        self.image_dark = Image.open("dark_photo.jpg")
        self.image_light = Image.open("light_photo.jpg")

        self.tk_image_dark = ImageTk.PhotoImage(self.image_dark)
        self.tk_image_light = ImageTk.PhotoImage(self.image_light)

        self.is_light_on = False

        self.label = tk.Label(root, image=self.tk_image_dark)
        self.label.pack()

        self.switch_button = tk.Button(root, text="Выключатель", command=self.toggle_image, font=("Arial", 16), width=20, height=2)
        self.switch_button.pack()

    def toggle_image(self):
        if self.is_light_on:
            self.label.config(image=self.tk_image_dark)
        else:
            self.label.config(image=self.tk_image_light)
        self.is_light_on = not self.is_light_on

if __name__ == "__main__":
    root = tk.Tk()
    app = LampApp(root)
    root.mainloop()
