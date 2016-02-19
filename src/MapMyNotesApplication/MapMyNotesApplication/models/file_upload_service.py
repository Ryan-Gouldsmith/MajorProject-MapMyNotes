
class FileUploadService(object):

    def __init__(self):
        print "foo"

    def save_users_file(self, filename, file_object):
        upload_directory = "MapMyNotesApplication/upload/"
        users_file = upload_directory + filename
        file_object.save(users_file)

    def is_forward_slash_in_filename(self, filename):
        return "/" in filename


    def prepare_file_path_file(self, filename):
        split_filename = filename.split("/")
        filename = split_filename[1]
        return filename
