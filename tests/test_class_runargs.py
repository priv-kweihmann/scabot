# SPDX-FileCopyrightText: 2021 Konrad Weihmann
# SPDX-License-Identifier: GPL-3.0-only

import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from base import TestBaseClass

class TestClassRunargs(TestBaseClass):

    @pytest.mark.parametrize('provider', ('mock', 'github', 'gitlab'))
    @pytest.mark.parametrize('project', ('1', '10000', '20000000'))
    @pytest.mark.parametrize('requestnum', ('1', '10000', '20000000'))
    @pytest.mark.parametrize('inputfiles', [TestBaseClass.file_in_testdir('bad-po-1.0.dm')])
    @pytest.mark.parametrize('preargs', (
                                            [], 
                                            ["--bottoken=foo"], 
                                            ["--botuser=foo"], 
                                            ["--botuser=foo", "--bottoken=foo"],
                                            ["--comment_only_affected_lines"],
                                            ["--comment_drafts"],
                                            ["--comment_indirect"]
                                            ))
    def test_runargs_good(self, provider, project, requestnum, inputfiles, preargs):
        self._create_args(provider=provider, project=project, requestnum=requestnum, inputfiles=inputfiles, preargs=preargs)

    @pytest.mark.parametrize('provider', ('', 'foo'))
    @pytest.mark.parametrize('project', '1')
    @pytest.mark.parametrize('requestnum', '1')
    @pytest.mark.parametrize('inputfiles', [TestBaseClass.file_in_testdir('bad-po-1.0.dm')])
    @pytest.mark.parametrize('preargs', [])
    def test_runargs_bad_provider(self, provider, project, requestnum, inputfiles, preargs):
        with pytest.raises(SystemExit):
            self._create_args(provider=provider, project=project, requestnum=requestnum, inputfiles=inputfiles, preargs=preargs)

    @pytest.mark.parametrize('provider', 'mock')
    @pytest.mark.parametrize('project', '')
    @pytest.mark.parametrize('requestnum', '1')
    @pytest.mark.parametrize('inputfiles', [TestBaseClass.file_in_testdir('bad-po-1.0.dm')])
    @pytest.mark.parametrize('preargs', [])
    def test_runargs_bad_project(self, provider, project, requestnum, inputfiles, preargs):
        with pytest.raises(SystemExit):
            self._create_args(provider=provider, project=project, requestnum=requestnum, inputfiles=inputfiles, preargs=preargs)

    @pytest.mark.parametrize('provider', 'mock')
    @pytest.mark.parametrize('project', '1')
    @pytest.mark.parametrize('requestnum', '')
    @pytest.mark.parametrize('inputfiles', [TestBaseClass.file_in_testdir('bad-po-1.0.dm')])
    @pytest.mark.parametrize('preargs', [])
    def test_runargs_bad_requestnum(self, provider, project, requestnum, inputfiles, preargs):
        with pytest.raises(SystemExit):
            self._create_args(provider=provider, project=project, requestnum=requestnum, inputfiles=inputfiles, preargs=preargs)

    @pytest.mark.parametrize('provider', 'mock')
    @pytest.mark.parametrize('project', '1')
    @pytest.mark.parametrize('requestnum', '1')
    @pytest.mark.parametrize('inputfiles', [])
    @pytest.mark.parametrize('preargs', [])
    def test_runargs_bad_inputfiles(self, provider, project, requestnum, inputfiles, preargs):
        with pytest.raises(SystemExit):
            self._create_args(provider=provider, project=project, requestnum=requestnum, inputfiles=inputfiles, preargs=preargs)

    @pytest.mark.parametrize('provider', 'mock')
    @pytest.mark.parametrize('project', '1')
    @pytest.mark.parametrize('requestnum', '1')
    @pytest.mark.parametrize('inputfiles', [TestBaseClass.file_in_testdir('bad-po-1.0.dm')])
    @pytest.mark.parametrize('preargs', (
                                            ["--notvalid"], 
                                            ["-n"], 
                                            ["--botuser"], 
                                            ["--botuser="], 
                                            ["--bottoken"], 
                                            ["--bottoken="],
                                            ["--comment_drafts="],
                                            ["--comment_indirect="],
                                        )
                            )
    def test_runargs_bad_optionals(self, provider, project, requestnum, inputfiles, preargs):
        with pytest.raises(SystemExit):
            self._create_args(provider=provider, project=project, requestnum=requestnum, inputfiles=inputfiles, preargs=preargs)

    def test_runargs_environment(self):
        os.environ["SCABOT_PROJECT"] = "1"
        os.environ["SCABOT_REQUEST"] = "2"
        os.environ["SCABOT_SERVER"] = "3"
        os.environ["SCABOT_BOTUSER"] = "4"
        os.environ["SCABOT_BOTTOKEN"] = "5"
        os.environ["SCABOT_COMMENT_AFFECTED_LINES"] = "True"
        os.environ["SCABOT_COMMENT_DRAFT_REQUEST"] = "True"
        os.environ["SCABOT_COMMENT_INDIRECT"] = "True"

        parser = self._create_args_parser()
        _result = parser.parse_args(['mock', TestBaseClass.file_in_testdir('bad-po-1.0.dm')])

        assert(_result.project == "1")
        assert(_result.request == "2")
        assert(_result.server == "3")
        assert(_result.botuser == "4")
        assert(_result.bottoken == "5")
        assert(_result.comment_only_affected_lines == True)
        assert(_result.comment_indirect == True)
