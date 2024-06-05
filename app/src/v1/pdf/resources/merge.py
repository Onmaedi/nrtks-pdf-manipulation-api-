import os
import base64
import json
from os import path
from uuid import uuid4

from flask import jsonify, request, abort
from flask_restful import Resource
import PyPDF2


class PdfMerger(Resource):
    def merger(self, tmp_folder_path, files_path:list=[]) -> str:
        merger = PyPDF2.PdfFileMerger()

        output_path = path.join(f"{tmp_folder_path}", f"{str(uuid4())}.pdf")
        for file in files_path:
            merger.append(file)
        
        merger.write(output_path)
        return output_path
    
    def post(self):
        try:
            file_names = []

            request_body = json.loads(request.data)
            files = request_body["files"]
            tmp_folder_name = str(uuid4())
            tmp_folder_path = path.join(path.abspath(""), tmp_folder_name)
            os.makedirs(tmp_folder_path)

            for file in files:
                file_name = path.join(tmp_folder_path, f"{str(uuid4())}.pdf")
                file_names.append(file_name)
                with open(file_name, "wb+") as file_pointer:
                    file_pointer.write(base64.b64decode(file))

            merged_pdf_path = self.merger(tmp_folder_path, file_names)

            with open(merged_pdf_path, "rb") as merged:
                merged_pdf_base64 = str(base64.b64encode(merged.read()), 'utf-8')
                file_names.append(merged_pdf_path)
        
            for file in file_names:
                os.remove(file)
            os.rmdir(tmp_folder_path)
                
            return jsonify({
                "base64file" : merged_pdf_base64
            })

            
        except json.decoder.JSONDecodeError:
            abort(500)
        except KeyError:
            abort(500)