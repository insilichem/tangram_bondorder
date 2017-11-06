#!/usr/bin/env python
# encoding: utf-8


from __future__ import print_function, division
# Python stdlib
import Tkinter as tk
import Pmw
# Chimera stuff
import chimera
# Own
from libplume.ui import PlumeBaseDialog, STYLES
from chimera.widgets import MoleculeOptionMenu, SortableTable
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
    help = "https://github.com/insilichem/plume_bondorder"
    VERSION = '0.0.1'
    VERSION_URL = "https://api.github.com/repos/insilichem/plume_bondorder/releases/latest"

    def __init__(self, *args, **kwargs):
        # GUI init
        self.title = 'Plume BondOrder'
        self.controller = None

        # Fire up
        super(BondOrderDialog, self).__init__(resizable=False, *args, **kwargs)

        # Triggers
        chimera.triggers.addHandler('selection changed', self._cmd_hilite_selected, None)

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
        self.ui_fill_all_btn = tk.Button(self.ui_edition, text='Fill with all')
        self.ui_fill_selected_btn = tk.Button(self.ui_edition, text='Fill with selection')
        self.ui_fill_defined_btn = tk.Button(self.ui_edition, text='Fill with defined')
        self.ui_hilite_selected_btn = tk.Button(self.ui_edition, text='Highlight selected')
        buttons = (self.ui_fill_all_btn, self.ui_fill_selected_btn,
                   self.ui_fill_defined_btn, self.ui_hilite_selected_btn)
        self.auto_pack(self.ui_edition, buttons, padx=5, pady=5, side='left')
        self.ui_edition.grid(row=row, columnspan=3, padx=5, pady=5, sticky='we')

        row +=1
        self.ui_table = t = _SortableTableWithEntries(self.canvas)
        self.ui_table.grid(row=row, padx=5, pady=5, sticky='news')
        kw = dict(anchor='w', refresh=False)
        t.addColumn('Bond', 'bond', format=str, headerPadX=75, **kw)
        t.addColumn('Order', 'var_order', format=lambda a: a, headerPadX=5, **kw)
        t.setData([_BondTableProxy(bond=b) for b in chimera.selection.currentBonds()])
        t.grid(row=row, column=0, columnspan=3, padx=5, pady=5, sticky='news')
        self.canvas.rowconfigure(row, weight=1)

    def Draw(self):
        m = self.ui_molecule.getvalue()
        draw_bond_orders(m)

    def Close(self):  # Singleton mode
        global ui
        ui = None
        super(BondOrderDialog, self).Close()

    def _cmd_calculate_btn(self, *args):
        molecule = self.ui_molecule.getvalue()
        engine = self.ui_methods.getvalue()
        try:
            assign_bond_orders(molecule, engine=engine.lower())
        except Exception as e:
            self.status('Could not compute automatically!', color='red', blankAfter=4)
        else:
            self.Draw()

    def _cmd_fill_all(self, *args):
        pass

    def _cmd_fill_selected(self, *args):
        pass

    def _cmd_fill_defined(self, *args):
        pass

    def _cmd_hilite_selected(self, *args):
        pass



class _BondTableProxy(object):

    """
    Proxy object to ease the creation of table rows

    Attributes
    ----------
    bond=bond
    order=order
    """

    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

        self.var_order = tk.DoubleVar()

    @property
    def order(self):
        return self.var_order.get()

    @order.setter
    def order(self, value):
        self.var_order.set(round(value, 1))


class _SortableTableWithEntries(SortableTable):

    def _createCell(self, hlist, row, col, datum, column):
        contents = column.displayValue(datum)
        if isinstance(contents, tk.StringVar):
            entry = Pmw.EntryField(hlist,
                                   entry_textvariable=contents,
                                   entry_width=3,
                                   validate=self._validate,
                                   **STYLES[Pmw.EntryField])
            widget = self._widgetData[(datum, column)] = entry
            hlist.item_create(row, col, itemtype="window", window=entry)
            return

        SortableTable._createCell(self, hlist, row, col, datum, column)

    @staticmethod
    def _validate(value):
        if 0 < value < 3:
            return Pmw.OK
        return Pmw.PARTIAL
