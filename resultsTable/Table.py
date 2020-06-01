import csv
import os
import webbrowser
from pathlib import Path

from PyQt5.uic.properties import QtCore

from resultsTable.resultsExctractor import ResultsExtractor

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QAbstractTableModel
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtWidgets import QMainWindow, QFileDialog
import configUtils
from PIL import Image


class Results(QMainWindow):
    def __init__(self, data, table_view, export_btn, parent=None):
        super(Results, self).__init__(parent)
        table_view.doubleClicked.connect(self.cell_clicked)

        self.model = TableModel(data)
        header = table_view.horizontalHeader()
        rows = table_view.verticalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        rows.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        table_view.setModel(self.model)

        export_btn.clicked.connect(self.export_table)

    @staticmethod
    def cell_clicked(item):
        ResultsExtractor.open_link(item)

    def resize_table(self):
        self.table.resizeRowsToContents()
        self.table.resizeColumnsToContents()

    def export_table(self):
        output = self.model._data.drop('Your Image Name', axis=1)
        for idx, row in output.iterrows():
            output.loc[idx, 'Image'] = output.loc[idx, 'Image'].split(configUtils.get_property("images_delimiter"))[0]
        options = QFileDialog.Options()
        file_name, _ = QtWidgets.QFileDialog().getSaveFileName(None, "Export table content", filter='CSV (*.csv)', options=options,
                                              directory=str(Path.home()) + '/report.csv')
        if file_name:
            try:
                output.to_csv(file_name)
            except PermissionError:
                pass


class TableModel(QAbstractTableModel):

    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            if index.column() == 0:
                return ""
            else:
                value = self._data.iloc[index.row(), index.column()]
                return str(value)

        if role == Qt.DecorationRole and index.column() == 0:  # add image to cell
            tmp_img_path = "resources/images_app/report"
            if not os.path.exists(tmp_img_path):
                os.makedirs(tmp_img_path)

            # if image already found and not removed by user
            tmp_img_path = tmp_img_path + "/" + str(index.row()) + ".jpg"
            if not os.path.exists(tmp_img_path):
                paths = self._data.iloc[index.row(), index.column()].split(configUtils.get_property("images_delimiter"))
                res_img = get_concat_h_blank(paths[0], paths[1])
                res_img.save(tmp_img_path)

            picture = QPixmap(tmp_img_path)
            picture = picture.scaled(120, 120, Qt.KeepAspectRatio)
            return picture

        if role == Qt.ForegroundRole and (index.column() == 3 or index.column() == 2):
            return QColor('blue')

        if role == Qt.BackgroundRole:
            if index.row() % 2 == 0:
                return QColor('#D3D3D3')
            else:
                return QColor('#C0C0C0')

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Vertical:
                return str(self._data.index[section] + 1)


def get_concat_h_blank(im1_path, im2_path, color=(0, 0, 0)):
    im1 = Image.open(r"{}".format(im1_path))
    im2 = Image.open(r"{}".format(im2_path))
    base_width = 300
    w_percent1 = (base_width / float(im1.size[0]))
    w_percent2 = (base_width / float(im2.size[0]))
    h_size1 = int((float(im1.size[1]) * float(w_percent1)))
    h_size2 = int((float(im2.size[1]) * float(w_percent2)))
    im1 = im1.resize((base_width, h_size1), Image.ANTIALIAS)
    im2 = im2.resize((base_width, h_size2), Image.ANTIALIAS)
    dst = Image.new('RGB', (im1.width + im2.width + 3, max(im1.height, im2.height)), color)
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width + 3, 0))
    return dst
