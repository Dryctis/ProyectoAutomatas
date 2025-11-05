import graphviz

class MaquinaDeEstados:
    
    def __init__(self, tabla_transiciones, estado_inicial='q0', estados_finales=None):
        """
        Inicializa la Máquina de Estados.
        :param tabla_transiciones: Diccionario que define las transiciones del autómata.
        :param estado_inicial: Estado de donde comienza el procesamiento.
        :param estados_finales: Conjunto de estados de aceptación.
        """
        if not tabla_transiciones:
            raise ValueError("La tabla de transiciones no puede estar vacía.")
            
        self.tabla_transiciones = tabla_transiciones
        self.estado_inicial = estado_inicial
        self.estado_actual = estado_inicial
        self.estados_finales = estados_finales if estados_finales is not None else set()
        
    def _obtener_tipo_caracter(self, caracter):
        """
        Clasifica el caracter de entrada según las categorías definidas en la tabla.
        """
        if caracter.isdigit():
            return 'digito'
        elif caracter in ['+', 'E', '-', '*', '/']:
            return caracter
        else:
            return 'INVALIDO' 

    def procesar_cadena(self, cadena):
        """
        Simula el recorrido de la cadena a través del autómata.
        """
        log_resultado = []
        log_resultado.append(f"--- Procesando cadena: '{cadena}' ---")
        
        self.estado_actual = self.estado_inicial
        valida = True
        
        if not cadena:
            log_resultado.append("Cadena vacía, no se procesa nada.")
            valida = False

        for caracter in cadena:
            tipo_caracter = self._obtener_tipo_caracter(caracter)
            
            if tipo_caracter == 'INVALIDO':
                log_resultado.append(f"  [Error] El caracter '{caracter}' NO es valido en este lenguaje.")
                valida = False
                break 

            if self.estado_actual in self.tabla_transiciones and \
               tipo_caracter in self.tabla_transiciones[self.estado_actual]:
                
                siguiente_estado = self.tabla_transiciones[self.estado_actual][tipo_caracter]
                log_resultado.append(f"  [OK] Transición: {self.estado_actual} --({caracter} -> {tipo_caracter})--> {siguiente_estado}")
                self.estado_actual = siguiente_estado
            else:
                log_resultado.append(f"  [Error] Transición NO definida desde {self.estado_actual} con '{caracter}' (tipo: {tipo_caracter}).")
                self.estado_actual = 'q_error'
                valida = False
                break
        
        log_resultado.append(f"--- Fin de cadena '{cadena}' ---")
        
        es_aceptada = valida and self.estado_actual in self.estados_finales
        
        if es_aceptada:
            log_resultado.append(f"Estado final: {self.estado_actual} (¡Cadena ACEPTADA!)")
        else:
            log_resultado.append(f"Estado final: {self.estado_actual} (Cadena RECHAZADA)")
            
        return "\n".join(log_resultado), es_aceptada

    
    def generar_y_abrir_diagrama(self, nombre_archivo="diagrama_automata"):
        """
        Crea un diagrama del autómata usando Graphviz, agrupando aristas 
        con el mismo origen y destino para mayor claridad.
        """
        try:
            
            dot = graphviz.Digraph(comment='Diagrama de Transiciones', graph_attr={'rankdir': 'LR'})
            dot.attr('node', shape='circle')
            
            
            dot.node('start_node', shape='point', style='invis')
            
            
            todos_los_estados = set(self.tabla_transiciones.keys())
            for transiciones in self.tabla_transiciones.values():
                todos_los_estados.update(transiciones.values())

           
            for estado in todos_los_estados:
                if estado in self.estados_finales:
                    dot.node(estado, shape='doublecircle') 
                elif estado in self.tabla_transiciones or estado == self.estado_inicial:
                    dot.node(estado, shape='circle') 
            dot.edge('start_node', self.estado_inicial)

           
            aristas_agrupadas = {}
            
            for estado_origen, transiciones in self.tabla_transiciones.items():
                for simbolo, estado_destino in transiciones.items():
                   
                    key = (estado_origen, estado_destino)
                    if key not in aristas_agrupadas:
                        aristas_agrupadas[key] = []
                    aristas_agrupadas[key].append(simbolo)
            
            
            print("Generando diagrama con aristas agrupadas...")
            for (origen, destino), simbolos in aristas_agrupadas.items():
               
                label = ", ".join(simbolos)
                dot.edge(origen, destino, label=label)
            
            
            
            dot.render(nombre_archivo, format='png', view=True, cleanup=True)
            return True, f"Diagrama '{nombre_archivo}.png' generado y abierto."

        except Exception as e:
            print(f"[Error Graphviz] {e}")
            
            if "failed to execute" in str(e) or "No such file or directory" in str(e):
                 return False, (
                    "¡Error! No se encontró el ejecutable de Graphviz.\n\n"
                    "Asegúrate de haber instalado Graphviz en tu SISTEMA (no solo la librería de Python) "
                    "y de que esté añadido al 'PATH' del sistema. Luego, reinicia la aplicación."
                )
            return False, f"Error inesperado al generar el diagrama: {e}"