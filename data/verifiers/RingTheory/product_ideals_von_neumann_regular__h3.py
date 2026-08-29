import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

CONDITION_LABELS = [
    "H_1: R is a von Neumann regular ring",
    "H_2: I is a two-sided ideal of R",
    "¬Q: IJ != I \\cap J"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if isinstance(witness, dict):
            R = witness.get('R', [])
            I = witness.get('I', [])
            J = witness.get('J', [])
        else:
            R, I, J = witness
    except Exception:
        return [False, False, False]

    def contains(lst, elem):
        return any(elem == x for x in lst)

    # H1: R is a von Neumann regular ring
    h1 = False
    try:
        if R:
            h1 = True
            # Check closure under subtraction and multiplication
            for a in R:
                for b in R:
                    if not contains(R, a - b): h1 = False; break
                    if not contains(R, a * b): h1 = False; break
                if not h1: break
            
            # Check commutativity of addition
            if h1:
                for a in R:
                    for b in R:
                        if a + b != b + a:
                            h1 = False
                            break
                    if not h1: break

            # Check associativity of multiplication
            if h1:
                for a in R:
                    for b in R:
                        for c in R:
                            if (a * b) * c != a * (b * c):
                                h1 = False
                                break
                        if not h1: break
                    if not h1: break

            # Check von Neumann regularity: for all a in R, exists x in R s.t. a*x*a == a
            if h1:
                for a in R:
                    if not any(a * x * a == a for x in R):
                        h1 = False
                        break
    except Exception:
        h1 = False

    # H2: I is a two-sided ideal of R
    h2 = False
    try:
        if I:
            h2 = True
            # I subset of R
            for i in I:
                if not contains(R, i): h2 = False; break
            
            # I closed under subtraction
            if h2:
                for a in I:
                    for b in I:
                        if not contains(I, a - b): h2 = False; break
                    if not h2: break
            
            # I absorbs multiplication from R
            if h2:
                for i in I:
                    for r in R:
                        if not contains(I, i * r): h2 = False; break
                        if not contains(I, r * i): h2 = False; break
                    if not h2: break
    except Exception:
        h2 = False

    # neg_Q: IJ != I \cap J
    neg_q = False
    try:
        I_cap_J = [x for x in I if contains(J, x)]
        
        ij_gens = []
        for i in I:
            for j in J:
                elem = i * j
                if not contains(ij_gens, elem):
                    ij_gens.append(elem)
                    
        IJ = []
        for g in ij_gens:
            IJ.append(g)
            
        if not IJ and R:
            # If IJ is empty, it should be the zero ideal {0}
            for x in R:
                if all(x + y == y for y in R):
                    IJ.append(x)
                    break
                    
        idx = 0
        while idx < len(IJ):
            for g in ij_gens:
                add_val = IJ[idx] + g
                if not contains(IJ, add_val):
                    IJ.append(add_val)
                    if len(IJ) > 1000:
                        raise ValueError("Closure too large")
                sub_val = IJ[idx] - g
                if not contains(IJ, sub_val):
                    IJ.append(sub_val)
                    if len(IJ) > 1000:
                        raise ValueError("Closure too large")
            idx += 1
            
        is_equal = True
        for x in IJ:
            if not contains(I_cap_J, x):
                is_equal = False
                break
        if is_equal:
            for x in I_cap_J:
                if not contains(IJ, x):
                    is_equal = False
                    break
                    
        neg_q = not is_equal
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]