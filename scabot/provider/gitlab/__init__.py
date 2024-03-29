# SPDX-FileCopyrightText: 2021 Konrad Weihmann
# SPDX-License-Identifier: GPL-3.0-only

import logging

import gitlab
import requests
from tenacity import retry
from tenacity.stop import stop_after_attempt
from tenacity.wait import wait_exponential

from scabot.notes import Note
from scabot.provider import Provider
from scabot.provider import SCABotProjectNotFoundError
from scabot.provider import SCABotRequestNotFoundError
from scabot.provider import SCABotServerCommError


class GitLabProvider(Provider):

    def __init__(self, args, username, token, serverurl, project, mrnumber):
        super().__init__(args, username, token, serverurl)
        self.__project = int(project)
        self.__mrnum = int(mrnumber)

        self.__session = requests.Session()
        self.__session.verify = False

        self.__mr = self.__get_mergerequest(self.__get_project())

        # get diffs
        self.__mr_changes = self.__mr.changes(all=True)
        for change in self.__mr_changes['changes']:
            self._changes.AddChange(
                change['new_path'], change['diff'], change['new_file'])

        self.__isvalid = self.__mr.state not in ['merged', 'closed']
        self.__isvalid &= not self.__is_draft() or self.AllowDrafts

    @property
    def Valid(self):
        return self.__isvalid

    def __is_draft(self):
        return self.__mr.work_in_progress

    @retry(wait=wait_exponential(multiplier=1, min=10, max=120), stop=stop_after_attempt(5))
    def __get_server_connection(self):
        try:
            return gitlab.Gitlab(self.ServerURL, private_token=self.Token, session=self.__session)
        except Exception as e:
            logging.error('GitLab connections failed')
            raise SCABotServerCommError(e)

    @retry(wait=wait_exponential(multiplier=1, min=10, max=120), stop=stop_after_attempt(5))
    def __get_project(self):
        try:
            return self.__get_server_connection().projects.get(self.__project)
        except Exception:
            logging.error('Project not found')
            raise SCABotProjectNotFoundError(self.__project)

    @retry(wait=wait_exponential(multiplier=1, min=10, max=120), stop=stop_after_attempt(5))
    def __get_mergerequest(self, proj):
        try:
            return proj.mergerequests.get(self.__mrnum)
        except Exception:
            logging.error('MR not found')
            raise SCABotRequestNotFoundError(self.__mrnum)

    @retry(wait=wait_exponential(multiplier=1, min=10, max=120), stop=stop_after_attempt(5))
    def SetNote(self, value: Note):
        _obj = {
            'body': value.body,
            'position': {
                'base_sha': self.__mr_changes['diff_refs']['base_sha'],
                'start_sha': self.__mr_changes['diff_refs']['start_sha'],
                'head_sha': self.__mr_changes['diff_refs']['head_sha'],
                'position_type': 'text',
                'old_line': value.lines[1] if len(value.lines) > 1 else None,
                'new_line': value.lines[0],
                'new_path': value.path,
            },
            'author': {
                'username': self.Username,
            },
        }
        try:
            self.__mr.discussions.create(_obj)
        except Exception:
            try:
                del _obj['position']['old_line']
                self.__mr.discussions.create(_obj)
            except Exception:
                logging.error(f'Set note {value} failed')  # noqa: G004

    def GetNote(self, input_):
        return Note(
            input_.get('author', {}).get('username', 'Unkwown user'),
            input_.get('body', ''),
            input_.get('position', {}).get('new_path', ''),
            input_.get('position', {}).get('new_line', -1),
            input_.get('position', {}).get('old_line', None),
            input_.get('resolved', False),
            input_.get('resolvable', True),
            input_,
        )

    @retry(wait=wait_exponential(multiplier=1, min=10, max=120), stop=stop_after_attempt(5))
    def GetNotes(self):
        mr = self.__mr
        res = []
        for discussion in mr.discussions.list(all=True):
            for note in mr.discussions.get(discussion.id).attributes['notes']:
                res.append(self.GetNote(note))
        return res

    @retry(wait=wait_exponential(multiplier=1, min=10, max=120), stop=stop_after_attempt(5))
    def ResolveNote(self, value: Note):
        note = self.__mr.discussions.get(value.reference.get('id'))
        note.resolve = True
        note.save()

    @retry(wait=wait_exponential(multiplier=1, min=10, max=120), stop=stop_after_attempt(5))
    def GetCurrentStatus(self) -> dict:
        return self.__mr
