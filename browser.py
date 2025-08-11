from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PyQt5.QtCore import QUrl

class Browser:
    def __init__(self):
        self.window = QWidget()
        self.window.setWindowTitle("JARVIS - Navegador")
        self.window.resize(1200, 800)

        self.layout = QVBoxLayout()
        self.horizontal = QHBoxLayout()

        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Digite a URL aqui")
        self.url_bar.setMinimumHeight(30)

        self.go_button = QPushButton("Go")
        self.go_button.setMinimumHeight(30)

        self.back_button = QPushButton("<")
        self.back_button.setMinimumHeight(30)

        self.forward_button = QPushButton(">")
        self.forward_button.setMinimumHeight(30)

        self.horizontal.addWidget(self.url_bar)
        self.horizontal.addWidget(self.go_button)
        self.horizontal.addWidget(self.back_button)
        self.horizontal.addWidget(self.forward_button)

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://google.com"))

        # Configurações do navegador
        self.browser.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        self.browser.settings().setAttribute(QWebEngineSettings.ErrorPageEnabled, False)
        self.browser.settings().setAttribute(QWebEngineSettings.JavascriptCanOpenWindows, False)

        # Conexões
        self.go_button.clicked.connect(self.go_to_url)
        self.url_bar.returnPressed.connect(self.go_to_url)
        self.back_button.clicked.connect(self.browser.back)
        self.forward_button.clicked.connect(self.browser.forward)
        self.browser.urlChanged.connect(self.update_url_bar)
        self.browser.titleChanged.connect(self.update_window_title)

        self.layout.addLayout(self.horizontal)
        self.layout.addWidget(self.browser)

        self.window.setLayout(self.layout)
        self.window.show()

    def go_to_url(self):
        url = self.url_bar.text().strip()
        if not url:
            url = "https://www.google.com"
        elif not url.startswith("http://") and not url.startswith("https://"):
            url = "https://" + url
        self.browser.setUrl(QUrl(url))

    def update_url_bar(self, q):
        self.url_bar.setText(q.toString())

    def update_window_title(self, title):
        self.window.setWindowTitle(f"JARVIS - {title}")


app = QApplication([])
window = Browser()
app.exec()