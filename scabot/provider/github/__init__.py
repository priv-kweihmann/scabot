# SPDX-FileCopyrightText: 2021 Konrad Weihmann
# SPDX-License-Identifier: GPL-3.0-only

import github3  # noqa: I900 false positive
from tenacity import retry
from tenacity.stop import stop_after_attempt
from tenacity.wait import wait_exponential

from scabot.notes import Note
from scabot.provider import Provider
from scabot.provider import SCABotProjectNotFoundError
from scabot.provider import SCABotRequestNotFoundError
from scabot.provider import SCABotServerCommError


class GitHubProvider(Provider):

    def __init__(self, args, username, token, serverurl, project, mrnumber):
        super().__init__(args, username, token, serverurl)
        self.__project = project
        self.__mrnum = mrnumber

        self.__repo = self.__get_connection()
        self.__pr = self.__get_pr()

        self._changes.AddChangeFromCollection(self.__pr.diff())

        self.__isvalid = self.__pr.state == 'open'
        self.__isvalid &= not self.__is_draft() or self.AllowDrafts

    @property
    def Valid(self):
        return self.__isvalid

    def __is_draft(self):
        return self.__pr.draft

    def __get_github_repo(self):
        return self.__project

    @retry(wait=wait_exponential(multiplier=1, min=10, max=120), stop=stop_after_attempt(5))
    def __get_connection(self):
        login = github3.login(self.Username, self.Token)
        if not login:
            raise SCABotServerCommError('Login failed. Check your credentials')
        res = login.repository(self.Username, self.__get_github_repo())
        if not res:
            raise SCABotProjectNotFoundError(self.__get_github_repo())
        return res

    @retry(wait=wait_exponential(multiplier=1, min=10, max=120), stop=stop_after_attempt(5))
    def __get_pr(self):
        res = self.__repo.pull_request(self.__mrnum)
        if not res:
            raise SCABotRequestNotFoundError(self.__mrnum)
        return res

    @retry(wait=wait_exponential(multiplier=1, min=10, max=120), stop=stop_after_attempt(5))
    def SetNote(self, value: Note):
        try:
            _ref = value.reference
            if not _ref:
                _ref = self.__get_pr().head.sha
            self.__pr.create_review_comment(
                value.body, _ref, value.path, value.lines[0])
        except Exception as e:
            raise SCABotServerCommError(e)

    def GetNote(self, input_):
        return Note(
            input_.user.login,
            input_.body_text,
            input_.path,
            input_.position,
            input_.original_position,
            reference=input_,
        )

    @retry(wait=wait_exponential(multiplier=1, min=10, max=120), stop=stop_after_attempt(5))
    def GetNotes(self):
        return [self.GetNote(x) for x in self.__pr.review_comments()]

    @retry(wait=wait_exponential(multiplier=1, min=10, max=120), stop=stop_after_attempt(5))
    def ResolveNote(self, value: Note):
        for c in self.__pr.review_comments():
            if c.id == value.reference.id:
                # Unfortunately github/v3-API doesn't allow
                # programatic resolving of comments
                # so we are going to delete them instead
                c.delete()
                break

    @retry(wait=wait_exponential(multiplier=1, min=10, max=120), stop=stop_after_attempt(5))
    def GetCurrentStatus(self) -> dict:
        return self.__pr.__dict__id
