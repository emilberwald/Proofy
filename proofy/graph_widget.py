import io
import json
import logging
import pathlib

import matplotlib.pyplot
import networkx
from PySide2.QtCore import Slot
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
    @Slot()
    def draw_graph(self):
        if self.graph:
            image = io.BytesIO()

            fig, ax = matplotlib.pyplot.subplots()
            networkx.draw(self.graph, ax=ax)
            fig.savefig(image, format="png")
            matplotlib.pyplot.close(fig)

            pixel_map = QPixmap()
            pixel_map.loadFromData(image.getvalue())
            self.resize(pixel_map.width(), pixel_map.height())
            self.label.setPixmap(pixel_map)
            self.update()

    @Slot()
    def get_file_types(self):
        return "Node Link Graph (*.json);;Adjacency Graph (*.json)"

    @Slot()
    def save_file(self, path: str, type: str):
        logger.info(f"Saving {path} {type}")
        if not self.graph:
            raise ValueError("No graph to save!")
        if "json" in type.lower():
            if "node link graph" in type.lower():
                with pathlib.Path(path).open("w") as file_p:
                    object = networkx.node_link_data(self.graph)
                    json.dump(object, file_p)
            elif "adjacency graph" in type.lower():
                with pathlib.Path(path).open("w") as file_p:
                    object = networkx.adjacency_data(self.graph)
                    json.dump(object, file_p)
            else:
                raise NotImplementedError()
        else:
            raise NotImplementedError()
        logger.info(f"Saved {path} {type}")

    @Slot()
    def open_file(self, path: str, type: str):
        logger.info(f"Opening {path} {type}")
        if "json" in type.lower():
            if "node link graph" in type.lower():
                self.graph = networkx.node_link_graph(json.loads(pathlib.Path(path).read_text()))
            elif "adjacency graph" in type.lower():
                self.graph = networkx.adjacency_graph(json.loads(pathlib.Path(path).read_text()))
            else:
                raise NotImplementedError()

    def __init__(self, log_handler):
        QWidget.__init__(self)
        logger.addHandler(log_handler)

        self.graph: networkx.MultiDiGraph = None

        self.layout = QVBoxLayout(self)

        self.label = QLabel(self)
        self.layout.addWidget(self.label)

        self.update_button = QPushButton("Update")
        self.update_button.clicked.connect(self.draw_graph)
        self.layout.addWidget(self.update_button)
