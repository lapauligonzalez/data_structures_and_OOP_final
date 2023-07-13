from LinkedRouters import *
from utils import validar_entero
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

class RoutingSim:
    def __init__(self, tiempo):
        self.tiempo = tiempo
        self.red = LinkedList()
        self.horario_inicial = datetime.now()


    def agrega_routers(self):
        for i in range(1, 8):
            router = Router(i)
            print("Se creo el " + router.id)
            router.cambiar_estado("AGREGADO")
            self.red.append(router)



    def escribir_archivo(self): #Genera el archivo con los paquetes recibidos en ese router para imprimirlo al final del programa
        current = self.red.head
        for i in range(self.red.size):
            nueva_lista = [] #Genera una lista con los routers excluyendo al que estamos parados para poder hacer el .txt prolijo
            router_agregar = self.red.head
            for router in range(self.red.size):
                if router_agregar.id != current.id:
                    nueva_lista.append(router_agregar)
                router_agregar = router_agregar.next
            with open(f"{current.id}.txt", mode="w") as txt_file: #Aca creamos un archivo .txt por ese router
                for router in nueva_lista:
                    txt_file.write("\n\nOrigen: " + str(router.id) + "\n")
                    for i in range(len(current.paquetes_recibidos)):
                        if current.paquetes_recibidos[i].origen == router.id:
                            txt_file.write(current.paquetes_recibidos[i].mensaje + "\n")
            current = current.next
                        
        
    def grafico_barras(self):
      cantidad_paquetes = []
      routers = ["router_1", "router_2", "router_3", "router_4", "router_5", "router_6", "router_7"]
      current = self.red.head
      for i in range(self.red.size):
          cantidad_paquetes.append(len(current.paquetes_recibidos))
          current = current.next

      plt.title(label = "Mensajes recibidos por router", fontsize = 20)
      plt.xlabel("Routers")
      plt.ylabel("Cantidad de paquetes recibidos")
      plt.bar(routers, cantidad_paquetes, color = "teal", width = 0.5)
      plt.show()

    def desactivar(self, contador_de_ciclos):
        current = self.red.head
        for i in range(self.red.size):
            num = random.randint(1,500)
            if num == 1:
                current.cambiar_estado("INACTIVO")
                print(current.id + " " + current.estado)
                current.cambiar_estado("EN_RESET")
                print(current.id + " " + current.estado)
                current.inactivo_hasta = contador_de_ciclos + random.randint(50,100)
                print(current.inactivo_hasta)
                self.red.inactivos.append(current)
                self.red.delete(current.id)
            current = current.next

    def reactivacion(self, contador_de_ciclos, end):
        for i in range(0,len(self.red.inactivos)-1):
            if self.red.inactivos[i].inactivo_hasta == contador_de_ciclos or end:
                print("Reavtivar router: ")
                if self.red.inactivos[i].id == "router_1": # Agregamos al 1 al head siempre que se vuelve a activar
                    self.red.inactivos[i].cambiar_estado("ACTIVO")
                    print(self.red.inactivos[i].id + " ACTIVO")
                    self.red.prepend(self.red.inactivos[i])
                    del self.red.inactivos[i]
                    continue
                if self.red.inactivos[i].id == "router_7": # Agregamos al 7 al final siempre que se vuelve a activar 
                    self.red.inactivos[i].cambiar_estado("ACTIVO")
                    print(self.red.inactivos[i].id + " ACTIVO")
                    self.red.append(self.red.inactivos[i])
                    del self.red.inactivos[i]
                    continue
                if self.red.is_empty(): # Agregamos al head si es que la lista esta vacia
                    self.red.inactivos[i].cambiar_estado("ACTIVO")
                    print(self.red.inactivos[i].id + " ACTIVO")
                    self.red.prepend(self.red.inactivos[i])
                    del self.red.inactivos[i]
                    continue
                posicion_del_actual = int(self.red.inactivos[i].id[-1]) #Buscamos la posicion que deberia ocupar el inactivo si estuviera la lista completa
                posicion_head = int(self.red.head.id[-1]) #buscamos la posicion que tendria que tener el head si la lista estuviera completa
                if posicion_head > posicion_del_actual: # Agregamos al head si no hay menor
                    self.red.inactivos[i].cambiar_estado("ACTIVO")
                    print(self.red.inactivos[i].id + " ACTIVO")
                    self.red.prepend(self.red.inactivos[i])
                    del self.red.inactivos[i]
                current = self.red.head
                current_posicion = int(current.id[-1])
                prev = None
                for j in range(self.red.size): # Agregamos al desactivado despues de el menor anterior al mayor
                    if current_posicion > posicion_del_actual:
                        self.red.inactivos[i].cambiar_estado("ACTIVO")
                        print(self.red.inactivos[i].id + " ACTIVO")
                        self.red.insert_after(prev.id, self.red.inactivos[i])
                        del self.red.inactivos[i]
                        break
                    prev = current
                    current = current.next
                    current_posicion = int(current.id[-1])
                if posicion_del_actual > current_posicion:
                    current.cambiar_estado("ACTIVO")
                    print(current.id + " ACTIVO")
                    self.red.append(self.red.inactivos[i]) # Agregamos al final si no hay mayor
                    del self.red.inactivos[i]

        for i in range(len(self.red.inactivos)):
            print(self.red.inactivos[i])


    def simulacion(self):
        self.agrega_routers()
        total_ciclos = int(segundos)*10
        contador_de_ciclos = 0
        horario = self.horario_inicial
        print(str(total_ciclos))
        while contador_de_ciclos < total_ciclos: 
            print("Ciclo: " + str(contador_de_ciclos))
            horario += timedelta(seconds=0.1)
            self.red.distribucion_paquetes_origen(contador_de_ciclos*100, horario)
            
            self.reactivacion(contador_de_ciclos, False)
            self.desactivar(contador_de_ciclos)

            current = self.red.head
            for i in range(self.red.size):
                current.distribuir_mensajes_llegada()
                current.pasar_mensajes()
                current = current.next

            contador_de_ciclos +=1

        self.reactivacion(contador_de_ciclos, True)
        current = self.red.head
        for i in range(1,self.red.size + 1):
            current.enviados_vs_recibidos()
            current = current.next
        
        self.escribir_archivo()
        print("El programa ha finalizado")

        self.grafico_barras()


segundos = input("Ingrese el tiempo que debe durar la simulación:  ")
while not validar_entero(segundos):
    print("El valor ingresado no es un entero válido.")
    segundos = input("Ingrese un número entero: ")

programa = RoutingSim(segundos)

programa.simulacion()

