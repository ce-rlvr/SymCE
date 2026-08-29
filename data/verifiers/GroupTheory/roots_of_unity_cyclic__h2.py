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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            n = witness.get('n')
            U_n = witness.get('U_n')
        else:
            n, U_n = witness
    except Exception:
        return [False, False]

    try:
        h1 = isinstance(n, int) and n > 0
    except Exception:
        h1 = False

    try:
        from sympy import sympify, simplify
        
        def check_Q(n, U_n):
            try:
                if not isinstance(n, int) or n <= 0:
                    return False
                if U_n is None:
                    return False
                
                U_n_tuple = tuple(U_n)
                if len(U_n_tuple) != n:
                    return False
                
                elements = [sympify(e) for e in U_n_tuple]
                
                # Check if all elements are numbers (complex numbers)
                for e in elements:
                    if not e.is_number:
                        return False
                        
                # Check that 0 is not in the set
                for e in elements:
                    if simplify(e) == 0 or e.is_zero:
                        return False
                        
                # Check that all elements are distinct
                for i in range(len(elements)):
                    for j in range(i + 1, len(elements)):
                        diff = simplify(elements[i] - elements[j])
                        if diff == 0 or diff.is_zero:
                            return False
                            
                # Check closure under multiplication
                for a in elements:
                    for b in elements:
                        prod = simplify(a * b)
                        found = False
                        for e in elements:
                            diff = simplify(prod - e)
                            if diff == 0 or diff.is_zero:
                                found = True
                                break
                        if not found:
                            return False
                            
                # A finite subset of C \ {0} closed under multiplication is a group.
                # Any finite subgroup of the multiplicative group of a field is cyclic.
                return True
            except Exception:
                return False

        q = check_Q(n, U_n)
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "¬Q: U_n does not form a cyclic group of order n under complex multiplication"
]

N_HYP = 1
NEG_Q_INDEX = 1