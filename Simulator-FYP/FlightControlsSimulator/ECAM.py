from collections import deque
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget

from PyQt5.QtCore import QTimer 

from ReceptorDatos import ReceptorDatos
from SeccionSuperior import SeccionSuperior
from SeccionCentral import SeccionCentral
from SeccionInferior import SeccionInferior

class ECAMWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ECAM")
        self.resize(900, 700)
        self.setStyleSheet("background-color : black;")

        self.receptorUDP = ReceptorDatos(
            "192.168.1.34",
            5005,
            1024
        )

        # Variables para los Outliers.
        self.histX = deque(maxlen=3)
        self.histY = deque(maxlen=3)

        self.seccionSuperior = SeccionSuperior()
        self.seccionCentral = SeccionCentral()
        self.seccionInferior = SeccionInferior()

        layoutPrincipal = QVBoxLayout()
        layoutPrincipal.setSpacing(1)

        layoutPrincipal.addWidget(self.seccionSuperior, 1)
        layoutPrincipal.addWidget(self.seccionCentral, 1)
        layoutPrincipal.addWidget(self.seccionInferior, 2)

        widget = QWidget()
        widget.setLayout(layoutPrincipal)
        self.setCentralWidget(widget)

        self.timer = QTimer()
        self.timer.timeout.connect(self.capturarDatos)
        self.timer.start(20)
    
    def capturarDatos(self):
        datos = self.receptorUDP.recepcion()

        if datos is not None:
            x, y, sw = datos
            print(f"X:{x} Y:{y}")

            # Filtramos los Outliers.
            x, y = self.filtrarOutliers(x, y)
            # Normalizamos los datos en el rango [-1, +1]
            xNorm, yNorm = self.normalizarDatos(x, y)
            # Aplicamos la ZonaM del Joystick.
            x, y = self.aplicarZonaM(xNorm, yNorm)

            # Envío datos a las secciones de la UI para su actualización.
            self.seccionSuperior.actualizarUI(sw)
            self.seccionCentral.actualizarUI(x)
            self.seccionInferior.actualizarUI(x, y)

    def filtrarOutliers(self, x, y):

        self.histX.append(x)
        self.histY.append(y)

        xFiltrado = sorted(self.histX)[len(self.histX) // 2]
        yFiltrado = sorted(self.histY)[len(self.histY) // 2]

        return xFiltrado, yFiltrado

    def normalizarDatos(self, x, y):
        centroX = 1956
        centroY = 1956

        if (x >= centroX):
            xNorm = (x - centroX) / (4095 - centroX)
        else:
            xNorm = (x - centroX) / centroX

        if (y >= centroY):
            yNorm = (y - centroY) / (4095 - centroY)
        else:
            yNorm = (y - centroY) / centroY

        xNorm = max(-1, min(1, xNorm))
        yNorm = max(-1, min(1, yNorm))

        return xNorm, yNorm

    def aplicarZonaM(self, x, y):
        zonaM = 0.02
        xNorm = x
        yNorm = y

        if (abs(x) <= zonaM):
            xNorm = 0.0

        if (abs(y) <= zonaM):
            yNorm = 0.0

        return xNorm, yNorm

if __name__ == "__main__":
    # Ventana Principal.
    app = QApplication(sys.argv)
    window = ECAMWindow()
    window.show()

    sys.exit(app.exec_())