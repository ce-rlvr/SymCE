import sympy
from sympy import ZZ, QQ
from sympy.abc import x, y, z
from sympy.polys.polytools import groebner, Poly

# Top-level setup
# The witness can be provided in one of three formats:
# 1. A dictionary: {'domain': ZZ, 'vars': [x], 'gens': [2, x]}
# 2. A 3-tuple: (ZZ, [x], [2, x])
# 3. A 2-tuple: (ZZ[x], [2, x])
# This represents the ideal I = (2, x) in the ring R = ZZ[x].

CONDITION_LABELS = [
    "H_1: I is a non-zero ideal of R",
    "¬Q: I is not a free R-module of rank 1"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        if isinstance(witness, dict):
            domain = witness.get('domain')
            vars = witness.get('vars', [])
            gens = witness.get('gens', [])
        elif isinstance(witness, tuple) and len(witness) == 3:
            domain, vars, gens = witness
        elif isinstance(witness, tuple) and len(witness) == 2:
            ring, gens = witness
            if hasattr(ring, 'symbols'):
                domain = ring.domain
                vars = ring.symbols
            else:
                domain = ring
                vars = []
        else:
            return [False, False]
            
        if domain == 'ZZ':
            domain = ZZ
        elif domain == 'QQ':
            domain = QQ
            
        if not isinstance(vars, (list, tuple)):
            vars = [vars]
    except Exception:
        return [False, False]
        
    # H_1: I is a non-zero ideal of R
    try:
        if not gens:
            h1 = False
        elif domain not in (ZZ, QQ):
            # We restrict to ZZ or QQ to ensure R is an integral domain
            h1 = False
        else:
            h1 = True
            all_zero = True
            for g in gens:
                if vars:
                    p = Poly(g, *vars, domain=domain)
                    if not p.is_zero:
                        all_zero = False
                else:
                    if domain(g) != domain.zero:
                        all_zero = False
            if all_zero:
                h1 = False
    except Exception:
        h1 = False

    # ¬Q: I is not a free R-module of rank 1
    # In an integral domain, a non-zero ideal is free of rank 1 iff it is principal.
    try:
        if not h1:
            neg_q = False
        elif not vars:
            # Over ZZ or QQ, every ideal is principal
            neg_q = False
        else:
            gb = groebner(gens, *vars, domain=domain)
            neg_q = len(gb) > 1
    except Exception:
        neg_q = False

    return [h1, neg_q]