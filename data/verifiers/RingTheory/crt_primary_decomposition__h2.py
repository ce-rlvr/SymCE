import math
import sympy
from sympy.abc import x, y, z
from sympy.ntheory import primefactors
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup for potential witness expressions
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

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: Associated prime ideals P_i = \\sqrt{Q_i} are pairwise comaximal",
    "¬Q: The quotient ring R/I is NOT isomorphic to the direct product \\prod_{i=1}^n R/Q_i"
]

N_HYP = 2
NEG_Q_INDEX = 2

def extract_int(val):
    if isinstance(val, int):
        return val
    if hasattr(val, 'is_Integer') and val.is_Integer:
        return int(val)
    if isinstance(val, str):
        return int(val)
    raise ValueError

def parse_witness(witness):
    # Handle dictionary format
    if isinstance(witness, dict):
        I = witness.get('I')
        Q_list = witness.get('Q_list', witness.get('Qs', witness.get('Q')))
        if Q_list is None:
            Q_list = [v for k, v in witness.items() if isinstance(k, str) and k.startswith('Q')]
        if I is not None and Q_list is not None:
            if not isinstance(Q_list, (list, tuple)):
                Q_list = [Q_list]
            return extract_int(I), [extract_int(q) for q in Q_list]
            
    # Handle tuple/list format
    if isinstance(witness, (tuple, list)):
        Q_list = None
        I = None
        for item in witness:
            if isinstance(item, (list, tuple)):
                Q_list = item
            elif I is None:
                try:
                    I = extract_int(item)
                except Exception:
                    pass
        if I is not None and Q_list is not None:
            return I, [extract_int(q) for q in Q_list]
            
        # Fallback: assume first integer is I, rest are Q_i
        ints = []
        for item in witness:
            try:
                ints.append(extract_int(item))
            except Exception:
                pass
        if len(ints) >= 2:
            return ints[0], ints[1:]
            
    raise ValueError

def conditions(witness) -> list[bool]:
    try:
        I_val, Q_vals = parse_witness(witness)
    except Exception:
        return [False, False, False]
        
    # H_1: R is a commutative ring
    # We evaluate the witness in the context of the integers ZZ, which is a commutative ring.
    h1 = True
    
    # H_2: Associated prime ideals P_i = \sqrt{Q_i} are pairwise comaximal
    # In ZZ, \sqrt{Q_i} is prime iff Q_i is a prime power (or 0).
    # They are pairwise comaximal iff gcd(Q_i, Q_j) == 1 for all i != j.
    try:
        h2 = True
        for q in Q_vals:
            q_abs = abs(q)
            if q_abs == 0:
                pass # Radical is (0), which is prime
            elif q_abs == 1:
                h2 = False  # (1) is not a prime ideal
                break
            else:
                if len(primefactors(q_abs)) != 1:
                    h2 = False  # Radical is not a prime ideal
                    break
        if h2:
            for i in range(len(Q_vals)):
                for j in range(i + 1, len(Q_vals)):
                    if math.gcd(Q_vals[i], Q_vals[j]) != 1:
                        h2 = False
                        break
    except Exception:
        h2 = False
        
    # ¬Q: The quotient ring R/I is NOT isomorphic to the direct product \prod_{i=1}^n R/Q_i
    # In ZZ, since Q_i are pairwise comaximal, \prod ZZ/Q_i is isomorphic to ZZ/(\prod Q_i).
    # ZZ/I is isomorphic to ZZ/(\prod Q_i) iff |I| == |\prod Q_i|.
    try:
        prod = 1
        for q in Q_vals:
            prod *= q
        neg_q = (abs(I_val) != abs(prod))
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]