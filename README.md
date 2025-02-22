# PLATEAU AWARD 2024出展作品　PLATEAU Urban Equalizer

![thumbnail](https://creativival.github.io/plateau-urban-equalizer/images/thumbnail.png)

このアプリは、PLATEAUプロジェクトの3D都市データを活用し、音楽に連動したサウンドエコライザー効果をビジュアル化するアプリケーションです。視覚と聴覚を融合した新しい都市体験を提供します。特にプログラミング初心者向けに詳細なコード解説を行い、自分で作成できるようにサポートしています。

## コード解説

- このアプリの詳細なコード解説を無料で提供しています。解説記事はプログラミング初心者向けに、プログラムの仕組みや作成手順をわかりやすく解説しています。

- 解説記事を参考に、プログラムの仕組みを理解し、自分でカスタマイズしたり、新しいプロジェクトに応用することができます。

- 以下のリンクから閲覧できます。

  - [note: PLATEAU Urban Equalizer 解説記事](https://note.com/creativival/n/nf040a73a152a)

## 主な機能

- **3D都市の構築**  
  PLATEAUプロジェクトが提供する地理データを元に3D都市を構築します。

- **音楽のリアルタイム解析**  
  音楽の振幅をリアルタイムで解析し、そのデータを元に都市エフェクトを生成します。

- **サウンドエコライザー機能**  
  音楽に連動してビルが上下に動き、波形の進行方向を切り替えることができます。

- **カメラ操作**  
  外部視点や内部視点を切り替え、自由に都市を探索できます。

## 利用シーン

『PLATEAU Urban Equalizer』は、3D都市データと音楽解析技術を活用した多機能なアプリケーションです。その応用範囲は幅広く、以下のような利用シーンが想定されています：

### 1. イベントや映像制作
- **まちづくりイベントでの上映**  
  音楽と連動した動きで、観客を魅了する都市エフェクトを提供します。
- **ミュージックビデオやプロモーション映像の背景**  
  ビル群が音楽に合わせて踊るビジュアルは、映像作品に動的な魅力をプラスします。

### 2. 教育と学習
- **工学部や情報系学生向けのプログラミング教材**  
  3Dレンダリングや音楽解析を通じて、実践的なプログラミングスキルを学ぶことができます。
- **初心者向けの学習サポート**  
  詳細なコード解説により、プログラミング初心者でも気軽に学べます。

### 3. アプリケーション開発のベース
- **3D都市アプリケーションのベースとして**  
  エコライザー機能を分離して、ゲーム、エンターテーメント、観光イベント、都市シミュレーション、研究用途などに応用可能です。
- **インタラクティブな都市体験アプリの構築**  
  カスタマイズ可能なコードを活用し、新しい都市体験アプリケーションを開発できます。

## カスタマイズ

『PLATEAU Urban Equalizer』は用途に応じて柔軟なカスタマイズが可能で、ユーザーの目的や好みに応じて設定を変更できます。以下は、主要なカスタマイズ項目の例です。

### 1. 基本設定
アプリの基本設定は、以下のように調整できます（main.py）：

```python
# アプリの基本設定
use_wireframe = False  # ワイヤーフレーム表示の有無（Trueにすると建物が線で描画されます）
use_simplified_coords = True  # 簡略化された座標を使用するかどうか（計算負荷軽減）
image_path = 'images/mirror_ball.png'  # 背景画像のパス
sound_path = 'sound/Dive_To_Mod.mp3'  # 再生する音楽ファイルのパス
```
- use_wireframe: ワイヤーフレーム表示を有効にすると、3D都市が構造として表示されます。デバッグや建物の構造確認に便利です。
- use_simplified_coords: 計算負荷を軽減するため、建物データの座標を簡略化します。高性能PCで精密なモデルを表示したい場合はFalseに設定します。
- image_path: 背景画像を変更することで、アプリの雰囲気を簡単に変えることができます。
- sound_path: 好きな音楽ファイルを指定することで、異なる楽曲に合わせたエフェクトを楽しめます。

### 2. 簡略化の度合い
建物データの頂点数を調整して、パフォーマンスを最適化できます（building.py）：

```python
# 簡略化の度合いを設定（値が大きいほど頂点数が減少）
simplification_tolerance = 30  # 必要に応じて調整
```

- simplification_tolerance: 値を大きくすると建物の形状が単純化され、計算負荷が軽減されます。ただし、形状が簡略化されすぎる場合があるため、適切な値を見つけることが重要です。

### 3. 波形エフェクトの調整

波の動きを調整するパラメータを変更できます（equalizer.py）：

```
wave_length = 500  # 波の長さ（値を大きくすると波が広がります）
wave_speed = 2  # 波の速度（波の進行速度を調整）
wave_height_scale = 1000  # 波の高さ（値を増やすとビルの上下動が大きくなります）
```

- wave_length: 波の長さを調整することで、都市全体の波動効果を変更できます。
- wave_speed: 波が進む速度を調整できます。
- wave_height_scale: ビルの動きの強さを制御します。

### 4. カメラ設定

カメラ操作の初期設定を変更可能です（camera.py）。

```
# 外部カメラの初期位置
self.camera.setPos(2048, -5000, 2048)  # 上空からの俯瞰視点
self.camera.lookAt(0, 0, 0)  # 注視点を都市の中心に設定
```

- 初期位置や注視点を変更して、アプリ起動時のカメラ視点をカスタマイズできます。

### 5. カスタマイズのメリット
- 好みの音楽や画像を使って個性的な都市エフェクトを演出できます。
- 波形エフェクトや簡略化パラメータを調整して、パフォーマンスとビジュアルを両立できます。
- 初心者でも各設定を変更するだけで、アプリケーションの挙動を簡単にカスタマイズ可能です。

ぜひこれらの設定を変更し、自分だけのオリジナル3D都市アプリケーションを作成してください！

## デモ画像

以下は、アプリの実行中の画面です。

![デモ画像1](https://creativival.github.io/plateau-urban-equalizer/images/demo1.png)
![デモ画像2](https://creativival.github.io/plateau-urban-equalizer/images/demo2.png)

## 必要な環境

- Python 3.10以上
- 必要ライブラリ：
  - `panda3d`
  - `pydub`
  - `sounddevice`
  - `numpy`
  - `Pillow`
  - `shapely`
  - `mapbox_vector_tile`

## インストール方法

1. 必要なライブラリをインストールします。
    ```bash
    pip install panda3d pydub sounddevice numpy Pillow shapely mapbox-vector-tile
    ```

2. リポジトリをクローンまたはダウンロードします。

    ```bash
    git clone https://github.com/your-repo/plateau-urban-equalizer.git
    cd plateau-urban-equalizer
    ```

3. PLATEAUプロジェクトの都市データをダウンロードします。このアプリでは処理を簡略化するために、plateau-lod2-mvtのデータセットを使用します。

   - [plateau-lod2-mvt GitHubレポジトリ](https://github.com/indigo-lab/plateau-lod2-mvt)
   - plateau-lod2-mvtは、CC-BY-4.0ライセンスで提供されています。
   - [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.ja)
   - ダウンロードしたデータを14/、15/、16/のフォルダに配置します。


4. 必要なデータ（背景画像、音楽ファイル）を適切なフォルダに配置します。

   - images/mirror_ball.png（背景画像はプロジェクトに収蔵）
   - sound/Dive_To_Mod.mp3（音楽ファイルはダウンロードして下さい。）
   - [Dive To Mod](https://dova-s.jp/bgm/play21452.html)
   - フリーBGM素材「Dive To Mod」by MFP【Marron Fields Production】

5. アプリを起動します。

    ```bash
    python main.py
    ```

## 操作方法

- カメラ操作
  - W / S / A / Dキー: カメラの前後左右移動
  - Q / Eキー: 上下移動
  - マウス: カメラの視点を回転

- アプリの操作
    - Spaceキー: 音楽再生＆エコライザー起動
    - Zキー: 波の進行方向を切り替え
    - Escapeキー: アプリ終了

##  プロジェクト構成

```plaintext
plateau-urban-equalizer/
├── 14/                      # PLATEAUプロジェクトの都市データ
├── 15/                      # PLATEAUプロジェクトの都市データ
├── 16/                      # PLATEAUプロジェクトの都市データ
├── city/
│   ├── building.py          # ビルデータの管理
│   ├── building_render.py   # ビルのレンダリング
│   ├── camera.py            # カメラ操作
│   ├── data_loader.py       # データの読み込み
│   ├── equalizer.py         # サウンドエコライザー機能
│   ├── sound.py             # 音楽解析と再生
│   ├── piano.py             # ピアノ機能（第6章　応用事例）
├── images/
│   └── mirror_ball.png      # 背景画像
├── sound/
│   └── Dive_To_Mod.mp3      # 音楽ファイル 
├── panda3d_example.py       # ウインドウ作成（第3章）
├── building_app_example.py  # ビルの描画（第3章）
├── main_part4.py            # アプリのエントリーポイント（第4章）
├── main.py                  # アプリのエントリーポイント（完成）
├── main_piano.py            # PLATEAU Piano（第6章　応用事例）
├── README.md                # 本ファイル
├── LICENSE                  # ライセンス
```

## 使い方のポイント

- **カスタマイズ**  
  main.py内のタイル座標を変更することで、異なる都市エリアを表示できます。ズームレベルに対応するタイル座標の調べ方は、[noteの解説記事の付録](https://note.com/creativival/n/nf040a73a152a#8f5f5aa9-bf06-493e-9ffd-0345d1dce662)を参照してください。

- **波形のパラメータ調整**  
  equalizer.py内のwave_lengthやwave_speedを変更することで、波形の挙動をカスタマイズ可能です。

- **初心者サポート**  
  各クラスや関数に詳細なコメントが付いており、プログラムの仕組みを学ぶ教材としても活用できます。特に、建築科の学生など、都市データを活用したプロジェクトに興味を持つ方におすすめです。

## トラブルシューティング

各種トラブルシューティングをまとめます。

### サウンド関係

音楽が再生できない原因として、次のようなものがあります。

- **サウンドパスが正しくない**  
  サウンドパスを修正

- **MP３ファイルが壊れている**  
  別のMP3ファイルに入れ替える

- **ffmpegがインストールされていない**  
  - 以下のコマンドでインストール可能です。
  - macOS: brew install ffmpeg
  - Ubuntu: sudo apt install ffmpeg
  - Windows: 公式サイトからダウンロードしてPATHを設定。

### 画像関係

画像が表示できない原因として、次のようなものがあります。

- **画像パスが正しくない**  
  画像パスを修正

- **画像ファイルが壊れている**  
  別の画像ファイルに入れ替える

### 応用事例

![PLATEAU Piano](https://creativival.github.io/plateau-urban-equalizer/images/piano.png)

本アプリケーションの柔軟性を示すため、応用事例として PLATEAU Piano を作成しました。PLATEAU Piano は、3D都市をピアノの鍵盤に見立て、音楽を演奏できるアプリケーションです。

詳しい作成手順やコードの詳細は、以下のリンクからご覧いただけます。この事例を参考に、ぜひ自分だけのオリジナルアプリケーションを作り上げてください！

- [PLATEAU Piano](https://note.com/creativival/n/nf040a73a152a#83633652-8e44-4aab-8aaf-7e7b5f3db92a)

### 他のプラットフォームへの移植

![PLATEAU Urban Equalizer Voyage](https://creativival.github.io/plateau-urban-equalizer/images/visionOS_app.png)

本アプリケーションをベースに、iPhone / iPad / Vision Pro向けのアプリケーションを開発しました。PLATEAU Urban Equalizerは、3D都市データを活用し、音楽に連動したサウンドエコライザー効果をビジュアル化するアプリケーションです。視覚と聴覚を融合した新しい都市体験を提供します。

- [iOS: PLATEAU Urban Equalizer](https://apps.apple.com/us/app/plateau-urban-equalizer/id6739744416)

- [visionOS: PLATEAU Urban Equalizer Voyage](https://apps.apple.com/us/app/plateau-urban-equalizer-voyage/id6740018877)
- 
## ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細は[LICENSEファイル](LICENSE)をご確認ください。

##  貢献

- このアプリを通じてPLATEAUプロジェクトに興味を持ち、都市データを活用したプロジェクトに挑戦していただければ幸いです。
- フィードバックや提案はぜひお寄せください。