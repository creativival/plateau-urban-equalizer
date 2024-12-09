import sys
import time
from pyo import *


class Piano:
    EXTENT = 4096
    WHITE_KEYS = ['z', 'x', 'c', 'v', 'b', 'n', 'm']
    BLACK_KEYS = ['s', 'd', 'g', 'h', 'j']
    KEY_MAPPING = {
        'z': ('C', 261.63), 's': ('C#', 277.18),
        'x': ('D', 293.66), 'd': ('D#', 311.13),
        'c': ('E', 329.63),
        'v': ('F', 349.23), 'g': ('F#', 369.99),
        'b': ('G', 392.00), 'h': ('G#', 415.30),
        'n': ('A', 440.00), 'j': ('A#', 466.16),
        'm': ('B', 493.88)
    }

    def __init__(self, base):
        """
        Pianoクラスの初期化

        Args:
            base: Panda3DのShowBaseオブジェクト
            building_list (list): 3D都市を構成する建物のリスト
        """
        self.base = base
        self.building_list = base.building_list
        self.key_to_building = {
            "z": [],
            "x": [],
            "c": [],
            "v": [],
            "b": [],
            "n": [],
            "m": [],
            "s": [],
            "d": [],
            "g": [],
            "h": [],
            "j": []
        }

        # Pyoサーバーの初期化
        self.server = Server().boot()
        self.server.start()

        # 建物の初期高さを設定
        self.initialize_building_heights()

        # キー入力を登録
        self.register_key_events()

        # アプリの停止
        self.base.accept('escape', self.stop)

    def play_tone(self, frequency):
        """
        指定された周波数の音を再生する

        Args:
            frequency (float): 再生する音の周波数（Hz）
        """
        sine_wave = Sine(freq=frequency, mul=0.5)
        sine_wave.out()
        time.sleep(0.5)  # 音を0.5秒再生
        sine_wave.stop()

    def initialize_building_heights(self):
        """
        建物の高さをピアノの鍵盤に対応付けて初期化
        """
        # 7つの鍵盤に対応する建物を設定
        x_step = self.EXTENT / 7
        for building in self.building_list:
            x, y = building.centroid.x, building.centroid.y
            if x < x_step:
                if building.color[0] == 0.0:
                    key = 's'
                else:
                    key = 'z'
            elif x < 1.5 * x_step:
                if building.color[0] == 0.0:
                    key = 's'
                else:
                    key = 'x'
            elif x < 2 * x_step:
                if building.color[0] == 0.0:
                    key = 'd'
                else:
                    key = 'x'
            elif x < 2.5 * x_step:
                if building.color[0] == 0.0:
                    key = 'd'
                else:
                    key = 'c'
            elif x < 3 * x_step:
                key = 'c'
            elif x < 4 * x_step:
                if building.color[0] == 0.0:
                    key = 'g'
                else:
                    key = 'v'
            elif x < 4.5 * x_step:
                if building.color[0] == 0.0:
                    key = 'g'
                else:
                    key = 'b'
            elif x < 5 * x_step:
                if building.color[0] == 0.0:
                    key = 'h'
                else:
                    key = 'b'
            elif x < 5.5 * x_step:
                if building.color[0] == 0.0:
                    key = 'h'
                else:
                    key = 'n'
            elif x < 6 * x_step:
                if building.color[0] == 0.0:
                    key = 'j'
                else:
                    key = 'n'
            elif x < 6.5 * x_step:
                if building.color[0] == 0.0:
                    key = 'j'
                else:
                    key = 'm'
            else:
                key = 'm'
            self.key_to_building[key].append(building)
            # print(f"key: {key}, x: {x}, y: {y}")

    def register_key_events(self):
        """
        キーボード入力をPanda3Dに登録
        """
        for key in self.KEY_MAPPING:
            self.base.accept(key, self.handle_key_press, [key])
            self.base.accept(f"{key}-up", self.handle_key_release, [key])

    def handle_key_press(self, key):
        """
        キー押下時の処理

        Args:
            key (str): 押されたキー
        """
        if key in self.KEY_MAPPING:
            _, frequency = self.KEY_MAPPING[key]
            self.play_tone(frequency)

            for building_key in self.key_to_building:
                if building_key == key:
                    for building in self.key_to_building.get(building_key):
                        if building:
                            if building.node.getSz() != 1:
                                building.node.setSz(1)
                else:
                    for building in self.key_to_building.get(building_key):
                        if building:
                            if building.node.getSz() == 1:
                                building.node.setSz(building.height)

    def handle_key_release(self, key):
        """
        キー解放時の処理

        Args:
            key (str): 解放されたキー
        """
        for building in self.base.building_list:
            if building:
                if building.node.getSz() == 1:
                    building.node.setSz(building.height)

    def stop(self):
        """
        リソースの解放とサーバー停止
        """
        print("アプリケーションを終了しています...")
        self.server.stop()  # Pyoサーバーを停止
        time.sleep(1)
        sys.exit()  # アプリケーションを終了
