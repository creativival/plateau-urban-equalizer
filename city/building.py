from shapely.geometry import Polygon, LinearRing, Point


class Building:
    # 簡略化の度合いを設定（値が大きいほど頂点数が減少）
    simplification_tolerance = 30  # 必要に応じて調整

    def __init__(self, base, building_id, coordinates, building_z):
        self.base = base
        self.id = building_id
        self.coordinates = coordinates
        self.building_z = building_z
        self.height = 0  # ビルの高さ（後で設定）
        self.color = (0.5, 0.5, 0.5, 1)  # デフォルトの色（グレー）

        # 簡略化した座標（初期値は元の座標）
        self.simplified_coords = coordinates

        # 重心の座標
        self.centroid = Point(0, 0)

        # 全ての頂点を含む円の半径（衝突判定用、未使用）
        self.bounding_circle_radius = 0

        # ビルのノードを作成し、シーンに追加
        self.node = base.buildings_node.attachNewNode(str(self.id))

        # ビルのジオメトリを計算し、インスタンス変数を設定
        self.calculate_geometry()

        # 画像からビルの色を取得
        self.extract_color_from_image(self.centroid.x, self.centroid.y)

    def calculate_geometry(self):
        """
        ビルのジオメトリ情報を計算し、インスタンス変数に設定します。
        """
        # 座標からシェイプリーのポリゴンを作成
        linear_ring = LinearRing(self.coordinates)
        polygon = Polygon(linear_ring)

        # ポリゴンの簡略化を行うかどうか
        if self.base.use_simplified_coords:
            # トポロジーを保持しつつ簡略化
            simplified_polygon = polygon.simplify(self.simplification_tolerance, preserve_topology=True)
        else:
            simplified_polygon = polygon  # 簡略化しない

        # 簡略化した頂点座標を取得
        self.simplified_coords = list(simplified_polygon.exterior.coords)

        # 重心の計算
        self.centroid = simplified_polygon.centroid

        # 包含円の半径を計算（衝突判定用）
        all_points = [Point(pt) for pt in self.simplified_coords]
        self.bounding_circle_radius = self.calculate_bounding_circle_radius(all_points, self.centroid)

        # 元の頂点数と簡略化後の頂点数を記録
        self.base.vertex_count += len(polygon.exterior.coords)
        self.base.simplified_vertex_count += len(simplified_polygon.exterior.coords)

    def extract_color_from_image(self, x, y):
        """
        ビルの重心座標から画像の対応する色を取得し、ビルの色として設定します。

        Args:
            x (float): 重心のX座標
            y (float): 重心のY座標
        """
        # ビルの座標範囲を画像のサイズにマッピング
        x_min, x_max = 0, 4096
        y_min, y_max = 0, 4096

        # 座標を画像のピクセル座標に変換
        pixel_x = int((x - x_min) / (x_max - x_min) * self.base.image_width)
        pixel_y = int((y - y_min) / (y_max - y_min) * self.base.image_height)

        # 画像の範囲内に収まるようにクリップ
        pixel_x = max(0, min(self.base.image_width - 1, pixel_x))
        pixel_y = max(0, min(self.base.image_height - 1, pixel_y))

        # 画像のY軸は上が0なので、Y座標を反転
        pixel_y = self.base.image_height - pixel_y - 1

        # ピクセルの色を取得
        color = self.base.background_image.getpixel((pixel_x, pixel_y))

        # RGBA値を0〜1の範囲に正規化して設定
        if len(color) == 4:
            r, g, b, a = color
        else:
            r, g, b = color
            a = 255  # アルファ値がない場合は255（不透明）

        self.color = (r / 255.0, g / 255.0, b / 255.0, a / 255.0)

    @staticmethod
    def calculate_bounding_circle_radius(points, centroid):
        """
        重心から各頂点までの距離を計算し、最大値を包含円の半径として返します。

        Args:
            points (list of Point): 頂点のリスト
            centroid (Point): 重心の座標

        Returns:
            float: 包含円の半径
        """
        # 重心から各ポイントまでの距離のリストを作成
        distances = [centroid.distance(point) for point in points]
        # 最大距離を半径として返す
        return max(distances)

    @staticmethod
    def calculate_centroid(points):
        """
        与えられたポイントの集合から重心を計算して返します。

        Args:
            points (list of Point): ポイントのリスト

        Returns:
            Point: 重心の座標
        """
        x_coords = [point.x for point in points]
        y_coords = [point.y for point in points]
        centroid_x = sum(x_coords) / len(x_coords)
        centroid_y = sum(y_coords) / len(y_coords)
        return Point(centroid_x, centroid_y)
