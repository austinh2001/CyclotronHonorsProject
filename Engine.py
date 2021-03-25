#Base Class for an Engine object
class Engine:
    
    def __init__(self):
        pass

    async def run(self):
        while True:
            print("Default Run")

    def handleEvents(self):
        pass

    def update(self):
        pass

    def render(self):
        pass
