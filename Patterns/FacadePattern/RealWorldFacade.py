"""
EventManager扮演了门面的角色，并简化了你的工作。
Facade与子系统进行交流，并代表你为婚姻完成所有的预订和准备工作。

Hotelier类用于预订酒店。他有一个方法，
用于检查当天是否有免费的酒店（__isAvailable）

Florist类负责花卉装饰。这个类提供了setFlowerRequirements()方法，
用于指定要使用哪些种类的花卉来装饰婚礼。

Caterer类用于跟备办宴席者打交道，并负责安排餐饮。Caterer提供了
一个公开的setCuisine()方法，用来指定婚宴的菜肴类型。

Musician类用来安排婚礼的音乐，它使用setMusicType()方法来了解
会务的音乐要求。
"""


class EventManager(object):
    def __init__(self):
        print("Event Manager:: Let me talk to the folks\n")

    def arrange(self):
        self.hotelier = Hotelier()
        self.hotelier.bookHotel()

        self.florist = Florist()
        self.florist.setFlowerRequirements()

        self.caterer = Caterer()
        self.caterer.setCuisine()

        self.musician = Musician()
        self.musician.setMusicType()


class Hotelier(object):
    def __init__(self):
        print("Arranging the Hotel for Marriage? --")

    def __isAvailable(self):
        print("Is the Hotel free for the event on given day?")
        return True

    def bookHotel(self):
        if self.__isAvailable():
            print("Registered the Booking\n\n")


class Florist(object):
    def __init__(self):
        print("Flower Decorations for the Event? --")

    def setFlowerRequirements(self):
        print("Carnations, Roses and Lilies world be used for Decorations\n\n")


class Caterer(object):
    def __init__(self):
        print("Food Arrangements for the Event --")

    def setCuisine(self):
        print("Chinese & Continental Cuisine to be served\n\n")


class Musician(object):
    def __init__(self):
        print("Musical Arrangements for the Marriage --")

    def setMusicType(self):
        print("Jazz and Classical will be played\n\n")


class You(object):
    def __init__(self):
        print("You:: Whoa! Marriage Arrangements??!!!")

    def askEventManager(self):
        print("You:: Let's Contact the Event Manager\n\n")
        em = EventManager()
        em.arrange()

    def __del__(self):
        print("You:: Thanks to Event Manager, all preparations done! Phew!")


you = You()
you.askEventManager()
