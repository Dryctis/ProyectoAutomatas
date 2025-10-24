class MaquinaDeEstados:
    
    def __init__(self, tabla_transiciones, estado_inicial='q0', estados_finales=None):
        if not tabla_transiciones:
            raise ValueError("La tabla de transiciones no puede estar vacía.")
            
        self.tabla_transiciones = tabla_transiciones
        self.estado_inicial = estado_inicial
        self.estado_actual = estado_inicial
        self.estados_finales = estados_finales if estados_finales is not None else set()
        
    def _obtener_tipo_caracter(self, caracter):
        if caracter.isdigit():
            return 'digito'
        elif caracter in ['+', 'E', '-', '*', '/']:
            return caracter
        else:
            return 'INVALIDO' 

    def procesar_cadena(self, cadena):
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