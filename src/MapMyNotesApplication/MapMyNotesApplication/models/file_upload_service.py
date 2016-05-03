import os
import time


class FileUploadService(object):
    # A LIST OF ACCEPTED FILES
    ACCEPTED_FILE_EXTENSIONS = [".jpg", ".png", ".tiff"]

    def __init__(self, filename):
        """
        Creates a new FileUploadService instance
        Parameters
        ----------
        filename: the filename which is being uploaded.
        """
        self.filename = filename
        self.upload_path = None

    def save_users_file(self, file_object):
        """
        Saves the file to filestore.
        Parameters
        ----------
        file_object: The Flask file object passed from the controller
        """
        file_object.save(self.upload_path)

    def is_forward_slash_in_filename(self):
        """
        Returns
        -------
        True if there's a forward slash in the name
        False if there's not a forward slash in the name
        """
        return "/" in self.filename

    def remove_slash_from_filename(self):
        """
        Removes the forward slash in any name of the filename
        """
        self.filename = self.filename.split("/")[1]

    def accepted_file_extension(self):
        """
        Checks the list to see if it's an appropriate file extention uploaded. This stops people uploading bad files
        Modified from Flask's guide: http://flask.pocoo.org/docs/0.10/patterns/fileuploads/
        Returns
        -------
        True if it is in the Accepted files
        False if it is not in the Accepted files
        """
        filename, file_extension = os.path.splitext(self.filename)
        return file_extension in self.ACCEPTED_FILE_EXTENSIONS

    def file_exists(self):
        """
        Check to see if the file actually exists
        Returns
        -------
        True if it does exist
        False if it does not exist
        """
        return os.path.isfile(self.upload_path)

    def is_png(self):
        """
        Checks to see if the image is a png or not
        Returns
        -------
        True if the extension matches .png
        False if the extension is not a png.
        """
        filename, file_extension = os.path.splitext(self.filename)
        return file_extension == '.png'

    def add_full_path_to_filename(self, upload_path):
        """
        Appends the fill path to the filename for saving
        Parameters
        ----------
        upload_path: The path to the location where the image will be saved

        Returns
        -------
        The modified filename and upload path
        """
        self.upload_path = "{}{}".format(upload_path, self.filename)
        return self.upload_path

    def update_filename(self, user_id, filename):
        """
        Updates the filename to account for the user ID, current time and the filename to make each one unique.
        Parameters
        ----------
        user_id: The user's id who is uploading the file
        filename: The string representation of the filename

        Returns
        -------
        The string representation of the concatenated filename
        """
        current_time = self.get_current_time()
        self.filename = "{}_{}_{}".format(user_id, current_time, filename)

    def get_current_time(self):
        """
        Returns
        -------
        returns the current time object based on the time using the time API.
        """
        return time.time()
