# SPDX-FileCopyrightText: 2021 Konrad Weihmann
# SPDX-License-Identifier: GPL-3.0-only

import logging
from typing import List
from typing import Set

from scabot.notes import Note
from scabot.provider import Provider
from scabot.scainput import SCAInput


class Request():

    def __init__(self, args, provider: Provider):
        self.__args = args
        self.__provider = provider

        self.__comment_indirect = args.comment_indirect

        self.__input_objects = []

        for f in self.__args.files:
            self.__input_objects += SCAInput.FromFile(f)

        self.__sca_findings = self.__get_matching_objects()

        self.__existing_notes = self.__provider.GetNotes()
        self.__new_noteset = [self.__provider.CreateNote(
            x) for x in self.__sca_findings]

    @property
    def ValidInputFiles(self) -> List[SCAInput]:
        return self.__input_objects

    @property
    def SCAFindings(self) -> Set[SCAInput]:
        return self.__sca_findings

    @property
    def NewNotes(self) -> Set[Note]:
        return {x for x in self.__new_noteset if x not in self.__existing_notes}

    @property
    def ResolveableNotes(self) -> Set[Note]:
        return {x for x in self.__existing_notes
                if x not in self.__new_noteset and x.user == self.__provider.Username}

    def __get_matching_objects(self) -> Set[SCAInput]:
        __modified_lines = self.__provider.GetChanges().ChangedContent
        __hits = set()
        for item in self.ValidInputFiles:
            if item.File in __modified_lines and int(item.Line) in __modified_lines[item.File]:
                __hits.add(item)
            if self.__comment_indirect:
                for k, v in {k: v for k, v in __modified_lines.items() if k in item.BBFiles}.items():
                    item.Line = min(v)
                    item.Message += ' ::: occured in file {file}'.format(file=item.File)
                    item.File = k
                    __hits.add(item)
        return __hits

    def Process(self):
        if not self.__provider.Valid:
            logging.warning('Request is closed or not to be commented, skipping')
            return
        for note in self.NewNotes:
            self.__provider.SetNote(note)
        for note in self.ResolveableNotes:
            note.resolved = True
            self.__provider.ResolveNote(note)
