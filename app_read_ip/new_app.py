import customtkinter as ctk

class NewApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Text Input App")
        self.geometry("500x200")

        self.label = ctk.CTkLabel(self, text = "etter name of web")
        self.label.pack(pady = 20, padx = 20)

        self.entry = ctk.CTkEntry(self, placeholder_text="Enter website name")
        self.entry.pack(pady=10, padx=20, fill='x', expand=True)


if __name__ == "__main__":
    app = NewApp()
    app.mainloop()