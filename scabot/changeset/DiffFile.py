# SPDX-FileCopyrightText: 2021 Konrad Weihmann
# SPDX-License-Identifier: GPL-3.0-only

from typing import List

from unidiff import PatchSet
from unidiff import UnidiffParseError


class DiffFile():

    def __init__(self, file, diff, newfile=False):
        self.__diff = diff
        self.__file = file
        self.__newfile = newfile
        self.__affectedlines = self.__get_modified_lines()

    def __get_patch(self):
        try:
            _patch = PatchSet(self.__diff)
        except UnidiffParseError:
            # On some version the diff header is missing
            # just add a fake one
            _patch = PatchSet(
                'diff --git a/{file} b/{file}\n--- a/{file}\n+++ b/{file}\n{diff}'.format(
                    file=self.__file, diff=self.__diff))
        return _patch.added_files + _patch.modified_files

    def __get_modified_lines(self):
        res = []
        for _f in self.__get_patch():
            for h in [x for x in _f]:
                res += h.target_lines()
        res = [x.target_line_no for x in res if not x.is_context]
        return res

    def __get_newly_added_content(self):
        res = []
        for _f in self.__get_patch():
            for h in [x for x in _f]:
                res += h.target_lines()
        res = [(x.target_line_no, x.value) for x in res if x.is_added]
        return res

    @property
    def File(self) -> str:
        return self.__file

    @property
    def NewFile(self) -> bool:
        return self.__newfile

    @property
    def Diff(self) -> str:
        return self.__diff

    @property
    def AffectedLines(self) -> List[int]:
        return self.__affectedlines

    @property
    def NewLines(self) -> List[int]:
        return self.__get_newly_added_content()


class DiffFileCollection():

    @staticmethod
    def get_diffs(diff):
        res = []
        if not isinstance(diff, str):
            diff = diff.decode('utf-8')
        _patch = PatchSet(diff)
        for f in _patch.added_files:
            res.append(DiffFile(f.path, str(f), newfile=True))
        for f in _patch.modified_files:
            res.append(DiffFile(f.path, str(f)))
        return res
