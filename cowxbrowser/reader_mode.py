from PyQt6.QtCore import QUrl


READER_JS = """
(function() {
    var existing = document.getElementById('__cowx_reader_style');
    if (existing) {
        existing.remove();
        return;
    }
    var style = document.createElement('style');
    style.id = '__cowx_reader_style';
    style.textContent = `
        body {
            max-width: 700px !important;
            margin: 40px auto !important;
            padding: 0 24px !important;
            font-family: Georgia, 'Times New Roman', serif !important;
            font-size: 18px !important;
            line-height: 1.8 !important;
            color: #222 !important;
            background: #fafafa !important;
            float: none !important;
        }
        nav, .sidebar, .ads, .ad, footer, .footer, .comments,
        .comment, .share, .social, .related, .recommended,
        script, iframe, .sidebar, .aside, [role="complementary"],
        [role="navigation"], .advertisement, .ad-container {
            display: none !important;
        }
        img, video {
            max-width: 100% !important;
            height: auto !important;
        }
        a { color: #3366cc !important; }
        h1, h2, h3 {
            font-family: -apple-system, Helvetica, Arial, sans-serif !important;
            line-height: 1.3 !important;
        }
        * {
            background: transparent !important;
            box-shadow: none !important;
            text-shadow: none !important;
        }
        p { margin: 1.2em 0 !important; }
    `;
    document.head.appendChild(style);
})();
"""


def toggle_reader_mode(webview):
    webview.page().runJavaScript(READER_JS)


class ReaderMode:
    @staticmethod
    def toggle(webview):
        toggle_reader_mode(webview)
