import sympy
from sympy import *

# Top-level setup for potential witness objects
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
    Check if the witness is a counterexample to the conjecture:
    "If R is a right Artinian ring, then the formal power series ring R[[x]] is not right Artinian."
    
    The only ring R for which R[[x]] is right Artinian is the zero ring.
    """
    h1 = False
    neg_q = False
    
    try:
        if isinstance(witness, str):
            s = witness.lower().strip()
            if s in ["z/1z", "z_1", "zero ring", "zero", "trivial ring", "{0}", "z/1", "0"]:
                h1 = True
                neg_q = True
            elif s in ["z", "zz", "q[x]", "z[x]", "r[x]", "c[x]"]:
                h1 = False
                neg_q = False
            elif "z/" in s or "f_" in s or "gf" in s or s in ["q", "r", "c"]:
                h1 = True
                neg_q = False
            else:
                h1 = False
                neg_q = False
        elif witness == sympy.QQ or witness == sympy.RR or witness == sympy.CC:
            h1 = True
            neg_q = False
        elif witness == sympy.ZZ:
            h1 = False
            neg_q = False
        elif hasattr(witness, "shape") and len(witness.shape) == 2:
            if witness.shape[0] == 0 or witness.shape[1] == 0:
                h1 = True
                neg_q = True
            else:
                h1 = False
                neg_q = False
        elif isinstance(witness, (list, tuple, set)):
            if list(witness) == [0] or list(witness) == []:
                h1 = True
                neg_q = True
            else:
                h1 = False
                neg_q = False
        else:
            # Interpret integer n as the ring Z/nZ
            n = abs(int(witness))
            if n == 1:
                h1 = True
                neg_q = True
            elif n == 0:
                # n = 0 corresponds to Z/0Z = Z, which is not Artinian
                h1 = False
                neg_q = False
            else:
                # n > 1 corresponds to Z/nZ, which is Artinian but its power series ring is not
                h1 = True
                neg_q = False
    except Exception:
        pass
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a right Artinian ring",
    "not Q: The formal power series ring R is right Artinian"
]

N_HYP = 1
NEG_Q_INDEX = 1