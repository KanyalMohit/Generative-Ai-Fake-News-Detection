import html
import sys
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QPlainTextEdit,
    QProgressBar,
    QScrollArea,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from api_worker import ApiWorker
from ui_components import ModeCard, MetricChip, ResultSection
from styles import get_stylesheet

BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.worker = None
        self.selected_mode = "text"
        self.selected_image = None
        self.selected_video = None

        self.setWindowTitle("Satya:- fake news and deepfakes detectores")
        self.resize(1560, 960)
        self.setMinimumSize(1360, 880)

        container = QWidget()
        self.setCentralWidget(container)
        root = QHBoxLayout(container)
        root.setContentsMargins(24, 24, 24, 24)
        root.setSpacing(20)

        root.addWidget(self.build_sidebar(), 0)
        root.addWidget(self.build_main_panel(), 1)

        self.apply_styles()
        self.update_mode_ui()
        self.reset_result_view()

    def build_sidebar(self):
        panel = QFrame()
        panel.setObjectName("sidebar")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(18)

        badge = QLabel("SATYA")
        badge.setObjectName("logoBadge")
        title = QLabel("Satya:-\nFake news and deepfakes detectores")
        title.setWordWrap(True)
        title.setObjectName("heroTitle")
        subtitle = QLabel(
            "Designed to feel premium: mode-led workflows, strong visual hierarchy, and result panels built for demos."
        )
        subtitle.setWordWrap(True)
        subtitle.setObjectName("heroSubtitle")

        layout.addWidget(badge)
        layout.addWidget(title)
        layout.addWidget(subtitle)

        self.mode_cards = {}
        grid = QGridLayout()
        grid.setHorizontalSpacing(12)
        grid.setVerticalSpacing(12)

        card_data = [
            ("Text", "Paste a claim, article, or long post and verify the core narrative.", ASSETS_DIR / "text_mode.svg", "text"),
            ("URL", "Point to a story link and let the backend inspect the page before scoring.", ASSETS_DIR / "url_mode.svg", "url"),
            ("Image", "Analyze screenshots, posters, memes, and visual misinformation.", ASSETS_DIR / "image_mode.svg", "image"),
            ("Video", "Queue deepfake analysis and watch the verdict pipeline complete.", ASSETS_DIR / "video_mode.svg", "video"),
        ]

        for index, (title_text, desc, icon, key) in enumerate(card_data):
            card = ModeCard(title_text, desc, icon, key)
            card.clicked.connect(lambda checked=False, k=key: self.select_mode(k))
            self.mode_cards[key] = card
            grid.addWidget(card, index // 2, index % 2)

        layout.addLayout(grid)

        activity = QFrame()
        activity.setObjectName("activityCard")
        activity_layout = QVBoxLayout(activity)
        activity_layout.setContentsMargins(18, 18, 18, 18)
        activity_layout.setSpacing(8)
        activity_title = QLabel("Live Activity")
        activity_title.setObjectName("sectionTitle")
        self.activity_label = QLabel(
            "Idle right now. When you run an analysis, this panel will describe what the desktop client is doing."
        )
        self.activity_label.setWordWrap(True)
        self.activity_label.setObjectName("activityBody")
        activity_layout.addWidget(activity_title)
        activity_layout.addWidget(self.activity_label)
        layout.addWidget(activity)

        layout.addStretch()
        footer = QLabel("Desktop GUI • FastAPI gateway • Gemini-first runtime")
        footer.setObjectName("sidebarFooter")
        layout.addWidget(footer)
        return panel

    def build_main_panel(self):
        wrapper = QFrame()
        wrapper.setObjectName("mainPanel")
        outer = QVBoxLayout(wrapper)
        outer.setContentsMargins(24, 24, 24, 24)
        outer.setSpacing(18)

        topbar = QHBoxLayout()
        topbar.setSpacing(14)
        
        # We removed the URL connection status chip to clean up the UI
        self.mode_chip = QLabel("Mode: Text")
        self.mode_chip.setObjectName("statusChipAccent")
        topbar.addWidget(self.mode_chip)
        topbar.addStretch()

        self.analyze_button = QPushButton("Analyze Text")
        self.analyze_button.setObjectName("analyzeButton")
        self.analyze_button.clicked.connect(self.run_analysis)
        topbar.addWidget(self.analyze_button)
        outer.addLayout(topbar)

        self.stack = QStackedWidget()
        self.stack.addWidget(self.build_text_page())
        self.stack.addWidget(self.build_url_page())
        self.stack.addWidget(self.build_image_page())
        self.stack.addWidget(self.build_video_page())
        outer.addWidget(self.stack)

        chip_row = QHBoxLayout()
        chip_row.setSpacing(12)
        self.metric_confidence = MetricChip("Confidence", "—")
        self.metric_research = MetricChip("Research Mode", "—")
        self.metric_credibility = MetricChip("Credibility", "—")
        self.metric_action = MetricChip("Action", "Waiting")
        chip_row.addWidget(self.metric_confidence)
        chip_row.addWidget(self.metric_research)
        chip_row.addWidget(self.metric_credibility)
        chip_row.addWidget(self.metric_action)
        outer.addLayout(chip_row)

        self.progress = QProgressBar()
        self.progress.setRange(0, 0)
        self.progress.setVisible(False)
        self.progress.setObjectName("progressBar")
        outer.addWidget(self.progress)

        results_scroll = QScrollArea()
        results_scroll.setWidgetResizable(True)
        results_scroll.setFrameShape(QFrame.NoFrame)
        results_container = QWidget()
        results_scroll.setWidget(results_container)
        results_layout = QVBoxLayout(results_container)
        results_layout.setContentsMargins(0, 0, 0, 0)
        results_layout.setSpacing(14)

        hero = QFrame()
        self.hero_frame = hero
        hero.setObjectName("verdictHero")
        hero_layout = QVBoxLayout(hero)
        hero_layout.setContentsMargins(22, 20, 22, 20)
        hero_layout.setSpacing(10)
        verdict_row = QHBoxLayout()
        verdict_row.setSpacing(12)
        self.verdict_badge = QLabel("READY")
        self.verdict_badge.setObjectName("verdictBadge")
        verdict_row.addWidget(self.verdict_badge, alignment=Qt.AlignLeft)
        verdict_row.addStretch()
        self.verdict_label = QLabel("Ready for analysis")
        self.verdict_label.setObjectName("verdictTitle")
        self.summary_label = QLabel("Select a mode, provide input, and generate a structured verification report.")
        self.summary_label.setWordWrap(True)
        self.summary_label.setObjectName("verdictSummary")
        hero_layout.addLayout(verdict_row)
        hero_layout.addWidget(self.verdict_label)
        hero_layout.addWidget(self.summary_label)
        results_layout.addWidget(hero)

        self.metrics = ResultSection("Overview")
        self.reasoning = ResultSection("Reasoning & Cross Verification")
        self.evidence = ResultSection("Evidence For / Against")
        self.claims = ResultSection("Claims, Uncertainty & Sources")

        results_layout.addWidget(self.metrics)
        results_layout.addWidget(self.reasoning)
        results_layout.addWidget(self.evidence)
        results_layout.addWidget(self.claims)

        outer.addWidget(results_scroll, 1)
        return wrapper

    def build_text_page(self):
        page = QFrame()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        heading = QLabel("Paste text or a news claim")
        heading.setObjectName("inputTitle")
        desc = QLabel("Use this for copied articles, headlines, viral posts, captions, or long-form claims.")
        desc.setObjectName("inputSubtitle")
        self.text_input = QPlainTextEdit()
        self.text_input.setPlaceholderText("Paste the text you want to verify...")
        self.text_input.setObjectName("editor")
        layout.addWidget(heading)
        layout.addWidget(desc)
        layout.addWidget(self.text_input)
        return page

    def build_url_page(self):
        page = QFrame()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        heading = QLabel("Verify a URL")
        heading.setObjectName("inputTitle")
        desc = QLabel("Drop in an article or post link and let the backend fetch page text before analysis.")
        desc.setObjectName("inputSubtitle")
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("https://example.com/news-story")
        self.url_input.setObjectName("lineInput")
        layout.addWidget(heading)
        layout.addWidget(desc)
        layout.addWidget(self.url_input)
        layout.addStretch()
        return page

    def build_image_page(self):
        page = QFrame()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        heading = QLabel("Analyze an image")
        heading.setObjectName("inputTitle")
        desc = QLabel("Use screenshots, posters, tweets, memes, or other image-based misinformation candidates.")
        desc.setObjectName("inputSubtitle")
        self.image_path_label = QLabel("No image selected yet")
        self.image_path_label.setObjectName("fileLabel")
        picker = QPushButton("Choose Image")
        picker.setObjectName("secondaryButton")
        picker.clicked.connect(self.pick_image)
        layout.addWidget(heading)
        layout.addWidget(desc)
        layout.addWidget(self.image_path_label)
        layout.addWidget(picker, alignment=Qt.AlignLeft)
        layout.addStretch()
        return page

    def build_video_page(self):
        page = QFrame()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        heading = QLabel("Inspect a video")
        heading.setObjectName("inputTitle")
        desc = QLabel("Queue a video for deepfake inspection through the backend gateway and worker.")
        desc.setObjectName("inputSubtitle")
        self.video_path_label = QLabel("No video selected yet")
        self.video_path_label.setObjectName("fileLabel")
        picker = QPushButton("Choose Video")
        picker.setObjectName("secondaryButton")
        picker.clicked.connect(self.pick_video)
        layout.addWidget(heading)
        layout.addWidget(desc)
        layout.addWidget(self.video_path_label)
        layout.addWidget(picker, alignment=Qt.AlignLeft)
        layout.addStretch()
        return page

    def select_mode(self, mode: str):
        self.selected_mode = mode
        self.stack.setCurrentIndex({"text": 0, "url": 1, "image": 2, "video": 3}[mode])
        self.update_mode_ui()
        prompts = {
            "text": "Ready to inspect pasted text for misinformation patterns.",
            "url": "Ready to fetch and analyze a live article URL.",
            "image": "Ready to send an image through the visual analysis flow.",
            "video": "Ready to queue deepfake inspection through the backend worker.",
        }
        self.activity_label.setText(prompts[mode])

    def update_mode_ui(self):
        for key, card in self.mode_cards.items():
            card.setChecked(key == self.selected_mode)
        self.mode_chip.setText(f"Mode: {self.selected_mode.capitalize()}")
        self.analyze_button.setText({
            "text": "Analyze Text",
            "url": "Analyze URL",
            "image": "Analyze Image",
            "video": "Analyze Video",
        }[self.selected_mode])

    def pick_image(self):
        path, _ = QFileDialog.getOpenFileName(self, "Choose image", "", "Images (*.png *.jpg *.jpeg *.webp *.gif)")
        if path:
            self.selected_image = path
            self.image_path_label.setText(path)
            self.activity_label.setText("Image loaded. Ready to send it to the backend.")

    def pick_video(self):
        path, _ = QFileDialog.getOpenFileName(self, "Choose video", "", "Videos (*.mp4 *.mov *.avi *.mkv *.webm)")
        if path:
            self.selected_video = path
            self.video_path_label.setText(path)
            self.activity_label.setText("Video queued locally. Run analysis to start worker-side inspection.")

    def set_loading(self, loading: bool, message: str | None = None):
        self.progress.setVisible(loading)
        self.analyze_button.setDisabled(loading)
        if message:
            self.activity_label.setText(message)

    def run_analysis(self):
        try:
            if self.selected_mode == "text":
                content = self.text_input.toPlainText().strip()
                if not content:
                    raise ValueError("Paste some text first.")
                self.worker = ApiWorker("text", payload={"content": content})
            elif self.selected_mode == "url":
                content = self.url_input.text().strip()
                if not content:
                    raise ValueError("Enter a URL first.")
                self.worker = ApiWorker("url", payload={"content": content})
            elif self.selected_mode == "image":
                if not self.selected_image:
                    raise ValueError("Choose an image file first.")
                self.worker = ApiWorker("image", file_path=self.selected_image)
            else:
                if not self.selected_video:
                    raise ValueError("Choose a video file first.")
                self.worker = ApiWorker("video", file_path=self.selected_video)
        except Exception as exc:
            QMessageBox.warning(self, "Missing input", str(exc))
            return

        self.activity_label.setText(f"Running {self.selected_mode} analysis and waiting for the backend response...")
        self.set_loading(True, f"Talking to backend...")
        self.worker.finished.connect(self.handle_result)
        self.worker.failed.connect(self.handle_error)
        self.worker.start()

    def reset_result_view(self):
        self.verdict_badge.setText("READY")
        self.verdict_label.setText("Ready for analysis")
        self.summary_label.setText("Select a mode, provide input, and generate a structured verification report.")
        self.metric_confidence.set_value("—")
        self.metric_research.set_value("—")
        self.metric_credibility.set_value("—")
        self.metric_action.set_value("Waiting")
        self.hero_frame.setProperty("verdictTone", "neutral")
        self.refresh_styles()

    def refresh_styles(self):
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()

    def bullet_html(self, items):
        if not items:
            return "<p style='color:#9aa3b2;'>No data returned.</p>"
        return "<ul>" + "".join(f"<li>{html.escape(str(item))}</li>" for item in items) + "</ul>"

    def set_verdict_tone(self, label: str, is_deepfake: bool):
        tone = "neutral"
        if label == "REAL":
            tone = "success"
        elif label in {"FAKE", "MISLEADING"} or is_deepfake:
            tone = "danger"
        elif label in {"UNKNOWN", "UNVERIFIED"}:
            tone = "warning"
        self.hero_frame.setProperty("verdictTone", tone)
        self.refresh_styles()

    def handle_result(self, data: dict):
        self.set_loading(False, f"Connected to backend.")
        label = data.get("label") or ("DEEPFAKE DETECTED" if data.get("is_deepfake") else "LIKELY AUTHENTIC")
        confidence = data.get("confidence", data.get("confidence_score", "N/A"))
        summary = data.get("summary") or data.get("verdict_explanation") or data.get("short_explanation") or "Analysis complete."
        research_mode = data.get("research_mode", "n/a")
        credibility = data.get("credibility_analysis", {}).get("credibility_score", "N/A")
        action = data.get("recommended_user_action", "Review carefully before sharing.")

        self.verdict_badge.setText(label.upper())
        self.verdict_label.setText(f"{label} • Confidence: {confidence}")
        self.summary_label.setText(summary)
        self.metric_confidence.set_value(confidence)
        self.metric_research.set_value(research_mode)
        self.metric_credibility.set_value(credibility)
        self.metric_action.set_value("Act carefully")
        self.activity_label.setText(f"Finished {self.selected_mode} analysis. Research mode: {research_mode}.")
        self.set_verdict_tone(label, bool(data.get("is_deepfake")))

        overview_html = f"""
        <p><b>Research mode:</b> {html.escape(str(research_mode))}</p>
        <p><b>Recommended action:</b> {html.escape(str(action))}</p>
        <p><b>Source credibility:</b> {html.escape(str(credibility))}</p>
        <p>{html.escape(str(data.get('credibility_analysis', {}).get('source_reputation', 'No source reputation note returned.')))}</p>
        """
        self.metrics.set_html(overview_html)

        reasoning_html = f"""
        <p><b>Final reasoning</b></p>
        <p>{html.escape(str(data.get('final_reasoning', data.get('verdict_explanation', 'No reasoning returned.'))))}</p>
        <p><b>Common points</b></p>
        <p>{html.escape(str(data.get('cross_verification', {}).get('common_points', 'N/A')))}</p>
        <p><b>Discrepancies</b></p>
        <p>{html.escape(str(data.get('cross_verification', {}).get('discrepancies', 'N/A')))}</p>
        """
        self.reasoning.set_html(reasoning_html)

        evidence_against = data.get("evidence_against") or data.get("visual_anomalies") or data.get("audio_anomalies")
        evidence_html = f"""
        <p><b>Evidence for</b></p>
        {self.bullet_html(data.get('evidence_for'))}
        <p><b>Evidence against</b></p>
        {self.bullet_html(evidence_against)}
        """
        self.evidence.set_html(evidence_html)

        citations = data.get("citations") or []
        citation_html = (
            "<ul>" + "".join(
                f"<li>{html.escape(c if isinstance(c, str) else c.get('url', str(c)))}</li>" for c in citations
            ) + "</ul>"
        ) if citations else "<p style='color:#9aa3b2;'>No citations returned.</p>"

        claims_html = f"""
        <p><b>Detected claims</b></p>
        {self.bullet_html(data.get('detected_claims'))}
        <p><b>Uncertainty notes</b></p>
        {self.bullet_html(data.get('uncertainty_notes'))}
        <p><b>Sources</b></p>
        {citation_html}
        """
        self.claims.set_html(claims_html)

    def handle_error(self, error: str):
        self.set_loading(False, f"Backend error")
        self.activity_label.setText("The backend returned an error. Review the message and try again.")
        QMessageBox.critical(self, "Analysis failed", error)

    def apply_styles(self):
        self.setStyleSheet(get_stylesheet())


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Satya:- fake news and deepfakes detectores")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
