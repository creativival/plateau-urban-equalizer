import math
from direct.stdpy import threading
from queue import Empty


class Equalizer:
    # 波のパラメータ
    wave_length = 500  # 波の長さ（空間的な波長）
    wave_speed = 2  # 波の速度（値を調整して波の進行速度を変える）
    wave_height_scale = 1000  # 波の高さを調整するスケール

    def __init__(self, base):
        self.base = base
        # 波の進行方向
        self.wave_directions = ['concentric', 'x_axis', 'y_axis', 'xy_axes']
        self.wave_direction_id = 0
        self.wave_direction = self.wave_directions[self.wave_direction_id]
        self.sound_thread = None

        # サウンドの再生とビルの高さ更新
        self.base.accept('space', self.play_app)

        # 波の進行方向を切り替え
        self.base.accept('z', self.switch_wave_direction)

    def switch_wave_direction(self):
        self.wave_direction_id = (self.wave_direction_id + 1) % len(self.wave_directions)
        self.wave_direction = self.wave_directions[self.wave_direction_id]
        print('Wave direction:', self.wave_direction)

    def play_app(self):
        if self.base.sound.is_playing.is_set():
            return

        self.play_sound()
        self.start_equalizer()

    def play_sound(self):
        # サウンドの再生を別スレッドで開始
        self.sound_thread = threading.Thread(target=self.base.sound.play)
        self.sound_thread.start()

    def start_equalizer(self):
        # ビルの高さを更新するタスクを追加
        self.base.taskMgr.doMethodLater(0.1, self.update_buildings_height_task, 'UpdateBuildingsTask')

    def update_buildings_height_task(self, task):
        if not self.base.sound.is_playing.is_set() and self.base.sound.amplitude_queue.empty():
            return task.done  # サウンドの再生が終了したらタスクを停止

        try:
            # 振幅データを取得
            amplitude = self.base.sound.amplitude_queue.get_nowait()
        except Empty:
            # 振幅データがまだない場合は次のフレームへ
            return task.cont

        # 振幅を正規化（0〜1の範囲）
        max_amplitude = 32768  # int16の最大値
        normalized_amplitude = amplitude / max_amplitude

        # 現在の時間を取得
        current_time = globalClock.getFrameTime()

        # ビルの高さを更新
        for building in self.base.building_list:
            x, y = building.centroid.x, building.centroid.y

            # 波の位相を計算
            if self.wave_direction == 'x_axis':
                phase = x / self.wave_length - self.wave_speed * current_time
            elif self.wave_direction == 'y_axis':
                phase = y / self.wave_length - self.wave_speed * current_time
            elif self.wave_direction == 'xy_axes':
                phase = (x + y) / self.wave_length - self.wave_speed * current_time
            else:  # 'concentric'
                phase = math.sqrt((x - 2048) ** 2 + (y - 2048) ** 2) / self.wave_length - self.wave_speed * current_time

            # 波の高さを計算
            wave_height = normalized_amplitude * math.sin(phase) * self.wave_height_scale + self.wave_height_scale / 4

            # ビルの高さを更新
            if building.node:
                building.node.setSz(max(wave_height, 1))  # 最小高さを1に設定

        return task.cont  # タスクを継続
