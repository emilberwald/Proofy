from PySide2.QtWidgets import QWidget, QComboBox, QPushButton, QVBoxLayout


class ToolsWidget(QWidget):
    def __init__(self, *args, slot_draw_graph, **kwargs):
        super(ToolsWidget, self).__init__(*args, **kwargs)
        self.add_axiom = QComboBox(parent=self)

        self.draw_graph = QPushButton(text="Draw Graph", parent=self)
        self.draw_graph.clicked.connect(slot_draw_graph)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.add_axiom)
        layout.addWidget(self.draw_graph)
        self.setLayout(layout)
