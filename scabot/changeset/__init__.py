# SPDX-FileCopyrightText: 2021 Konrad Weihmann
# SPDX-License-Identifier: GPL-3.0-only

from collections import defaultdict
from typing import List

from scabot.changeset.DiffFile import DiffFile
from scabot.changeset.DiffFile import DiffFileCollection


class Changeset(object):

    def __init__(self, args):
        self.__changes = []
        self.__affected_lines_only = args.comment_only_affected_lines if args else False

    @property
    def Changes(self) -> List[DiffFile]:
        return self.__changes

    @property
    def ChangedContent(self) -> dict:
        _res = defaultdict(set)
        for c in self.__changes:
            _res[c.File].update(
                c.AffectedLines if self.__affected_lines_only else range(1, 100000))
        return _res

    def AddChange(self, file, diff, newfile=False):
        self.__changes.append(DiffFile(file, diff, newfile))

    def AddChangeFromCollection(self, diff):
        self.__changes += DiffFileCollection.get_diffs(diff)
