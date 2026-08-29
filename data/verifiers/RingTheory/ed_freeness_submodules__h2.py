import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, CyclicGroup, AlternatingGroup, DihedralGroup
from sympy import eye, zeros, ZZ, QQ, Symbol

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: R is a Euclidean domain",
    "H_2: M is a submodule of F",
    "¬Q: M is not a free R-module of rank k <= n"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if isinstance(witness, dict):
            R = witness.get("R")
            F = witness.get("F")
            M = witness.get("M")
            n = witness.get("n")
        else:
            R, F, M, n = witness
            
        # H1: R is a Euclidean domain
        h1 = False
        try:
            if R == ZZ:
                h1 = True
            elif str(R) in ["Z", "ZZ", "Q[x]", "R[x]", "C[x]", "QQ[x]", "RR[x]", "CC[x]"]:
                h1 = True
        except Exception:
            pass
            
        # H2: M is a submodule of F
        h2 = False
        try:
            if M == F:
                h2 = True
            elif hasattr(M, 'is_subgroup') and hasattr(F, 'is_subgroup'):
                if M.is_subgroup(F):
                    h2 = True
            elif isinstance(F, list) and isinstance(M, list):
                if M == F:
                    h2 = True
        except Exception:
            pass
            
        # neg_Q: M is NOT a free R-module of rank k <= n
        neg_q = False
        try:
            if R == ZZ or str(R) in ["Z", "ZZ"]:
                if hasattr(M, 'order'):
                    ord_M = M.order()
                    if ord_M > 1 and ord_M != float('inf'):
                        neg_q = True
                elif isinstance(M, list):
                    # If represented as a list of invariants, any non-zero invariant means torsion
                    if any(inv != 0 for inv in M):
                        neg_q = True
                    else:
                        # If it is free, check if rank > n
                        if n is not None and len(M) > n:
                            neg_q = True
                elif isinstance(M, int):
                    if M > 1:
                        neg_q = True
            elif "x" in str(R):
                # For polynomial rings, a finite dimensional vector space (matrix) is a torsion module
                if hasattr(M, 'is_Matrix') and M.is_Matrix:
                    neg_q = True
        except Exception:
            pass
            
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]