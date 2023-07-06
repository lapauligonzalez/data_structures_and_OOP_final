class Paquetes():
    def _init_(self, mensaje, origen, destino, horario):
        self.mensaje = mensaje
        self.origen = origen
        self.destino = destino
        self.horario = horario

    def _str_(self):
        return f"El mensaje ({self.mensaje}), proviene del router {self.origen}, el destino es el router {self.destino}, y fue enviado en el horario {self.horario}."