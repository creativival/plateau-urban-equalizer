from panda3d.core import GeomVertexFormat, GeomVertexData, GeomVertexWriter
from panda3d.core import Geom, GeomTriangles, GeomNode


class BuildingRenderer:
    # ズームレベルごとの高さ補正係数
    Z_SCALES = {
        14: 2.695,
        15: 5.390,
        16: 10.780
    }

    def __init__(self, building):
        base_coords = building.simplified_coords

        # 頂点データが閉じているかチェックし、閉じていなければ閉じる
        base_coords = BuildingRenderer.ensure_closed(base_coords)

        # 頂点が右回りか左回りか判定し、左回りに調整して面が描画されるようにする
        if BuildingRenderer.is_clockwise(base_coords):
            base_coords = base_coords[::-1]  # 順序を反転

        # 高さの補正
        building.height = building.building_z * BuildingRenderer.Z_SCALES[building.base.zoom_level]

        # 頂点データの作成
        format = GeomVertexFormat.getV3c4()  # 3次元座標とRGBA色を持つフォーマット
        vdata = GeomVertexData('building', format, Geom.UHStatic)  # 静的なデータ
        vertex = GeomVertexWriter(vdata, 'vertex')  # 頂点データのライター
        color_writer = GeomVertexWriter(vdata, 'color')  # 色データのライター

        # ライターを使って頂点を追加（底面と上面）
        for x, y in base_coords:
            # 底面の頂点
            vertex.addData3f(x, y, 0)
            color_writer.addData4f(*building.color)
        for x, y in base_coords:
            # 上面の頂点
            vertex.addData3f(x, y, 1)
            color_writer.addData4f(*building.color)

        # プリミティブ（基本形状）の作成
        tris = GeomTriangles(Geom.UHStatic)

        # 上面のポリゴンを作成するため、プリミティブに頂点を登録する
        # 多角形を三角形に分割する
        num_vertices = len(base_coords)
        for i in range(1, num_vertices - 2):
            # 三角形の頂点インデックスを登録
            tris.addVertices(num_vertices + 0, num_vertices + i, num_vertices + i + 1)

        # 側面のポリゴンを作成ため、プリミティブに頂点を登録する
        for i in range(num_vertices - 1):
            # 側面を構成する頂点インデックス
            idx0 = i
            idx1 = i + 1
            idx2 = num_vertices + i + 1
            idx3 = num_vertices + i

            # 側面を2つの三角形で構成
            tris.addVertices(idx0, idx1, idx2)
            tris.addVertices(idx0, idx2, idx3)

        # ジオメトリの作成
        geom = Geom(vdata)  # 頂点データからジオメトリを作成
        geom.addPrimitive(tris)  # プリミティブを追加
        node = GeomNode('building')  # GeomNodeノードを作成
        node.addGeom(geom)  # ジオメトリをノードに追加
        building_nodepath = building.node.attachNewNode(node)  # ノードをシーンに追加

        # ビルの高さを設定
        building.node.setSz(building.height)

        # ワイヤーフレーム表示に設定
        if building.base.use_wireframe:
            building_nodepath.setRenderModeWireframe()
            building_nodepath.setRenderModeThickness(2)  # 線の太さを調整（任意）

    @staticmethod
    def ensure_closed(coords):
        """
        頂点リストが閉じているかをチェックし、閉じていない場合は最初の頂点をリストの最後に追加する。

        Args:
            coords (list of tuple): 頂点の座標リスト

        Returns:
            list of tuple: 閉じた頂点の座標リスト
        """
        if coords[0] != coords[-1]:
            coords.append(coords[0])
        return coords

    @staticmethod
    def is_clockwise(coords):
        """
        多角形の頂点座標を受け取り、時計回りか反時計回りかを判定します。

        Args:
            coords: 多角形の頂点座標のリスト。各頂点は(x, y)のタプルまたはリストで表されます。

        Returns:
            時計回りの場合はTrue、反時計回りの場合はFalse、点が一直線上にある場合はNoneを返します。
        """
        if len(coords) < 3:
            return None  # 3点未満では多角形を形成しない

        # 外積の総和を計算
        sum_cross_product = 0
        for i in range(len(coords)):
            x1, y1 = coords[i]
            x2, y2 = coords[(i + 1) % len(coords)]  # 次の頂点、最後は最初の頂点に戻る
            sum_cross_product += (x2 - x1) * (y2 + y1)

        if sum_cross_product > 0:
            return True  # 時計回り
        elif sum_cross_product < 0:
            return False  # 反時計回り
        else:
            return None  # 点が一直線上
