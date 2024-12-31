import os
import sqlite3
import json
from mapbox_vector_tile import decode  # PBFファイルのデコードに使用
from city.building import Building  # 既存のBuildingクラスをcityフォルダーからインポート
from city.building_render import BuildingRenderer


class BuildingDataManager:
    def __init__(self, db_name, base=None, root_folder="14"):
        """
        BuildingDataManagerクラスの初期化
        Args:
            db_path (str): SQLite3データベースのパス
            base: Buildingクラスで必要なBaseオブジェクト
            root_folder (str): PBFファイルを走査するルートフォルダー
        """
        self.db_path = f'database/{db_name}'
        self.base = base
        self.root_folder = root_folder
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        """
        データベースにテーブルを作成し、z_x_yに基づくインデックスを作成
        """
        # テーブル作成
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS buildings (
            id INTEGER PRIMARY KEY,
            z_x_y TEXT NOT NULL,
            building_id INTEGER,
            coordinates TEXT,
            simplified_coords TEXT,
            building_z REAL,
            centroid_x REAL,
            centroid_y REAL,
            bounding_circle_radius REAL
        )
        ''')

        # z_x_yのインデックス作成
        self.cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_z_x_y ON buildings (z_x_y);
        ''')

        # コミットして変更を保存
        self.conn.commit()

    def ensure_counterclockwise(self, coords):
        """
        座標が時計回りの場合は反転して反時計回りにする

        Args:
            coords: 多角形の頂点座標のリスト

        Returns:
            反時計回りの座標リスト
        """
        if BuildingRenderer.is_clockwise(coords):
            return coords[::-1]  # 反転して反時計回りにする
        return coords

    def save_building_to_db(self, pbf_file, building):
        """
        Buildingオブジェクトをデータベースに保存
        Args:
            pbf_file (str): PBFファイル名（例: 15/29117/12892.pbf）
            building (Building): 保存対象のBuildingオブジェクト
        """
        coordinates_str = json.dumps(building.coordinates)
        simplified_coords_str = json.dumps(building.simplified_coords)
        z_x_y = pbf_file.split('.pbf')[0].replace('/', '_')

        self.cursor.execute(
            '''
            INSERT INTO buildings (
                z_x_y, building_id, coordinates, simplified_coords,
                building_z, centroid_x, centroid_y, bounding_circle_radius
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''',
            (
                z_x_y,
                building.id,
                coordinates_str,
                simplified_coords_str,
                building.building_z,
                building.centroid.x,
                building.centroid.y,
                building.bounding_circle_radius,
            )
        )

    def process_pbf_file(self, pbf_file):
        """
        PBFファイルを処理してデータベースに保存
        Args:
            folder_name (str): PBFファイルが含まれるフォルダー名
            pbf_file (str): PBFファイルのパス
        """
        try:
            # PBFファイルを読み込む
            with open(pbf_file, 'rb') as f:
                tile_data = f.read()

            # PBFデータをデコード
            tile_dict = decode(tile_data)

            # 'bldg' レイヤーを対象に処理
            features = tile_dict.get('bldg', {}).get('features', [])
            if not features:
                print(f"No building data found in {pbf_file}")
                return

            # 建物データを処理
            for feature in features:
                building_id = feature.get('id')
                geometry = feature.get('geometry', {}).get('coordinates')
                building_z = feature.get('properties', {}).get('z')

                if not geometry or building_z is None:
                    print(f"Incomplete data for building ID {building_id} in {pbf_file}")
                    continue

                # 座標のネストの深さをチェック
                depth = self.get_list_depth(geometry)

                # Buildingオブジェクトを作成
                if depth == 3:
                    # 単一のポリゴン
                    coordinates = self.ensure_counterclockwise(geometry[0])  # 時計回りを修正
                    building = Building(
                        base=self.base,
                        building_id=building_id,
                        coordinates=coordinates,
                        building_z=building_z
                    )
                    building.calculate_geometry()
                    self.save_building_to_db(pbf_file, building)
                elif depth == 4:
                    # 複数のポリゴン（例: 穴あきポリゴン）
                    for polygon in geometry:
                        coordinates = self.ensure_counterclockwise(polygon[0])  # 時計回りを修正
                        building = Building(
                            base=self.base,
                            building_id=building_id,
                            coordinates=coordinates,
                            building_z=building_z
                        )
                        building.calculate_geometry()
                        self.save_building_to_db(pbf_file, building)
                else:
                    print(f"Unexpected geometry depth for building ID {building_id} in {pbf_file}")

            self.conn.commit()
        except Exception as e:
            print(f"Error processing file {pbf_file}: {e}")

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
            return 1 + max(BuildingDataManager.get_list_depth(item) for item in lst)
        else:
            return 0

    def process_all_pbf_files(self):
        """
        ルートフォルダー内の全てのPBFファイルを処理
        """
        for root, _, files in os.walk(self.root_folder):
            for file_name in files:
                if file_name.endswith(".pbf"):
                    pbf_path = os.path.join(root, file_name)
                    print(f"Processing {pbf_path}")
                    self.process_pbf_file(pbf_path)

    def close(self):
        """
        データベース接続を閉じる
        """
        self.conn.close()


if __name__ == "__main__":
    # 使用例
    base = None  # 必要ならBaseオブジェクトを渡す
    manager = BuildingDataManager(db_name='buildings_10_11_12_13_14.db', root_folder="14")
    manager.process_all_pbf_files()
    manager.close()
