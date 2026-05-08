def get_stylesheet():
    return """
        QWidget {
            background: #0a1020;
            color: #eef2ff;
            font-family: 'Segoe UI', 'Inter', sans-serif;
            font-size: 14px;
        }
        QMainWindow {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #070b16, stop:0.45 #10162c, stop:1 #07111e);
        }
        #sidebar, #mainPanel {
            background: rgba(13, 20, 38, 0.94);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 28px;
        }
        #logoBadge {
            padding: 8px 14px;
            border-radius: 16px;
            background: rgba(109, 94, 247, 0.18);
            border: 1px solid rgba(165, 155, 255, 0.28);
            color: #d9d4ff;
            font-weight: 800;
            letter-spacing: 1px;
        }
        #heroTitle {
            font-size: 30px;
            font-weight: 800;
            line-height: 1.2em;
        }
        #heroSubtitle, #sidebarFooter, .cardSubtitle, #inputSubtitle, #verdictSummary, #activityBody {
            color: #9aa3b2;
            line-height: 1.55em;
        }
        #cardEyebrow {
            color: #84dbff;
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 1.8px;
        }
        ModeCard, QPushButton {
            border: none;
        }
        ModeCard {
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.06);
            border-radius: 24px;
            text-align: left;
        }
        ModeCard:hover {
            background: rgba(255,255,255,0.08);
            border: 1px solid rgba(255,255,255,0.13);
        }
        ModeCard:checked {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 rgba(109,94,247,0.26), stop:1 rgba(29,213,192,0.18));
            border: 1px solid rgba(165, 155, 255, 0.42);
        }
        QLabel[class="cardTitle"] {
            font-size: 18px;
            font-weight: 700;
        }
        QLabel[class="cardSubtitle"] {
            font-size: 13px;
            background: transparent;
        }
        #activityCard, #metricChip {
            background: rgba(255,255,255,0.035);
            border: 1px solid rgba(255,255,255,0.07);
            border-radius: 22px;
        }
        #statusChipAccent {
            padding: 10px 14px;
            border-radius: 16px;
            background: rgba(29,213,192,0.12);
            border: 1px solid rgba(29,213,192,0.24);
            color: #82f4e5;
        }
        #analyzeButton {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #6d5ef7, stop:1 #18c7b1);
            color: white;
            padding: 14px 22px;
            border-radius: 18px;
            font-size: 15px;
            font-weight: 700;
        }
        #analyzeButton:hover {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #8072ff, stop:1 #24e2ca);
        }
        #secondaryButton {
            background: rgba(255,255,255,0.07);
            border: 1px solid rgba(255,255,255,0.10);
            padding: 12px 18px;
            border-radius: 16px;
            font-weight: 600;
        }
        #inputTitle {
            font-size: 22px;
            font-weight: 700;
        }
        #editor, #lineInput {
            background: rgba(255,255,255,0.035);
            border: 1px solid rgba(255,255,255,0.07);
            border-radius: 18px;
            padding: 14px;
            selection-background-color: #6d5ef7;
        }
        #editor {
            min-height: 230px;
        }
        #fileLabel {
            padding: 16px;
            border-radius: 16px;
            background: rgba(255,255,255,0.035);
            border: 1px dashed rgba(255,255,255,0.18);
            color: #cdd4e1;
        }
        #verdictHero {
            border-radius: 24px;
            border: 1px solid rgba(165,155,255,0.20);
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 rgba(109,94,247,0.22), stop:1 rgba(24,199,177,0.12));
        }
        #verdictHero[verdictTone="success"] {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 rgba(26,182,110,0.28), stop:1 rgba(18,64,45,0.32));
            border: 1px solid rgba(92,232,162,0.26);
        }
        #verdictHero[verdictTone="danger"] {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 rgba(239,87,120,0.30), stop:1 rgba(78,21,49,0.34));
            border: 1px solid rgba(255,130,160,0.22);
        }
        #verdictHero[verdictTone="warning"] {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 rgba(255,182,72,0.28), stop:1 rgba(90,48,16,0.34));
            border: 1px solid rgba(255,210,125,0.22);
        }
        #verdictBadge {
            padding: 8px 12px;
            border-radius: 14px;
            background: rgba(255,255,255,0.10);
            color: white;
            font-size: 11px;
            font-weight: 800;
            letter-spacing: 1.2px;
        }
        #verdictTitle {
            font-size: 30px;
            font-weight: 800;
        }
        #resultCard {
            background: rgba(255,255,255,0.035);
            border: 1px solid rgba(255,255,255,0.07);
            border-radius: 22px;
        }
        #sectionTitle {
            font-size: 17px;
            font-weight: 700;
        }
        #sectionBody {
            background: transparent;
            color: #dfe7ff;
            border: none;
        }
        QTextBrowser {
            background: transparent;
            border: none;
            background-color: transparent !important;
        }
        #sectionBody a {
            color: #7edcff;
        }
        #metricLabel {
            color: #93a0b8;
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 1.2px;
            text-transform: uppercase;
        }
        #metricValue {
            color: #eef2ff;
            font-size: 18px;
            font-weight: 700;
        }
        #progressBar {
            background: rgba(255,255,255,0.04);
            border-radius: 10px;
            min-height: 8px;
        }
        #progressBar::chunk {
            border-radius: 10px;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #6d5ef7, stop:1 #18c7b1);
        }
        QScrollArea, QScrollBar:vertical, QScrollBar:horizontal {
            background: transparent;
            border: none;
        }
    """
