import numpy as np
from pydub import AudioSegment
import sounddevice as sd
from queue import Queue
import threading


class Sound:
    def __init__(self, file_path, chunk_size=1024, update_interval=0.1):
        # 音声データの読み込みと前処理
        self.audio = AudioSegment.from_mp3(file_path).set_channels(1).set_frame_rate(44100)
        self.raw_data = np.frombuffer(self.audio.raw_data, dtype=np.int16)
        self.sample_rate = self.audio.frame_rate
        self.chunk_size = chunk_size
        self.update_interval = update_interval

        # 再生用のフレームカウンタ（現在の再生位置を追跡）
        self.audio_frame = [0]

        # 振幅データを格納するキュー（解析結果を格納）
        self.amplitude_queue = Queue()

        # 再生中フラグ（スレッドセーフな状態管理）
        self.is_playing = threading.Event()

    def audio_callback(self, outdata, frames, time, status):
        """
        再生中に呼び出されるコールバック関数。音声データを出力し、振幅データを解析します。

        Args:
            outdata (numpy.ndarray): 出力バッファ。
            frames (int): 再生するフレーム数。
            time: 再生タイミング情報（未使用）。
            status: 再生ステータス情報（未使用）。

        Raises:
            sd.CallbackStop: 音声データが終了した場合。
        """
        # 再生範囲を計算
        start = self.audio_frame[0]
        end = start + frames
        data = self.raw_data[start:end]

        # データが足りない場合（音声の終端）
        if len(data) < frames:
            # ゼロでパディングして無音を補充
            data = np.pad(data, (0, frames - len(data)), 'constant')

            # 出力バッファにデータをコピー
            outdata[:len(data)] = data.reshape(-1, 1)
            outdata[len(data):] = np.zeros((frames - len(data), 1), dtype='int16')

            # 振幅を計算してキューに追加
            amplitude = self._calculate_amplitude(data)
            self.amplitude_queue.put(amplitude)

            # 再生終了を通知
            raise sd.CallbackStop()

        # 通常データ処理
        outdata[:] = data.reshape(-1, 1)

        # 振幅を計算してキューに追加
        amplitude = self._calculate_amplitude(data)
        self.amplitude_queue.put(amplitude)

        # 再生位置を更新
        self.audio_frame[0] += frames

    def play(self):
        """
        音声データの再生を開始します。
        """
        # 再生中フラグをセット
        self.is_playing.set()

        # サウンドデバイスのストリームを開いて再生
        with sd.OutputStream(
            samplerate=self.sample_rate,
            channels=1,
            dtype='int16',
            callback=self.audio_callback,
            blocksize=int(self.sample_rate * self.update_interval)
        ):
            # 音声データの再生時間に応じてスリープ
            sd.sleep(int(len(self.raw_data) / self.sample_rate * 1000))

        # 再生が完了したら再生中フラグをクリア
        self.is_playing.clear()

    def _calculate_amplitude(self, data):
        """
        振幅（RMS値）を計算します。

        Args:
            data (numpy.ndarray): 音声データ。

        Returns:
            float: 振幅のRMS値。
        """
        return np.sqrt(np.mean(data.astype(np.float32) ** 2))
