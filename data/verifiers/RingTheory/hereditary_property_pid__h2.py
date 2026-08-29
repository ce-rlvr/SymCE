import sympy
from sympy.combinatorics import CyclicGroup, SymmetricGroup, AlternatingGroup, DihedralGroup
from sympy.matrices import eye, zeros

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

Z = sympy.ZZ
Q = sympy.QQ

def conditions(witness) -> list[bool]:
    # Parse witness flexibly to accommodate different LLM output formats
    try:
        if isinstance(witness, dict):
            R = witness.get("R", sympy.ZZ)
            M = witness.get("M")
            P = witness.get("P", M)
        elif isinstance(witness, tuple):
            if len(witness) == 3:
                R, P, M = witness
            elif len(witness) == 2:
                R, M = witness
                P = M
            elif len(witness) == 1:
                R = sympy.ZZ
                M = witness[0]
                P = M
            else:
                return [False, False, False]
        else:
            R = sympy.ZZ
            M = witness
            P = witness
            
        if M is None or P is None:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: R is a principal ideal domain
    h1 = False
    try:
        if hasattr(R, 'is_PID') and R.is_PID:
            h1 = True
        elif R in (sympy.S.Integers, sympy.ZZ):
            h1 = True
    except Exception:
        pass

    # H_2: M is a submodule of P
    h2 = False
    try:
        if R in (sympy.S.Integers, sympy.ZZ):
            if M == P:
                if hasattr(P, 'is_abelian') and P.is_abelian:
                    h2 = True
                elif isinstance(P, list) and all(isinstance(x, int) for x in P):
                    h2 = True
            else:
                if hasattr(M, 'generators') and hasattr(P, 'contains'):
                    if getattr(P, 'is_abelian', False) and getattr(M, 'is_abelian', False):
                        if all(P.contains(g) for g in M.generators):
                            h2 = True
                elif isinstance(P, list) and isinstance(M, list):
                    if all(isinstance(x, int) for x in P) and all(isinstance(x, int) for x in M):
                        if all(M.count(k) <= P.count(k) for k in set(M)):
                            h2 = True
    except Exception:
        pass

    # ¬Q: M is not a projective R-module
    neg_q = False
    try:
        if R in (sympy.S.Integers, sympy.ZZ):
            if hasattr(M, 'is_trivial'):
                # For finite groups over Z, projective iff free iff trivial
                neg_q = not M.is_trivial
            elif isinstance(M, list) and all(isinstance(x, int) for x in M):
                # For lists of invariant factors, projective iff free iff no torsion
                if any(n != 0 and abs(n) != 1 for n in M):
                    neg_q = True
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "H_2: M is a submodule of P",
    "¬Q: M is not a projective R-module"
]

N_HYP = 2
NEG_Q_INDEX = 2