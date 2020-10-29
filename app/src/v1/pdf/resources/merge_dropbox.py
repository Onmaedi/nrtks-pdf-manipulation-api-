import os
from os import path
import json

from flask import jsonify, request, abort, current_app
from flask_restful import Resource
import dropbox
from uuid import uuid4
import PyPDF2
import base64


class DropboxFileHandler:
    def __init__(self):
        self.__token = os.getenv("DROPBOX_TOKEN")
        self.__dropbox = dropbox.Dropbox(self.__token)

    def download(self, dropbox_file_path, tmp_folder_path):
        try:
            *_, extension = path.splitext(dropbox_file_path)
            tmp_file_name = f"{str(uuid4())}{extension}"
            tmp_file_path = path.join(tmp_folder_path, tmp_file_name)

            res, response = self.__dropbox.files_download(
                path=dropbox_file_path)

            with open(tmp_file_path, "wb+") as temp_file:
                temp_file.write(response.content)

            return tmp_file_path
        except:
            return False


class PdfMergerDropbox(Resource):
    def merger(self, tmp_folder_path, files_path: list = []) -> str:
        if not files_path:
            return ""
        merger = PyPDF2.PdfFileMerger()

        output_path = path.join(f"{tmp_folder_path}", f"{str(uuid4())}.pdf")
        for file in files_path:
            merger.append(file)

        merger.write(output_path)
        return output_path

    def post(self):
        try:
            request_body = json.loads(request.data)

            tmp_folder_name = str(uuid4())

            tmp_folder_path = path.join(path.abspath(""), tmp_folder_name)

            os.makedirs(tmp_folder_path)

            tmp_files = []
            for file in request_body["files"]:
                tmp_file_path = DropboxFileHandler().download(file, tmp_folder_path)
                if tmp_file_path:
                    tmp_files.append(tmp_file_path)

            merged_file_path = self.merger(tmp_folder_path, tmp_files)

            if not merged_file_path:
                return jsonify({
                    "base64file": ""
                })

            tmp_files.append(merged_file_path)

            with open(merged_file_path, "rb") as merged:
                merged_pdf_base64 = str(
                    base64.b64encode(merged.read()), 'utf-8')

            for tmp_file in tmp_files:
                os.remove(tmp_file)
            os.rmdir(tmp_folder_path)

            return jsonify({
                "base64file": merged_pdf_base64
            })

        except Exception as e:
            print(e)
            abort(500)
