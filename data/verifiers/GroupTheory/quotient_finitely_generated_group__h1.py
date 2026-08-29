import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

# Top-level setup
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "¬Q: The quotient group G/N is not finitely generated"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    h1 = False
    neg_q = False
    
    G, N = None, None
    if isinstance(witness, tuple) and len(witness) == 2:
        G, N = witness
    elif hasattr(witness, 'G') and hasattr(witness, 'N'):
        G = witness.G
        N = witness.N

    if G is not None and N is not None:
        # Check H1: N is a normal subgroup of G
        try:
            if hasattr(G, 'is_normal'):
                h1 = bool(G.is_normal(N))
            elif hasattr(N, 'is_normal_in'):
                h1 = bool(N.is_normal_in(G))
            elif hasattr(witness, 'is_normal'):
                h1 = bool(witness.is_normal())
        except Exception:
            pass
            
        # Check neg_Q: G/N is not finitely generated
        try:
            Q_group = None
            if hasattr(G, 'quotient_group'):
                Q_group = G.quotient_group(N)
            else:
                try:
                    Q_group = G / N
                except Exception:
                    pass
            
            if Q_group is not None:
                if hasattr(Q_group, 'is_finitely_generated'):
                    is_fg = Q_group.is_finitely_generated
                    if callable(is_fg):
                        is_fg = is_fg()
                    neg_q = not bool(is_fg)
                elif hasattr(Q_group, 'generators'):
                    try:
                        neg_q = len(list(Q_group.generators)) == float('inf')
                    except TypeError:
                        neg_q = False
                else:
                    neg_q = False
            else:
                # Fallback: if N is trivial, G/N is isomorphic to G
                is_trivial = False
                if hasattr(N, 'is_trivial'):
                    is_trivial = N.is_trivial
                    if callable(is_trivial):
                        is_trivial = is_trivial()
                elif hasattr(N, 'order'):
                    order = N.order
                    if callable(order):
                        order = order()
                    is_trivial = (order == 1)
                
                if is_trivial:
                    if hasattr(G, 'is_finitely_generated'):
                        is_fg = G.is_finitely_generated
                        if callable(is_fg):
                            is_fg = is_fg()
                        neg_q = not bool(is_fg)
        except Exception:
            pass

    # Fallback for custom witness object without explicit G and N attributes
    if not h1:
        try:
            if hasattr(witness, 'N_is_normal_in_G'):
                h1 = bool(witness.N_is_normal_in_G())
            elif hasattr(witness, 'is_normal'):
                h1 = bool(witness.is_normal())
            elif hasattr(witness, 'is_normal_subgroup'):
                h1 = bool(witness.is_normal_subgroup())
        except Exception:
            pass
            
    if not neg_q:
        try:
            if hasattr(witness, 'quotient_is_finitely_generated'):
                neg_q = not bool(witness.quotient_is_finitely_generated())
            elif hasattr(witness, 'G_mod_N_is_finitely_generated'):
                neg_q = not bool(witness.G_mod_N_is_finitely_generated())
            elif hasattr(witness, 'is_quotient_finitely_generated'):
                neg_q = not bool(witness.is_quotient_finitely_generated())
        except Exception:
            pass

    return [h1, neg_q]