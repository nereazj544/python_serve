import tkinter
import customtkinter

customtkinter.set_appearance_mode("System")  # "System", "Dark", "Light" (modo de apariencia)
customtkinter.set_default_color_theme("blue")  # blue, dark-blue, green, dark-green, light-blue, dark-light-blue


app = customtkinter.CTk()  # Crear la ventana principal
app.geometry("800x600")  # Establecer el tamaño de la ventana


def button_function():
    print("Botón presionado")  # Acción al presionar el botón   

button = customtkinter.CTkButton(master=app, text="Presionar", command=button_function)  # Crear un botón
button.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)  # Colocar el botón en el centro de la ventana
app.mainloop()  # Iniciar el bucle principal de la aplicación