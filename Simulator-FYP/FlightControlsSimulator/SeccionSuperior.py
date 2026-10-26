from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPen, QColor, QFont, QPolygon
from PyQt5.QtCore import QPoint, Qt

class SeccionSuperior(QWidget):
    def __init__(self):
        super().__init__()

        self.joystickSW = 0
        self.joystickSWant = 0
        self.desplegarSpoilers = False

    def paintEvent(self, event):
        painter = QPainter(self)

        painter.fillRect(self.rect(), Qt.black)

        self.dibujarTexoPag(painter)
        self.dibujarCorchetes(painter)
        self.dibujarLineasSpoilers(painter)
        self.dibujarTextoDisplays(painter)
        self.dibujarIndicadorSpoilers(painter, self.joystickSW)

    def actualizarUI(self, sw):
        # Comprobamos si se ha pulsado el botón del joystick.
        # Cambio de 1 --> 0.
        if ((self.joystickSWant == 1) and (sw == 0)):
            self.desplegarSpoilers = not self.desplegarSpoilers

        self.joystickSWant = sw

        self.update()

    def dibujarIndicadorSpoilers(self, painter, switch):
        # Si se cumple la condición se dibujan los spoilers
        # desplegados.
        if self.desplegarSpoilers:
            colorVerde = QColor(0, 255, 0)

            painter.setPen(QPen(colorVerde, 1))
            painter.setBrush(Qt.NoBrush)

            posiciones = [
                (162, 125),
                (212, 120),
                (262, 115),
                (312, 110),
                (362, 105),
                (512, 105),
                (562, 110),
                (612, 115),
                (662, 120),
                (712, 125)
            ]

            for x, y in posiciones:

                # Línea vertical de la flecha
                painter.drawLine(
                    x, y,
                    x, y - 32
                )

                # Punta triangular cerrada
                triangulo = QPolygon([
                    QPoint(x,     y - 44),
                    QPoint(x - 8, y - 32),
                    QPoint(x + 8, y - 32)
                ])

                painter.drawPolygon(triangulo)


    # FUNCIONES QUE DIBUJAN LOS ELEMENTOS ESTÁTICOS.
    def dibujarTexoPag(self, painter):
        painter.setPen(QColor(255, 255, 255))
        fuente = QFont("Times New Roman", 30)
        fuente.setUnderline(True)
        painter.setFont(fuente)
        painter.drawText(10, 25, "F/CTL")

    def dibujarCorchetes(self, painter):
        painter.setPen(QPen(QColor(255, 255, 255), 1.5))

        # Corchete superior izq.
        painter.drawLine(150, 70, 350, 45)
        painter.drawLine(150, 70, 150, 75)
        painter.drawLine(350, 45, 350, 50)

        # Corchete inferior izq.
        painter.drawLine(190, 140, 350, 125)
        painter.drawLine(190, 140, 190, 135)
        painter.drawLine(350, 125, 350, 120)

        # Corchete superior der.
        painter.drawLine(525, 45, 725, 70)
        painter.drawLine(525, 45, 525, 50)
        painter.drawLine(725, 70, 725, 75)

        # Corchete inferior der.
        painter.drawLine(525, 125, 685, 140)
        painter.drawLine(525, 125, 525, 120)
        painter.drawLine(685, 140, 685, 135)

    def dibujarLineasSpoilers(self, painter):
        painter.setPen(QPen(QColor(0, 255, 0), 2))

        # Spoilers ala izquierda.
        painter.drawLine(155, 125, 170, 125)
        painter.drawLine(205, 120, 220, 120)
        painter.drawLine(255, 115, 270, 115)
        painter.drawLine(305, 110, 320, 110)
        painter.drawLine(355, 105, 370, 105)

        # Spoilers ala derecha.
        painter.drawLine(505, 105, 520, 105)
        painter.drawLine(555, 110, 570, 110)
        painter.drawLine(605, 115, 620, 115)
        painter.drawLine(655, 120, 670, 120)
        painter.drawLine(705, 125, 720, 125)

    def dibujarTextoDisplays(self, painter):
        # Texto Speed Brakes.
        painter.setPen(QColor(255, 255, 255))
        painter.setFont(QFont("Times New Roman", 17))
        painter.drawText(400, 130, "SPD BRK")

        # Texto Sistema de Presion Hidráulica.
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(80, 80, 80))
        painter.drawRect(402, 30, 19, 25)
        painter.drawRect(427, 30, 19, 25)
        painter.drawRect(452, 30, 19, 25)
        
        painter.setPen(QColor(0, 255, 0))
        painter.setFont(QFont("Times New Roman", 17))
        painter.drawText(405, 48, "G")
        painter.drawText(430, 48, "B")
        painter.drawText(455, 48, "Y")