from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from fastapi.concurrency import run_in_threadpool
from starlette.background import BackgroundTask
from utils.file_utils import cleanup, handle_download_error
import yt_dlp
import os
import shutil
import uuid

router  = APIRouter(prefix="/video", tags=["Video"])

@router.get("/download", response_class=FileResponse)
async def download(url: str):
    def run_download():

        ydl_opts = {
            "format": "bv*+ba/b",
            "merge_output_format": "mp4",
            "outtmpl": "download/%(title)s.%(ext)s",
            "noplaylist": True,
            "postprocessor_args": [
                "-c:v", "libx264",
                "-c:a", "aac"
            ],
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
        filename=os.path.basename(filename),
        media_type="application/octet-stream"
    )

@router.get("/playlist")
async def download_playlist(url: str, limit: int):

    os.makedirs("download", exist_ok=True)

    download_id = str(uuid.uuid4())
    download_dir = f"download/{download_id}"
    os.makedirs(download_dir, exist_ok=True)

    def run_download():

        ydl_opts = {
            "format": "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]",
            "playlistend": limit,
            "merge_output_format": "mp4",
            "outtmpl": f"{download_dir}/%(title)s.%(ext)s",
            "postprocessor_args": [
                "-c:v", "libx264",
                "-c:a", "aac"
            ],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.extract_info(url, download=True)

        zip_path = shutil.make_archive(
            f"download/{download_id}",
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
        filename="playlist.zip",
        media_type="application/zip",
        background=BackgroundTask(cleanup, download_dir)
    )