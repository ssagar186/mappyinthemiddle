import tkinter as tk
from src.address_check import AddressCheck


class FrontEndTools:
    def __init__(self):
        self.root = tk.Tk()
        self.text_area = tk.Text(self.root, height=5, width=30)
        self.addresses = []
        self.address = None
        self.create_front_end()
        self.main_loop()


    def create_front_end(self):
        self.root.title("Input Coordinates")
        self.text_area.pack()

    def get_input(self):
        input_text = self.text_area.get("1.0", tk.END)
        print("Input:", input_text)
        return input_text

    def main_loop(self):
        get_button = tk.Button(self.root, text="Get Input", command=self.get_input)
        get_button.pack()
        self.root.mainloop()