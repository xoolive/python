import sys

import pandas as pd
import requests
from PyQt5 import QtCore, QtGui, QtWidgets

from ..core.api import api_points
from ..core.utils import readtime


def dont_crash(fn):
    """
    Wraps callbacks: a simple information is raised in place of a program crash.
    """

    def safe_exec(self, *args, **kwargs):
        try:
            return fn(self, *args, **kwargs)
        except Exception as e:
            QtWidgets.QMessageBox.information(
                self, type(e).__name__, " ".join(str(x) for x in e.args)
            )

    return safe_exec


class PandasTableModel(QtGui.QStandardItemModel):
    columns = {
        "start": "Début",
        "end": "Fin",
        "title": "Titre",
        "authors": "Auteur",
        "titreAlbum": "Album",
        "anneeEditionMusique": "Année",
        "label": "Label",
    }

    def __init__(self, data, parent=None):
        QtGui.QStandardItemModel.__init__(self, parent)
        self._data = (
            data[self.columns.keys()]
            .assign(
                start=lambda df: df.start.apply(readtime),
                end=lambda df: df.end.apply(readtime),
            )
            .rename(columns=self.columns)
        )
        for row in self._data.values.tolist():
            data_row = [QtGui.QStandardItem(f"{elt}") for elt in row]
            self.appendRow(data_row)

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return self._data.shape[1]

    def headerData(self, x, orientation, role):
        if (
            orientation == QtCore.Qt.Horizontal
            and role == QtCore.Qt.DisplayRole
        ):
            return self._data.columns[x]
        if orientation == QtCore.Qt.Vertical and role == QtCore.Qt.DisplayRole:
            return self._data.index[x]
        return None


class MainScreen(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setWindowTitle("À l'écoute sur FIP")
        self.setGeometry(10, 10, 900, 300)

        self.set_widgets()
        self.set_layout()
        self.get_content()
        self.set_callbacks()

    def set_widgets(self):
        mainLayout = QtWidgets.QHBoxLayout()

        # Partie à gauche
        gauche = QtWidgets.QVBoxLayout()
        mainLayout.addLayout(gauche)

        self.menu_radios = QtWidgets.QComboBox()
        gauche.addWidget(self.menu_radios)
        for radio_name in api_points.keys():
            self.menu_radios.addItem(radio_name)

        self.rafraichir = QtWidgets.QPushButton("Rafraîchir")
        gauche.addWidget(self.rafraichir)

        self.pixmap = QtGui.QPixmap()
        self.visual = QtWidgets.QLabel()
        gauche.addWidget(self.visual)

        #  Partie à droite
        self.music_widget = QtWidgets.QWidget()
        self.music_view = QtWidgets.QTableView(self.music_widget)
        mainLayout.addWidget(self.music_widget)

        mainWidget = QtWidgets.QWidget()
        mainWidget.setLayout(mainLayout)
        self.setCentralWidget(mainWidget)

    @dont_crash
    def get_content(self, *args, **kwargs):
        # Lecture du contenu du menu déroulant pour le nom de la radio
        url = self.menu_radios.currentText()
        response = requests.get(api_points[url])
        response.raise_for_status()
        # Construction du pd.DataFrame
        self.results = pd.DataFrame.from_records(
            list(response.json()["steps"].values())
        )
        self.music_model = PandasTableModel(self.results)
        self.music_view.setModel(self.music_model)
        self.get_image()

    @dont_crash
    def get_image(self, idx: int = -2, *args, **kwargs):
        img_response = requests.get(self.results.iloc[idx].visual)
        img_response.raise_for_status()
        # Lecture de la représentation binaire de l'image
        self.pixmap.loadFromData(img_response.content)
        self.visual.setPixmap(self.pixmap.scaledToHeight(250))

    def set_layout(self):
        self.menu_radios.setMaximumWidth(400)
        self.music_widget.setMinimumWidth(800)
        self.music_widget.setMinimumHeight(300)
        self.music_view.setMinimumWidth(800)
        self.music_view.setMinimumHeight(300)
        self.rafraichir.setMaximumWidth(150)

    def set_callbacks(self):
        self.rafraichir.clicked.connect(self.get_content)
        self.menu_radios.activated.connect(self.get_content)


def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainScreen()
    main.show()
    return app.exec_()
