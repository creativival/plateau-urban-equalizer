from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from PIL import Image
from city.data_loader import DataLoader
from city.building_render import BuildingRenderer
from city.camera import Camera
from city.sound import Sound
import math
from direct.stdpy import threading
from queue import Empty


class BuildingApp(ShowBase):
    # 元の頂点数と簡略化後の頂点数
    vertex_count = 0
    simplified_vertex_count = 0
    # アプリの基本設定
    use_wireframe = False  # ワイヤーフレーム表示の有無
    use_simplified_coords = True  # 簡略化された座標を使用するかどうか
    image_path = 'images/mirror_ball.png'
    sound_path = 'sound/Dive_To_Mod.mp3'
    # 波の進行方向
    wave_direction = 'concentric'  # 'concentric', 'x_axis', 'y_axis' or 'xy_axes'

    def __init__(self, zoom_level, tile_x, tile_y):
        super().__init__()

        # インスタンス変数
        self.zoom_level = zoom_level

        # ウインドウの設定
        self.props = WindowProperties()
        self.props.setTitle('Plateau Urban Equalizer')  # タイトルを設定
        self.props.setSize(1600, 900)  # ウインドウサイズは環境に合わせて調整する。
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

        # Soundクラスを初期化
        self.sound = Sound(self.sound_path)

        # サウンドの再生とビルの高さ更新を時間差で開始
        self.taskMgr.doMethodLater(1, self.play_sound, 'PlaySound')
        self.taskMgr.doMethodLater(2, self.start_equalizer, 'StartEqualizer')

    def play_sound(self, task):
        # サウンドの再生を別スレッドで開始
        self.sound_thread = threading.Thread(target=self.sound.play)
        self.sound_thread.start()

        return task.done  # タスクを停止

    def start_equalizer(self, task):
        # ビルの高さを更新するタスクを追加
        self.taskMgr.doMethodLater(0.1, self.update_buildings_height_task, 'UpdateBuildingsTask')

        return task.done  # タスクを停止

    def update_buildings_height_task(self, task):
        if not self.sound.is_playing.is_set() and self.sound.amplitude_queue.empty():
            return task.done  # サウンドの再生が終了したらタスクを停止

        try:
            # 振幅データを取得
            amplitude = self.sound.amplitude_queue.get_nowait()
        except Empty:
            # 振幅データがまだない場合は次のフレームへ
            return task.cont

        # 振幅を正規化（0〜1の範囲）
        max_amplitude = 32768  # int16の最大値
        normalized_amplitude = amplitude / max_amplitude

        # 現在の時間を取得
        current_time = globalClock.getFrameTime()

        # 波のパラメータ
        wave_length = 500  # 波の長さ（空間的な波長）
        wave_speed = 2  # 波の速度（値を調整して波の進行速度を変える）
        wave_height_scale = 500  # 波の高さを調整するスケール

        # ビルの高さを更新
        for building in self.building_list:
            x, y = building.centroid.x, building.centroid.y

            # 波の位相を計算
            if self.wave_direction == 'x_axis':
                phase = x / wave_length - wave_speed * current_time
            elif self.wave_direction == 'y_axis':
                phase = y / wave_length - wave_speed * current_time
            elif self.wave_direction == 'xy_axes':
                phase = (x + y) / wave_length - wave_speed * current_time
            else:  # 'concentric'
                phase = math.sqrt((x - 2048) ** 2 + (y - 2048) ** 2) / wave_length - wave_speed * current_time

            # 波の高さを計算
            wave_height = normalized_amplitude * math.sin(phase) * wave_height_scale + wave_height_scale / 4

            # ビルの高さを更新
            if building.node:
                building.node.setSz(max(wave_height, 1))  # 最小高さを1に設定

        return task.cont  # タスクを継続


if __name__ == '__main__':
    # 渋谷駅のタイル座標35.6582972,139.70146677
    # ズームレベル 14: x=14549, y=6452
    # ズームレベル 15: x=29099, y=12905
    # ズームレベル 16: x=58199, y=25811

    # タイル座標を指定
    z = 14
    x = 14549
    y = 6452
    # z = 15
    # x = 29099
    # y = 12905
    # z = 16
    # x = 58199
    # y = 25811

    # 東京駅のタイル座標
    # ズームレベル 14: x=14552, y=6451
    # ズームレベル 15: x=29105, y=12903
    # ズームレベル 16: x=58211, y=25807

    # タイル座標を指定
    # z = 14
    # x = 14552
    # y = 6451
    # z = 15
    # x = 29105
    # y = 12903
    # z = 16
    # x = 58211
    # y = 25807

    app = BuildingApp(z, x, y)
    app.run()
