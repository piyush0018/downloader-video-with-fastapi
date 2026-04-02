from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from fastapi.concurrency import run_in_threadpool
from starlette.background import BackgroundTask
from utils.file_utils import cleanup, handle_download_error
import yt_dlp
import os
import shutil
import uuid

router = APIRouter(prefix="/audio", tags=["Audio"])

@router.get("/download")
async def download_audio(url: str):

    def run_download():

        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": "audio/%(title)s.%(ext)s",
            "noplaylist": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        return filename

    try:
        filename = await run_in_threadpool(run_download)
    except Exception as e:
        handle_download_error(e)

    if not os.path.exists(filename):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(
        filename,
        media_type="application/octet-stream",
        filename=os.path.basename(filename)
    )

@router.get("/playlist")
async def download_audio_playlist(url: str, limit: int):

    os.makedirs("audio", exist_ok=True)

    download_id = str(uuid.uuid4())
    download_dir = f"audio/{download_id}"
    os.makedirs(download_dir, exist_ok=True)

    def run_download():

        ydl_opts = {
            "format": "bestaudio/best",
            "playlistend": limit,
            "outtmpl": f"{download_dir}/%(title)s.%(ext)s",
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.extract_info(url, download=True)

        zip_path = shutil.make_archive(
            f"audio/{download_id}",
            "zip",
            download_dir
        )

        return zip_path

    try:
        zip_file = await run_in_threadpool(run_download)

    except Exception as e:

        cleanup(download_dir)
        handle_download_error(e)

    return FileResponse(
        zip_file,
        filename="playlist_audio.zip",
        media_type="application/zip",
        background=BackgroundTask(cleanup, download_dir)
    )