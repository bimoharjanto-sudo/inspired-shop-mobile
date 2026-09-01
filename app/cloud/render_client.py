import json
import os
import urllib.request
import urllib.error


class CloudRenderClient:
    """
    Thin client untuk Cloud Render Bridge.

    CATATAN:
    HF_TOKEN TIDAK BOLEH disimpan di APK.
    APK hanya berkomunikasi dengan bridge.
    """

    def __init__(self, base_url=None):
        self.base_url = (
            base_url
            or os.environ.get("AI_HUMAN_RENDER_BRIDGE_URL", "")
        ).rstrip("/")

    def is_configured(self):
        return bool(self.base_url)

    def submit(self, scene):
        if not self.base_url:
            return {
                "status": "bridge_not_configured",
                "message": "Cloud Render Bridge belum dikonfigurasi."
            }

        payload = json.dumps(scene).encode("utf-8")

        request = urllib.request.Request(
            f"{self.base_url}/render",
            data=payload,
            headers={
                "Content-Type": "application/json",
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                body = response.read().decode("utf-8")

            return json.loads(body)

        except urllib.error.HTTPError as exc:
            return {
                "status": "http_error",
                "code": exc.code,
                "message": str(exc),
            }

        except urllib.error.URLError as exc:
            return {
                "status": "connection_error",
                "message": str(exc),
            }

        except Exception as exc:
            return {
                "status": "error",
                "message": str(exc),
            }
