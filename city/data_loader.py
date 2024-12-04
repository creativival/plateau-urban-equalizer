import os
from mapbox_vector_tile import decode
from .building import Building


class DataLoader:
    def __init__(self, base, zoom_level, tile_x, tile_y):
        self.base = base
        self.zoom_level = zoom_level
        self.tile_x = tile_x
        self.tile_y = tile_y

        # 建物データの読み込み
        self.load_buildings()

    def load_buildings(self):
        """
        建物データを読み込み、Buildingインスタンスを作成してリストに追加します。
        """
        # PBFファイルのパスを構築
        pbf_file = f'{self.zoom_level}/{self.tile_x}/{self.tile_y}.pbf'

        # ファイルが存在するか確認
        if not os.path.isfile(pbf_file):
            print(f"PBFファイルが見つかりません: {pbf_file}")
            return

        # PBFファイルの読み込み
        with open(pbf_file, 'rb') as f:
            tile_data = f.read()
            tile_dict = decode(tile_data)

        # 'bldg' レイヤーのフィーチャーを処理
        for feature in tile_dict.get('bldg', {}).get('features', []):
            building_id = feature.get('id')
            coordinates = feature.get('geometry', {}).get('coordinates')
            building_z = feature.get('properties', {}).get('z')

            if coordinates is None or building_z is None:
                print(f"建物ID {building_id} のデータが不完全です。")
                continue

            # 座標のネストの深さを取得
            depth = self.get_list_depth(coordinates)

            # Buildingインスタンスの作成
            if depth == 3:
                # 単一のポリゴンの場合
                building = Building(self.base, building_id, coordinates[0], building_z)
                self.base.building_list.append(building)
            elif depth == 4:
                # 複数のポリゴン（穴あきポリゴンなど）の場合
                for coords in coordinates:
                    building = Building(self.base, building_id, coords[0], building_z)
                    self.base.building_list.append(building)
            else:
                print(f"建物ID {building_id} の座標の深さが予期しない値です（深さ: {depth}）")

    @staticmethod
    def get_list_depth(lst):
        """
        リストのネストの深さを再帰的に計算します。

        Args:
            lst (list): ネストされたリスト

        Returns:
            int: リストのネストの深さ
        """
        if isinstance(lst, list):
            if not lst:
                return 1  # 空のリストの深さは1
            return 1 + max(DataLoader.get_list_depth(item) for item in lst)
        else:
            return 0
