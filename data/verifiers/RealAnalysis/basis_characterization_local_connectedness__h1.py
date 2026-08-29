import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import S, Interval, FiniteSet, Union, Complement, ImageSet, Set
import math
import itertools
import functools

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
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness):
    neg_q = False
    try:
        # Check if witness has a custom property/method for local connectedness
        if hasattr(witness, 'is_locally_connected'):
            if callable(witness.is_locally_connected):
                neg_q = not witness.is_locally_connected()
            else:
                neg_q = not witness.is_locally_connected
            return [bool(neg_q)]
            
        if hasattr(witness, 'has_connected_basis'):
            if callable(witness.has_connected_basis):
                neg_q = not witness.has_connected_basis()
            else:
                neg_q = not witness.has_connected_basis
            return [bool(neg_q)]

        # Check if witness is a string representing a known counterexample
        if isinstance(witness, str):
            w_lower = witness.lower()
            if w_lower in ["rationals", "q", "s.rationals", "cantor set", "cantor", "topologist's sine curve"]:
                return [True]

        # Check if witness is a tuple (X, tau) representing a finite topological space
        if isinstance(witness, tuple) and len(witness) == 2:
            X, tau = witness
            try:
                X_set = set(X)
                tau_sets = [set(U) for U in tau]
                is_top = True
                if set() not in tau_sets or X_set not in tau_sets:
                    is_top = False
                if is_top:
                    for U in tau_sets:
                        for V in tau_sets:
                            if U.intersection(V) not in tau_sets:
                                is_top = False
                            if U.union(V) not in tau_sets:
                                is_top = False
                if is_top:
                    connected_open_sets = []
                    for U in tau_sets:
                        is_conn = True
                        for V in tau_sets:
                            for W in tau_sets:
                                if V.issubset(U) and W.issubset(U) and V.union(W) == U and V.intersection(W) == set() and V != set() and W != set():
                                    is_conn = False
                                    break
                            if not is_conn: break
                        if is_conn:
                            connected_open_sets.append(U)
                    
                    has_basis = True
                    for U in tau_sets:
                        for x in U:
                            if not any(x in B and B.issubset(U) for B in connected_open_sets):
                                has_basis = False
                                break
                        if not has_basis:
                            break
                    
                    neg_q = not has_basis
                    return [neg_q]
            except Exception:
                pass

        # Check if witness is a sympy Set
        if isinstance(witness, Set):
            if witness == S.Rationals:
                neg_q = True
            elif witness == Complement(S.Reals, S.Rationals):
                neg_q = True
            elif witness in (S.Reals, S.Integers, S.Naturals, S.Naturals0):
                neg_q = False
            elif isinstance(witness, Interval):
                neg_q = False
            elif isinstance(witness, FiniteSet):
                neg_q = False
            elif isinstance(witness, Union):
                if all(isinstance(arg, (Interval, FiniteSet)) for arg in witness.args):
                    neg_q = False
                else:
                    has_zero = any(isinstance(arg, FiniteSet) and 0 in arg for arg in witness.args)
                    has_imageset = any(isinstance(arg, ImageSet) for arg in witness.args)
                    if has_zero and has_imageset:
                        neg_q = True
            return [neg_q]

    except Exception:
        pass

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: X does not have a basis for its topology consisting of connected open sets"
]

N_HYP = 0
NEG_Q_INDEX = 0