import sys
import time
from pyo import *


class Piano:
    EXTENT = 4096
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
        """
        self.base = base
        self.building_list = base.building_list
        self.key_to_building = {key: [] for key in self.KEY_MAPPING}
        self.key_map = {key: False for key in self.KEY_MAPPING}  # 各キーの状態を管理

        # Pyoサーバーの初期化
        self.server = Server().boot()
        self.server.start()

        # 建物の初期高さを設定
        self.initialize_key_to_building()

        # キー入力を登録
        self.register_key_events()

        # 高さの更新タスクを追加
        self.base.taskMgr.add(self.update_building_heights, "UpdateBuildingHeights")

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

    def initialize_key_to_building(self):
        """
        建物をピアノの鍵盤に対応付ける
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
            self.key_map[key] = True  # キー状態を更新
            _, frequency = self.KEY_MAPPING[key]
            self.play_tone(frequency)

    def handle_key_release(self, key):
        """
        キー解放時の処理

        Args:
            key (str): 解放されたキー
        """
        if key in self.KEY_MAPPING:
            self.key_map[key] = False  # キー状態を更新

    def update_building_heights(self, task):
        """
        キー入力状態に基づいて建物の高さを更新するタスク

        Args:
            task: Panda3Dのタスク
        """
        for key, is_pressed in self.key_map.items():
            for building in self.key_to_building[key]:
                if is_pressed:
                    if building.node.getSz() != 1:
                        building.node.setSz(1)
                else:
                    if building.node.getSz() == 1:
                        building.node.setSz(building.height)
        return task.cont

    def stop(self):
        """
        リソースの解放とサーバー停止
        """
        print("アプリケーションを終了しています...")
        self.server.stop()  # Pyoサーバーを停止
        time.sleep(1)
        sys.exit()  # アプリケーションを終了
