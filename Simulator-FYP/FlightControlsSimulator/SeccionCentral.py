import sys
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPen, QColor, QFont
from PyQt5.QtCore import QPoint, Qt

class SeccionCentral(QWidget):

    def __init__(self):
        super().__init__()

        self.joystickX = 0

    def paintEvent(self, event):
        painter = QPainter(self)

        painter.fillRect(self.rect(), Qt.black)

        self.dibujarAleronIzq(painter)
        self.dibujarAleronDer(painter)
        self.dibujarELACSEC(painter)
        self.dibujarIndicadorAIL(painter, self.joystickX)

    def actualizarUI(self, x):
        self.joystickX = x

        self.update()

    def dibujarIndicadorAIL(self, painter, posicionX):
        # Convertimos [-1,1 ] --> [5, 150].
        yIzq = int(24 + ((posicionX + 1) / 2) * (150 - 24))
        yDer = int(24 + (((-posicionX) + 1) / 2) * (150 - 24))
        painter.setPen(Qt.NoPen)

        # Triángulo Izquierdo.
        puntos = [
            QPoint(100, yIzq),
            QPoint(114, yIzq - 6),
            QPoint(114, yIzq + 6)
        ]
        painter.setBrush(Qt.NoBrush)
        painter.setPen(QPen(QColor(0, 255, 0), 1.5))
        painter.drawPolygon(puntos)

        # Triángulo Derecho.
        puntos = [
            QPoint(760, yDer),
            QPoint(746, yDer - 6),
            QPoint(746, yDer + 6)
        ]
        painter.setBrush(Qt.NoBrush)
        painter.setPen(QPen(QColor(0, 255, 0), 1.5))
        painter.drawPolygon(puntos)


    # FUNCIONES QUE DIBUJAN LOS ELEMENTOS ESTÁTICOS.
    def dibujarAleronIzq(self, painter):
        # Texto.
        painter.setPen(QColor(255, 255, 255))
        painter.setFont(QFont("Times New Roman", 17))
        painter.drawText(50, 15, "L")
        painter.drawText(40, 30, "AIL")

        # Resto de componentes.
        painter.setPen(QPen(QColor(255, 255, 255), 1.5))

        painter.drawLine(100, 5, 100, 150)     # Línea vertical.

        painter.setBrush(Qt.NoBrush)

        # Cuadrados.
        painter.drawRect(93, 5, 7, 19)         # x, y, ancho, alto
        painter.drawRect(92, 150, 8, 10)

        # Líneas en la mitad.
        painter.drawLine(100, 87, 93, 87)
        painter.drawLine(100, 82, 93, 82)

        # Rectángulo central.
        painter.drawRect(90, 92, 10, 6)

        # Displays Sistema de Presión Hidráulica.
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(80, 80, 80))
        painter.drawRect(125, 140, 19, 25)
        painter.drawRect(150, 140, 19, 25)

        painter.setPen(QColor(0, 255, 0))
        painter.setFont(QFont("Times New Roman", 17))
        painter.drawText(128, 158, "B")
        painter.drawText(153, 158, "G")

    def dibujarAleronDer(self, painter):
        # Texto.
        painter.setPen(QColor(255, 255, 255))
        painter.setFont(QFont("Times New Roman", 17))
        painter.drawText(805, 15, "R")
        painter.drawText(795, 30, "AIL")

        # Resto de componentes.
        painter.setPen(QPen(QColor(255, 255, 255), 1.5))

        painter.drawLine(760, 5, 760, 160)     # Línea vertical.

        painter.setBrush(Qt.NoBrush)

        # Cuadrados.
        painter.drawRect(760, 5, 7, 19)         # x, y, ancho, alto
        painter.drawRect(760, 150, 8, 10)

        # Líneas en la mitad.
        painter.drawLine(760, 87, 767, 87)
        painter.drawLine(760, 82, 767, 82)

        # Rectángulo central.
        painter.drawRect(760, 92, 10, 6)

        # Displays Sistema de Presión Hidráulica.
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(80, 80, 80))
        painter.drawRect(689, 140, 19, 25)
        painter.drawRect(714, 140, 19, 25)

        painter.setPen(QColor(0, 255, 0))
        painter.setFont(QFont("Times New Roman", 17))
        painter.drawText(692, 158, "G")
        painter.drawText(717, 158, "B")

    def dibujarELACSEC(self, painter):
        painter.setPen(QColor(255, 255, 255))
        # Primer cuadrante ELAC.
        painter.drawLine(200, 77, 280, 77)
        painter.drawLine(280, 77, 280, 50)
        painter.drawLine(280, 50, 272, 50)

        # Segundo cuadrante ELAC.
        painter.drawLine(230, 93, 310, 93)
        painter.drawLine(310, 93, 310, 66)
        painter.drawLine(310, 66, 302, 66)

        # Primer cuadrante SEC.
        painter.drawLine(520, 77, 600, 77)
        painter.drawLine(600, 77, 600, 50)
        painter.drawLine(600, 50, 592, 50)

        # Segundo cuadrante SEC.
        painter.drawLine(550, 93, 630, 93)
        painter.drawLine(630, 93, 630, 66)
        painter.drawLine(630, 66, 622, 66)

        # Tercer cuadrante SEC.
        painter.drawLine(580, 109, 660, 109)
        painter.drawLine(660, 109, 660, 82)
        painter.drawLine(660, 82, 652, 82)

        # Texto ELAC.
        painter.setPen(QColor(255, 255, 255))
        painter.setFont(QFont("Times New Roman", 17))
        painter.drawText(205, 70, "ELAC")

        # Texto SEC.
        painter.setPen(QColor(255, 255, 255))
        painter.setFont(QFont("Times New Roman", 17))
        painter.drawText(530, 70, "SEC")

        # Números verdes.
        painter.setPen(QColor(0, 255, 0))
        painter.setFont(QFont("Verdana", 17))

        painter.drawText(263, 70, "1")              # 1 ELAC.
        painter.drawText(293, 86, "2")              # 2 ELAC.
        painter.drawText(583, 70, "1")              # 1 SEC.
        painter.drawText(613, 86, "2")              # 2 SEC.
        painter.drawText(643, 102, "3")              # 3 SEC.