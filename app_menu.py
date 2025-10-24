import customtkinter as ctk
import table_manager
import automata_core
from tkinter import messagebox

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    
    def __init__(self):
        super().__init__()

       
        self.title("Proyecto Automata FSM")
        self.geometry("700x500")

 
        self.estados_finales = {'q4', 'q6'} 
        self.tabla_actual = table_manager.cargar_tabla_default()
        self.fsm_instance = automata_core.MaquinaDeEstados(
            self.tabla_actual, 
            estados_finales=self.estados_finales
        )

   
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0) 
        self.grid_rowconfigure(1, weight=0) 
        self.grid_rowconfigure(2, weight=1) 
        self.title_label = ctk.CTkLabel(self, text="Validador de Cadenas FSM", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 10))

      
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.input_frame.grid_columnconfigure(0, weight=1) 

        self.cadena_entry = ctk.CTkEntry(self.input_frame, placeholder_text="Ingrese la cadena a validar...")
        self.cadena_entry.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="ew")

     
        self.procesar_btn = ctk.CTkButton(self.input_frame, text="Validar Cadena", command=self.procesar_cadena_gui)
        self.procesar_btn.grid(row=0, column=1, padx=(5, 10), pady=10)

    
        self.resultado_textbox = ctk.CTkTextbox(self, state="disabled", font=("Consolas", 13))
        self.resultado_textbox.grid(row=2, column=0, padx=20, pady=(10, 20), sticky="nsew")

       
        self.resultado_textbox.configure(state="normal")
        self.resultado_textbox.insert("1.0", "Bienvenido al Validador de Cadenas.\n\n")
        self.resultado_textbox.insert("end", "El autómata ha sido cargado desde 'tabla.json'.\n")
        self.resultado_textbox.insert("end", "Ingrese una cadena arriba y presione 'Validar'.")
        self.resultado_textbox.configure(state="disabled")


    def procesar_cadena_gui(self):
        """
        Toma la cadena del Entry, la procesa y muestra el log en el Textbox.
        """
        cadena = self.cadena_entry.get()
        
    
        log_string, es_aceptada = self.fsm_instance.procesar_cadena(cadena)
        
     
        self.resultado_textbox.configure(state="normal")
        self.resultado_textbox.delete("1.0", "end")
        self.resultado_textbox.insert("1.0", log_string)
        self.resultado_textbox.configure(state="disabled")

