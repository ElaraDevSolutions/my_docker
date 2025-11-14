import sys
import traceback
import docker
import threading

from PyQt6.QtCore import QTimer, pyqtSignal, QObject, Qt
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtWidgets import (
    QApplication,
    QGridLayout,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QListWidget,
    QMenu,
    QMessageBox,
    QSystemTrayIcon,
    QPushButton,
    QWidget,
)
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtCore import QUrl


class TrayIcon(QSystemTrayIcon):
    def __init__(self, app):
        super(TrayIcon, self).__init__(QIcon('icon.png'), parent=app)
        self.setToolTip("My Docker")


class Details(QWidget):
    def __init__(self):
        super(Details, self).__init__()
        self.setWindowTitle("My Docker")
        self.setGeometry(300, 300, 640, 480)
        layout = Layout()

        self.setLayout(layout)
        # self.list.itemClicked.connect(self.list.clicked)


class Layout(QHBoxLayout):
    def __init__(self):
        super(Layout, self).__init__()
        self.list = ContainerList()
        self.list.setMaximumWidth(200)
        self.addWidget(self.list)

        # Use QTimer instead of threading.Timer to run on the UI thread
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.load_list)
        self.load_list()
        self.timer.start()

        vbox = QGridLayout()
        vbox.addWidget(QLabel("A"), 1, 3)
        vbox.addWidget(QLabel("B"))
        vbox.addWidget(QLabel("C"))
        vbox.addWidget(QLabel("D"))
        vbox.addWidget(QLabel("E"))

        self.addLayout(vbox)

    def load_list(self):
        docker = Docker()
        self.list.clear()
        for container in docker.containers:
            emoji = '🟢' if getattr(container, 'status', '') == 'running' else '⚪'
            self.list.addItem(f"{emoji} {container.name}")

        # Removed threading.Timer; QTimer handles updates.


class _SignalEmitter(QObject):
    # emits a completion message (string) to the main thread
    finished = pyqtSignal(str)


class ContainerList(QListWidget):
    def clicked(self, item):
        QMessageBox.information(self, "Notice", "You clicked on " + item.text())


class Docker:
    def __init__(self):
        self.client = docker.from_env()
        self.containers = self.client.containers.list(all=True)


