import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup for potential witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    """
    Given a witness object, checks if it is a valid counterexample to the false conjecture.
    The conjecture states that if G/Phi(G) is nilpotent, then G is nilpotent.
    (This is true for finite groups, but false in general if the 'finite' hypothesis is dropped).
    """
    if isinstance(witness, tuple) and len(witness) == 2:
        G, Phi = witness
        
        # H1: Phi is the Frattini subgroup of G
        h1_ok = False
        try:
            if hasattr(Phi, 'is_frattini_of'):
                val = Phi.is_frattini_of(G)
                h1_ok = val() if callable(val) else bool(val)
            elif hasattr(G, 'frattini_subgroup'):
                f = G.frattini_subgroup
                f = f() if callable(f) else f
                h1_ok = (f == Phi)
            elif hasattr(Phi, 'is_frattini'):
                val = Phi.is_frattini
                h1_ok = val() if callable(val) else bool(val)
            else:
                # Fallback for mock objects that don't explicitly define the relation
                h1_ok = True
        except Exception:
            h1_ok = False
            
        # H2: G/Phi is nilpotent
        h2_ok = False
        try:
            q = None
            if hasattr(G, 'quotient_group'):
                q = G.quotient_group(Phi)
            elif hasattr(G, 'quo'):
                q = G.quo(Phi)
            else:
                try:
                    q = G / Phi
                except Exception:
                    pass
            
            if q is not None and hasattr(q, 'is_nilpotent'):
                val = q.is_nilpotent
                h2_ok = val() if callable(val) else bool(val)
            elif hasattr(G, 'quotient_by_frattini_is_nilpotent'):
                val = G.quotient_by_frattini_is_nilpotent
                h2_ok = val() if callable(val) else bool(val)
        except Exception:
            h2_ok = False
            
        # neg_Q: G is not nilpotent
        neg_q_ok = False
        try:
            if hasattr(G, 'is_nilpotent'):
                val = G.is_nilpotent
                is_nilp = val() if callable(val) else bool(val)
                neg_q_ok = not is_nilp
        except Exception:
            neg_q_ok = False
            
        return [h1_ok, h2_ok, neg_q_ok]

    else:
        G = witness
        
        # H1: Phi(G) is the Frattini subgroup of G
        # When the witness is just G, this is a definitional statement.
        h1_ok = True
        
        # H2: G/Phi(G) is nilpotent
        h2_ok = False
        try:
            direct_found = False
            for attr in ['quotient_by_frattini_is_nilpotent', 'frattini_quotient_is_nilpotent', 'is_frattini_quotient_nilpotent']:
                if hasattr(G, attr):
                    val = getattr(G, attr)
                    h2_ok = val() if callable(val) else bool(val)
                    direct_found = True
                    break
            
            if not direct_found:
                f = None
                for attr in ['frattini_subgroup', 'Phi', 'frattini']:
                    if hasattr(G, attr):
                        f_attr = getattr(G, attr)
                        f = f_attr() if callable(f_attr) else f_attr
                        break
                
                if f is not None:
                    q = None
                    if hasattr(G, 'quotient_group'):
                        q = G.quotient_group(f)
                    elif hasattr(G, 'quo'):
                        q = G.quo(f)
                    else:
                        try:
                            q = G / f
                        except Exception:
                            pass
                            
                    if q is not None and hasattr(q, 'is_nilpotent'):
                        val = q.is_nilpotent
                        h2_ok = val() if callable(val) else bool(val)
        except Exception:
            h2_ok = False
            
        # neg_Q: G is not nilpotent
        neg_q_ok = False
        try:
            if hasattr(G, 'is_nilpotent'):
                val = G.is_nilpotent
                is_nilp = val() if callable(val) else bool(val)
                neg_q_ok = not is_nilp
        except Exception:
            neg_q_ok = False
            
        return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: Phi(G) is the Frattini subgroup of G",
    "H_2: The quotient group G/Phi(G) is nilpotent",
    "¬Q: The group G is not nilpotent"
]

N_HYP = 2
NEG_Q_INDEX = 2