# SPDX-FileCopyrightText: 2021 Konrad Weihmann
# SPDX-License-Identifier: GPL-3.0-only

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from base import TestBaseClass

class TestClassSCAInput(TestBaseClass):

    def test_scainput_properties(self):
        from scabot.scainput import SCAInput

        x = SCAInput()

        assert(self.has_attribute(x, 'File'))
        assert(self.has_attribute(x, 'Scope'))
        assert(self.has_attribute(x, 'BuildPath'))
        assert(self.has_attribute(x, 'Line'))
        assert(self.has_attribute(x, 'Column'))
        assert(self.has_attribute(x, 'Severity'))
        assert(self.has_attribute(x, 'Message'))
        assert(self.has_attribute(x, 'ID'))
        assert(self.has_attribute(x, 'PackageName'))
        assert(self.has_attribute(x, 'Tool'))
        assert(self.has_attribute(x, 'BBFiles'))

        # test is writeable
        x.File = 'foo'
        x.Scope = 'foo'
        x.BuildPath = 'foo'
        x.Line = 'foo'
        x.Column = 'foo'
        x.Severity = 'foo'
        x.Message = 'foo'
        x.ID = 'foo'
        x.PackageName = 'foo'
        x.Tool = 'foo'
        x.BBFiles = ['foo']

    def test_scainput_compare(self):
        from scabot.scainput import SCAInput

        a = SCAInput(File="a")
        b = SCAInput(File="a")
        c = SCAInput(File="b")

        assert(a == b)
        assert(a != c)


    def test_scainput_id_explode(self):
        from scabot.scainput import SCAInput

        a = SCAInput(File="a", ID="a", Tool="tool")
        assert(a.GetFormattedID() == "tool.tool.a")

        a = SCAInput(File="a", ID="tool.a", Tool="tool")
        assert(a.GetFormattedID() == "tool.tool.a")

        a = SCAInput(File="a", ID="tool.tool.a", Tool="tool")
        assert(a.GetFormattedID() == "tool.tool.a")

    def test_scainput_formatted_messages(self):
        from scabot.scainput import SCAInput

        a = SCAInput(File="a", ID="a", Tool="tool", Message="msg", PackageName="b")

        assert(a.GetFormattedMessage() == '[Package:b Tool:tool] msg')
        