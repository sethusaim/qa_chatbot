import sys


def error_message_detail(error, error_detail: sys):
    """
    The function returns a detailed error message including the name of the Python script, line number,
    and error message.

    Args:
      error: The error object that was raised during the execution of the code.
      error_detail (sys): The `error_detail` parameter is expected to be an object of the `sys` module,
    which is used to access information about the Python interpreter and its environment. Specifically,
    this function expects `error_detail` to contain information about an exception that was raised in
    the code.

    Returns:
      an error message string that includes the name of the Python script where the error occurred, the
    line number of the error, and the error message itself.
    """
    _, _, exc_tb = error_detail.exc_info()

    file_name = exc_tb.tb_frame.f_code.co_filename

    error_message = "Error occurred python script name [{0}] line number [{1}] error message [{2}]".format(
        file_name, exc_tb.tb_lineno, str(error)
    )

    return error_message


class CustomException(Exception):
    def __init__(self, error_message, error_detail: sys):
        """
        :param error_message: error message in string format
        """
        super().__init__(error_message)

        self.error_message = error_message_detail(
            error_message, error_detail=error_detail
        )

    def __str__(self):
        """
        This function returns the error message as a string.

        Returns:
          The `__str__` method is returning the `error_message` attribute of the object.
        """
        return self.error_message
