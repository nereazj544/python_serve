import customtkinter 
import tkinter as tk
# Interfaz de usuario en Python

def main_custom ():
    customtkinter.set_appearance_mode("System") # "System", "Dark", "Light" (modo de apariencia)
    customtkinter.set_default_color_theme("blue") # blue, dark-blue, green, dark-green, light-blue, dark-light-blue

    app = customtkinter.CTk() # Crear la ventana principal
    
    app.geometry("800x600") # Establecer el tamaño de la ventana
    app.title("Interfaz de Usuario con CustomTkinter") # Título de la ventana


if __name__ == "__main__":
    main_custom() # Llamar a la función principal para iniciar la aplicación
    app.mainloop() # Iniciar el bucle principal de la aplicación
