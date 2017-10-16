#!/usr/bin/env python
# encoding: utf-8

"""
Bond order perception engines

API is self-documented below.
"""

def convert_molecule(molecule):
    """
    Parameters
    ----------
    molecule : chimera.molecule

    Returns
    -------
    converted : object
        Converted molecule for that framework
    atom_map : dict
        Maps chimera.Atom objects to converted.Atom objects or their indices
    """
    raise NotImplementedError('Use of one the submodules instead')


def compute_bond_order(molecule, atom_1, atom_2, cached_mol=None, atom_map=None):
    """
    Parameters
    ----------
    molecule : chimera.molecule
    atom_1, atom_2 : chimera.Atom
    cached_mol : object
        If not provided, `convert_molecule` will be called
    atom_map : dict
        If not provided, `convert_molecule` will be called

    Returns
    -------
    bond_order : float
    cached_mol : object
    atom_map : dict
    """
    raise NotImplementedError('Use of one the submodules instead')