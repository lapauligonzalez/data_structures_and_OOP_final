from LinkedRouters import *


class RoutingSim:
    def __init__(self, tiempo):
        self.red_routers = LinkedList()
        self.tiempo = tiempo
        for i in range(1, 7):
            router = Router(i)
            self.red_routers.append(router)



        

    



