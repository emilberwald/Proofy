import logging

from PySide2 import QtWidgets
from PySide2.QtCore import Slot, Qt, QSettings, QByteArray
from PySide2.QtGui import QKeySequence, QCloseEvent
from PySide2.QtWidgets import QMainWindow, QApplication, QAction, QFileDialog, QDockWidget, QMessageBox, QToolBar, QMenu

from __init__ import __version__
from widgets.graphwidget import GraphWidget
from widgets.logconsolewidget import LogConsoleWidget
from widgets.toolswidget import ToolsWidget

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class MainWindow(QMainWindow):
    def __init__(self, app: QApplication):
        super().__init__()

        self.current_file = None

        self.console_dock: QDockWidget = None
        self.tools_dock: QDockWidget = None

        self.toolbar: QToolBar = None

        self.graph_widget: GraphWidget = None
        self.log_console_widget: LogConsoleWidget = None
        self.tools_widget: ToolsWidget = None

        self.file_menu: QMenu = None
        self.help_menu: QMenu = None
        self.view_menu: QMenu = None
        self.docks_menu: QMenu = None

        self.about_action: QAction = None
        self.new_action: QAction = None
        self.open_action: QAction = None
        self.save_action: QAction = None
        self.save_as_action: QAction = None
        self.exit_action: QAction = None
        self.toggle_tools_dock: QAction = None
        self.toggle_console_dock: QAction = None

        self.create_actions(app)
        self.create_widgets()
        self.create_docks()
        self.create_menus()
        self.create_toolbar()
        self.create_statusbar()

        self.setCentralWidget(self.graph_widget)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.console_dock)
        self.addDockWidget(Qt.RightDockWidgetArea, self.tools_dock)
        self.addToolBar(self.toolbar)
        self.setWindowTitle(self.tr("Proofy"))

        self.read_settings()

    def create_statusbar(self):
        self.statusBar().showMessage(self.tr("Welcome to Proofy!"))

    def create_docks(self):
        self.console_dock = QDockWidget(self.tr("Console"))
        self.console_dock.setWidget(self.log_console_widget)

        self.tools_dock = QDockWidget(self.tr("Tools"))
        self.tools_dock.setWidget(self.tools_widget)

    def create_toolbar(self):
        self.toolbar = QToolBar(self.tr("Tools"), self)
        self.toolbar.setStatusTip(self.tr("Tools"))
        self.toolbar.addActions(
            [self.new_action, self.open_action, self.save_action, self.save_as_action, self.exit_action]
        )
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.about_action)

    def create_widgets(self):
        self.log_console_widget = LogConsoleWidget()
        self.log_console_widget.add_loggers(logger)
        self.graph_widget = GraphWidget(self.log_console_widget)
        self.tools_widget = ToolsWidget(slot_draw_graph=self.graph_widget.draw_graph)

    def create_menus(self):
        self.file_menu = self.menuBar().addMenu("File")
        self.file_menu.setStatusTip(self.tr("File operations"))
        self.file_menu.addActions(
            [self.new_action, self.open_action, self.save_action, self.save_as_action, self.exit_action]
        )

        self.view_menu = self.menuBar().addMenu("View")
        self.view_menu.setStatusTip(self.tr("View settings"))
        self.docks_menu = self.view_menu.addMenu("Docks")
        self.docks_menu.addAction(self.toggle_tools_dock)
        self.docks_menu.addAction(self.toggle_console_dock)

        self.help_menu = self.menuBar().addMenu("Help")
        self.help_menu.setStatusTip(self.tr("Help"))
        self.help_menu.addAction(self.about_action)

    def create_actions(self, app):

        self.about_action = QAction(app.style().standardIcon(QtWidgets.QStyle.SP_MessageBoxInformation), "About", self)
        self.about_action.setStatusTip("Show information about Proofy")
        self.about_action.triggered.connect(self.about)

        self.new_action = QAction(app.style().standardIcon(QtWidgets.QStyle.SP_FileDialogNewFolder), "New...", self)
        self.new_action.setStatusTip(self.tr("Create a new file"))
        self.new_action.setShortcuts(QKeySequence.New)
        self.new_action.triggered.connect(self.new)

        self.open_action = QAction(app.style().standardIcon(QtWidgets.QStyle.SP_DialogOpenButton), "Open...", self)
        self.open_action.setStatusTip(self.tr("Open file"))
        self.open_action.setShortcuts(QKeySequence.Open)
        self.open_action.triggered.connect(self.open)

        self.save_action = QAction(app.style().standardIcon(QtWidgets.QStyle.SP_DialogSaveButton), "Save...", self)
        self.save_action.setStatusTip(self.tr("Save file"))
        self.save_action.setShortcuts(QKeySequence.Save)
        self.save_action.triggered.connect(self.save)

        self.save_as_action = QAction(app.style().standardIcon(QtWidgets.QStyle.SP_DriveFDIcon), "Save As...", self)
        self.save_as_action.setStatusTip(self.tr("Save to file"))
        self.save_as_action.setShortcuts(QKeySequence.SaveAs)
        self.save_as_action.triggered.connect(self.save_as)

        self.exit_action = QAction(app.style().standardIcon(QtWidgets.QStyle.SP_DialogCloseButton), "Exit", self)
        self.exit_action.setStatusTip(self.tr("Exit Proofy"))
        self.exit_action.setShortcuts(QKeySequence.Quit)
        self.exit_action.triggered.connect(self.exit)

        self.toggle_console_dock = QAction("Toggle Console Dock", self)
        self.toggle_console_dock.setStatusTip("Toggle visibility of the console dock")
        self.toggle_console_dock.triggered.connect(
            lambda _: self.console_dock.setVisible(not self.console_dock.isVisible())
        )

        self.toggle_tools_dock = QAction("Toggle Tools Dock", self)
        self.toggle_tools_dock.setStatusTip("Toggle visibility of the tools dock")
        self.toggle_tools_dock.triggered.connect(lambda _: self.tools_dock.setVisible(not self.tools_dock.isVisible()))

    @Slot()
    def about(self):
        logger.debug(locals())
        QMessageBox.about(
            self,
            "About Proofy",
            self.tr(
                f"""
                <h1>Proofy {__version__}</h1>
                <p>
                <b>Proofy is a formal proof system GUI.</b>
                </p>
                <p>
                Oh, it looks like Proofy wants to talk!
                <blockquote>Proofy likes Sequent Calculus! And circles! And edges! And arrows! And ...</blockquote>
                </p>
                """
            ),
        )

    def closeEvent(self, event: QCloseEvent):
        logger.debug(locals())
        if self.save_prompt():
            self.write_settings()
            event.accept()
        else:
            event.ignore()

    @Slot()
    def exit(self):
        logger.debug(locals())
        if self.save_prompt():
            QApplication.quit()

    @Slot()
    def new(self):
        logger.debug(locals())
        if self.save_prompt():
            self.current_file = None

    @Slot()
    def open(self):
        logger.debug(locals())
        if self.save_prompt():
            if (
                path := QFileDialog.getOpenFileName(
                    self, caption=self.tr("Open File"), filter=self.graph_widget.get_open_file_extensions()
                )
            ) :
                try:
                    QApplication.setOverrideCursor(Qt.WaitCursor)
                    self.graph_widget.open_file(*path)
                    self.statusBar().showMessage(f"Opened {path} successfully")
                except Exception as e:
                    logger.error(e)
                finally:
                    QApplication.restoreOverrideCursor()

    def read_settings(self):
        logger.debug(locals())
        settings = QSettings("EAB", "Proofy")
        self.restoreGeometry(QByteArray(settings.value("presentation/geometry")))
        self.restoreState(QByteArray(settings.value("presentation/state")))

    @Slot()
    def save(self):
        logger.debug(locals())
        if self.current_file:
            self.save_file()
        else:
            self.save_as()

    @Slot()
    def save_as(self):
        logger.debug(locals())
        if (
            path := QFileDialog.getSaveFileName(
                self, caption=self.tr("Save File"), filter=self.graph_widget.get_save_file_extensions()
            )
        ) :
            self.current_file = path
            self.save_file()

    def save_file(self):
        logger.debug(locals())
        try:
            QApplication.setOverrideCursor(Qt.WaitCursor)
            self.graph_widget.save_file(*self.current_file)
        except Exception as e:
            logger.error(e)
        finally:
            QApplication.restoreOverrideCursor()

    def save_prompt(self):
        logger.debug(locals())
        if self.current_file:
            ret = QMessageBox.warning(
                self,
                self.tr("Application"),
                self.tr(
                    """
                    Do you want to save your current work?
                    """
                ),
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
            )
            logger.debug(ret)
            if ret == QMessageBox.Save:
                self.save()
                return True
            elif ret == QMessageBox.Discard:
                return True
            elif ret == QMessageBox.Cancel:
                return False
            else:
                raise NotImplementedError()
        else:
            return True

    def write_settings(self):
        logger.debug(locals())
        settings = QSettings("EAB", "Proofy")
        settings.setValue("presentation/geometry", self.saveGeometry())
        settings.setValue("presentation/state", self.saveState(int(__version__.replace(".", ""))))
