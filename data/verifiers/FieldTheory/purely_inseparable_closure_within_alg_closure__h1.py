import sympy
from sympy import *
import sympy.combinatorics as comb
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup for standard objects
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

CONDITION_LABELS = [
    "H_1: \\overline{F} is an algebraic closure of F",
    "H_2: E is the set of all elements in \\overline{F} that are purely inseparable over F",
    "¬Q: E is not a subfield of \\overline{F}, or the field extension \\overline{F}/E is not separable"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    h1 = False
    h2 = False
    q1 = True
    q2 = True

    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            F, F_bar, E = witness
            
            # H1: \overline{F} is an algebraic closure of F
            if hasattr(F_bar, 'is_algebraic_closure_of'):
                h1 = bool(F_bar.is_algebraic_closure_of(F))
            elif hasattr(F_bar, 'is_algebraic_closure'):
                v = F_bar.is_algebraic_closure
                if callable(v):
                    try: h1 = bool(v(F))
                    except Exception: h1 = bool(v())
                else:
                    h1 = bool(v)
                
            # H2: E is the purely inseparable closure
            if hasattr(E, 'is_purely_inseparable_closure_of'):
                h2 = bool(E.is_purely_inseparable_closure_of(F, F_bar))
            elif hasattr(E, 'is_purely_inseparable_closure'):
                v = E.is_purely_inseparable_closure
                if callable(v):
                    try: h2 = bool(v(F, F_bar))
                    except Exception:
                        try: h2 = bool(v(F))
                        except Exception: h2 = bool(v())
                else:
                    h2 = bool(v)
                    
            # Q1: E is a subfield of \overline{F}
            if hasattr(E, 'is_subfield_of'):
                q1 = bool(E.is_subfield_of(F_bar))
            elif hasattr(E, 'is_subfield'):
                v = E.is_subfield
                if callable(v):
                    try: q1 = bool(v(F_bar))
                    except Exception: q1 = bool(v())
                else:
                    q1 = bool(v)
                    
            # Q2: \overline{F}/E is separable
            if hasattr(F_bar, 'is_separable_over'):
                q2 = bool(F_bar.is_separable_over(E))
            elif hasattr(F_bar, 'is_separable_extension'):
                v = F_bar.is_separable_extension
                if callable(v):
                    try: q2 = bool(v(E))
                    except Exception: q2 = bool(v())
                else:
                    q2 = bool(v)
                    
        else:
            # Handle dictionary or single mock object witness
            def get_p(names, default=False):
                if isinstance(witness, dict):
                    for n in names:
                        if n in witness: return bool(witness[n])
                else:
                    for n in names:
                        if hasattr(witness, n):
                            v = getattr(witness, n)
                            if callable(v):
                                try: return bool(v())
                                except Exception: pass
                            else:
                                return bool(v)
                return default
                
            h1 = get_p(['F_bar_is_alg_closure_of_F', 'is_algebraic_closure', 'h1'], False)
            h2 = get_p(['E_is_purely_inseparable_closure', 'is_purely_inseparable', 'h2'], False)
            q1 = get_p(['E_is_subfield', 'is_subfield', 'q1'], True)
            q2 = get_p(['F_bar_over_E_is_separable', 'is_separable', 'q2'], True)
            
    except Exception:
        pass

    # The conclusion fails if E is not a subfield OR \overline{F}/E is not separable
    neg_q = not (q1 and q2)
    
    return [h1, h2, neg_q]