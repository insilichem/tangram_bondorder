#!/usr/bin/env python
# encoding: utf-8


"""
Implements several bond order perception engines within UCSF Chimera
and allows their representation.
"""
from __future__ import print_function, division
from chimera.misc import getPseudoBondGroup
from chimera.colorTable import getColorByName
from random import choice
from importlib import import_module


def assign_bond_orders(molecule, engine='openbabel'):
    engine = import_module('bondorder.engines.{}'.format(engine))
    converted, atom_map = engine.convert_molecule(molecule)

    for bond in molecule.bonds:
        a1, a2 = bond.atoms
        order, obmol, atom_map = engine.compute_bond_order(molecule, a1, a2, 
            cached_mol=converted, atom_map=atom_map)
        bond.order = order


def draw_bond_orders(molecule, error_spring=True):
    pbg = getPseudoBondGroup('Bond order errors', associateWith=[molecule])
    pbg.lineWidth, pbg.lineType, pbg.color = 2, 1, getColorByName('red')
    def draw_spring(bond):
        pbg = getPseudoBondGroup('Bond order errors')
        pb = pbg.newPseudoBond(*bond.atoms)
        pb.drawMode = 2
        pb.radius = bond.radius + 0.1

    for bond in molecule.bonds:
        order = getattr(bond, 'order', None)
        if not order:
            print('! Invalid order for bond', bond)
            if error_spring:
                draw_spring(bond)
            continue
        if not hasattr(bond, '_oldradius'):
            bond._oldradius = bond.radius
        bond.radius = bond._oldradius * order * 0.5

    return pbg

