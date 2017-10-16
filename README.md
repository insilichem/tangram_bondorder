# Plume BondOrder

Automatic bond order perception for UCSF Chimera using several backend engines:

    - RDKit
    - OpenBabel
    - ...

It is also able to depict them, as long as each `Bond` object contains an `order` attribute. This can come from the aforementioned backends, or directly from the original molecule file (mol2 files, Gaussian outputs, etc).

Commands implemented:

    - bondorderdraw [molecule]
    - bondorderread [molecule] [format]
    - bondordercalc [molecule] [engine]