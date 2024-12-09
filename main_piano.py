from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from PIL import Image
from city.data_loader import DataLoader
from city.building_render import BuildingRenderer
from city.camera import Camera
from city.sound import Sound
from city.equalizer import Equalizer
from city.piano import Piano  # （1）


class BuildingApp(ShowBase):
    # 元の頂点数と簡略化後の頂点数
    vertex_count = 0
    simplified_vertex_count = 0
    # アプリの基本設定
    use_wireframe = False  # ワイヤーフレーム表示の有無
    use_simplified_coords = True  # 簡略化された座標を使用するかどうか
    image_path = 'images/mirror_ball.png'  # ここから（2）
    image_path = 'images/mirror_ball.png'  # ここまで（2）
    sound_path = 'sound/Dive_To_Mod.mp3'

    def __init__(self, zoom_level, tile_x, tile_y):
        super().__init__()

        # インスタンス変数
        self.zoom_level = zoom_level

        # ウインドウの設定
        self.props = WindowProperties()
        self.props.setTitle('Plateau Urban Equalizer')  # タイトルを設定
        self.props.setSize(1600, 900)  # ウインドウサイズは環境に合わせて調整する。
        self.props.setSize(1440, 900)  # ウインドウサイズは環境に合わせて調整する。
        self.win.requestProperties(self.props)
        self.setBackgroundColor(0, 0, 0)  # ウインドウの背景色を黒に設定。

        # 全てを配置するノード
        self.world_node = self.render.attachNewNode('world_node')
        self.world_node.setPos(-2048, -2048, 0)  # 地図の中心を原点に移動

        # 座標軸を表示する
        self.axis = self.loader.loadModel('zup-axis')
        self.axis.reparentTo(self.render)
        self.axis.setScale(100)  # 座標軸の長さを設定

        # 地面を描画
        self.card = CardMaker('ground')
        self.card.setFrame(0, 4096, 0, 4096)
        self.ground = self.world_node.attachNewNode(self.card.generate())
        self.ground.setP(-90)
        self.ground.setColor(0, 0.5, 0, 0.3)  # 緑色
        # 透明度属性とブレンディングを有効にする
        self.ground.setTransparency(TransparencyAttrib.MAlpha)

        # カメラコントローラーを初期化
        self.camera_controller = Camera(self)

        # 背景画像の読み込み
        self.background_image = Image.open(self.image_path)
        self.image_width, self.image_height = self.background_image.size

        # 全てのビルを配置するノード
        self.buildings_node = self.world_node.attachNewNode('buildings_node')

        # 建物データをロード
        self.building_list = []
        DataLoader(self, zoom_level, tile_x, tile_y)
        print("元の頂点数:", self.vertex_count)
        print("簡略化後の頂点数:", self.simplified_vertex_count)

        # ビルを配置
        for building in self.building_list:
            BuildingRenderer(building)

        # アプリの停止
        self.accept('escape', exit)

        # # Soundクラスを初期化  # ここから（3）
        # self.sound = Sound(self.sound_path)
        #
        # # イコライザーを初期化
        # self.equalizer = Equalizer(self)  # ここまで（3）

        # ピアノを初期化
        self.piano = Piano(self)  # （4）


if __name__ == '__main__':
    # 渋谷駅のタイル座標35.6582972,139.70146677
    # ズームレベル 14: x=14549, y=6452
    # ズームレベル 15: x=29099, y=12905
    # ズームレベル 16: x=58199, y=25811

    # タイル座標を指定
    # z = 14
    # x = 14549
    # y = 6452
    z = 15
    x = 29099
    y = 12905
    # z = 16
    # x = 58199
    # y = 25811

    app = BuildingApp(z, x, y)
    app.run()
