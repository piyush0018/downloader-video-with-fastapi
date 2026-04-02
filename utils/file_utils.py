import os
import shutil
from fastapi import HTTPException
from yt_dlp.utils import DownloadError, ExtractorError

def cleanup(folder):
    if os.path.exists(folder):
        shutil.rmtree(folder)

def ensure_directories():
    os.makedirs("audio", exist_ok=True)
    os.makedirs("download", exist_ok=True)
    
def handle_download_error(e: Exception):

    msg = str(e).lower()

    if any(x in msg for x in [
        "private",
        "login",
        "sign in",
        "confirm your age",
        "not a bot",
        "cannot parse data"
    ]):
        raise HTTPException(403, "Video requires authentication")

    if any(x in msg for x in [
        "unavailable",
        "deleted",
        "not found"
    ]):
        raise HTTPException(404, "Video unavailable")

    if "not available in your country" in msg:
        raise HTTPException(403, "Video blocked in this region")

    if isinstance(e, ExtractorError) or "cannot parse data" in msg:
        raise HTTPException(
            400,
            "Platform temporarily unsupported"
        )

    if any(x in msg for x in [
        "timed out",
        "name resolution",
        "unable to resolve"
    ]):
        raise HTTPException(503, "Network error")

    if isinstance(e, DownloadError):
        raise HTTPException(400, "Download failed")

    raise HTTPException(500, "Internal server error")