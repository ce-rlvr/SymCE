import sympy
from sympy import S
import math
import itertools
import functools

# Top-level setup
Reals = S.Reals

def conditions(witness):
    """
    Checks if the witness is a valid counterexample.
    
    PREFERRED WITNESS FORMAT (Finite Topological Spaces):
    witness = {
        'X': [1, 2],
        'tau_X': [[], [1, 2]],
        'Y': [1, 2],
        'tau_Y': [[], [1], [2], [1, 2]],
        'A': [1, 2],
        'f': {1: 1, 2: 2}
    }
    """
    if not isinstance(witness, dict):
        return [False, False, False]

    # Attempt 1: Finite Topology
    if 'tau_X' in witness and 'tau_Y' in witness:
        try:
            X = frozenset(witness.get('X', []))
            tau_X = {frozenset(u) for u in witness.get('tau_X', [])}
            Y = frozenset(witness.get('Y', []))
            tau_Y = {frozenset(u) for u in witness.get('tau_Y', [])}
            A = frozenset(witness.get('A', []))
            
            f_raw = witness.get('f', {})
            if isinstance(f_raw, list):
                try:
                    f = dict(f_raw)
                except Exception:
                    f = f_raw
            else:
                f = f_raw

            def is_topology(pts, tau):
                if frozenset() not in tau: return False
                if pts not in tau: return False
                for u in tau:
                    if not u.issubset(pts): return False
                    for v in tau:
                        if u.union(v) not in tau: return False
                        if u.intersection(v) not in tau: return False
                return True

            def is_connected(S_set, tau):
                if not S_set: return True
                sub_tau = {u.intersection(S_set) for u in tau}
                for u in sub_tau:
                    if not u: continue
                    for v in sub_tau:
                        if not v: continue
                        if u.union(v) == S_set and not u.intersection(v):
                            return False
                return True

            h1_ok = is_topology(X, tau_X) and is_topology(Y, tau_Y)
            h2_ok = A.issubset(X) and is_connected(A, tau_X)

            if callable(f):
                fA = frozenset(f(a) for a in A)
                if not fA.issubset(Y):
                    neg_q = False
                else:
                    neg_q = not is_connected(fA, tau_Y)
            elif isinstance(f, dict):
                if not all(a in f for a in A):
                    neg_q = False
                else:
                    fA = frozenset(f[a] for a in A)
                    if not fA.issubset(Y):
                        neg_q = False
                    else:
                        neg_q = not is_connected(fA, tau_Y)
            else:
                neg_q = False

            return [bool(h1_ok), bool(h2_ok), bool(neg_q)]
        except Exception:
            pass

    # Attempt 2: Sympy Sets
    if 'A' in witness and 'f' in witness:
        try:
            A = witness['A']
            f = witness['f']
            
            h1_ok = True
            
            def is_sympy_conn(S_set):
                if getattr(S_set, 'is_Interval', False): return True
                if S_set == sympy.S.Reals: return True
                if isinstance(S_set, sympy.FiniteSet) and len(S_set) <= 1: return True
                if S_set == sympy.EmptySet: return True
                return False
                
            h2_ok = is_sympy_conn(A)
            
            if hasattr(f, 'expr') and hasattr(f, 'variables'):
                img = sympy.imageset(f, A)
                if isinstance(img, sympy.ImageSet):
                    neg_q = False
                else:
                    neg_q = not is_sympy_conn(img)
            else:
                neg_q = False
                
            return [bool(h1_ok), bool(h2_ok), bool(neg_q)]
        except Exception:
            pass

    return [False, False, False]

CONDITION_LABELS = [
    "H_1: X and Y are topological spaces",
    "H_2: A is a connected subset of X",
    "¬Q: The image f(A) is not a connected subset of Y"
]

N_HYP = 2
NEG_Q_INDEX = 2