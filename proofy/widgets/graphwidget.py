import importlib.resources
import json
import logging
import pathlib

import networkx
from PySide2.QtCore import Slot, QStandardPaths
from PySide2.QtWebEngineWidgets import QWebEngineView, QWebEnginePage, QWebEngineSettings
from PySide2.QtWidgets import QWidget, QHBoxLayout

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class GraphWidget(QWidget):
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

    def draw_index(self):
        if not self.graph:
            logger.warning("No graph to draw found!")
        width = self.contentsRect().width()
        height = self.contentsRect().height()
        pagewidth = int(width) - 10
        pageheight = int(height) - 10
        logger.info(f"{width}x{height}")
        html = importlib.resources.read_text(__package__, "index.thtml", encoding="utf-8-sig")
        html = (
            html.replace(
                "$graph",
                "'" + json.dumps(networkx.node_link_data(self.graph)) + "'"
                if self.graph
                else """'{"directed":true,"multigraph":true,"graph":[],"nodes":[],"links":[]}'""",
            )
            .replace("$width", str(pagewidth))
            .replace("$height", str(pageheight))
        )
        path = pathlib.Path(QStandardPaths.writableLocation(QStandardPaths.AppLocalDataLocation)) / "index.html"
        logger.info(f"""Saving html to {path.absolute()}""")
        path.write_text(html)

        self.index.setHtml(html)
        self.index.settings().setAttribute(QWebEngineSettings.ShowScrollBars, False)
        self.webview.setPage(self.index)
        self.webview.resize(width, height)
        self.webview.show()
        self.update()

    @Slot()
    def draw_graph(self):
        logger.debug(locals())
        self.draw_index()

    @Slot()
    def get_open_file_extensions(self):
        logger.debug(locals())
        return ";;".join(
            [
                "Node Link Graph (*.json)",
                "Adjacency Graph (*.json)",
                "GraphML (.graphml)",
                "LEDA (*.gw, *.lgr, *.leda)",
                "Pajek (*.net)",
            ]
        )

    @Slot()
    def get_save_file_extensions(self):
        logger.debug(locals())
        return ";;".join(["Node Link Graph (*.json)", "Adjacency Graph (*.json)"])

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
        elif "graphml" in file_type.lower():
            self.graph = networkx.read_graphml(path)
        elif "leda" in file_type.lower():
            self.graph = networkx.read_leda(path)
        elif "pajek" in file_type.lower():
            self.graph = networkx.read_pajek(path)
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
