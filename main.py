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
            self.red.append(router)



    def escribir_archivo(self): #Genera el archivo con los paquetes recibidos en ese router para imprimirlo al final del programa
        current = self.red.head
        for i in range(self.red.size):
            nueva_lista = [] #Genera una lista con los routers excluyendo al que estamos parados para poder hacer el .txt prolijo
            router_agregar = self.red.head
            while len(nueva_lista) < self.red.size: 
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
            num = random.randint(1,1000)
            if num == 1:
                current.cambiar_estado("INACTIVO")
                current.cambiar_estado("EN_RESET")
                current.inactivo_hasta = contador_de_ciclos + random.randint(50,100)
                self.red.inactivos.append(current)
                self.red.delete(current.id)
            current = current.next

    def reactivacion(self, contador_de_ciclos, fin):
        for i in range(len(self.red.inactivos)):
            if self.red.inactivos[i].inactivo_hasta == contador_de_ciclos or fin:
                if self.red.inactivos[i].id == "router_1":
                    self.red.prepend(self.red.inactivos[i])
                    continue
                print(self.red.inactivos[i].id)
                posicion_del_actual = int(self.red.inactivos[i].id[-1])
                if self.red.is_empty():
                    self.red.prepend(self.red.inactivos[i])
                    continue
                current = self.red.head
                current_posicion = int(current.id[-1])
                prev = None
                while current_posicion < posicion_del_actual:
                    current_posicion = int(current.id[-1])
                    prev = current
                    current = current.next
                else:
                    self.red.prepend(self.red.inactivos[i])
                self.red.insert_after(prev.id, self.red.inactivos[i])
                current = self.red.head
                for j in range(self.red.size):
                    if current.id == self.red.inactivos[i].id:
                        current.cambiar_estado("ACTIVO")
                    current = current.next
                self.red.inactivos.remove[i]

    def simulacion(self):
        self.agrega_routers()
        total_ciclos = int(segundos)*10
        contador_de_ciclos = 0
        horario = self.horario_inicial
        while contador_de_ciclos < total_ciclos: 
            horario += timedelta(seconds=0.1)
            self.red.distribucion_paquetes_origen(contador_de_ciclos*100, horario)
            print("paquetes distribuidos")
            
            self.reactivacion(contador_de_ciclos, False)
            self.desactivar(contador_de_ciclos)

            current = self.red.head
            for i in range(self.red.size):
                current.distribuir_mensajes_llegada()
                print("mensajes llegada distribuidos")
                current.pasar_mensajes()
                current = current.next
                print("mensajes enviados al siguiente router")
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




  # def desactivar(self):
    #     current = self.head
    #     for i in range(self.size):
    #         num = random.randint(1,100)
    #         if num == 42:
    #             current.cambiar_estado("INACTIVO")
    #             self.inactivos.append(current)
    #             self.delete(current.id)
    #         current = current.next
    
