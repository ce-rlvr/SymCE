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
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

ZZ = sympy.ZZ
QQ = sympy.QQ

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The conjecture drops the hypothesis that S is a multiplicative set.
    If S is not a multiplicative set, the localization S^{-1}M is undefined,
    hence it is not a finitely generated S^{-1}R-module.
    """
    try:
        if isinstance(witness, dict):
            R = witness.get('R', None)
            M = witness.get('M', None)
            S = witness.get('S', None)
        elif isinstance(witness, (list, tuple)) and len(witness) == 3:
            R, M, S = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    # H_1: R is a commutative ring with identity
    try:
        if R in [ZZ, QQ]:
            h1 = True
        elif hasattr(R, 'is_commutative'):
            h1 = bool(R.is_commutative)
        else:
            h1 = False
    except Exception:
        h1 = False
        
    # H_2: M is a finitely generated R-module
    try:
        if isinstance(M, (list, tuple, set)):
            h2 = True
        elif hasattr(M, '__iter__') and not isinstance(M, str):
            M_list = []
            iterator = iter(M)
            for _ in range(101):
                try:
                    M_list.append(next(iterator))
                except StopIteration:
                    break
            h2 = len(M_list) <= 100
        else:
            h2 = False
    except Exception:
        h2 = False
        
    # ¬Q: S^{-1}M is NOT a finitely generated S^{-1}R-module
    # This occurs when S is not a valid multiplicative set (e.g., not closed under multiplication or missing 1).
    try:
        if hasattr(S, '__iter__') and not isinstance(S, str):
            S_list = []
            iterator = iter(S)
            for _ in range(101):
                try:
                    S_list.append(next(iterator))
                except StopIteration:
                    break
            
            if len(S_list) <= 100:
                is_mult = True
                if not any(s == 1 for s in S_list):
                    is_mult = False
                else:
                    for a in S_list:
                        for b in S_list:
                            if (a * b) not in S_list:
                                is_mult = False
                                break
                        if not is_mult:
                            break
                neg_q = not is_mult
            else:
                neg_q = False
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: M is a finitely generated R-module",
    "¬Q: The localized module S^{-1}M is NOT a finitely generated S^{-1}R-module (e.g., S is not a multiplicative set)"
]

N_HYP = 2
NEG_Q_INDEX = 2