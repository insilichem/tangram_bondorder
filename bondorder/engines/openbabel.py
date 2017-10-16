#!/usr/bin/env python
# encoding: utf-8


from __future__ import print_function, division, absolute_import


def convert_molecule(molecule):
    import openbabel as ob
    obmol = ob.OBMol()
    atom_map = {}
    i = 0
    for residue in molecule.residues:
        r = obmol.NewResidue()
        r.SetName(residue.type)
        r.SetNum(residue.id.position)
        r.SetChain(residue.id.chainId)
        r.SetInsertionCode(residue.id.insertionCode)
        for catom in residue.atoms:
            i +=1
            atom_map[catom] = i + 1
            a = obmol.NewAtom()
            a.SetResidue(r)
            a.SetAtomicNum(catom.element.number)
            a.SetVector(*catom.coord().data())
    
    for bond in molecule.bonds:
        a1, a2 = bond.atoms
        b = obmol.AddBond(atom_map[a1], atom_map[a2], 1)
    
    obmol.PerceiveBondOrders()
    return obmol, atom_map


def compute_bond_order(molecule, a1, a2, cached_mol=None, atom_map=None):
    obmol = cached_mol
    if None in (obmol, atom_map):
        obmol, atom_map = convert_molecule(molecule)
    bond = obmol.GetBond(atom_map[a1], atom_map[a2])
    order = bond.GetBondOrder() if bond else None
    return order, obmol, atom_map
