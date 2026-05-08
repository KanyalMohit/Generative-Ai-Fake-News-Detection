from pathlib import Path
from PySide6.QtCore import Qt
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QPushButton,
    QTextBrowser,
    QVBoxLayout,
    QSizePolicy
)

class ModeCard(QPushButton):
    def __init__(self, title: str, subtitle: str, icon_path: Path, mode_key: str):
        super().__init__()
        self.mode_key = mode_key
        self.setCheckable(True)
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumHeight(172)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(10)

        icon = QSvgWidget(str(icon_path))
        icon.setFixedSize(68, 68)
        layout.addWidget(icon, alignment=Qt.AlignLeft)

        eyebrow = QLabel("MODE")
        eyebrow.setObjectName("cardEyebrow")
        title_label = QLabel(title)
        title_label.setProperty("class", "cardTitle")
        subtitle_label = QLabel(subtitle)
        subtitle_label.setWordWrap(True)
        subtitle_label.setProperty("class", "cardSubtitle")

        layout.addWidget(eyebrow)
        layout.addWidget(title_label)
        layout.addWidget(subtitle_label)
        layout.addStretch()


class MetricChip(QFrame):
    def __init__(self, title: str, value: str):
        super().__init__()
        self.setObjectName("metricChip")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(4)
        self.title = QLabel(title)
        self.title.setObjectName("metricLabel")
        self.value = QLabel(value)
        self.value.setObjectName("metricValue")
        layout.addWidget(self.title)
        layout.addWidget(self.value)

    def set_value(self, value: str):
        self.value.setText(str(value))


class ResultSection(QFrame):
    def __init__(self, title: str):
        super().__init__()
        self.setObjectName("resultCard")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(10)

        heading = QLabel(title)
        heading.setObjectName("sectionTitle")
        layout.addWidget(heading)

        self.body = QTextBrowser()
        self.body.setOpenExternalLinks(True)
        self.body.setFrameShape(QFrame.NoFrame)
        self.body.setMinimumHeight(140)
        self.body.setObjectName("sectionBody")

        # Explicitly make the QTextBrowser transparent to avoid black backgrounds
        self.body.setStyleSheet("QTextBrowser { background-color: transparent; border: none; }")
        
        # In PySide6, setting viewport autoFillBackground to False helps transparency
        self.body.viewport().setAutoFillBackground(False)
        self.body.setAttribute(Qt.WA_TranslucentBackground)

        layout.addWidget(self.body)

    def set_html(self, html_text: str):
        # We specify transparent background directly on the HTML body
        document = self.body.document()
        document.setDocumentMargin(0)
        html_content = f"<html><body style='background-color: transparent; color: #dfe7ff;'>{html_text}</body></html>"
        self.body.setHtml(html_content)
