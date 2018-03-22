#!/usr/bin/env python
# encoding: utf-8


from __future__ import print_function, division
import chimera

class BondOrderExtension(chimera.extension.EMO):

    def name(self):
        return 'Tangram BondOrder'

    def description(self):
        return "Bond order perception assignment and calculation"

    def categories(self):
        return ['InsiliChem']

    def icon(self):
        return

    def activate(self):
        self.module('gui').showUI()


chimera.extension.manager.registerExtension(BondOrderExtension(__file__))