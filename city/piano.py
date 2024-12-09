import sys
import time
import numpy as np
import simpleaudio as sa


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

        # 建物の初期高さを設定
        self.initialize_key_to_building()

        # キー入力を登録
        self.register_key_events()

        # 高さの更新タスクを追加
        self.base.taskMgr.add(self.update_building_heights, "UpdateBuildingHeights")

    def generate_sine_wave(self, frequency, duration=0.5, sample_rate=44100, amplitude=0.5):
        """
        サイン波を生成

        Args:
            frequency (float): 周波数（Hz）
            duration (float): 継続時間（秒）
            sample_rate (int): サンプルレート
            amplitude (float): 音量（0.0〜1.0）

        Returns:
            numpy.ndarray: 音声データ
        """
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        wave = amplitude * np.sin(2 * np.pi * frequency * t)
        audio = (wave * 32767).astype(np.int16)  # 16-bit PCM形式に変換
        return audio

    def play_tone(self, frequency):
        """
        指定された周波数の音を再生

        Args:
            frequency (float): 再生する音の周波数（Hz）
        """
        audio = self.generate_sine_wave(frequency)
        play_obj = sa.play_buffer(audio, 1, 2, 44100)
        play_obj.wait_done()

    def initialize_key_to_building(self):
        """
        建物をピアノの鍵盤に対応付ける
        """
        # 7つの鍵盤に対応する建物を設定
        x_step = self.EXTENT / 7
        for building in self.building_list:
            x, y = building.centroid.x, building.centroid.y
            if x < x_step:
                if self.is_black(building.color):
                    key = 's'
                else:
                    key = 'z'
            elif x < 1.5 * x_step:
                if self.is_black(building.color):
                    key = 's'
                else:
                    key = 'x'
            elif x < 2 * x_step:
                if self.is_black(building.color):
                    key = 'd'
                else:
                    key = 'x'
            elif x < 2.5 * x_step:
                if self.is_black(building.color):
                    key = 'd'
                else:
                    key = 'c'
            elif x < 3 * x_step:
                key = 'c'
            elif x < 4 * x_step:
                if self.is_black(building.color):
                    key = 'g'
                else:
                    key = 'v'
            elif x < 4.5 * x_step:
                if self.is_black(building.color):
                    key = 'g'
                else:
                    key = 'b'
            elif x < 5 * x_step:
                if self.is_black(building.color):
                    key = 'h'
                else:
                    key = 'b'
            elif x < 5.5 * x_step:
                if self.is_black(building.color):
                    key = 'h'
                else:
                    key = 'n'
            elif x < 6 * x_step:
                if self.is_black(building.color):
                    key = 'j'
                else:
                    key = 'n'
            elif x < 6.5 * x_step:
                if self.is_black(building.color):
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
    
    @staticmethod
    def is_black(color):
        """
        色が黒かどうかを判定

        Args:
            color (tuple): RGBの色情報

        Returns:
            bool: 黒の場合はTrue、それ以外はFalse
        """
        return color[0] == 0.0 and color[1] == 0.0 and color[2] == 0.0
