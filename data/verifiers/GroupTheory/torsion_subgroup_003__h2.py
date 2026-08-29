import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Standard group theory objects
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)  # Isomorphic to the Klein four-group
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

# Standard linear algebra objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def has_finite_order(g):
    """Check if an element has finite order."""
    from sympy import oo
    try:
        if hasattr(g, 'order'):
            o = g.order()
            return o != oo and o > 0
    except Exception:
        pass
    try:
        if hasattr(g, 'is_Matrix') and g.is_Matrix:
            if g.shape[0] != g.shape[1]:
                return False
            I = g.eye(g.rows)
            p = g
            for _ in range(100):
                if p == I:
                    return True
                p = p * g
            return False
    except Exception:
        pass
    return False

def order_is_infinite(g):
    """Check if an element has infinite order."""
    from sympy import oo
    try:
        if hasattr(g, 'order'):
            o = g.order()
            return o == oo
    except Exception:
        pass
    try:
        if hasattr(g, 'is_Matrix') and g.is_Matrix:
            if g.shape[0] != g.shape[1]:
                return False
            I = g.eye(g.rows)
            p = g
            for _ in range(100):
                if p == I:
                    return False
                p = p * g
            return True
    except Exception:
        pass
    return False

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    The witness can be a group G, a tuple (G, a, b) where a and b are torsion elements 
    whose product has infinite order, or a custom mock object.
    """
    if isinstance(witness, tuple) and len(witness) > 0:
        G = witness[0]
    else:
        G = witness

    # H_1: Let G be an abelian group
    h1_ok = False
    try:
        if hasattr(G, 'is_abelian'):
            val = G.is_abelian() if callable(G.is_abelian) else G.is_abelian
            h1_ok = bool(val)
        elif hasattr(G, 'is_commutative'):
            val = G.is_commutative() if callable(G.is_commutative) else G.is_commutative
            h1_ok = bool(val)
        elif hasattr(G, 'generators'):
            gens = list(G.generators)
            h1_ok = True
            for i in range(len(gens)):
                for j in range(i+1, len(gens)):
                    if gens[i] * gens[j] != gens[j] * gens[i]:
                        h1_ok = False
                        break
                if not h1_ok:
                    break
        elif isinstance(G, (list, tuple, set)):
            elements = list(G)
            h1_ok = True
            for i in range(len(elements)):
                for j in range(i+1, len(elements)):
                    if elements[i] * elements[j] != elements[j] * elements[i]:
                        h1_ok = False
                        break
                if not h1_ok:
                    break
    except Exception:
        h1_ok = False

    # ¬Q: T is not a subgroup of G
    # T is the set of torsion elements (elements of finite order).
    # T is a subgroup iff it is closed under the group operation.
    neg_q = False
    try:
        if hasattr(witness, 'T_is_subgroup'):
            val = witness.T_is_subgroup() if callable(witness.T_is_subgroup) else witness.T_is_subgroup
            neg_q = not bool(val)
        elif hasattr(G, 'T_is_subgroup'):
            val = G.T_is_subgroup() if callable(G.T_is_subgroup) else G.T_is_subgroup
            neg_q = not bool(val)
        elif isinstance(witness, tuple) and len(witness) >= 3:
            a = witness[1]
            b = witness[2]
            if has_finite_order(a) and has_finite_order(b) and order_is_infinite(a * b):
                neg_q = True
        elif hasattr(G, 'generators'):
            gens = list(G.generators)
            for a in gens:
                for b in gens:
                    if has_finite_order(a) and has_finite_order(b) and order_is_infinite(a * b):
                        neg_q = True
                        break
                if neg_q:
                    break
        elif isinstance(G, (list, tuple, set)):
            elements = list(G)
            for a in elements:
                for b in elements:
                    if has_finite_order(a) and has_finite_order(b) and order_is_infinite(a * b):
                        neg_q = True
                        break
                if neg_q:
                    break
    except Exception:
        pass

    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: G is an abelian group",
    "¬Q: T is not a subgroup of G"
]

N_HYP = 1
NEG_Q_INDEX = 1