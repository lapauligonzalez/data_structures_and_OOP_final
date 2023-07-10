from collections import deque

class LinkedList: #Cómo nos aseguramos de que es una lista enlazada circular?
    def __init__(self):
        self.head = None
        self.size = 0

    def is_empty(self):
        return self.head is None
    
    def __str__(self):
        nodo = self.head
        cadena = ""
        if self.size == 0:
            return "La lista enlazada está vacía."
        else:
            while nodo is not None:
                cadena += str(nodo) + '\t'
                nodo = nodo.next
        return cadena
    
    def append(self, id): #Para agregar un nodo al final de la lista
        new_Router = Router(id)
        if self.is_empty():
            self.head = new_Router
            self.head.next = self.head
            self.size += 1
        else:
            current = self.head
            while current.next.id != self.head.id: #mientras que el nodo no sea head
                current = current.next #avanzar un lugar en la lista
            current.next = new_Router #el proximo nodo va a ser el nuevo router
            new_Router.next = self.head #hacemos que la lista sea circular
            self.size += 1

    def prepend(self, id): #Para agregar un router al principio de la lista
        new_Router = Router(id)
        if self.is_empty():
            self.head = new_Router
            self.size += 1
        else:
            new_Router.next = self.head
            self.head = new_Router
            self.size += 1

    def delete(self, id):
        if self.is_empty():
            print("La lista enlazada está vacía, no hay nada que borrar.")
            return

        if self.head.id == id: #Aca borra el router si es el head
            self.head = self.head.next
            self.size -= 1
            return

        current = self.head
        prev = None
        while current and current.id != id:
                prev = current
                current = current.head

        if current is None:
            print("El ID del router no fue encontrado.")
            return

        prev.next = current.next
        self.size -= 1

    def pasar_mensajes(self,id):
        current = self.head
        while current.id != id:
            current = current.next 
        
        for i in len(current.paquetes_transitorios):
            paquete_enviado = current.paquetes_transitorios.sale_paquete()
            current.next.paquetes_llegada.agregar_paquete(paquete_enviado)
        for i in len(current.paquetes_locales):
            paquete_enviado = current.paquetes_locales.sale_paquete()
            current.next.paquetes_llegada.agregar_paquete(paquete_enviado)

    def distribucion_paquetes_origen(self): #Lee el archivo de los paquetes y distribuye los mensajes en los router origen
        current = self.head
        while True:
          paquetes_file = "C:/Users/paula/OneDrive/Documentos/Facultad/Estructura de Datos/paquetes.csv"
          with open(paquetes_file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if ',' in line:
                    origen, destino, mensaje = line.strip().split(",")
                    if origen == current.id:
                        current.cola_origen.agregar_paquete(Paquete(mensaje, origen, destino)) #Agrega el paquete en la cola origen del router
          current = current.next
          if current.id == self.head.id:
            break
    


class Router:
    def __init__(self, id):
        self.id = f"router_{id}"
        self.estado = "AGREGADO"
        self.paquetes_recibidos = Colas()
        self.paquetes_llegada = Colas()
        self.paquetes_transitorios = Colas()
        self.paquetes_locales = Colas()
        self.next = None

    def _str_(self):
        return f"{self.id}"

    def escribir_archivo(self): #Genera el archivo con los paquetes recibidos en ese router para imprimirlo al final del programa
        with open(f"{self.id}.txt", mode="w") as txt_file:
            for paquete in self.paquetes_recibidos:
                txt_file.write(str(paquete) + "\n")

    def distribuir_mensajes_llegada(self):
        for i in len(self.paquetes_llegada):
            paquete_distribuir = self.paquetes_llegada.sale_paquete()
            if paquete_distribuir.destino == self.id:
                self.paquetes_recibidos.agregar_paquete(paquete_distribuir)
            else:
                self.paquetes_transitorios.agregar_paquete(paquete_distribuir)
            




class Colas:
    def __init__(self):
        self.paquetes_esperando = deque()

    def agregar_paquete(self, paquete):
        self.paquetes_esperando.append(paquete)

    def sale_paquete(self):
        return self.paquetes_esperando.popleft()
        
    def hay_paquetes(self):
        return len(self.paquetes_esperando) > 0


class Paquete:
    def __init__(self, mensaje, origen, destino, horario):
        self.mensaje = mensaje
        self.origen = origen
        self.destino = destino
        self.horario = horario

    def __str__(self):
        return f"El mensaje ({self.mensaje}), proviene del router {self.origen}, el destino es el router {self.destino}, y fue enviado en el horario {self.horario}."


