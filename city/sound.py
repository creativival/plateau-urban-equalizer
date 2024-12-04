import numpy as np
from pydub import AudioSegment
import sounddevice as sd
from queue import Queue
import threading


class Sound:
    def __init__(self, file_path, chunk_size=1024, update_interval=0.1):
        # MP3ファイルの読み込みと前処理
        self.audio = AudioSegment.from_mp3(file_path)
        self.audio = self.audio.set_channels(1)  # モノラルに変換
        self.audio = self.audio.set_frame_rate(44100)  # サンプリングレートを設定

        # 音声データをNumPy配列に変換
        self.raw_data = np.frombuffer(self.audio.raw_data, dtype=np.int16)
        self.sample_rate = self.audio.frame_rate
        self.chunk_size = chunk_size
        self.update_interval = update_interval

        # 再生用のフレームカウンタ（現在の再生位置を追跡）
        self.audio_frame = [0]

        # 振幅データを格納するキュー（解析結果を格納）
        self.amplitude_queue = Queue()

        # 再生中フラグ（Trueなら再生中）
        self.is_playing = threading.Event()

    def audio_callback(self, outdata, frames, time, status):
        """
        再生中に呼び出されるコールバック関数。

        Args:
            outdata (numpy.ndarray): 出力バッファ。
            frames (int): 再生するフレーム数。
            time: 再生タイミング情報（未使用）。
            status: 再生ステータス情報（未使用）。

        Raises:
            sd.CallbackStop: 音声データが終了した場合に再生を停止。
        """
        # 再生位置を計算
        start = self.audio_frame[0]
        end = start + frames

        # チャンクサイズ分のデータを取得
        data = self.raw_data[start:end]

        # データが足りない場合（音声データの終端に到達）
        if len(data) < frames:
            # 足りない部分をゼロで埋める（無音にする）
            data = np.pad(data, (0, frames - len(data)), 'constant')
            outdata[:len(data)] = data.reshape(-1, 1)
            outdata[len(data):] = np.zeros((frames - len(data), 1), dtype='int16')

            # 振幅を計算してキューに追加
            amplitude = np.sqrt(np.mean(data.astype(np.float32) ** 2))
            self.amplitude_queue.put(amplitude)

            # 再生を停止
            raise sd.CallbackStop()
        else:
            # データを出力バッファにコピー
            outdata[:] = data.reshape(-1, 1)

            # 振幅を計算してキューに追加
            amplitude = np.sqrt(np.mean(data.astype(np.float32) ** 2))
            self.amplitude_queue.put(amplitude)

        # 再生位置を更新
        self.audio_frame[0] += frames

    def play(self):
        """
        音声データの再生を開始します。
        再生中に振幅データを解析し、キューに格納します。
        """
        # 再生中フラグをセット
        self.is_playing.set()

        # ストリーミング再生を開始
        with sd.OutputStream(
            samplerate=self.sample_rate,  # サンプリングレート
            channels=1,  # モノラル
            dtype='int16',  # データ型
            callback=self.audio_callback,  # コールバック関数
            blocksize=int(self.sample_rate * self.update_interval)  # 更新間隔をフレーム数に変換
        ):
            # 再生が完了するまでスリープ
            sd.sleep(int(len(self.raw_data) / self.sample_rate * 1000))

        # 再生中フラグをクリア
        self.is_playing.clear()
