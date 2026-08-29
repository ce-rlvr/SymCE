import sympy
from sympy import eye
from sympy.polys.domains import QQ, ZZ, GF
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: The characteristic of F is not equal to 2",
    "¬Q: The center Z(G) does not consist of exactly two elements: I and -I"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if isinstance(witness, dict):
            F = witness.get('F')
            G = witness.get('G')
            n = witness.get('n')
        elif isinstance(witness, tuple) and len(witness) == 2:
            if isinstance(witness[0], int):
                n, F = witness
                G = None
            else:
                F, G = witness
                n = None
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H1: F is a field
    try:
        h1 = bool(F.is_Field)
    except Exception:
        h1 = False

    # H2: The characteristic of F is not equal to 2
    try:
        h2 = bool(F.characteristic() != 2)
    except Exception:
        h2 = False

    # neg_Q: The center Z(G) does not consist of exactly two elements: I and -I
    try:
        if G is not None:
            if hasattr(G, 'generate'):
                gen = G.generate()
            elif hasattr(G, 'elements'):
                gen = G.elements
            else:
                gen = iter(G)
                
            elements = []
            too_large = False
            for i, g in enumerate(gen):
                if i > 5000:
                    too_large = True
                    break
                elements.append(g)
                
            if too_large:
                neg_q = False
            elif not elements:
                neg_q = True
            else:
                first = elements[0]
                if not hasattr(first, 'shape'):
                    neg_q = True
                else:
                    dim = first.shape[0]
                    I = eye(dim)
                    minus_I = -I
                    
                    if hasattr(G, 'generators'):
                        gens = G.generators
                    else:
                        gens = elements
                        
                    char = F.characteristic()
                    
                    def matrix_eq(A, B):
                        if A.shape != B.shape:
                            return False
                        diff = A - B
                        for val in diff:
                            try:
                                v = val.as_expr()
                            except Exception:
                                v = val
                            if char > 0:
                                try:
                                    if int(v) % char != 0:
                                        return False
                                except Exception:
                                    if sympy.sympify(v) % char != 0:
                                        return False
                            else:
                                if sympy.sympify(v) != 0:
                                    return False
                        return True

                    # Find center
                    center = []
                    for g in elements:
                        if all(matrix_eq(g * h, h * g) for h in gens):
                            center.append(g)
                            
                    has_I = any(matrix_eq(c, I) for c in center)
                    has_minus_I = any(matrix_eq(c, minus_I) for c in center)
                    
                    distinct_center = []
                    for c in center:
                        if not any(matrix_eq(c, dc) for dc in distinct_center):
                            distinct_center.append(c)
                            
                    if len(distinct_center) == 2 and has_I and has_minus_I:
                        neg_q = False
                    else:
                        neg_q = True
        elif n is not None:
            # Implicitly G = SL(n, F)
            if F.is_FiniteField:
                roots = []
                for i in range(F.order):
                    elem = F(i)
                    if elem**n == F.one:
                        roots.append(elem)
                has_one = any(r == F.one for r in roots)
                has_minus_one = any(r == -F.one for r in roots)
                if len(roots) == 2 and has_one and has_minus_one:
                    neg_q = False
                else:
                    neg_q = True
            else:
                if n % 2 == 1:
                    neg_q = True
                else:
                    neg_q = False
        else:
            neg_q = True
    except Exception:
        neg_q = True

    return [h1, h2, neg_q]