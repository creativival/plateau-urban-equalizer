from direct.showbase.ShowBase import ShowBase


class MyApp(ShowBase):
    def __init__(self):
        super().__init__()


app = MyApp()
app.run()