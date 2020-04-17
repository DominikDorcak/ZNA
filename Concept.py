class Concept:

    def __init__(self,intent,extent):
        self.intent = intent
        self.extent = set(extent)

    def __str__(self):
        return str(self.extent)

    def __hash__(self):
       return hash(str(self))

    def __eq__(self, other):
        ot = list(other.extent)
        th = list(self.extent)
        for i in range(len(ot)):
            if not ot[i]==th[i]:
                return False
        return True


