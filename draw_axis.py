from direct.showbase.ShowBase import ShowBase
from panda3d.core import *

class App(ShowBase):
  def __init__(self):
    ShowBase.__init__(self)

    # ウインドウの設定
    self.props = WindowProperties()
    self.props.setTitle('App')
    self.props.setSize(900, 600)
    self.win.requestProperties(self.props)

    # 地球と座標軸を表示する
    self.axis = self.loader.loadModel('zup-axis')
    self.axis.reparentTo(self.render)

app = App()
app.run()
