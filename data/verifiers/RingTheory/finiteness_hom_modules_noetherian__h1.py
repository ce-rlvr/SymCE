import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Given a witness object, checks whether it is a valid counterexample to the false conjecture:
    "Let R be a ring. Let M and N be finitely generated R-modules. Then Hom_R(M, N) is a finitely generated R-module."
    """
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get('M_is_finitely_generated', witness.get('M_is_fg', False)))
            h2 = bool(witness.get('N_is_finitely_generated', witness.get('N_is_fg', False)))
            hom_fg = bool(witness.get('Hom_is_finitely_generated', witness.get('Hom_is_fg', True)))
            neg_q = not hom_fg
            
        elif isinstance(witness, tuple) and len(witness) == 3:
            M, N, Hom = witness
            
            if hasattr(M, 'is_finitely_generated'):
                val = M.is_finitely_generated
                h1 = bool(val() if callable(val) else val)
            elif hasattr(M, 'is_fg'):
                val = M.is_fg
                h1 = bool(val() if callable(val) else val)
                
            if hasattr(N, 'is_finitely_generated'):
                val = N.is_finitely_generated
                h2 = bool(val() if callable(val) else val)
            elif hasattr(N, 'is_fg'):
                val = N.is_fg
                h2 = bool(val() if callable(val) else val)
                
            if hasattr(Hom, 'is_finitely_generated'):
                val = Hom.is_finitely_generated
                hom_fg = bool(val() if callable(val) else val)
                neg_q = not hom_fg
            elif hasattr(Hom, 'is_fg'):
                val = Hom.is_fg
                hom_fg = bool(val() if callable(val) else val)
                neg_q = not hom_fg
                
        else:
            # Check M
            if hasattr(witness, 'M_is_finitely_generated'):
                val = witness.M_is_finitely_generated
                h1 = bool(val() if callable(val) else val)
            elif hasattr(witness, 'M_is_fg'):
                val = witness.M_is_fg
                h1 = bool(val() if callable(val) else val)
            elif hasattr(witness, 'M'):
                if hasattr(witness.M, 'is_finitely_generated'):
                    val = witness.M.is_finitely_generated
                    h1 = bool(val() if callable(val) else val)
                elif hasattr(witness.M, 'is_fg'):
                    val = witness.M.is_fg
                    h1 = bool(val() if callable(val) else val)
            
            # Check N
            if hasattr(witness, 'N_is_finitely_generated'):
                val = witness.N_is_finitely_generated
                h2 = bool(val() if callable(val) else val)
            elif hasattr(witness, 'N_is_fg'):
                val = witness.N_is_fg
                h2 = bool(val() if callable(val) else val)
            elif hasattr(witness, 'N'):
                if hasattr(witness.N, 'is_finitely_generated'):
                    val = witness.N.is_finitely_generated
                    h2 = bool(val() if callable(val) else val)
                elif hasattr(witness.N, 'is_fg'):
                    val = witness.N.is_fg
                    h2 = bool(val() if callable(val) else val)
            
            # Check Hom
            if hasattr(witness, 'Hom_is_finitely_generated'):
                val = witness.Hom_is_finitely_generated
                hom_fg = bool(val() if callable(val) else val)
                neg_q = not hom_fg
            elif hasattr(witness, 'Hom_is_fg'):
                val = witness.Hom_is_fg
                hom_fg = bool(val() if callable(val) else val)
                neg_q = not hom_fg
            elif hasattr(witness, 'Hom'):
                if hasattr(witness.Hom, 'is_finitely_generated'):
                    val = witness.Hom.is_finitely_generated
                    hom_fg = bool(val() if callable(val) else val)
                    neg_q = not hom_fg
                elif hasattr(witness.Hom, 'is_fg'):
                    val = witness.Hom.is_fg
                    hom_fg = bool(val() if callable(val) else val)
                    neg_q = not hom_fg

    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: M is a finitely generated R-module",
    "H_2: N is a finitely generated R-module",
    "¬Q: Hom_R(M, N) is not a finitely generated R-module"
]

N_HYP = 2
NEG_Q_INDEX = 2