# SPDX-FileCopyrightText: 2021 Konrad Weihmann
# SPDX-License-Identifier: GPL-3.0-only

from itertools import product
from typing import List


class Note(object):

    def __init__(self, user: str, body: str, path: str, line_number: int,
                 old_linenumber=None, resolved=False, can_resolve=True, reference=None):
        super().__init__()
        self.__user = user
        self.__body = body
        self.__path = path
        self.__possibleLinesNumbers = [line_number]
        if old_linenumber:
            self.__possibleLinesNumbers.append(old_linenumber)
        self.__canResolve = can_resolve
        self.__isResolved = resolved
        self.__reference = reference

    @property
    def user(self) -> str:
        return self.__user

    @property
    def path(self) -> str:
        return self.__path

    @path.setter
    def path(self, value: str):
        self.__path = value

    @property
    def body(self) -> str:
        return self.__body

    @body.setter
    def body(self, value: str):
        self.__body = value

    @property
    def lines(self) -> List[int]:
        return self.__possibleLinesNumbers

    @property
    def can_resolve(self) -> bool:
        return self.__canResolve

    @property
    def resolved(self) -> bool:
        return self.__isResolved

    @resolved.setter
    def resolved(self, value: bool):
        self.__isResolved = value if self.can_resolve else self.__isResolved

    @property
    def reference(self):
        return self.__reference

    def __hash__(self):
        return hash(self.__repr__())

    def __eq__(self, other):
        if not isinstance(other, Note):
            return False

        _a = {'user': self.user, 'path': self.path, 'body': self.body}
        _b = {'user': other.user, 'path': other.path, 'body': other.body}
        _lines_combinations = product(self.lines, other.lines)
        return any(
            {**_a, **{'line': x[0]}} == {**_b, **{'line': x[1]}} for x in _lines_combinations
        )

    def __ne__(self, other):
        return (not self.__eq__(other))

    def __repr__(self):
        return '{path}:{lines} - [{user}]: {body}'.format(
            path=self.path,
            lines=self.__possibleLinesNumbers,
            user=self.__user,
            body=self.__body)
