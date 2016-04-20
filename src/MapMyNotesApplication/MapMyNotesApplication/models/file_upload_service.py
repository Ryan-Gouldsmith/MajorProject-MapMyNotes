import os


class FileUploadService(object):
    ACCEPTED_FILE_EXTENSIONS = [".jpg", ".png", ".tiff"]

    def __init__(self, filename):
        self.filename = filename
        self.upload_path = None

    def save_users_file(self, file_object):
        file_object.save(self.upload_path)

    def is_forward_slash_in_filename(self):
        return "/" in self.filename

    def remove_slash_from_filename(self):
        self.filename = self.filename.split("/")[1]

    def accepted_file_extension(self):
        filename, file_extension = os.path.splitext(self.filename)
        return file_extension in self.ACCEPTED_FILE_EXTENSIONS

    def file_exists(self):
        return os.path.isfile(self.upload_path)

    def is_png(self):
        filename, file_extension = os.path.splitext(self.filename)
        return file_extension == '.png'

    def add_full_path_to_filename(self, upload_path):
        self.upload_path = "{}{}".format(upload_path, self.filename)
        return self.upload_path

    def update_filename(self, user_id, filename):
        self.filename = "{}_{}".format(user_id, filename)
