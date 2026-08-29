import sympy
from sympy import eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import math
import itertools
import functools

# Top-level setup
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

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample.
    Expected witness formats:
      - (n, R, I) where n is an integer modulo, R and I are lists of integers.
      - (R, I) where R and I are lists of elements supporting +, -, *, == (e.g., SymPy matrices).
      - Object with attributes R, I, and optionally n.
    """
    h1_ok = False
    neg_q_ok = False
    
    try:
        # Unpack witness for H1
        n = None
        if isinstance(witness, tuple) and len(witness) == 3 and isinstance(witness[0], int):
            n, R_in, I_in = witness
            R = list(set(x % n for x in R_in))
            I = list(set(x % n for x in I_in))
            def add(a, b): return (a + b) % n
            def mul(a, b): return (a * b) % n
            def neg(a): return (-a) % n
            def eq(a, b): return (a - b) % n == 0
        elif isinstance(witness, tuple) and len(witness) == 2:
            R_in, I_in = witness
            R = list(R_in)
            I = list(I_in)
            def add(a, b): return a + b
            def mul(a, b): return a * b
            def neg(a): return -a
            def eq(a, b): return a == b
        elif hasattr(witness, 'R') and hasattr(witness, 'I'):
            R = list(witness.R)
            I = list(witness.I)
            if hasattr(witness, 'n') and isinstance(witness.n, int):
                n = witness.n
                R = list(set(x % n for x in R))
                I = list(set(x % n for x in I))
                def add(a, b): return (a + b) % n
                def mul(a, b): return (a * b) % n
                def neg(a): return (-a) % n
                def eq(a, b): return (a - b) % n == 0
            else:
                def add(a, b): return a + b
                def mul(a, b): return a * b
                def neg(a): return -a
                def eq(a, b): return a == b
        else:
            raise ValueError("Unrecognized witness format")

        h1_ok = True
        if not R or not I:
            h1_ok = False
            
        if h1_ok:
            # Check R is a ring (closed under +, -, *)
            for a in R:
                if not any(eq(neg(a), b) for b in R): h1_ok = False
                for b in R:
                    if not any(eq(add(a, b), c) for c in R): h1_ok = False
                    if not any(eq(mul(a, b), c) for c in R): h1_ok = False
                    
        if h1_ok:
            # Check commutativity of addition
            for a in R:
                for b in R:
                    if not eq(add(a, b), add(b, a)): h1_ok = False

        if h1_ok:
            # Check I is subset of R
            for i in I:
                if not any(eq(i, a) for a in R): h1_ok = False
                
        if h1_ok:
            # Check I is an ideal
            for i in I:
                if not any(eq(neg(i), j) for j in I): h1_ok = False
                for j in I:
                    if not any(eq(add(i, j), k) for k in I): h1_ok = False
                for r in R:
                    if not any(eq(mul(i, r), k) for k in I): h1_ok = False
                    if not any(eq(mul(r, i), k) for k in I): h1_ok = False
                    
    except Exception:
        h1_ok = False

    try:
        # Re-unpack for neg_Q to ensure independence
        n = None
        if isinstance(witness, tuple) and len(witness) == 3 and isinstance(witness[0], int):
            n, R_in, I_in = witness
            R = list(set(x % n for x in R_in))
            I = list(set(x % n for x in I_in))
            def mul(a, b): return (a * b) % n
            def eq(a, b): return (a - b) % n == 0
        elif isinstance(witness, tuple) and len(witness) == 2:
            R_in, I_in = witness
            R = list(R_in)
            I = list(I_in)
            def mul(a, b): return a * b
            def eq(a, b): return a == b
        elif hasattr(witness, 'R') and hasattr(witness, 'I'):
            R = list(witness.R)
            I = list(witness.I)
            if hasattr(witness, 'n') and isinstance(witness.n, int):
                n = witness.n
                R = list(set(x % n for x in R))
                I = list(set(x % n for x in I))
                def mul(a, b): return (a * b) % n
                def eq(a, b): return (a - b) % n == 0
            else:
                def mul(a, b): return a * b
                def eq(a, b): return a == b
        else:
            raise ValueError("Unrecognized witness format")

        # Ann(R/I) = { r in R | r * s in I for all s in R }
        ann = []
        for r in R:
            is_in_ann = True
            for s in R:
                rs = mul(r, s)
                if not any(eq(rs, i) for i in I):
                    is_in_ann = False
                    break
            if is_in_ann:
                ann.append(r)
                
        # Check if Ann(R/I) == I
        ann_subset_I = all(any(eq(a, i) for i in I) for a in ann)
        I_subset_ann = all(any(eq(i, a) for a in ann) for i in I)
        
        neg_q_ok = not (ann_subset_I and I_subset_ann)
        
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: I is an ideal of R",
    "¬Q: Ann(R/I) != I"
]

N_HYP = 1
NEG_Q_INDEX = 1