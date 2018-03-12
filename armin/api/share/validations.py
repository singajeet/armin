"""
.. module:: validations
   :platform: Any
   :synopsis: Validators for validating various kind of variables
.. moduleauthor:: Ajeet Singh <singajeet@gmail.com>
"""
from armin.api.share.constants import N, V, F


class Validator(object):
    """Provides various kind of validation functions

    """

    def __init__(self, action_type=N.RAISE):
        """Default constructor

        Args:
            action_type (N): Action that needs to be performed, Raise error or Return False

        """
        self._action_type = action_type
        self._is_validation_completed = False
        self._status = F.VALID

    def not_none(self, arg):
        """Check arg value and change status to invalid if it is none

        Args:
            arg: check value for not none

        """
        self.reset_if_validation_done()
        if arg is None:
            self.raise_or_invalidate()
        return self

    def not_empty(self, arg):
        """Check if arg is not empty
        """
        self.reset_if_validation_done()
        if arg is None or str(arg).isspace or str(arg).count <= 0:
            self.raise_or_invalidate()
        return self

    def raise_or_invalidate(self):
        """Raise exception or set status as invalid

        """
        if self._action_type == N.RAISE:
            raise Exception('Invalid value provided for parameter')
        else:
            self._status = F.INVALID

    def validate(self):
        """Returns status of all validations done

        """
        self._is_validation_completed = True
        return False if self._status == F.INVALID else True

    def reset_if_validation_done(self):
        """Resets the validator if validation ops has been completed\
                (by calling the validate method()

        """
        if self._is_validation_completed:
            self._is_validation_completed = False
            self._status = F.VALID
