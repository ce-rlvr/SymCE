import sympy
from sympy.combinatorics import Permutation
from sympy.matrices import Matrix

# Top-level setup
S3 = sympy.combinatorics.SymmetricGroup(3)
S4 = sympy.combinatorics.SymmetricGroup(4)
A4 = sympy.combinatorics.AlternatingGroup(4)
D4 = sympy.combinatorics.DihedralGroup(4)
C4 = sympy.combinatorics.CyclicGroup(4)
V4 = sympy.combinatorics.AlternatingGroup(4)
Z2 = sympy.combinatorics.CyclicGroup(2)
Z3 = sympy.combinatorics.CyclicGroup(3)
Z4 = sympy.combinatorics.CyclicGroup(4)
Z6 = sympy.combinatorics.CyclicGroup(6)
trivial = sympy.combinatorics.CyclicGroup(1)

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness) -> list[bool]:
    h1_ok = False
    h2_ok = False
    neg_q_ok = False

    try:
        if hasattr(witness, 'I') and hasattr(witness, 'J'):
            I = witness.I
            J = witness.J
            
            if hasattr(witness, 'is_ideal'):
                h1_ok = bool(witness.is_ideal(I))
                h2_ok = bool(witness.is_ideal(J))
            else:
                h1_ok = True
                h2_ok = True
                
            if hasattr(witness, 'supp'):
                supp_IJ = set(witness.supp(I * J))
                supp_I = set(witness.supp(I))
                supp_J = set(witness.supp(J))
                neg_q_ok = (supp_IJ != supp_I.union(supp_J))
            elif hasattr(I, 'support'):
                supp_IJ = set((I * J).support())
                supp_I = set(I.support())
                supp_J = set(J.support())
                neg_q_ok = (supp_IJ != supp_I.union(supp_J))
                
        elif isinstance(witness, (tuple, list)) and len(witness) == 2:
            I, J = witness
            
            if hasattr(I, 'eigenvals') and hasattr(J, 'eigenvals'):
                h1_ok = I.is_square
                h2_ok = J.is_square
                supp_IJ = set((I * J).eigenvals().keys())
                supp_I = set(I.eigenvals().keys())
                supp_J = set(J.eigenvals().keys())
                neg_q_ok = (supp_IJ != supp_I.union(supp_J))
                
            elif hasattr(I, 'support') and hasattr(J, 'support'):
                h1_ok = True
                h2_ok = True
                supp_IJ = set((I * J).support())
                supp_I = set(I.support())
                supp_J = set(J.support())
                neg_q_ok = (supp_IJ != supp_I.union(supp_J))
                
            elif isinstance(I, int) and isinstance(J, int):
                h1_ok = True
                h2_ok = True
                def supp(n):
                    if n == 0:
                        return {"all"}
                    if n in (1, -1):
                        return set()
                    return set(sympy.primefactors(abs(n)))
                
                supp_IJ = supp(I * J)
                supp_I = supp(I)
                supp_J = supp(J)
                
                if supp_IJ == {"all"}:
                    q_ok = (supp_I == {"all"} or supp_J == {"all"})
                else:
                    q_ok = (supp_IJ == supp_I.union(supp_J))
                neg_q_ok = not q_ok
                
            elif hasattr(I, 'free_symbols') and hasattr(J, 'free_symbols'):
                h1_ok = True
                h2_ok = True
                supp_IJ = (I * J).free_symbols
                supp_I = I.free_symbols
                supp_J = J.free_symbols
                neg_q_ok = (supp_IJ != supp_I.union(supp_J))
                
    except Exception:
        pass

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: I is an ideal of R",
    "H_2: J is an ideal of R",
    "¬Q: Supp(R/(IJ)) != Supp(R/I) U Supp(R/J)"
]

N_HYP = 2
NEG_Q_INDEX = 2