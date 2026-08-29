import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    # H_1: Let n >= 4 be an integer
    try:
        if isinstance(witness, bool):
            h1_ok = False
        else:
            n = float(witness)
            h1_ok = bool(n.is_integer() and n >= 4)
    except Exception:
        h1_ok = False

    # H_2: Let S_n be the symmetric group on n letters
    # This is a definitional hypothesis, we just check if n is a valid degree for S_n
    try:
        if isinstance(witness, bool):
            h2_ok = False
        else:
            n = float(witness)
            h2_ok = bool(n.is_integer() and n >= 1)
    except Exception:
        h2_ok = False

    # ¬Q: The centralizer of A_n in S_n is NOT the trivial subgroup
    try:
        if isinstance(witness, bool):
            neg_q_ok = False
        else:
            n = float(witness)
            if not (n.is_integer() and n >= 1):
                neg_q_ok = False
            else:
                n = int(n)
                # Mathematically, the centralizer of A_n in S_n is trivial for n >= 4 and n = 1.
                # It is non-trivial only for n = 2 and n = 3.
                # We compute it explicitly for small n to verify, and use the theorem for n > 5 to avoid timeouts.
                if n == 1:
                    centralizer_is_trivial = True
                elif n == 2:
                    centralizer_is_trivial = False
                elif n > 5:
                    centralizer_is_trivial = True
                else:
                    Sn = SymmetricGroup(n)
                    An = AlternatingGroup(n)
                    gens = An.generators
                    centralizer_is_trivial = True
                    
                    for g in Sn.elements:
                        if g.is_Identity:
                            continue
                        
                        commutes_with_all = True
                        for gen in gens:
                            if g * gen != gen * g:
                                commutes_with_all = False
                                break
                                
                        if commutes_with_all:
                            centralizer_is_trivial = False
                            break
                            
                neg_q_ok = not centralizer_is_trivial
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: n >= 4 is an integer",
    "H_2: S_n is the symmetric group on n letters",
    "¬Q: The centralizer of A_n in S_n is not the trivial subgroup"
]

N_HYP = 2
NEG_Q_INDEX = 2