#!/usr/bin/env python
# encoding: utf-8


from __future__ import print_function, division, absolute_import


def convert_molecule(molecule):
    from rdkit.Chem import Mol, EditableMol, Atom, Conformer
    mol = Mol()
    emol = EditableMol(mol)
    conformer = Conformer()
    atom_map = {}
    for atom in molecule.atoms:
        a = Atom(atom.element.number)
        atom_map[atom] = i = emol.AddAtom(a)
        conformer.SetAtomPosition(i, atom.coord().data())
    
    for bond in molecule.bonds:
        a1, a2 = bond.atoms
        emol.AddBond(atom_map[a1], atom_map[a2])
    
    mol = emol.GetMol()
    mol.AddConformer(conformer)

    return mol, atom_map


def compute_bond_order(molecule, a1, a2, cached_mol=None, atom_map=None):
    rdmol = cached_mol
    if None in (rdmol, atom_map):
        rdmol, atom_map = convert_molecule(molecule)
    bond = rdmol.GetBondBetweenAtoms(atom_map[a1], atom_map[a2])
    order = bond.GetBondTypeAsDouble() if bond else None
    print('rdmol ->', rdmol,  
    'atom_map ->', atom_map,  
    'atom_map[a1] ->', atom_map[a1],  
    'atom_map[a2] ->', atom_map[a2],  
    'bond ->', bond,  
    'order ->', order)
    return order, rdmol, atom_map
