# Downloader Video API

A simple **FastAPI-based API** for downloading **videos and audio** using **yt-dlp**.

The API allows:

- Downloading a **single video**
- Downloading **audio from a video**
- Downloading **playlists (with a configurable limit)**
- Returning **ZIP files for playlist downloads**
- Automatic **temporary file cleanup**
- Proper **error handling for common restrictions**

The project is **Docker-ready** and includes `ffmpeg` for video/audio processing.

---

# Features

- FastAPI asynchronous API
- Video download in **MP4**
- Audio download in **best available format**
- Playlist download with configurable limit
- Automatic ZIP packaging for playlists
- Automatic cleanup of temporary files
- Structured router architecture
- Docker support
- Error handling for common download issues

---

# Project Structure

```
.
├── main.py
├── routers
│   ├── video.py
│   └── audio.py
├── utils
│   └── file_utils.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
```

---

# Requirements

- Python **3.12+**
- **ffmpeg** installed
- **yt-dlp**

---

# Installation (Local)

## 1. Clone the repository

```bash
git clone https://github.com/Dikar265/downloader-video-with-fastapi.git
cd downloader-video-with-fastapi
```

## 2. Create a virtual environment

### Linux / macOS

```bash
python3.12 -m venv venv
source venv/bin/activate
```

### Windows (PowerShell)

```powershell
py -3.12 -m venv venv
venv\Scripts\Activate.ps1
```

After activation you should see:

```
(venv)
```

in your terminal.

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Install FFmpeg

`yt-dlp` requires **ffmpeg** for merging audio and video.

### Ubuntu / Debian

```bash
sudo apt install ffmpeg
```

### macOS

```bash
brew install ffmpeg
```

### Windows

Download from:

https://ffmpeg.org/download.html

---

# Run the API

```bash
uvicorn main:app --reload
```

Server will start at:

```
http://localhost:8000
```

Interactive API documentation:

```
http://localhost:8000/docs
```

---

# Running with Docker

Build and start the container:

```bash
docker compose up --build
```

API will be available at:

```
http://localhost:8000
```

---

# API Endpoints

## Download Video

```
GET /video/download
```

Query parameters:

| Parameter | Type | Description |
|-----------|------|-------------|
| url | string | YouTube video URL |

Example:

```
/video/download?url=https://youtube.com/watch?v=VIDEO_ID
```

Returns a **video file (MP4)**.

---

## Download Video Playlist

```
GET /video/playlist
```

Query parameters:

| Parameter | Type | Description |
|-----------|------|-------------|
| url | string | Playlist URL |
| limit | int | Maximum number of videos |

Example:

```
/video/playlist?url=https://youtube.com/playlist?list=PLAYLIST_ID&limit=5
```

Returns a **ZIP file containing videos**.

---

## Download Audio

```
GET /audio/download
```

Query parameters:

| Parameter | Type | Description |
|-----------|------|-------------|
| url | string | YouTube video URL |

Example:

```
/audio/download?url=https://youtube.com/watch?v=VIDEO_ID
```

Returns the **best available audio file**.

---

## Download Audio Playlist

```
GET /audio/playlist
```

Query parameters:

| Parameter | Type | Description |
|-----------|------|-------------|
| url | string | Playlist URL |
| limit | int | Maximum number of items |

Example:

```
/audio/playlist?url=https://youtube.com/playlist?list=PLAYLIST_ID&limit=10
```

Returns a **ZIP file containing audio files**.

---

# Error Handling

The API converts common `yt-dlp` errors into proper HTTP responses.

| Status Code | Description |
|-------------|-------------|
| 400 | Download failed |
| 403 | Authentication required / private video |
| 404 | Video unavailable |
| 503 | Network error |
| 500 | Internal server error |

---

# Temporary File Management

The API automatically:

- Creates required directories (`audio`, `download`)
- Compresses playlist downloads
- Removes temporary directories after the response is sent

---

# Technologies Used

- **FastAPI**
- **yt-dlp**
- **FFmpeg**
- **Uvicorn**
- **Docker**

---

# Disclaimer

This project is intended for **educational and personal use**.  
Make sure you comply with the **terms of service of the platforms you download content from**.

---