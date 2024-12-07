# PLATEAU AWARD 2024出展作品　PLATEAU Urban Equalizer

![thumbnail](https://creativival.github.io/plateau-urban-equalizer/images/thumbnail.png)

このアプリは、PLATEAUプロジェクトの3D都市データを活用し、音楽に連動したサウンドエコライザー効果をビジュアル化するアプリケーションです。視覚と聴覚を融合した新しい都市体験を提供します。特にプログラミング初心者向けに詳細なコード解説を行い、自分で作成できるようにサポートしています。

## コード解説

- このアプリの詳細なコード解説を無料で提供しています。解説記事はプログラミング初心者向けに、プログラムの仕組みや作成手順をわかりやすく解説しています。

- 解説記事を参考に、プログラムの仕組みを理解し、自分でカスタマイズしたり、新しいプロジェクトに応用することができます。

- 以下のリンクから閲覧できます。

  - [note: PLATEAU Urban Equalize解説記事](https://note.com/creativival/n/nf040a73a152a)

## 主な機能

- **3D都市の構築**  
  PLATEAUプロジェクトが提供する地理データを元に3D都市を構築します。

- **音楽のリアルタイム解析**  
  音楽の振幅をリアルタイムで解析し、そのデータを元に都市エフェクトを生成します。

- **サウンドエコライザー機能**  
  音楽に連動してビルが上下に動き、波形の進行方向を切り替えることができます。

- **カメラ操作**  
  外部視点や内部視点を切り替え、自由に都市を探索できます。

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
├── images/
│   └── mirror_ball.png      # 背景画像
├── sound/
│   └── Dive_To_Mod.mp3      # 音楽ファイル 
├── panda3d_example.py       # ウインドウ作成（第3章）
├── building_app_example.py  # ビルの描画（第3章）
├── main_part4.py            # アプリのエントリーポイント（第4章）
├── main.py                  # アプリのエントリーポイント（完成）
├── README.md                # 本ファイル
├── LICENSE                  # ライセンス
```

## 使い方のポイント

- **カスタマイズ**  
  main.py内のタイル座標を変更することで、異なる都市エリアを表示できます。ズームレベルに対応するタイル座標の調べ方は、上記の解説記事の付録を参照してください。

- **波形のパラメータ調整**  
  equalizer.py内のwave_lengthやwave_speedを変更することで、波形の挙動をカスタマイズ可能です。

- **初心者サポート**  
  各クラスや関数に詳細なコメントが付いており、プログラムの仕組みを学ぶ教材としても活用できます。特に、建築科の学生など、都市データを活用したプロジェクトに興味を持つ方におすすめです。

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細は[LICENSEファイル](LICENSE)をご確認ください。

##  貢献

- このアプリを通じてPLATEAUプロジェクトに興味を持ち、都市データを活用したプロジェクトに挑戦していただければ幸いです。
- フィードバックや提案はぜひお寄せください。