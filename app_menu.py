import customtkinter as ctk
import table_manager
import automata_core
from tkinter import messagebox

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class ToplevelEditor(ctk.CTkToplevel):
    def __init__(self, parent_app):
        super().__init__(parent_app)
        self.parent_app = parent_app  

        self.title("Editor de Tabla de Transiciones")
        self.geometry("800x400")

        
        self.estados = table_manager.ESTADOS
        self.entradas = table_manager.ENTRADAS
        
        
        self.celdas_entry = {}

        
        for j, entrada in enumerate(self.entradas):
            label = ctk.CTkLabel(self, text=entrada, font=ctk.CTkFont(weight="bold"))
            label.grid(row=0, column=j + 1, padx=5, pady=5)

        
        for i, estado in enumerate(self.estados):
            label = ctk.CTkLabel(self, text=estado, font=ctk.CTkFont(weight="bold"))
            label.grid(row=i + 1, column=0, padx=5, pady=5)
            
            self.celdas_entry[estado] = {}
            
            for j, entrada in enumerate(self.entradas):
                entry = ctk.CTkEntry(self, width=70)
                entry.grid(row=i + 1, column=j + 1, padx=3, pady=3)
                
            
                valor = self.parent_app.tabla_actual.get(estado, {}).get(entrada, "")
                if valor:
                    entry.insert(0, valor)
                
                
                self.celdas_entry[estado][entrada] = entry

        
        save_btn = ctk.CTkButton(self, text="Guardar Cambios y Recargar Autómata", command=self.guardar_cambios)
        save_btn.grid(row=len(self.estados) + 2, column=0, columnspan=len(self.entradas) + 1, pady=20)

    def guardar_cambios(self):
        print("Guardando cambios en la tabla...")
        nueva_tabla = {}
        
        try:
            
            for estado in self.estados:
                nueva_tabla[estado] = {}
                for entrada in self.entradas:
                    valor = self.celdas_entry[estado][entrada].get()
                    if valor:  
                        nueva_tabla[estado][entrada] = valor
            
            
            self.parent_app.actualizar_tabla_y_fsm(nueva_tabla)
            
            messagebox.showinfo("Éxito", "Tabla guardada y autómata recargado.")
            self.destroy()  
            
        except Exception as e:
            messagebox.showerror("Error al Guardar", f"Hubo un error al procesar la tabla: {e}")


class App(ctk.CTk):
    
    def __init__(self):
        super().__init__()
       
        self.title("Proyecto Automata FSM")
        self.geometry("700x500")
 
        self.estados_finales = {'q4', 'q6'} 
        self.tabla_actual = table_manager.cargar_tabla_default()
        self.fsm_instance = None  
        self.actualizar_fsm_instance() 
        
    
        self.editor_window = None

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

    
        self.button_frame = ctk.CTkFrame(self.input_frame, fg_color="transparent")
        self.button_frame.grid(row=0, column=1, padx=(5, 10), pady=10)

        self.procesar_btn = ctk.CTkButton(self.button_frame, text="Validar Cadena", command=self.procesar_cadena_gui)
        self.procesar_btn.grid(row=0, column=0, padx=5)

        
        self.edit_btn = ctk.CTkButton(self.button_frame, text="Editar Tabla", 
                                      fg_color="transparent", border_width=2,
                                      command=self.abrir_editor_tabla)
        self.edit_btn.grid(row=0, column=1, padx=5)

       
        self.diagrama_btn = ctk.CTkButton(self.button_frame, text="Ver Diagrama",
                                          fg_color="transparent", border_width=2,
                                          command=self.mostrar_diagrama_gui)
        self.diagrama_btn.grid(row=0, column=2, padx=5) 

    
        self.resultado_textbox = ctk.CTkTextbox(self, state="disabled", font=("Consolas", 13))
        
    
        self.resultado_textbox.grid(row=2, column=0, padx=20, pady=(10, 20), sticky="nsew")
        
        
    def abrir_editor_tabla(self):
        if self.editor_window is None or not self.editor_window.winfo_exists():
            self.editor_window = ToplevelEditor(self)  
            self.editor_window.transient(self)        
            self.editor_window.grab_set()             
        else:
            self.editor_window.focus()  

    def actualizar_fsm_instance(self):
        try:
            self.fsm_instance = automata_core.MaquinaDeEstados(
                self.tabla_actual, 
                estados_finales=self.estados_finales
            )
            print("Instancia de FSM actualizada/recargada.")
        except Exception as e:
            messagebox.showerror("Error Crítico", f"No se pudo cargar el autómata: {e}")
            self.fsm_instance = None 

    def actualizar_tabla_y_fsm(self, nueva_tabla):
        self.tabla_actual = nueva_tabla
        
       
        table_manager.guardar_tabla_default(self.tabla_actual)
        
       
        self.actualizar_fsm_instance()
        
       
        self.resultado_textbox.configure(state="normal")
        self.resultado_textbox.delete("1.0", "end")
        self.resultado_textbox.insert("1.0", "¡Éxito! Nueva tabla guardada y recargada.\n")
        self.resultado_textbox.configure(state="disabled")

    def mostrar_diagrama_gui(self):
        if not self.fsm_instance:
            messagebox.showerror("Error", "El autómata no está cargado correctamente.")
            return
        
        print("Generando diagrama...")
      
        exito, mensaje = self.fsm_instance.generar_y_abrir_diagrama()
        
        if exito:
            messagebox.showinfo("Diagrama Generado", mensaje)
        else:
          
            messagebox.showerror("Error de Graphviz", mensaje)
 

    def procesar_cadena_gui(self):
        if not self.fsm_instance:
             messagebox.showerror("Error", "El autómata no está cargado correctamente.")
             return
             
        cadena = self.cadena_entry.get()
        log_string, es_aceptada = self.fsm_instance.procesar_cadena(cadena)
        
        self.resultado_textbox.configure(state="normal")
        self.resultado_textbox.delete("1.0", "end")
        self.resultado_textbox.insert("1.0", log_string)
        self.resultado_textbox.configure(state="disabled")
