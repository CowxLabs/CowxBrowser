from PyQt6.QtWebEngineCore import QWebEngineUrlRequestInterceptor


AD_DOMAINS = {
    "doubleclick.net",
    "googlesyndication.com",
    "googleadservices.com",
    "googletagmanager.com",
    "google-analytics.com",
    "googletagservices.com",
    "googlesyndication.com",
    "amazon-adsystem.com",
    "adnxs.com",
    "rubiconproject.com",
    "pubmatic.com",
    "criteo.com",
    "outbrain.com",
    "taboola.com",
    "sharethrough.com",
    "scorecardresearch.com",
    "quantserve.com",
    "krxd.net",
    "adsrvr.org",
    "casalemedia.com",
    "moatads.com",
    "adsafeprotected.com",
    "bluekai.com",
    "exelator.com",
    "demdex.net",
    "33across.com",
    "indexww.com",
    "openx.net",
    "contextweb.com",
    "sovrn.com",
    "media.net",
    "advertising.com",
    "tribalfusion.com",
    "turn.com",
    "atdmt.com",
    "invitemedia.com",
    "netmng.com",
    "tracking1099.com",
    "adzerk.net",
    "adition.com",
    "adform.com",
    "adfox.ru",
    "adriver.ru",
    "cpmstar.com",
    "trafficfactory.biz",
    "propellerads.com",
    "popads.net",
    "onclckds.com",
}

TRACKING_DOMAINS = {
    "analytics.",
    "tracking.",
    "pixel.",
    "beacon.",
}


class AdBlockerInterceptor(QWebEngineUrlRequestInterceptor):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._enabled = True

    def set_enabled(self, enabled: bool):
        self._enabled = enabled

    def interceptRequest(self, info):
        if not self._enabled:
            return
        url = info.requestUrl().toString().lower()
        for domain in AD_DOMAINS:
            if domain in url:
                info.block(True)
                return
        for prefix in TRACKING_DOMAINS:
            if prefix in url:
                info.block(True)
                return
