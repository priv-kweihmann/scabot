# SPDX-FileCopyrightText: 2021 Konrad Weihmann
# SPDX-License-Identifier: GPL-3.0-only

import json
import os

from scabot.notes import Note
from scabot.provider import Provider
from scabot.provider import SCABotProjectNotFoundError
from scabot.provider import SCABotRequestNotFoundError


class MockProvider(Provider):

    def __init__(self, args, username, token, serverurl, project, mrnumber):
        super().__init__(args, username, token, serverurl)

        self.__projectnumber = project
        self.__requestnumber = mrnumber
        self.__serverurl = serverurl
        self.__username = username

        try:
            with open(self.__get_file_path()) as i:
                self.__db = json.load(i)
        except Exception:
            self.__db = {}

        self.__isvalid = not self.__get_request(
            self.__get_project()).get('closed', False)
        self.__isvalid &= not self.__is_draft() or self.AllowDrafts

        for item in self.__get_request(self.__get_project()).get('diffs', []):
            self._changes.AddChange(item.get('file'), item.get(
                'diff'), item.get('newfile', False))

    @property
    def Valid(self):
        return self.__isvalid

    def __is_draft(self):
        return self.__get_request(self.__get_project()).get('wip', False)

    def __get_project(self):
        res = self.GetCurrentStatus().get('projects', {}).get(self.__projectnumber, {})
        if not res:
            raise SCABotProjectNotFoundError(self.__projectnumber)
        return res

    def __get_request(self, proj):
        res = proj.get('requests', []).get(self.__requestnumber, {})
        if not res:
            raise SCABotRequestNotFoundError(self.__projectnumber)
        return res

    def __get_file_path(self):
        return os.path.join(self.__serverurl, '{project}_{num}.json'.format(
                            project=self.__projectnumber, num=self.__requestnumber))

    def __get_notes(self):
        return self.__get_request(self.__get_project()).get('notes', [])

    def SetNote(self, value: Note):
        _obj = {
            'user': value.user,
            'body': value.body,
            'path': value.path,
            'line_number': value.lines[0],
            'resolved': value.resolved,
            'can_resolve': value.can_resolve,
        }
        self.__db['projects'][self.__projectnumber]['requests'][self.__requestnumber]['notes'].append(
            _obj)

    def GetNote(self, input_: dict):
        return Note(input_.get('user', ''), input_.get('body', ''), input_.get('path', ''), input_.get(
            'line_number', 0), input_.get('old_linenumber', None), input_.get('resolved', False),
            input_.get('can_resolve', True), reference=input_)

    def GetNotes(self):
        return [self.GetNote(x) for x in self.__get_notes()]

    def ResolveNote(self, value: Note):
        for n in self.__get_request(self.__get_project()).get('notes', []):  # pragma: no cover
            if n == value.reference:
                n['resolved'] = True
                break

    def GetCurrentStatus(self) -> dict:
        return self.__db
