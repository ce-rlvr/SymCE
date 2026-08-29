import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

# Top-level setup
S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Given a witness (e.g., a tuple (R, S) or just a subset S of ZZ),
    check if it satisfies the remaining hypotheses and falsifies the conclusion.
    The dropped hypothesis is that S is a multiplicatively closed subset.
    """
    try:
        if isinstance(witness, dict):
            R = witness.get('R', sympy.ZZ)
            S = witness.get('S', [])
        elif isinstance(witness, tuple) and len(witness) == 2:
            R, S = witness
        else:
            R = sympy.ZZ
            S = witness
            
        # H_1: R is a commutative ring
        try:
            h1 = getattr(R, 'is_commutative', True)
        except Exception:
            h1 = False
            
        # neg_Q: The canonical map R -> S^-1 R is not an epimorphism in CommRing.
        # This happens when S^-1 R fails to be a valid ring under the standard fraction 
        # construction, which occurs exactly when S is not multiplicatively closed.
        try:
            S_list = list(S)
            is_closed = True
            
            try:
                one = R.one
            except AttributeError:
                one = 1
                
            if one not in S_list:
                is_closed = False
            else:
                for a in S_list:
                    for b in S_list:
                        try:
                            if hasattr(R, 'mul'):
                                prod = R.mul(a, b)
                            else:
                                prod = a * b
                        except Exception:
                            is_closed = False
                            break
                        
                        if prod not in S_list:
                            is_closed = False
                            break
                    if not is_closed:
                        break
            neg_q = not is_closed
        except Exception:
            neg_q = False
            
        return [bool(h1), bool(neg_q)]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "¬Q: The canonical map R -> S^-1 R is not an epimorphism in the category of commutative rings"
]

N_HYP = 1
NEG_Q_INDEX = 1