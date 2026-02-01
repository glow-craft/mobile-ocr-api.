from fastapi import FastAPI, UploadFile, File
import pytesseract
from PIL import Image
from pypdf import PdfWriter
import io

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Mobile se banayi gayi API chal rahi hai!"}

@app.post("/image-to-text")
async def image_to_text(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))
    text = pytesseract.image_to_string(image)
    return {"filename": file.filename, "extracted_text": text}

@app.post("/merge-pdfs")
async def merge_pdfs(files: list[UploadFile] = File(...)):
    merger = PdfWriter()
    for file in files:
        pdf_bytes = io.BytesIO(await file.read())
        merger.append(pdf_bytes)
    return {"status": "Success", "message": "PDFs merged successfully inside server."}
