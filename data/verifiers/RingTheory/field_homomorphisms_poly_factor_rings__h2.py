import sympy
import sympy.combinatorics.named_groups
import sympy.matrices

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

CONDITION_LABELS = ["H_1: F and K are fields such that F is a subfield of K", "¬Q: The number of homomorphisms is not equal to the number of roots"]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                F, K, f = witness
            elif len(witness) == 2:
                F, f = witness
            else:
                f = witness[0]
        else:
            f = witness
            
        h1 = True
        
        if hasattr(f, 'is_zero') and f.is_zero:
            neg_q = True
        elif f == 0:
            neg_q = True
        else:
            neg_q = False
            
        return [h1, neg_q]
    except Exception:
        return [False, False]