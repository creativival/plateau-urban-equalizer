from panda3d.core import WindowProperties


class Camera:
    heading_angular_velocity = 1500  # カメラの水平回転速度
    pitch_angular_velocity = 500  # カメラの垂直回転速度
    max_pitch_angle = 60  # カメラの最大ピッチ角度
    min_pitch_angle = -80  # カメラの最小ピッチ角度

    def __init__(self, base):
        self.base = base
        self.mode = 'external'  # 'external'（外部視点）または 'internal'（内部視点）

        # カメラの初期設定
        self.setup_cameras()

        # キー入力のマッピング
        self.base.accept('c', self.toggle_mode)  # 'c'キーでカメラモードを切り替え

        # キー入力状態を管理するマップ
        self.key_map = {
            "forward": False, "backward": False,
            "left": False, "right": False,
            "up": False, "down": False
        }
        self.mouse_sensitivity = 0.2  # マウス感度

        # キー入力の受付
        self.setup_key_bindings()

        # マウスの初期設定
        self.disable_mouse_control()  # マウスを非アクティブ化
        self.prev_mouse_pos = (0, 0)  # 前フレームのマウス位置

        # カメラ制御のタスクを登録
        self.base.taskMgr.add(self.update, 'camera_update_task')

    def setup_cameras(self):
        """
        カメラの初期設定を行います。
        現在のモード（external/internal）に応じて設定を変更します。
        """
        if self.mode == 'external':
            self.setup_external_camera()
        elif self.mode == 'internal':
            self.setup_internal_camera()

    def setup_external_camera(self):
        """
        外部カメラの設定を行います。
        """
        self.base.disableMouse()  # デフォルトのカメラ制御を無効化
        self.base.camera.setPos(2048, -5000, 2048)  # カメラを上空に配置
        self.base.camera.lookAt(0, 0, 0)  # 原点を注視
        self.enable_mouse_control()  # マウスでカメラを回転可能にする

    def setup_internal_camera(self):
        """
        内部カメラの設定を行います。
        """
        self.base.disableMouse()
        self.base.camera.setPos(0, 0, 1.6)  # カメラを地面上に配置
        self.base.camera.setHpr(0, 0, 0)  # カメラの回転を初期化
        self.disable_mouse_control()

    def toggle_mode(self):
        """
        カメラモードを切り替えます。
        """
        self.mode = 'internal' if self.mode == 'external' else 'external'
        self.setup_cameras()

    def setup_key_bindings(self):
        """
        キー入力のマッピングを設定します。
        """
        key_actions = [
            ('w', 'forward', True), ('w-up', 'forward', False),
            ('s', 'backward', True), ('s-up', 'backward', False),
            ('a', 'left', True), ('a-up', 'left', False),
            ('d', 'right', True), ('d-up', 'right', False),
            ('q', 'up', True), ('q-up', 'up', False),
            ('e', 'down', True), ('e-up', 'down', False),
        ]
        for key, action, value in key_actions:
            self.base.accept(key, self.set_key, [action, value])

    def set_key(self, key, value):
        """
        キー入力状態を設定します。

        Args:
            key (str): キー名。
            value (bool): キーの状態（True: 押下、False: 離された）。
        """
        self.key_map[key] = value

    def enable_mouse_control(self):
        """
        マウス制御を有効化し、カーソルを非表示にします。
        """
        props = WindowProperties()
        props.setCursorHidden(True)
        self.base.win.requestProperties(props)
        self.base.win.movePointer(0, int(self.base.win.getProperties().getXSize() / 2),
                                  int(self.base.win.getProperties().getYSize() / 2))
        self.prev_mouse_pos = None

    def disable_mouse_control(self):
        """
        マウス制御を無効化し、カーソルを表示します。
        """
        props = WindowProperties()
        props.setCursorHidden(False)
        self.base.win.requestProperties(props)

    def update(self, task):
        """
        カメラの状態を更新するタスク。

        Args:
            task: Panda3Dのタスクオブジェクト。

        Returns:
            task.cont: タスクを継続する。
        """
        dt = globalClock.getDt()
        if self.mode == 'internal':
            self.control_internal_camera(dt)
        elif self.mode == 'external':
            self.control_external_camera(dt)
        return task.cont

    def control_internal_camera(self, dt):
        """
        内部カメラ（プレイヤー視点）の制御。

        Args:
            dt (float): フレーム間の経過時間。
        """
        speed = 200 * dt
        x_direction = self.base.camera.getMat().getRow3(0)
        y_direction = self.base.camera.getMat().getRow3(1)
        camera_x, camera_y, camera_z = self.base.camera.getPos()

        if self.key_map['forward']:
            camera_x = camera_x + y_direction.x * speed
            camera_y = camera_y + y_direction.y * speed
        if self.key_map['backward']:
            camera_x = camera_x - y_direction.x * speed
            camera_y = camera_y - y_direction.y * speed
        if self.key_map['left']:
            camera_x = camera_x - x_direction.x * speed
            camera_y = camera_y - x_direction.y * speed
        if self.key_map['right']:
            camera_x = camera_x + x_direction.x * speed
            camera_y = camera_y + x_direction.y * speed
        if self.key_map['up']:
            camera_z = camera_z + speed
        if self.key_map['down']:
            camera_z = camera_z - speed

        self.base.camera.setPos(camera_x, camera_y, camera_z)

        # マウスによる視点の回転
        if self.base.mouseWatcherNode.hasMouse():
            x = self.base.mouseWatcherNode.getMouseX()
            y = self.base.mouseWatcherNode.getMouseY()
            if self.prev_mouse_pos is not None:
                dx = x - self.prev_mouse_pos[0]
                dy = y - self.prev_mouse_pos[1]
                heading = self.base.camera.getH() - dx * Camera.heading_angular_velocity * speed
                pitch = self.base.camera.getP() + dy * Camera.pitch_angular_velocity * speed
                pitch = min(Camera.max_pitch_angle, max(Camera.min_pitch_angle, pitch))
                self.base.camera.setH(heading)
                self.base.camera.setP(pitch)
            self.prev_mouse_pos = (x, y)

    def control_external_camera(self, dt):
        """
        外部カメラ（鳥瞰視点）の制御。

        Args:
            dt (float): フレーム間の経過時間。
        """
        speed = 500 * dt
        if self.key_map['forward']:
            self.base.camera.setY(self.base.camera, speed)
        if self.key_map['backward']:
            self.base.camera.setY(self.base.camera, -speed)
        if self.key_map['left']:
            self.base.camera.setX(self.base.camera, -speed)
        if self.key_map['right']:
            self.base.camera.setX(self.base.camera, speed)
        if self.key_map['up']:
            self.base.camera.setZ(self.base.camera.getZ() + speed)
        if self.key_map['down']:
            self.base.camera.setZ(self.base.camera.getZ() - speed)

        # マウスによるカメラの回転
        if self.base.mouseWatcherNode.hasMouse():
            x = self.base.mouseWatcherNode.getMouseX()
            y = self.base.mouseWatcherNode.getMouseY()
            if self.prev_mouse_pos is not None:
                dx = x - self.prev_mouse_pos[0]
                dy = y - self.prev_mouse_pos[1]
                self.base.camera.setH(self.base.camera.getH() - dx * 100 * self.mouse_sensitivity)
                self.base.camera.setP(self.base.camera.getP() - dy * 100 * self.mouse_sensitivity)
            self.prev_mouse_pos = (x, y)
