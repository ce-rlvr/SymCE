import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup, AbelianGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics import PermutationGroup
from sympy import Matrix, eye, zeros, Rational
import math
import itertools
import functools

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
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
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (G, characters) where:
      - G is a PermutationGroup
      - characters is a list of homomorphisms (each can be a dict, a function, or a list of values)
    """
    try:
        G, raw_characters = witness
        if hasattr(G, 'elements'):
            elements = list(G.elements)
        else:
            elements = list(G)
            
        if not isinstance(raw_characters, (list, tuple)):
            return [False, False, False]
            
        # Normalize characters to a list of dictionaries mapping group elements to field values
        characters = []
        for chi in raw_characters:
            if isinstance(chi, dict):
                characters.append(chi)
            elif callable(chi):
                characters.append({g: chi(g) for g in elements})
            elif isinstance(chi, (list, tuple)):
                characters.append({elements[i]: chi[i] for i in range(len(elements))})
            else:
                return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: F is a field (and characters are valid homomorphisms to F^x)
    try:
        h2 = True
        if not characters:
            h2 = False
        else:
            for chi in characters:
                for g in elements:
                    if g not in chi:
                        h2 = False
                        break
                    val = chi[g]
                    # Check if value belongs to a field (numbers or SymPy expressions)
                    if not isinstance(val, (int, float, complex, sympy.Expr)):
                        h2 = False
                        break
                    # Homomorphisms to F^x cannot map to 0
                    if val == 0:
                        h2 = False
                        break
                    # Check homomorphism property: chi(g*h) = chi(g)*chi(h)
                    for h in elements:
                        if g*h not in chi:
                            h2 = False
                            break
                        val_gh = chi[g*h]
                        val_h = chi[h]
                        if val_gh != val * val_h:
                            diff = val_gh - val * val_h
                            if isinstance(diff, sympy.Expr):
                                if sympy.simplify(diff) != 0:
                                    h2 = False
                                    break
                            else:
                                h2 = False
                                break
                    if not h2: break
                if not h2: break
    except Exception:
        h2 = False

    # neg_Q: The homomorphisms are linearly dependent over F
    try:
        matrix_rows = []
        for chi in characters:
            row = [chi[g] for g in elements]
            matrix_rows.append(row)
        
        # A matrix where rows are characters and columns are group elements.
        # The characters are linearly dependent iff the rank is less than the number of characters.
        M = Matrix(matrix_rows)
        neg_q = M.rank() < len(characters)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: F is a field",
    "¬Q: The homomorphisms are linearly dependent over F"
]

N_HYP = 2
NEG_Q_INDEX = 2