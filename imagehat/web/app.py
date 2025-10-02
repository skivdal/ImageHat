import os
import shutil
import tempfile
from fastapi import FastAPI, File, UploadFile, HTTPException, status
from imagehat.parsers.jpeg_parser import JPEGParser


app = FastAPI()

ALLOWED_CONTENT_TYPES = ["image/jpeg"]


@app.post("/api/upload")
async def upload_image(file: UploadFile = File(...)):
    """
    Accepts an image file (JPEG) via multipart/form-data,
    streams it to a temporary file, extracts EXIF data
    and returns the data as a JSON response.
    """
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Unsupported file type. Only {', '.join(ALLOWED_CONTENT_TYPES)} are supported.",
        )

    temp_file_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
            shutil.copyfileobj(file.file, temp_file)
            temp_file_path = temp_file.name

        try:
            if file.content_type == "image/jpeg":
                parser = JPEGParser(temp_file_path)
                data = parser.get_exif_image_data()
                return data
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Failed to parse the image file: {str(e)}",
            )

    finally:
        await file.close()
        if temp_file_path and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)


def main():
    import uvicorn
    uvicorn.run("imagehat.web.app:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()
