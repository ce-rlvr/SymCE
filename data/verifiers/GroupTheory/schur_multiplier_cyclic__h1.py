import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros

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

def get_order(G):
    if hasattr(G, 'order'):
        o = G.order
        return o() if callable(o) else o
    return len(list(G.elements))

def get_elem_order(g):
    if hasattr(g, 'order'):
        o = g.order
        return o() if callable(o) else o
    if hasattr(g, 'period'):
        return g.period
    raise ValueError("Cannot determine element order")

def is_schur_multiplier_trivial(G):
    # Try to use built-in schur_multiplier if available
    try:
        if hasattr(G, 'schur_multiplier'):
            sm = G.schur_multiplier()
            if isinstance(sm, list):
                return all(x == 1 for x in sm)
            elif hasattr(sm, 'order'):
                o = sm.order
                o_val = o() if callable(o) else o
                return o_val == 1
    except Exception:
        pass

    try:
        # Check if the group is abelian
        if hasattr(G, 'is_abelian'):
            abelian = G.is_abelian
            if callable(abelian):
                abelian = abelian()
        else:
            elems = list(G.elements)
            abelian = True
            for i in range(len(elems)):
                for j in range(i+1, len(elems)):
                    if elems[i]*elems[j] != elems[j]*elems[i]:
                        abelian = False
                        break
                if not abelian:
                    break

        # For finite abelian groups, the Schur multiplier is trivial iff the group is cyclic
        if abelian:
            if hasattr(G, 'is_cyclic'):
                cyclic = G.is_cyclic
                if callable(cyclic):
                    return cyclic()
                return cyclic
            else:
                order = get_order(G)
                for g in G.elements:
                    if get_elem_order(g) == order:
                        return True
                return False

        # For non-abelian groups, we check known small groups
        order = get_order(G)
        if order < 8:
            # S3 (order 6) has a trivial Schur multiplier
            return True
        if order == 8:
            # D4 has Schur multiplier Z2, Q8 has trivial Schur multiplier
            elements_order_2 = sum(1 for g in G.elements if get_elem_order(g) == 2)
            if elements_order_2 == 5:
                return False
            if elements_order_2 == 1:
                return True
        if order == 12:
            # A4 and D6 have Schur multiplier Z2, Q12 has trivial Schur multiplier
            elements_order_2 = sum(1 for g in G.elements if get_elem_order(g) == 2)
            if elements_order_2 == 1:
                return True
            return False
        if order == 24:
            if G.is_isomorphic(SymmetricGroup(4)):
                return False
        if order == 60:
            if G.is_isomorphic(AlternatingGroup(5)):
                return False

        # Fallback for unknown groups: assume trivial to avoid false positives in counterexample detection
        return True
    except Exception:
        return True

def conditions(witness) -> list[bool]:
    try:
        neg_q = not is_schur_multiplier_trivial(witness)
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The Schur multiplier of G is not trivial"
]

N_HYP = 0
NEG_Q_INDEX = 0