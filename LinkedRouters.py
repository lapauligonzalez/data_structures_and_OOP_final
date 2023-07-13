from collections import deque
from datetime import datetime, timedelta
import csv
import os
import random

if os.path.isfile("system_log.csv"): #Borra el archivo de system_log para que no se appendee abajo de una simulacion anterior
  os.remove("system_log.csv")

class LinkedList:
    def __init__(self):
        self.head = None
        self.size = 0
        self.inactivos = []

    def is_empty(self):
        if self.size == 0:
            return True
        else:
            return False

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

    def append(self, new_router): #Para agregar un nodo al final de la lista
        if self.is_empty():
            self.head = new_router
            self.head.next = self.head
            self.size += 1
        else:
            current = self.head
            while current.next.id != self.head.id: #mientras que el nodo no sea head
                current = current.next #avanzar un lugar en la lista
            current.next = new_router #el proximo nodo va a ser el nuevo router
            new_router.next = self.head #hacemos que la lista sea circular
            self.size += 1
        new_router.cambiar_estado("ACTIVO")

    def prepend(self, new_router): #Para agregar un router al principio de la lista
        if self.is_empty():
            self.head = new_router
            self.size += 1
        else:
            current = self.head
            while self.head.id != current.next.id:
                current = current.next
            current.next = new_router
            new_router.next = self.head
            self.head = new_router
            new_router.cambiar_estado("ACTIVO")
            self.size += 1


    def insert_after(self, id_prev, new_router):
        current = self.head
        while id_prev != current.id:
            current = current.next
        new_router.next = current.next
        current.next = new_router
        self.size += 1


    def delete(self, id):
        current = self.head.next
        if self.head.id == id: #Aca borra el router
            while current.next.id != self.head.id:
                current = current.next
            current.next = self.head.next
            self.head = self.head.next
            self.size -= 1
            return
        current = self.head
        prev = None
        while current and current.id != id:
            prev = current
            current = current.next

        prev.next = current.next
        self.size -= 1
        if self.size == 0:
            self.head = None

    def distribucion_paquetes_origen(self, desde, horario): #Lee el archivo de los paquetes y distribuye los mensajes en los router origen
        main_path = os.path.abspath(__file__)
        dir_path = os.path.dirname(main_path)
        paquetes_file = os.path.join(dir_path, 'Paquetes.csv')
        with open(paquetes_file, 'r') as f:
            lines = f.readlines()
        contador = 0
        for line in lines:
            if contador <= desde:
                contador += 1
                continue
            if contador > desde+99:
                break
            if ',' in line:
                origen, destino, mensaje = line.strip().split(",")

                current = self.head
                for i in range(self.size):
                    if origen == current.id:
                        current.paquetes_locales.agregar_paquete(Paquete(mensaje, origen, destino, horario)) #Agrega el paquete en la cola origen del router
                    for i in range(len(self.inactivos)):
                        if origen == self.inactivos[i].id:
                            self.inactivos[i].paquetes_locales.agregar_paquete(Paquete(mensaje, origen, destino, horario))
                    current = current.next
                            
                    
                contador +=1



    
        

class Router:
    def __init__(self, id):
        self.id = f"router_{id}"
        self.estado = None
        self.inactivo_hasta = 0
        self.paquetes_recibidos = [] #Todos los paquetes que llegan desde otro router que partenecen a este
        self.paquetes_llegada = Colas() #Todos los paquetes que llegan de otro router
        self.paquetes_transitorios = Colas() #Todos los paquetes que llegan de otro router que son para retransmitir
        self.paquetes_locales = Colas() #Todos los paquetes que se originan en ese router que son para otros routers
        self.contador_transitorios = 0
        self.next = None

    def __str__(self):
        return f"{self.id}"

    def enviados_vs_recibidos(self):
        n=(self.contador_transitorios/(self.contador_transitorios+len(self.paquetes_recibidos)))*100
        m=100-n
        print(f"En el {self.id} hay un "+ str(round(n,2)) + " porciento de mensajes reenviados y un " + str(round(m,2)) + " porciento de mensajes recibidos")
    
    def distribuir_mensajes_llegada(self):
        for i in range(self.paquetes_llegada.size):
            paquete_distribuir = self.paquetes_llegada.sale_paquete()
            if paquete_distribuir.destino == self.id:
                self.paquetes_recibidos.append(paquete_distribuir)
            else:
                self.contador_transitorios += 1 #Va contando la cantidad de paquetes que son a reenviar
                self.paquetes_transitorios.agregar_paquete(paquete_distribuir)

    def cambiar_estado(self, nuevo_estado): #Cuando se actualize los estados que se actualice el archivo
      estado_anterior = self.estado
      self.estado = nuevo_estado
      with open("system_log.csv", mode = "a", newline="") as csv_file:
        writer = csv.writer(csv_file)
        timestamp = datetime.now()
        writer.writerow([self.id, timestamp, nuevo_estado])

    def pasar_mensajes(self):
        for i in range(self.paquetes_transitorios.size):
            paquete_enviado = self.paquetes_transitorios.sale_paquete()
            self.next.paquetes_llegada.agregar_paquete(paquete_enviado)
        for i in range(self.paquetes_locales.size):
            paquete_enviado = self.paquetes_locales.sale_paquete()
            self.next.paquetes_llegada.agregar_paquete(paquete_enviado)

class Colas:
    def __init__(self):
        self.paquetes_esperando = deque()
        self.size = 0

    def agregar_paquete(self, paquete):
        self.paquetes_esperando.append(paquete)
        self.size +=1

    def sale_paquete(self):
        self.size -=1
        return self.paquetes_esperando.popleft()
    
    def hay_paquetes(self):
        return self.size > 0


class Paquete:
    def __init__(self, mensaje, origen, destino, horario):
        self.mensaje = mensaje
        self.origen = origen
        self.destino = destino
        self.horario = horario

    def __str__(self):
        return f'Horario:{self.horario}\n{self.mensaje}\n'

