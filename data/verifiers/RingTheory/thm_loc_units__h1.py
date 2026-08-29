import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros

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
    The conjecture claims that in any ring R, a/s is a unit in S^{-1}R iff 
    there exists b in R such that ab is in S.
    (This is true for commutative rings, but fails for non-commutative rings 
    where the Ore condition might fail or one-sided inverses don't imply two-sided).
    """
    try:
        R = witness.R
        S = witness.S
        a = witness.a
        s = witness.s
        zero = witness.zero
    except Exception:
        return [False, False, False, False]

    # H1: S is a multiplicatively closed subset of R
    try:
        h1 = True
        for x in S:
            if x not in R:
                h1 = False
                break
            for y in S:
                if (x * y) not in S:
                    h1 = False
                    break
    except Exception:
        h1 = False

    # H2: a is an element of R
    try:
        h2 = a in R
    except Exception:
        h2 = False

    # H3: s is an element of S
    try:
        h3 = s in S
    except Exception:
        h3 = False

    # neg_Q: The fraction a/s is a unit in S^{-1}R iff exists b in R such that ab in S
    try:
        # Check if there exists b in R such that ab in S
        exists_b = False
        for b in R:
            if (a * b) in S:
                exists_b = True
                break
        
        # Check if S^{-1}R is well-defined by verifying the Left Ore condition.
        # If the Ore condition fails, the localization S^{-1}R does not exist,
        # meaning a/s cannot be a unit in it.
        ore_condition = True
        for r in R:
            for s_ in S:
                # Left Ore Condition 1: for all r in R, s_ in S, exists r' in R, s' in S st s' r == r' s_
                found1 = False
                for r_prime in R:
                    for s_prime in S:
                        if s_prime * r == r_prime * s_:
                            found1 = True
                            break
                    if found1: break
                if not found1:
                    ore_condition = False
                    break
                
                # Left Ore Condition 2: if r s_ == 0, then exists s' in S st s' r == 0
                if r * s_ == zero:
                    found2 = False
                    for s_prime in S:
                        if s_prime * r == zero:
                            found2 = True
                            break
                    if not found2:
                        ore_condition = False
                        break
            if not ore_condition:
                break
        
        if ore_condition:
            # For finite rings, if the Ore condition holds, S^{-1}R is a finite ring.
            # In a finite ring, a right inverse implies a two-sided inverse (unit).
            # Thus, exists_b (which gives a right inverse) is equivalent to being a unit.
            is_unit = exists_b
        else:
            # If the Ore condition fails, S^{-1}R is not defined.
            is_unit = False
            
        # The conclusion fails if the equivalence does not hold
        neg_q = (is_unit != exists_b)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: S is a multiplicatively closed subset of R",
    "H_2: a is an element of R",
    "H_3: s is an element of S",
    "¬Q: The equivalence between a/s being a unit and exists b in R with ab in S fails"
]

N_HYP = 3
NEG_Q_INDEX = 3