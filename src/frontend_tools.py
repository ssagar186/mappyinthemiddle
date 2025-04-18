import tkinter as tk

class FrontEndTools:
    def __init__(self):
        pass

    def create_front_end(self):
        root = tk.Tk()
        root.title("Text Input Example")

        text_area = tk.Text(root, height=5, width=30)
        text_area.pack()

        def get_input():
            input_text = text_area.get("1.0", tk.END)
            print("Input:", input_text)

        get_button = tk.Button(root, text="Get Input", command=get_input)
        get_button.pack()

        root.mainloop()