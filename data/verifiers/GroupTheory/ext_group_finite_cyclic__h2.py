import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy import oo
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
O2 = zeros(2,2)
O3 = zeros(3,3)

class InfiniteCyclicGroup:
    @property
    def is_abelian(self): return True
    @property
    def is_cyclic(self): return True
    def order(self): return oo
    @property
    def generators(self): return [1]
    def __eq__(self, other): return isinstance(other, InfiniteCyclicGroup)

Z = InfiniteCyclicGroup()

def conditions(witness) -> list[bool]:
    # Extract G, A, and n from the witness
    if isinstance(witness, tuple):
        if len(witness) == 2:
            G, A = witness
            if isinstance(G, int):
                n = G
            elif isinstance(G, str) and G.upper() == 'Z':
                n = oo
            else:
                try:
                    n = G.order()
                except Exception:
                    n = oo
        elif len(witness) == 3:
            G, A, n = witness
        else:
            return [False, False, False]
    else:
        return [False, False, False]

    # H_1: A is an abelian group
    h1 = False
    try:
        if hasattr(A, 'is_abelian'):
            h1 = bool(A.is_abelian)
        elif isinstance(A, int) or A == oo:
            h1 = True
        elif isinstance(A, InfiniteCyclicGroup):
            h1 = True
        elif isinstance(A, str) and A.upper() in ['Z', 'Q', 'R', 'C']:
            h1 = True
    except Exception:
        pass

    # H_2: G is a cyclic group of order n
    h2 = False
    try:
        if isinstance(G, int) or G == oo:
            h2 = True
        elif isinstance(G, str) and G.upper() == 'Z':
            if n == 0 or n == oo or n == 'oo':
                h2 = True
        else:
            is_cyc = False
            if hasattr(G, 'is_cyclic'):
                if callable(G.is_cyclic):
                    is_cyc = G.is_cyclic()
                else:
                    is_cyc = G.is_cyclic
            elif hasattr(G, 'generators') and len(G.generators) == 1:
                is_cyc = True
            elif hasattr(G, 'elements') and getattr(G, 'is_abelian', False):
                o = G.order()
                if o != oo:
                    is_cyc = any(g.order() == o for g in G.elements)
            
            if is_cyc:
                if hasattr(G, 'order'):
                    o = G.order()
                    if o == n or (o == oo and n == 0) or (o == 0 and n == oo):
                        h2 = True
                else:
                    h2 = True
    except Exception:
        pass

    # ¬Q: Ext^1(G, A) is not isomorphic to A/nA
    # If G is finite cyclic, Ext^1(G, A) is always isomorphic to A/nA.
    # If G is infinite cyclic (Z), Ext^1(Z, A) = 0, and A/nA = A/0A = A.
    # They are isomorphic if and only if A is trivial.
    neg_q = False
    try:
        is_G_inf = (n == 0 or n == oo or n == 'oo')
        
        is_A_trivial = False
        if isinstance(A, int) and A == 1:
            is_A_trivial = True
        elif isinstance(A, str) and A == '0':
            is_A_trivial = True
        else:
            if hasattr(A, 'order') and A.order() == 1:
                is_A_trivial = True
            elif hasattr(A, 'elements') and len(list(A.elements)) == 1:
                is_A_trivial = True
                
        if is_G_inf:
            if not is_A_trivial:
                neg_q = True
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A is an abelian group",
    "H_2: G is a cyclic group of order n",
    "¬Q: Ext^1(G, A) is not isomorphic to A/nA"
]

N_HYP = 2
NEG_Q_INDEX = 2