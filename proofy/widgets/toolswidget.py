from enum import Enum

from PySide2.QtGui import QStandardItemModel, QStandardItem
from PySide2.QtWidgets import QWidget, QComboBox, QPushButton, QVBoxLayout, QLineEdit, QTableView, QFrame

from widgets.graphwidget import GraphWidget


class PropositionalLogicSymbols(Enum):
    TRUE = "⊤"
    FALSE = "⊥"
    NOT = "¬"
    AND = "∧"
    OR = "∨"
    IMPLIES = "→"


class QuantifierSymbols(Enum):
    FORALL = "∀"
    EXISTS = "∃"


class MetalogicSymbols(Enum):
    ENTAILS_SYNTACTICALLY = "⊢"
    ENTAILS_SEMANTICALLY = "⊨"


class ToolsWidget(QWidget):
    def __init__(self, *args, graph_widget: GraphWidget, **kwargs):
        super(ToolsWidget, self).__init__(*args, **kwargs)

        self.mode_combobox_widget = QComboBox(parent=self)
        self.setStatusTip("Mode")
        self.mode_combobox_widget.addItems(["Axiom", "Well Formed Formula", "Substitution", "Inference Rule"])
        self.input_widget = QLineEdit(self)
        self.input_widget.setStatusTip("Input unicode text inside in this field.")

        self.character_map_model = QStandardItemModel(self)
        symbols = [
            [e.value for e in PropositionalLogicSymbols],
            [e.value for e in QuantifierSymbols],
            [e.value for e in MetalogicSymbols],
        ]
        for i, symbol_set in enumerate(symbols):
            for j, symbol in enumerate(symbol_set):
                self.character_map_model.setItem(j, i, QStandardItem(symbol))
        self.character_map_widget = QTableView(self)
        self.character_map_widget.setModel(self.character_map_model)

        self.draw_graph_button_widget = QPushButton(text="Draw Graph", parent=self)
        self.draw_graph_button_widget.clicked.connect(graph_widget.draw_graph)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.input_widget)
        layout.addWidget(self.get_separator_widget())
        layout.addWidget(self.mode_combobox_widget)
        layout.addWidget(self.character_map_widget)
        layout.addWidget(self.get_separator_widget())
        layout.addWidget(self.draw_graph_button_widget)
        self.setLayout(layout)

    def get_separator_widget(self):
        separator = QFrame(self)
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        return separator
