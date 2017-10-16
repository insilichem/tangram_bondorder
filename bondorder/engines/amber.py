#!/usr/bin/env python
# encoding: utf-8


from __future__ import print_function, division, absolute_import


def compute_bond_order(molecule, a1, a2, cached_mol=None, atom_map=None):
    mol = cached_mol
    if None in (mol, atom_map):
        mol, atom_map = run_bondtype(molecule)
    new_a1, new_a2 = None, None
    for atom in mol.atoms:
        if str(atom) == str(a1):
            new_a1 = atom
        elif str(atom) == str(a2):
            new_a2 = atom
    bond = new_a1.bondsMap[new_a2]
    return bond.order


def run_bondtype(molecule):
    from WriteMol2 import writeMol2
    from OpenSave import osTemporaryFile
    from subprocess import call
    import chimera
    tmpfilein = osTemporaryFile(suffix='.mol2', prefix='bondtype_')
    tmpfileout = osTemporaryFile(suffix='.mol2', prefix='bondtype_')
    writeMol2([molecule], tmpfilein, temporary=True)
    call(['bondtype', '-i', tmpfilein, '-o', tmpfileout, '-f', 'mol2', '-j', 'full'])
    processed = chimera.openModels.open(tmpfileout, temporary=True)
    return processed