from PIL import Image

"""
A reference for how Python Image Library can extract the exif data from an image
http://www.blog.pythonlibrary.org/2010/03/28/getting-photo-metadata-exif-using-python/

http://www.awaresystems.be/imaging/tiff/tifftags/privateifd/exif.html
Referenced for the image number and what they mean in the dict returned by get exif.

http://stackoverflow.com/questions/23064549/get-date-and-time-when-photo-was-taken-from-exif-data-using-pil
Good for finding out the reference link to the image numbers and what the exif data actually meant.

get exif returns keys which correspond to numbers on an EXIF standard
36867 is the key for the time the image was taken.
"""


class ExifParser(object):
    IMAGE_START_TIME = 36867

    def __init__(self, filename):
        """
        Creates a new Exif Parser
        Parameters
        ----------
        filename: The filename which is currently being analysed for EXIF data.
        """
        self.filename = filename
        self.image = Image.open(self.filename)
        self.exif_data = None

    def parse_exif(self):
        """
        Uses the PIL __getexif() API to extract the EXIF data
        Returns
        -------
        Any associated EXIF data.
        """
        self.exif_data = self.image._getexif()
        return self.exif_data

    def get_image_date(self):
        """
        Uses the EXIF data to attempt to extract that START time key
        Returns
        -------
        The start time of the image
        None if nothing could be found.
        """
        return self.exif_data[self.IMAGE_START_TIME] if self.exif_data is not None else None
