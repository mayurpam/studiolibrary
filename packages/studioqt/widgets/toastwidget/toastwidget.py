#Embedded file name: C:/Users/hovel/Dropbox/packages/studiolibrary/1.23.2/build27/studiolibrary/packages/studioqt\widgets\toastwidget\toastwidget.py
import logging
from studioqt import QtGui
from studioqt import QtCore
from studioqt import QtWidgets
import studioqt
logger = logging.getLogger(__name__)

class ToastWidget(QtWidgets.QLabel):
    DEFAULT_DURATION = 500
    FOREGROUND_COLOR = QtGui.QColor(255, 255, 255)
    BACKGROUND_COLOR = QtGui.QColor(0, 0, 0)

    def __init__(self, *args):
        QtWidgets.QLabel.__init__(self, *args)
        self.setMouseTracking(True)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        self._alpha = 255
        self._messageDisplayTimer = QtCore.QTimer(self)
        self._messageDisplayTimer.timeout.connect(self.fadeOut)
        self._messageFadeOutTimer = QtCore.QTimer(self)
        self._messageFadeOutTimer.timeout.connect(self._fadeOut)

    def alignTo(self, widget, padding = 30):
        width = self.textWidth() + padding
        height = self.textHeight() + padding
        x = widget.width() / 2 - width / 2
        y = (widget.height() - height) / 1.2
        self.setGeometry(x, y, width, height)

    def textRect(self):
        text = self.text()
        font = self.font()
        metrics = QtGui.QFontMetricsF(font)
        return metrics.boundingRect(text)

    def textWidth(self):
        textWidth = self.textRect().width()
        return max(0, textWidth)

    def textHeight(self):
        textHeight = self.textRect().height()
        return max(0, textHeight)

    def fadeOut(self):
        """
        :rtype: None
        """
        self._messageFadeOutTimer.start(5)

    def _fadeOut(self):
        """
        :rtype: None
        """
        alpha = self.alpha()
        if alpha > 0:
            alpha -= 2
            self.setAlpha(alpha)
        else:
            self.hide()
            self._messageFadeOutTimer.stop()
            self._messageDisplayTimer.stop()

    def setText(self, text, duration = None):
        """
        :type text: str
        :rtype: None
        """
        QtWidgets.QLabel.setText(self, text)
        duration = duration or self.DEFAULT_DURATION
        self.setAlpha(255)
        self._messageDisplayTimer.stop()
        self._messageDisplayTimer.start(duration)
        self.show()
        self.update()
        self.repaint()

    def alpha(self):
        """
        :rtype: float
        """
        return float(self._alpha)

    def setAlpha(self, value):
        """
        :type value: float
        :rtype: None
        """
        if value < 0:
            value = 0
        textAlpha = value
        backgroundAlpha = value / 1.4
        color = ToastWidget.FOREGROUND_COLOR
        backgroundColor = ToastWidget.BACKGROUND_COLOR
        color = studioqt.Color.fromColor(color)
        color.setAlpha(textAlpha)
        backgroundColor = studioqt.Color.fromColor(backgroundColor)
        backgroundColor.setAlpha(backgroundAlpha)
        styleSheet = 'color: {0}; background-color: {1};'
        styleSheet = styleSheet.format(color.toString(), backgroundColor.toString())
        self.setStyleSheet(styleSheet)
        self._alpha = value
