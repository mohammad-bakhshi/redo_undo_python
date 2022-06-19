import sys
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.QtGui import QPixmap, QColor, QPainter, QKeySequence
from PyQt5.QtWidgets import QLabel, QApplication, QShortcut
from stack import Stack
import copy


class Canvas(QLabel):
    def __init__(self, height, width, background_color=QColor('#FFFFFF')):
        super().__init__()
        qpixmap = QPixmap(int(height), int(width))
        qpixmap.fill(background_color)
        self.setPixmap(qpixmap)
        self.pen_color = QColor('#000000')
        self.stack = Stack(10000)
        self.undo_lines = Stack(20)
        self.redo_lines = Stack(20)

    def set_pen_color(self, color):
        self.pen_color = QtGui.QColor(color)

    def draw_point(self, x, y):
        painter = QPainter(self.pixmap())
        p = painter.pen()
        p.setWidth(4)
        p.setColor(self.pen_color)
        painter.setPen(p)
        painter.drawPoint(x, y)
        painter.end()
        self.update()

    def draw_line(self, x0, y0, x1, y1):
        painter = QPainter(self.pixmap())
        p = painter.pen()
        p.setWidth(4)
        p.setColor(self.pen_color)
        painter.setPen(p)
        painter.drawLine(x0, y0, x1, y1)
        painter.end()
        self.update()

    def mousePressEvent(self, e: QtGui.QMouseEvent):
        self.draw_point(e.x(), e.y())
        self.prev_point = (e.x(), e.y())
        self.stack.push(self.prev_point)

    def mouseMoveEvent(self, e):
        self.draw_line(self.prev_point[0],
                       self.prev_point[1], e.x(), e.y())
        self.prev_point = (e.x(), e.y())
        self.stack.push(self.prev_point)

    def mouseReleaseEvent(self, e):
        if self.undo_lines.is_full():
            print('stack if full')
        else:
            self.prev_point = tuple()
            self.undo_lines.push(self.stack)
            self.stack = Stack(10000)
            self.update()

    def draw_stack_line(self, stack_lines):
        canvas = self.pixmap()
        canvas.fill(QColor('#FFFFFF'))
        self.update()
        for i in range(0, stack_lines._num):
            line = stack_lines.pop()
            reverse = Stack(10000)
            for j in range(0, line._num):
                reverse.push(line.pop())
            for k in range(1, reverse._num):
                source = reverse.pop()
                destination = reverse.peek()
                self.draw_line(source[0], source[1],
                               destination[0], destination[1])
            if reverse._num == 1:
                source = reverse.pop()
                self.draw_point(source[0], source[1])
        self.update()

    def undo(self):
        if self.undo_lines.is_empty():
            print('can not undo')
        else:
            # pop undo and read all undoes then write
            self.redo_lines.push(self.undo_lines.pop())
            temp = copy.deepcopy(self.undo_lines)
            self.draw_stack_line(temp)

    def redo(self):
        if self.redo_lines.is_empty():
            print('can not redo')
        else:
            # pop redo and read all undoes
            self.undo_lines.push(self.redo_lines.pop())
            temp = copy.deepcopy(self.undo_lines)
            self.draw_stack_line(temp)


class PaletteButton(QtWidgets.QPushButton):

    def __init__(self, color):
        super().__init__()
        self.setFixedSize(QtCore.QSize(32, 32))
        self.color = color
        self.setStyleSheet("background-color: %s;" %
                           color + "border-radius : 15; ")


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.colors = [
            '#000002', '#868687', '#900124', '#ed2832', '#2db153', '#13a5e7', '#4951cf',
            '#fdb0ce', '#fdca0f', '#eee3ab', '#9fdde8', '#7a96c2', '#cbc2ec', '#a42f3b',
            '#f45b7a', '#c24998', '#81588d', '#bcb0c2', '#dbcfc2',
        ]
        app = QApplication.instance()
        screen = app.primaryScreen()
        geometry = screen.availableGeometry()
        self.canvas = Canvas(geometry.width()*0.60, geometry.height()*0.7)
        w = QtWidgets.QWidget()
        w.setStyleSheet("background-color: #313234")
        l = QtWidgets.QVBoxLayout()  # vertical layout
        w.setLayout(l)
        l.addWidget(self.canvas)

        self.shortcut_undo = QShortcut(QKeySequence('Ctrl+z'), self)
        self.shortcut_undo.activated.connect(self.on_undo)

        self.shortcut_redo = QShortcut(QKeySequence('Ctrl+y'), self)
        self.shortcut_redo.activated.connect(self.on_redo)

        palette = QtWidgets.QHBoxLayout()  # horizontal layout
        self.add_palette_button(palette)
        l.addLayout(palette)

        self.setCentralWidget(w)

    def on_redo(self):
        self.canvas.redo()

    def on_undo(self):
        self.canvas.undo()

    def add_palette_button(self, palette):
        for c in self.colors:
            item = PaletteButton(c)
            item.pressed.connect(self.set_canvas_color)
            palette.addWidget(item)

    def set_canvas_color(self):
        sender = self.sender()
        self.canvas.set_pen_color(sender.color)


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.setWindowFlags(QtCore.Qt.WindowCloseButtonHint |
                      QtCore.Qt.WindowMinimizeButtonHint)
window.show()
app.exec_()

# Window dimensions
