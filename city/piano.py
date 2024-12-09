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
        self.key_to_building = {}

        # Pyoサーバーの初期化
        self.server = Server().boot()
        self.server.start()

        # 建物の初期高さを設定
        self.initialize_building_heights()

        # キー入力を登録
        self.register_key_events()

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
                key = 'z'
            elif x < 2 * x_step:
                key = 'x'
            elif x < 3 * x_step:
                key = 'c'
            elif x < 4 * x_step:
                key = 'v'
            elif x < 5 * x_step:
                key = 'b'
            elif x < 6 * x_step:
                key = 'n'
            else:
                key = 'm'
            self.key_to_building[key] = building
            print(f"key: {key}, x: {x}, y: {y}")

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

    def handle_key_release(self, key):
        """
        キー解放時の処理

        Args:
            key (str): 解放されたキー
        """
        if key in self.KEY_MAPPING:
            building = self.key_to_building.get(key)
            if building:
                building.node.setSz(5)
