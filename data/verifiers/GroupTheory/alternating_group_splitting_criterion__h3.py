import sympy
from sympy.combinatorics import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup for witness expressions
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
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple: (n, x, K)
    """
    try:
        if len(witness) == 3:
            n, x, K = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: n is an integer strictly greater than 1
    try:
        h1_ok = isinstance(n, int) and n > 1
    except Exception:
        h1_ok = False

    # H_2: x is an element of the alternating group A_n
    try:
        h2_ok = isinstance(x, Permutation) and x.is_even and x.size <= n
    except Exception:
        h2_ok = False

    # ¬Q: The conclusion FAILS at the witness.
    # Conclusion: K splits into exactly two distinct conjugacy classes in A_n 
    # iff the centralizer of x in S_n is contained in A_n.
    try:
        if not (h1_ok and h2_ok) or n > 8:
            # If hypotheses fail or n is too large (to prevent TLE), we cannot properly evaluate
            neg_q_ok = False
        else:
            # Evaluate P: K splits into exactly two distinct conjugacy classes in A_n
            An = AlternatingGroup(n)
            An_elements = list(An.generate())
            An_classes = []
            unseen = set(An_elements)
            while unseen:
                rep = unseen.pop()
                cclass = set()
                for g in An_elements:
                    cclass.add(g * rep * ~g)
                An_classes.append(cclass)
                unseen -= cclass
                
            try:
                K_set = set(K)
            except Exception:
                K_set = None
                
            if K_set is not None:
                count = 0
                union_classes = set()
                for c in An_classes:
                    if c.issubset(K_set):
                        count += 1
                        union_classes |= c
                P = (count == 2 and union_classes == K_set)
            else:
                P = False
                
            # Evaluate Q: the centralizer of x in S_n is contained in A_n
            # This is true iff the cycle type of x in S_n consists of distinct odd integers.
            lengths = [len(c) for c in x.cyclic_form]
            lengths += [1] * (n - sum(lengths))
            
            Q = True
            if any(l % 2 == 0 for l in lengths):
                Q = False
            elif len(set(lengths)) != len(lengths):
                Q = False
                
            # The conclusion is P == Q. We want its negation.
            neg_q_ok = (P != Q)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: n is an integer strictly greater than 1",
    "H_2: x is an element of the alternating group A_n",
    "¬Q: The equivalence between K splitting into exactly two distinct conjugacy classes in A_n and the centralizer of x in S_n being contained in A_n fails"
]

N_HYP = 2
NEG_Q_INDEX = 2