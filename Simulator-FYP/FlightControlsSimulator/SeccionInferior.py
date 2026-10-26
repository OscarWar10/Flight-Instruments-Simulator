import math
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPainterPath, QPen, QColor,QFont
from PyQt5.QtCore import QPoint, QPointF, Qt

class SeccionInferior(QWidget):
    def __init__(self):
        super().__init__()

        self.joystickX = 0
        self.joystickY = 0

    def paintEvent(self, event):
        painter = QPainter(self)

        painter.fillRect(self.rect(), Qt.black)

        self.dibujarElevadorIzq(painter)
        self.dibujarElevadorDer(painter)
        self.dibujarPitchRudder(painter)
        self.dibujarTimonCola(painter)
        self.dibujarIndicadorELEV(painter, self.joystickY)
        self.dibujarGradosELEV(painter, self.joystickY)
        self.dibujarIndicadorRudder(painter, self.joystickX)

    def actualizarUI(self, x, y):
        self.joystickX = x
        self.joystickY = y

        self.update()

    def dibujarIndicadorELEV(self, painter, posicionY):
        # Convert [-1,1 ] --> [5, 150].
        y = int(30 + (((-posicionY) + 1) / 2) * (185 - 30))
        painter.setPen(Qt.NoPen)

        # Triángulo IZQ.
        puntos = [
            QPoint(220, y),
            QPoint(234, y - 7),
            QPoint(234, y + 7)
        ]
        painter.setBrush(Qt.NoBrush)
        painter.setPen(QPen(QColor(0, 255, 0), 1.5))
        painter.drawPolygon(puntos)

        # Triángulo DER.
        puntos = [
            QPoint(640, y),
            QPoint(626, y - 7),
            QPoint(626, y + 7)
        ]
        painter.setBrush(Qt.NoBrush)
        painter.setPen(QPen(QColor(0, 255, 0), 1.5))
        painter.drawPolygon(puntos)

    def dibujarGradosELEV(self, painter, posicionY):
        angulo = self.calcularGradosELEV(posicionY)

        if angulo < 0:
            posicion = "UP"
        elif angulo > 0:
            posicion = "DOWN"
        else:
            posicion = " "

        painter.setPen(QColor(0, 255, 0))
        painter.setFont(QFont("Times New Roman", 21))
        painter.drawText(385, 50, f"{angulo:.1f}º")

        painter.setFont(QFont("Times New Roman", 18))

        if posicion != " ":
            if posicion == "UP":
                painter.drawText(445, 50, posicion)
            else:
                painter.drawText(425, 50, posicion)

    def calcularGradosELEV(self, posicionY):
        if posicionY < 0:
            # [-1, 0] --> [-13.5º, 0º]
            angulo = posicionY * 13.5
        else:
            # [0, 1] --> [0º, 4º]
            angulo = posicionY * 4

        return angulo

    def dibujarIndicadorRudder(self, painter, posicion):

        posicion = max(-1.0, min(1.0, posicion))

        # ±45°
        angulo = math.radians(posicion * 45)

        cx = 430
        cy = 190

        # Indicador en posición neutra
        p1 = (430, 263)  # punta
        p2 = (422, 190)  # base izquierda
        p3 = (438, 190)  # base derecha

        # Punto de control para curvar la base
        pc = (430, 177)

        # Rotar todos los puntos
        p1 = self.rotar_punto(*p1, cx, cy, angulo)
        p2 = self.rotar_punto(*p2, cx, cy, angulo)
        p3 = self.rotar_punto(*p3, cx, cy, angulo)
        pc = self.rotar_punto(*pc, cx, cy, angulo)

        path = QPainterPath()

        # Punta -> base izquierda
        path.moveTo(QPointF(*p1))
        path.lineTo(QPointF(*p2))

        # Base curva
        path.quadTo(
            QPointF(*pc),
            QPointF(*p3)
        )

        # Base derecha -> punta
        path.lineTo(QPointF(*p1))

        painter.setBrush(Qt.NoBrush)
        painter.setPen(QPen(QColor(0, 255, 0), 2))

        painter.drawPath(path)

    def rotar_punto(self, x, y, cx, cy, ang):
        dx = x - cx
        dy = y - cy

        xr = dx * math.cos(ang) - dy * math.sin(ang)
        yr = dx * math.sin(ang) + dy * math.cos(ang)

        return cx + xr, cy + yr


    # FUNCIONES QUE DIBUJAN LOS ELEMENTOS ESTÁTICOS.
    def dibujarElevadorIzq(self, painter):
        # Texto.
        painter.setPen(QColor(255, 255, 255))
        painter.setFont(QFont("Times New Roman", 17))
        painter.drawText(165, 40, "L")
        painter.drawText(150, 60, "ELEV")

        painter.setPen(QPen(QColor(255, 255, 255), 1.5))
        painter.drawLine(220, 30, 220, 185)      # Línea vertical.

        painter.setBrush(Qt.NoBrush)

        # Cuadrados.
        painter.drawRect(210, 30, 10, 11)
        painter.drawRect(210, 185, 10, 11)

        # Réctangulo central.
        painter.drawRect(213, 135, 7, 5)

        # Displays Sistema de Presión Hidráulica.
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(80, 80, 80))
        painter.drawRect(150, 160, 19, 25)
        painter.drawRect(175, 160, 19, 25)

        painter.setPen(QColor(0, 255, 0))
        painter.setFont(QFont("Times New Roman", 17))
        painter.drawText(153, 178, "B")
        painter.drawText(178, 178, "G")

    def dibujarElevadorDer(self, painter):
        # Texto.
        painter.setPen(QColor(255, 255, 255))
        painter.setFont(QFont("Times New Roman", 17))
        painter.drawText(690, 40, "R")
        painter.drawText(675, 60, "ELEV")

        painter.setPen(QPen(QColor(255, 255, 255), 1.5))

        painter.drawLine(640, 30, 640, 185)  # Línea vertical.

        painter.setBrush(Qt.NoBrush)

        # Cuadrados.
        painter.drawRect(640, 29, 10, 11)
        painter.drawRect(640, 184, 10, 11)

        # Rectángulo central.
        painter.drawRect(640, 135, 7, 5)

        # Displays Sistema de Presion Hidráulica.
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(80, 80, 80))
        painter.drawRect(670, 160, 19, 25)
        painter.drawRect(695, 160, 19, 25)

        painter.setPen(QColor(0, 255, 0))
        painter.setFont(QFont("Times New Roman", 17))
        painter.drawText(673, 178, "Y")
        painter.drawText(698, 178, "B")

    def dibujarPitchRudder(self, painter):
        # Texto.
        painter.setPen(QColor(255, 255, 255))
        painter.setFont(QFont("Times New Roman", 20))
        painter.drawText(330, 20, "PITCH TRIM")

        # Displays Sistema de Presión Hidráulico.
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(80, 80, 80))
        painter.drawRect(470, 1, 19, 25)
        painter.drawRect(495, 1, 19, 25)
        painter.drawRect(396, 105, 19, 25)
        painter.drawRect(421, 105, 19, 25)
        painter.drawRect(446, 105, 19, 25)

        painter.setPen(QColor(0, 255, 0))
        painter.setFont(QFont("Times New Roman", 17))
        painter.drawText(473, 19, "G")
        painter.drawText(498, 19, "Y")
        painter.drawText(399, 123, "G")
        painter.drawText(425, 123, "B")
        painter.drawText(449, 123, "Y")

        # Pitch Trim.
        painter.setPen(QPen(QColor(255, 255, 255), 1.5))
        painter.drawLine(365, 55, 300, 75)
        painter.drawLine(300, 75, 300, 95)
        painter.drawLine(300, 95, 400, 90)

        painter.drawLine(460, 90, 560, 95)
        painter.drawLine(560, 95, 560, 75)
        painter.drawLine(560, 75, 495, 55)

        # Texto RUD.
        painter.setPen(QColor(255, 255, 255))
        painter.setFont(QFont("Times New Roman", 17))
        painter.drawText(412, 94, "RUD")

    def dibujarTimonCola(self, painter):
        # Curva.
        camino = QPainterPath()
        # Punto inicial.
        camino.moveTo(355, 250)
        # Control1, Control2, PuntoFinal
        camino.quadTo(430, 275, 505, 250)        
        painter.setPen(QPen(QColor(255, 255, 255), 1.5))
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(camino)

        # Rectángulos extremos.
        painter.drawLine(367, 255, 366, 258)
        painter.drawLine(366, 258, 374, 261)
        painter.drawLine(374, 261, 376, 257)

        painter.drawLine(493, 255, 494, 258)
        painter.drawLine(494, 258, 486, 261)
        painter.drawLine(486, 261, 484, 257)

        # Rectágulo central.
        painter.drawLine(426 , 262, 426, 267)
        painter.drawLine(426 , 267, 434, 267)
        painter.drawLine(434 , 267, 434, 263)

        # Marcas verdes.
        painter.setPen(QPen(QColor(0, 255, 0), 1.5))
        painter.drawLine(366, 254, 360, 270)
        painter.drawLine(360, 270, 365, 272)

        painter.drawLine(430, 267, 430, 275)

        painter.drawLine(494, 254, 500, 270)
        painter.drawLine(500, 270, 495, 272)