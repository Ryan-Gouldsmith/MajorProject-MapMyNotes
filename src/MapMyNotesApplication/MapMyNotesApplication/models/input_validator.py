class InputValidator(object):
    def __init__(self, params):
        """
        Creates an input validator instance
        Parameters
        ----------
        params: The params from the users input
        """
        self.errors = []
        self.params = params

    def check_all_params_are_less_than_schema_length(self):
        """
        Performs sanity check against the length  of the params.
        Returns
        -------
        True if there are errors identified
        False if there are no errors identified
        """
        if len(self.params["module_code_data"]) > 50:
            self.errors.append("Module code length too long, max 50 characters.")

        if len(self.params['lecturer_name_data']) > 100:
            self.errors.append("Lecture name is too long, max length 100 characters")

        if len(self.params['location_data']) > 100:
            self.errors.append("Location data too long, max length 100 characters")

        if len(self.params['title_data']) > 100:
            self.errors.append("title data too long, max length 100 characters")

        return len(self.errors) == 0

    def get_errors(self):
        """
        Returns
        -------
        A list of errors
        """
        return self.errors

    def check_all_params_exist(self):
        """
        Checks to see if the key exists and ensures that the keys are not empty spaces
        Returns
        -------
        True if there are not errors.
        False if there are errors.
        """

        if "module_code_data" not in self.params or "lecturer_name_data" not in self.params \
                or 'location_data' not in self.params or "date_data" not in self.params or 'title_data' not in self.params \
                or 'time_data' not in self.params:
            return False

        """ REFERENCE isspace checks for empty spaces
            http://stackoverflow.com/questions/2405292/how-to-check-if-text-is-empty-spaces-tabs-newlines-in-python
        """
        if self.params['module_code_data'].isspace() or self.params['lecturer_name_data'].isspace() \
            or self.params['location_data'].isspace() or self.params['date_data'].isspace() \
            or self.params['title_data'].isspace() or self.params['time_data'].isspace():
            return False

        return True
