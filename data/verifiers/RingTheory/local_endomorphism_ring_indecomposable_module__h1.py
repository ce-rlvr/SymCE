import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import factorint

# Top-level setup
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
    h1 = False
    h2 = False
    neg_q = False

    try:
        # 1. Duck typing / Dictionary representation
        if isinstance(witness, dict):
            if 'is_indecomposable' in witness:
                h1 = bool(witness['is_indecomposable'])
            if 'has_finite_length' in witness:
                h2 = bool(witness['has_finite_length'])
            if 'endomorphism_ring_is_local' in witness:
                neg_q = not bool(witness['endomorphism_ring_is_local'])
            else:
                neg_q = not h1
            return [h1, h2, neg_q]

        if hasattr(witness, 'is_indecomposable') and hasattr(witness, 'has_finite_length'):
            h1 = bool(witness.is_indecomposable())
            h2 = bool(witness.has_finite_length())
            if hasattr(witness, 'endomorphism_ring_is_local'):
                neg_q = not bool(witness.endomorphism_ring_is_local())
            else:
                neg_q = not h1
            return [h1, h2, neg_q]

        # 2. SymPy Matrix (representing a k[x]-module)
        if isinstance(witness, sympy.Matrix):
            h2 = True
            x = sympy.Symbol('x')
            char_poly = witness.charpoly(x).as_expr()
            try:
                min_poly = witness.minimal_polynomial(x)
                if hasattr(min_poly, 'as_expr'):
                    min_poly = min_poly.as_expr()
            except AttributeError:
                min_poly = char_poly
            
            if sympy.expand(char_poly - min_poly) == 0:
                factors = sympy.factor_list(char_poly)
                if len(factors[1]) == 1:
                    h1 = True
            neg_q = not h1
            return [h1, h2, neg_q]

        # 3. Permutation Group (representing a Z-module / finite abelian group)
        if isinstance(witness, PermutationGroup):
            if witness.is_abelian:
                h2 = True
                order = witness.order()
                if order > 1:
                    factors = factorint(order)
                    if len(factors) == 1 and witness.is_cyclic:
                        h1 = True
                neg_q = not h1
            return [h1, h2, neg_q]

        # 4. Integer (representing Z/nZ as a Z-module)
        if isinstance(witness, (int, sympy.Integer)):
            n = int(witness)
            if n > 1:
                h2 = True
                factors = factorint(n)
                if len(factors) == 1:
                    h1 = True
                neg_q = not h1
            return [h1, h2, neg_q]

    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: M is an indecomposable R-module",
    "H_2: M has finite length as an R-module",
    "¬Q: The endomorphism ring End_R(M) is not a local ring"
]

N_HYP = 2
NEG_Q_INDEX = 2