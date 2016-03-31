import os
class FileUploadService(object):

    ACCEPTED_FILE_EXTENSIONS = [".jpg",".png",".tiff"]

    def save_users_file(self, file_path, file_object):
        file_object.save(file_path)

    def is_forward_slash_in_filename(self, filename):
        return "/" in filename


    def prepare_file_path_file(self, filename):
        split_filename = filename.split("/")
        filename = split_filename[1]
        return filename

    def accepted_file_extension(self, filename):
        filename, file_extension = os.path.splitext(filename)
        return file_extension in self.ACCEPTED_FILE_EXTENSIONS

    def file_exists(self, filename):
        return os.path.isfile(filename)

    def is_png(self, filename):
        filename, file_extension = os.path.splitext(filename)
        return file_extension == '.png'
