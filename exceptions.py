class NoTextFilesError(Exception):

    def __str__(self):
        msg = "No text file in the target directory"
        return msg


class NoTargetDirectoryError(Exception):

    def __str__(self):
        msg = "Target search directory does not exist"
        return msg


class NoIndexDirectoryError(Exception):

    def __str__(self):
        msg = "Index files directory does not exist"
        return msg


class NoIndexFileError(Exception):

    def __str__(self):
        msg = "Index file does not exist"
        return msg
