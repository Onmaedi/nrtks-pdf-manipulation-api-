import os
from os import path
import json
import base64
from uuid import uuid4

from flask import request, jsonify, abort, Response
from flask_restful import Resource
import dropbox
from dropbox.files import ListFolderResult, FileMetadata
import PyPDF2


class DropboxFileHandler:
    def __init__(self):
        self.__token = os.getenv("DROPBOX_TOKEN")
        self.__dropbox = dropbox.Dropbox(self.__token)

    def download(self, dropbox_file_path, tmp_folder_path):
        try:
            *_, extension = path.splitext(dropbox_file_path)
            tmp_file_name = f"{str(uuid4())}{extension}"
            tmp_file_path = path.join(tmp_folder_path, tmp_file_name)

            *_, response = self.__dropbox.files_download(
                path=dropbox_file_path)

            with open(tmp_file_path, "wb+") as temp_file:
                temp_file.write(response.content)

            return tmp_file_path
        except:
            ...

    def folder_list_files(self, folder_path: str) -> ListFolderResult:
        files = self.__dropbox.files_list_folder(folder_path)
        return files

    def exists_folder(self, folder_path) -> bool:
        try:
            self.__dropbox.files_get_metadata(folder_path)
            return True
        except:
            return False

class MergeDropboxFolder(Resource):
    def __init__(self):
        ...

    def merger(self, tmp_folder_path, files_path: list = []) -> str:
        merger = PyPDF2.PdfFileMerger()

        output_path = path.join(f"{tmp_folder_path}", f"{str(uuid4())}.pdf")
        for file in files_path:
            merger.append(file)

        merger.write(output_path)
        return output_path

    def post(self):
        try:
            tmp_folder_name = str(uuid4())
            tmp_folder_path = path.join(path.abspath(""), tmp_folder_name)
            os.makedirs(tmp_folder_path)
            tmp_files = []
            merged_files = []

            request_body = json.loads(request.data)
            folder_path = request_body["folderPath"]

            if not DropboxFileHandler().exists_folder(folder_path):
                return jsonify({"message": "This folder could not be found."})

            files = DropboxFileHandler().folder_list_files(folder_path)
            for file in files.entries:
                tmp_files.append(DropboxFileHandler().download(
                    file.path_display, tmp_folder_path))
                merged_files.append(file.path_display)

            tmp_merged_file_path = self.merger(tmp_folder_path, tmp_files)

            tmp_files.append(tmp_merged_file_path)

            with open(tmp_merged_file_path, "rb") as merged:
                merged_pdf_base64 = str(
                    base64.b64encode(merged.read()), 'utf-8')

            for tmp_file in tmp_files:
                os.remove(tmp_file)
            os.rmdir(tmp_folder_path)

            return jsonify({
                "filesMerged": merged_files,
                "base64file": merged_pdf_base64
            })
        except:
            abort(500)
