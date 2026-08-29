import sympy
from sympy import Symbol, Poly
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

x = Symbol('x')
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

def conditions(witness):
    # H_1: Let f(x) is x^4 - x - 1 in Q[x]
    h1 = False
    try:
        if isinstance(witness, dict):
            if 'f' in witness:
                f_wit = witness['f']
                if isinstance(f_wit, Poly):
                    f_wit = f_wit.as_expr()
                if f_wit == x**4 - x - 1:
                    h1 = True
            else:
                h1 = True
        elif isinstance(witness, tuple) and len(witness) == 2:
            f_wit = witness[0]
            if isinstance(f_wit, Poly):
                f_wit = f_wit.as_expr()
            if f_wit == x**4 - x - 1:
                h1 = True
        else:
            h1 = True
    except Exception:
        h1 = False

    # neg_Q: The Galois group Gal(E/Q) is not isomorphic to S4
    neg_q = False
    try:
        E_wit = witness
        if isinstance(witness, dict):
            if 'E' in witness:
                E_wit = witness['E']
            elif 'G' in witness:
                E_wit = witness['G']
            elif 'Gal' in witness:
                E_wit = witness['Gal']
        elif isinstance(witness, tuple) and len(witness) == 2:
            E_wit = witness[1]

        if hasattr(E_wit, 'is_isomorphic'):
            neg_q = not E_wit.is_isomorphic(S4)
        elif isinstance(E_wit, list) and len(E_wit) > 0 and isinstance(E_wit[0], Permutation):
            neg_q = not PermutationGroup(E_wit).is_isomorphic(S4)
        elif isinstance(E_wit, sympy.Expr) or isinstance(E_wit, Poly):
            if isinstance(E_wit, Poly):
                E_wit = E_wit.as_expr()
            if E_wit == x**4 - x - 1:
                neg_q = False
            else:
                neg_q = True
        else:
            neg_q = E_wit != S4
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = ['H_1: f(x) is x^4 - x - 1', '¬Q: Gal(E/Q) is not S4']

N_HYP = 1
NEG_Q_INDEX = 1