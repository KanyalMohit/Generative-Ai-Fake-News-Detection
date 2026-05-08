import json
import os
import requests
from PySide6.QtCore import QThread, Signal

API_BASE = os.environ.get("TRUTH_LENS_API", "http://127.0.0.1:8000")

class ApiWorker(QThread):
    finished = Signal(dict)
    failed = Signal(str)

    def __init__(self, mode: str, payload: dict | None = None, file_path: str | None = None):
        super().__init__()
        self.mode = mode
        self.payload = payload or {}
        self.file_path = file_path

    def run(self):
        try:
            if self.mode in {"text", "url"}:
                data = {
                    "content": self.payload.get("content", ""),
                    "is_url": self.mode == "url",
                }
                response = requests.post(f"{API_BASE}/analyze/text", json=data, timeout=180)
                if not response.ok:
                    raise RuntimeError(self._format_error(response, "text/url analysis"))
                self.finished.emit(response.json())
                return

            if self.mode in {"image", "video"}:
                endpoint = "/analyze/image" if self.mode == "image" else "/analyze/video"
                with open(self.file_path, "rb") as handle:
                    files = {"file": (os.path.basename(self.file_path), handle)}
                    response = requests.post(f"{API_BASE}{endpoint}", files=files, timeout=600)
                if not response.ok:
                    raise RuntimeError(self._format_error(response, f"{self.mode} analysis"))
                payload = response.json()

                if self.mode == "video":
                    job_id = payload.get("job_id")
                    if not job_id:
                        raise RuntimeError("Video job did not return a job_id.")
                    for _ in range(120):
                        poll = requests.get(f"{API_BASE}/analyze/video/{job_id}", timeout=60)
                        if not poll.ok:
                            raise RuntimeError(self._format_error(poll, "video status polling"))
                        job = poll.json()
                        status = job.get("status")
                        if status == "COMPLETED":
                            result = job.get("result")
                            self.finished.emit(json.loads(result) if isinstance(result, str) else result)
                            return
                        if status == "FAILED":
                            raise RuntimeError(job.get("error") or "Video analysis failed.")
                        self.msleep(2500)
                    raise TimeoutError("Video analysis timed out while waiting for the worker.")

                self.finished.emit(payload)
                return

            raise RuntimeError(f"Unsupported mode: {self.mode}")
        except requests.exceptions.ConnectionError:
            self.failed.emit(
                f"Could not connect to the backend. Make sure the API Gateway is running on port 8000."
            )
        except Exception as exc:
            self.failed.emit(str(exc))

    def _format_error(self, response, stage: str):
        try:
            payload = response.json()
            detail = payload.get("detail") if isinstance(payload, dict) else payload
        except Exception:
            detail = response.text or "Unknown backend error"
        return f"{stage} failed ({response.status_code}): {detail}"
