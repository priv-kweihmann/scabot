# SPDX-FileCopyrightText: 2021 Konrad Weihmann
# SPDX-License-Identifier: GPL-3.0-only

import json
import logging
import os
from typing import List


class SCAInput():

    def __init__(self, **kwargs):
        self.__File = ''
        self.__BuildPath = ''
        self.__Line = '1'
        self.__Column = '1'
        self.__Severity = ''
        self.__Message = ''
        self.__ID = ''
        self.__PackageName = ''
        self.__Tool = ''
        self.__Scope = ''
        self.__bbfiles = []
        for k, v in kwargs.items():  # pragma: no cover
            x = getattr(self, k)
            if x is not None:  # pragma: no cover
                setattr(self, k, v)

    @property
    def File(self) -> str:
        return self.__File

    @File.setter
    def File(self, value: str):
        self.__File = value

    @property
    def Scope(self) -> str:
        return self.__Scope

    @Scope.setter
    def Scope(self, value: str):
        self.__Scope = value

    @property
    def BuildPath(self) -> str:
        return self.__BuildPath

    @BuildPath.setter
    def BuildPath(self, value: str):
        self.__BuildPath = value

    @property
    def Line(self) -> str:
        return self.__Line

    @Line.setter
    def Line(self, value: str):
        self.__Line = value

    @property
    def Column(self) -> str:
        return self.__Column

    @Column.setter
    def Column(self, value: str):
        self.__Column = value

    @property
    def Severity(self) -> str:
        return self.__Severity

    @Severity.setter
    def Severity(self, value: str):
        self.__Severity = value

    @property
    def Message(self) -> str:
        return self.__Message

    @Message.setter
    def Message(self, value: str):
        self.__Message = value

    @property
    def ID(self) -> str:
        return self.__ID

    @ID.setter
    def ID(self, value: str):
        self.__ID = value

    @property
    def PackageName(self) -> str:
        return self.__PackageName

    @PackageName.setter
    def PackageName(self, value: str):
        self.__PackageName = value

    @property
    def Tool(self) -> str:
        return self.__Tool

    @Tool.setter
    def Tool(self, value: str):
        self.__Tool = value

    @property
    def BBFiles(self) -> List[str]:
        return self.__bbfiles

    @BBFiles.setter
    def BBFiles(self, value: List[str]):
        self.__bbfiles = value

    def GetPlainID(self) -> str:
        tmp = self.__ID or ''
        tool_prefix = [x for x in tmp.split(
            '.') if x == self.__Tool or x.lower() == self.__Tool.lower()]
        _id = [x for x in tmp.split('.') if x != self.__Tool]
        if any(tool_prefix):
            return '{prefix}.{id}'.format(prefix='.'.join(tool_prefix), id='_'.join(_id))
        return '_'.join(_id)

    def GetFormattedMessage(self) -> str:
        return '[Package:{package} Tool:{tool}] {msg}'.format(package=self.__PackageName,
                                                              tool=self.__Tool,
                                                              msg=self.__Message)

    def GetFormattedID(self) -> str:
        res = self.GetPlainID()
        if res.startswith('{tool}.{tool}'.format(tool=self.__Tool)):
            pass
        elif res.startswith('{tool}'.format(tool=self.__Tool)):
            res = '{tool}.{res}'.format(tool=self.__Tool, res=res)
        else:
            res = '{tool}.{tool}.{res}'.format(tool=self.__Tool, res=res)
        return res

    def GetPath(self, exportpath=None) -> str:
        return os.path.join(exportpath or self.__BuildPath or '', self.__File)

    def __repr__(self):
        return '{path}:{line}:{col} [{severity}]: {msg} ({id}) :: {scope}'.format(
            path=self.GetPath(),
            line=self.__Line,
            col=self.__Column,
            severity=self.__Severity,
            msg=self.__Message,
            id=self.GetFormattedID(),
            scope=self.__Scope)

    def __eq__(self, other):
        return str(other) == str(self)

    def __ne__(self, other):
        return (not self.__eq__(other))

    def __hash__(self):
        return hash(self.__repr__())

    @staticmethod
    def FromFile(file_: str) -> List:
        res = []
        try:
            with open(file_) as j:
                res = [SCAInput(**i) for i in json.load(j)]
        except FileNotFoundError:
            logging.error(f'{file_} not found')  # noqa: G004
        except Exception as e:
            logging.exception(e)
        return res
