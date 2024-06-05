import os
import base64
import json
from os import path
from uuid import uuid4

from flask import jsonify, request, abort
from flask_restful import Resource
from PyPDF2 import PdfFileReader, PdfFileWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io


class PdfWriter(Resource):
    def write(self, pdf_file_path: str, content_text: list, tmp_folder_path) -> str:
        try:

            existing_pdf = PdfFileReader(open(pdf_file_path, "rb"))
            if existing_pdf.pages.lengthFunction() == 0:
                return ""
            heigth = int(existing_pdf.pages.getFunction(
                0).mediaBox.getHeight())
            width = int(existing_pdf.pages.getFunction(0).mediaBox.getWidth())

            packet = io.BytesIO()

            num_pages = existing_pdf.getNumPages()

            can = canvas.Canvas(packet, pagesize=letter)

            for multiplier, text in enumerate(content_text):
                y_pos = heigth - 10 * (multiplier + 1)
                can.drawRightString(int(width) - 5, y_pos, text)
            can.save()

            packet.seek(0)
            new_pdf = PdfFileReader(packet)

            output = PdfFileWriter()

            for count in range(num_pages):
                page = existing_pdf.getPage(count)
                page.mergePage(new_pdf.getPage(0))
                output.addPage(page)

            new_pdf_path = path.join(tmp_folder_path, f"{str(uuid4())}.pdf")

            outputStream = open(new_pdf_path, "wb+")
            output.write(outputStream)
            outputStream.close()

            return new_pdf_path

        except Exception as exc:
            print(exc)
            return ""

    def post(self):
        try:
            request_body = json.loads(request.data)
            file = request_body["file"]
            content_text = request_body["content_text"]

            tmp_folder_name = str(uuid4())
            tmp_folder_path = path.join(path.abspath(""), tmp_folder_name)

            os.makedirs(tmp_folder_path)
            temp_file_name = f"{uuid4()}.pdf"
            temp_file_path = path.join(tmp_folder_name, temp_file_name)

            with open(temp_file_path, "wb+") as file_pointer:
                file_pointer.write(base64.b64decode(file))

            new_file_path = self.write(
                temp_file_path, content_text, tmp_folder_path)

            if not new_file_path:
                os.remove(temp_file_path)
                os.rmdir(tmp_folder_path)
                return jsonify({
                    "base64file": ""
                })

            with open(new_file_path, "rb") as pdf_file:
                new_pdf_base64 = str(
                    base64.b64encode(pdf_file.read()), 'utf-8')

            os.remove(temp_file_path)
            os.remove(new_file_path)
            os.rmdir(tmp_folder_path)

            return jsonify({
                "base64file": new_pdf_base64
            })

        except json.decoder.JSONDecodeError:
            abort(500)
        except KeyError:
            abort(500)
