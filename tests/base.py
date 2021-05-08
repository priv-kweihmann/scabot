# SPDX-FileCopyrightText: 2021 Konrad Weihmann
# SPDX-License-Identifier: GPL-3.0-only

import os
import sys


class TestBaseClass():

    TESTFILES_DIR = os.path.abspath(os.path.dirname(__file__) + "/../testfiles")

    @classmethod
    def setup_class(cls):
        sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + "/../"))

    def _create_args(self, provider="mock", server=TESTFILES_DIR, project="0", requestnum="0", inputfiles=[], preargs=[]):
        return self._create_args_parser().parse_args(preargs + [provider, "--server={}".format(server), 
            "--project={}".format(project), "--request={}".format(requestnum), *inputfiles])

    def _create_args_parser(self):
        from scabot.runargs import create_parser
        return create_parser()

    def _create_provider(self, args):
        from scabot.runargs import create_provider_instance
        return create_provider_instance(args)

    def _create_request(self, args, provider):
        from scabot.runargs import create_request_instance
        return create_request_instance(args, provider)

    @staticmethod
    def file_in_testdir(file):
        if not file.startswith(TestBaseClass.TESTFILES_DIR):
            return os.path.join(TestBaseClass.TESTFILES_DIR, file.lstrip('/'))
        return file

    def has_method(self, obj, method):
        return callable(getattr(obj, method, None))

    def has_attribute(self, obj, attr):
        return hasattr(obj, attr)
