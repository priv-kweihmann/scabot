# SPDX-FileCopyrightText: 2021 Konrad Weihmann
# SPDX-License-Identifier: GPL-3.0-only

import abc
from typing import List

from scabot.changeset import Changeset
from scabot.notes import Note
from scabot.scainput import SCAInput


class Provider(abc.ABC, metaclass=abc.ABCMeta):

    def __init__(self, args, username, token, serverurl):
        self.__username = username
        self.__token = token
        self.__server = serverurl
        self._changes = Changeset(args)
        self.__allow_drafts = args.comment_drafts

    @property
    def Username(self) -> str:
        return self.__username

    @property
    def Token(self) -> str:
        return self.__token

    @property
    def ServerURL(self) -> str:
        return self.__server

    @property
    def AllowDrafts(self) -> bool:
        return self.__allow_drafts

    @abc.abstractproperty
    def Valid() -> bool:
        raise NotImplementedError()

    @abc.abstractmethod
    def GetCurrentStatus(self) -> dict:
        raise NotImplementedError()

    @abc.abstractmethod
    def GetNotes(self) -> List[Note]:
        raise NotImplementedError()

    @abc.abstractmethod
    def GetNote(self, input) -> Note:
        raise NotImplementedError()

    @abc.abstractmethod
    def SetNote(self, value: Note):
        raise NotImplementedError()

    def CreateNote(self, input: SCAInput) -> Note:
        return Note(self.Username, input.GetFormattedMessage(), input.File, int(input.Line))

    @abc.abstractmethod
    def ResolveNote(self, value: Note):
        raise NotImplementedError()

    def GetChanges(self):
        return self._changes


class SCABotError(Exception):

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class SCABotServerCommError(SCABotError):

    def __init__(self, exception):
        super().__init__('Server communication error: {err}'.format(err=exception)) # pragma: no cover


class SCABotProjectNotFoundError(SCABotError):

    def __init__(self, projectref):
        super().__init__('Project {proj} not found'.format(proj=projectref))


class SCABotRequestNotFoundError(SCABotError):

    def __init__(self, requestref):
        super().__init__('Request {req} not found'.format(req=requestref))
