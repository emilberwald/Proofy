import io
import json
import logging
import pathlib

import decorators
import matplotlib.pyplot
import networkx
from PySide2.QtCore import Slot, QByteArray
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class GraphWidget(QWidget):
    def __init__(self, log_console):
        logger.debug(locals())
        QWidget.__init__(self)
        log_console.add_loggers(logger)

        self.graph = None

        self.layout = QVBoxLayout(self)

        self.label = QLabel(self)
        self.layout.addWidget(self.label)

        self.update_button = QPushButton("Update")
        self.update_button.clicked.connect(self.draw_graph)
        self.layout.addWidget(self.update_button)

    @Slot()
    def draw_graph(self):
        logger.debug(locals())
        if self.graph:
            image = io.BytesIO()

            fig, ax = matplotlib.pyplot.subplots()
            networkx.draw(self.graph, ax=ax)
            fig.savefig(image, format="png")
            matplotlib.pyplot.close(fig)

            pixel_map = QPixmap()
            pixel_map.loadFromData(QByteArray(image.getvalue()))
            self.resize(pixel_map.width(), pixel_map.height())
            self.label.setPixmap(pixel_map)
            self.update()

    @Slot()
    def get_file_types(self):
        logger.debug(locals())
        return "Node Link Graph (*.json);;Adjacency Graph (*.json)"

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
