#!/usr/bin/env python
# encoding: utf-8


from __future__ import print_function, division
# Python stdlib
import Tkinter as tk
import Pmw
# Chimera stuff
import chimera
# Own
from libplume.ui import PlumeBaseDialog
from chimera.widgets import MoleculeOptionMenu
from bondorder.core import assign_bond_orders, draw_bond_orders

ui = None  # singleton
def showUI():
    if chimera.nogui:
        tk.Tk().withdraw()
    global ui
    if not ui:
        ui = BondOrderDialog()
    ui.enter()


class BondOrderDialog(PlumeBaseDialog):

    buttons = ('Draw', 'Close')
    default = None
    help = 'http://www.insilichem.com'


    def __init__(self, *args, **kwargs):
        # GUI init
        self.title = 'Plume BondOrder'
        self.controller = None

        # Fire up
        super(BondOrderDialog, self).__init__(resizable=False, *args, **kwargs)

        # Triggers
        chimera.triggers.addHandler('selection changed', self._cb_fill_order, None)

    def fill_in_ui(self, parent):
        self.canvas.columnconfigure(0, weight=1)
        row = 0
        self.ui_calculation = tk.LabelFrame(self.canvas, text='Perceive bond order')
        self.ui_molecule = MoleculeOptionMenu(self.ui_calculation, labelpos='w',
                                              label_text='Analyze')
        self.ui_methods = Pmw.OptionMenu(self.ui_calculation, label_text='with',
                                         labelpos='w', items=['RDKit',
                                                              'OpenBabel',
                                                              'Single'])
        self.ui_calculate_btn = tk.Button(self.ui_calculation, text='Go!',
                                          command=self._cmd_calculate_btn)
        self.ui_calculation.grid(row=row, padx=5, pady=5, sticky='we')
        self.ui_calculation.columnconfigure(0, weight=1)
        self.ui_molecule.grid(row=0, column=0, padx=5, pady=5, sticky='we')
        self.ui_methods.grid(row=0, column=1, padx=5, pady=5)
        self.ui_calculate_btn.grid(row=0, column=2, padx=5, pady=5)

        row +=1
        self.ui_edition = tk.LabelFrame(self.canvas, text='Manual edition')
        self.ui_order_fld = Pmw.EntryField(self.ui_edition, entry_width=4,
                                           validate=self._order_validator,
                                           labelpos='w', label_text='<Select one bond>')
        self.ui_order_fld['entry_state'] = 'disabled'
        self.ui_order_btn = tk.Button(self.ui_edition, text='Write',
                                      command=self._cmd_order_btn)
        self.ui_order_btn['state'] = 'disabled'
        self.ui_edition.grid(row=row, padx=5, pady=5, sticky='we')
        self.ui_edition.columnconfigure(0, weight=1)
        self.ui_order_fld.grid(row=0, column=0, padx=5, pady=5, sticky='we')
        self.ui_order_btn.grid(row=0, column=1, padx=5, pady=5)


    def Draw(self):
        m = self.ui_molecule.getvalue()
        draw_bond_orders(m)

    def Close(self):  # Singleton mode
        global ui
        ui = None
        super(BondOrderDialog, self).Close()

    def _cmd_order_btn(self, *args):
        order = self.ui_order_fld.getvalue()
        for bond in chimera.selection.currentBonds():
            bond.order = order

    def _cmd_calculate_btn(self, *args):
        molecule = self.ui_molecule.getvalue()
        engine = self.ui_methods.getvalue()
        try:
            assign_bond_orders(molecule, engine=engine.lower())
        except Exception as e:
            self.status('Could not compute automatically!', color='red', blankAfter=4)
        else:
            self.Draw()

    def _cb_fill_order(self, *args, **kwargs):
        selected_bonds = chimera.selection.currentBonds()
        length = len(selected_bonds)
        if not length:
            label = '<Select one bond>'
            self.ui_order_fld.clear()
            self.ui_order_fld['entry_state'] = 'disabled'
            self.ui_order_fld['label_text'] = label

            self.ui_order_btn['state'] = 'disabled'
        elif length == 1:
            bond = selected_bonds[0]
            label = str(bond)
            self.ui_order_fld['entry_state'] = 'normal'
            self.ui_order_fld['label_text'] = label
            self.ui_order_btn['state'] = 'normal'
            order = getattr(bond, 'order', '')
            self.ui_order_fld.setvalue(order)
        else:
            self.ui_order_fld['entry_state'] = 'normal'
            self.ui_order_fld['label_text'] = '<More than one selected>'
            self.ui_order_fld.setvalue('')
            self.ui_order_btn['state'] = 'normal'

    def _order_validator(self, value):
        try:
            value = float(value)
        except (TypeError, ValueError):
            value = -1
        btn = getattr(self, 'ui_order_btn', {})
        if 0 < value < 3:
            btn['state'] = 'normal'
            return Pmw.OK
        else:
            btn['state'] = 'disabled'
            return Pmw.PARTIAL