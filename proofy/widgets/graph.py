import importlib.resources
import io
import json
import logging
import pathlib

import matplotlib.pyplot
import networkx
from PySide2.QtCore import Slot, QByteArray
from PySide2.QtGui import QPixmap
from PySide2.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PySide2.QtWidgets import QWidget, QHBoxLayout

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Graph(QWidget):
    def __init__(self, log_console):
        logger.debug(locals())
        QWidget.__init__(self)
        log_console.add_loggers(logger)

        self.graph = None
        self.webview = QWebEngineView(parent=self)
        self.index = QWebEnginePage(self)

        worklayout = QHBoxLayout(parent=self)
        worklayout.addWidget(self.webview)
        self.setLayout(worklayout)

    @staticmethod
    def to_qpixmap(graph: networkx.MultiDiGraph) -> QPixmap:
        if graph:
            image = io.BytesIO()

            fig, ax = matplotlib.pyplot.subplots()
            networkx.draw(graph, ax=ax)
            fig.savefig(image, format="png")
            matplotlib.pyplot.close(fig)

            pixel_map = QPixmap()
            pixel_map.loadFromData(QByteArray(image.getvalue()))
            return pixel_map

    def draw_index(self):
        if not self.graph:
            logger.warning("No graph to draw found!")
        html = importlib.resources.read_text(__package__, "index.thtml", encoding="utf-8-sig")
        html = (
            html.replace(
                "$graph",
                "'" + json.dumps(networkx.node_link_data(self.graph)) + "'"
                if self.graph
                else """'{"directed":true,"multigraph":true,"graph":[],"nodes":[],"links":[]}'""",
            )
            .replace("$width", "640")
            .replace("$height", "320")
        )
        logger.info(f"""Saving html to {pathlib.Path("index.html").absolute()}""")
        pathlib.Path("index.html").write_text(html)

        self.index.setHtml(html)
        self.webview.setPage(self.index)
        self.webview.resize(640, 320)
        self.webview.show()
        self.update()

    @Slot()
    def draw_graph(self):
        logger.debug(locals())
        self.draw_index()

    @Slot()
    def get_file_types(self):
        logger.debug(locals())
        return ";;".join(["Node Link Graph (*.json)", "Adjacency Graph (*.json)",])

    @Slot(str, str)
    def open_file(self, path: str, file_type: str):
        logger.debug(locals())
        if "json" in file_type.lower():
            if "node link graph" in file_type.lower():
                self.graph = networkx.node_link_graph(json.loads(pathlib.Path(path).read_text()))
            elif "adjacency graph" in file_type.lower():
                self.graph = networkx.adjacency_graph(json.loads(pathlib.Path(path).read_text()))
            else:
                raise NotImplementedError()
        else:
            raise NotImplementedError()

    @Slot(str, str)
    def save_file(self, path: str, file_type: str):
        logger.debug(locals())
        if not self.graph:
            raise ValueError("No graph to save!")
        if "json" in file_type.lower():
            if "node link graph" in file_type.lower():
                with pathlib.Path(path).open("w") as file_p:
                    data = networkx.node_link_data(self.graph)
                    json.dump(data, file_p)
                    del data
            elif "adjacency graph" in file_type.lower():
                with pathlib.Path(path).open("w") as file_p:
                    data = networkx.adjacency_data(self.graph)
                    json.dump(data, file_p)
                    del data
            else:
                raise NotImplementedError()
        else:
            raise NotImplementedError()