class Application:
    def __init__(self):
        self.app = QApplication(sys.argv)
        try:
            self.app.setStyle('Fusion')
        except Exception:
            pass
        QApplication.setQuitOnLastWindowClosed(False)
        self.trayIcon = TrayIcon(self.app)
        self.menu = QMenu()
        self.trayIcon.setContextMenu(self.menu)

        # Dynamic container actions
        self.container_actions = []
        self.container_separator = None

        # Static actions (created first to serve as insertion point)
        self.about_action = self.menu.addAction('About')
        self.about_action.triggered.connect(self.show_about)
        self.exit_action = self.menu.addAction("Exit")
        self.exit_action.triggered.connect(lambda: QApplication.instance().quit())

        # Timer to refresh the container list in the menu
        self.refresh_timer = QTimer()
        self.refresh_timer.setInterval(10000)  # 10s
        self.refresh_timer.timeout.connect(self.refresh_container_actions)
        self.refresh_container_actions()  # populate initial list
        self.refresh_timer.start()

        self.trayIcon.show()
        # PyQt6: exec_ was replaced by exec
        sys.exit(self.app.exec())

    def refresh_container_actions(self):
        """Refresh the container actions in the tray menu."""
        # Remove previous actions and separator
        for act in self.container_actions:
            self.menu.removeAction(act)
        self.container_actions.clear()
        if self.container_separator:
            self.menu.removeAction(self.container_separator)
            self.container_separator = None

        try:
            docker_client = Docker()
            containers = docker_client.containers
        except Exception as e:
            # If Docker daemon is unavailable, show a warning action
            warn_action = self.menu.insertAction(self.menu.actions()[0] if self.menu.actions() else None, QMenu().addAction(f"Docker unavailable: {e}"))
            self.container_actions.append(warn_action)
            print(f"[Tray] Error listing containers: {e}")
            return

        # Insert each container BEFORE the 'About' action to keep them on top
        insertion_point = self.about_action
        for c in containers:
            status = getattr(c, 'status', '')
            emoji = '🟢' if status == 'running' else '⚪'
            text = f"{emoji} {c.name}"
            action = QAction(text, self.menu)
            action.setData({'id': c.id, 'name': c.name, 'status': status})

            def _handler(checked=False, container=c):
                emitter = _SignalEmitter()

                def on_finished(message: str):
                    # refresh on the UI thread and show notification
                    self.refresh_container_actions()
                    # show a popup notification only after completing the action
                    try:
                        self.trayIcon.showMessage("My Docker", message)
                    except Exception:
                        print(f"[Tray] {message}")

                emitter.finished.connect(on_finished)

                # Potentially blocking operation: run in a thread
                def work():
                    msg = ""
                    try:
                        client = docker.from_env()
                        cont = client.containers.get(container.id)
                        if getattr(cont, 'status', container.status) == 'running':
                            print(f"[Tray] Stopping container {cont.name}")
                            cont.stop()
                            msg = f"Container {cont.name} stopped"
                        else:
                            print(f"[Tray] Starting container {cont.name}")
                            cont.start()
                            msg = f"Container {cont.name} started"
                    except Exception as e:
                        msg = f"Error switching container {container.name}: {e}"
                        print(f"[Tray] {msg}")
                    finally:
                        try:
                            emitter.finished.emit(msg)
                        except Exception:
                            pass

                threading.Thread(target=work, daemon=True).start()

            action.triggered.connect(_handler)
            self.menu.insertAction(insertion_point, action)
            self.container_actions.append(action)
            print(f"[Tray] Container {c.name} status {status} emoji={emoji}")

        # Add separator between dynamic list and static actions if there are containers
        if self.container_actions:
            self.container_separator = self.menu.insertSeparator(insertion_point)

    def show_about(self):
        # Show a non-modal About window that describes the project and offers an optional Patreon button.
        try:
            self.about = About()
            self.about.show()
        except Exception as e:
            print(f"[Tray] Failed to open About window: {e}")


class About(QWidget):
    def __init__(self):
        super(About, self).__init__()
        self.setWindowTitle('About My Docker')
        self.setFixedSize(480, 260)

        # Center the window on the primary screen if available
        screen = QApplication.primaryScreen()
        if screen is not None:
            geom = screen.availableGeometry()
            x = geom.x() + (geom.width() - self.width()) // 2
            y = geom.y() + (geom.height() - self.height()) // 2
            self.move(x, y)

        # Content: description and optional Patreon button
        description = (
            "<h3>My Docker</h3>"
            "<p>We are an open-source community building a small tray utility to monitor and control Docker containers from your system tray.</p>"
            "<p>If you find this tool useful, you can support development via Patreon. Donations are optional and appreciated.</p>"
        )

        # Left: logo (icon.png)
        logo_label = QLabel()
        try:
            pix = QIcon('icon.png').pixmap(64, 64)
            logo_label.setPixmap(pix)
        except Exception:
            logo_label.setText('My Docker')

        label = QLabel(description)
        label.setOpenExternalLinks(True)
        label.setWordWrap(True)
        label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

        # Buttons: Open Patreon (optional) and Close
        btn_open = QPushButton('Open Patreon')
        btn_close = QPushButton('Close')

        def open_patreon():
            url = QUrl("https://patreon.com/ElaraDevSolutions?utm_medium=unknown&utm_source=join_link&utm_campaign=creatorshare_creator&utm_content=copyLink")
            try:
                QDesktopServices.openUrl(url)
            except Exception:
                print('[Tray] Failed to open Patreon URL')

        btn_open.clicked.connect(open_patreon)
        btn_close.clicked.connect(self.close)

        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        button_layout.addWidget(btn_open)
        button_layout.addWidget(btn_close)

        # Compose left (logo) + right (text + buttons)
        right_layout = QVBoxLayout()
        right_layout.addWidget(label)
        right_layout.addLayout(button_layout)

        main_layout = QHBoxLayout()
        main_layout.addWidget(logo_label)
        main_layout.addLayout(right_layout)
        self.setLayout(main_layout)


if __name__ == '__main__':
    Application()