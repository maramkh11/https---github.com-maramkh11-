from Utilities.common.common_enums import Status


class AssertResult:

    def __init__(self, actual_result, expected_result, status: Status, error_message: str):
        self._actual_result = actual_result
        self._expected_result = expected_result
        self._status = status
        self._error_message = error_message
        self._assert_reult

    def _assert_reult(self):
        if self._status.name is Status.EQUAL:
            assert self._actual_result is self._expected_result, self._error_message
        elif self._status.name is Status.NOT_EQUAL:
            assert self._actual_result is not self._expected_result, self._error_message
        elif self._status.name is Status.CONTAINS:
            assert self._actual_result in self._expected_result, self._error_message
        elif self._status.name is Status.NOT_CONTAINS:
            assert self._actual_result not in self._expected_result, self._error_message
