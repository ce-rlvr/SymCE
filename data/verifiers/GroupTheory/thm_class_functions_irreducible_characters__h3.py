import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
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

def conditions(witness) -> list[bool]:
    try:
        G, f = witness
    except Exception:
        return [False, False, False]
    
    def eval_f(func, x):
        if isinstance(func, dict):
            return func[x]
        return func(x)

    # H_1: G is a finite group
    try:
        h1 = False
        if hasattr(G, 'elements') and hasattr(G, 'is_group') and G.is_group:
            elements = list(G.elements)
            if len(elements) > 0:
                h1 = True
    except Exception:
        h1 = False

    # H_2: f: G -> C is a function
    try:
        h2 = False
        if h1:
            if callable(f) or isinstance(f, dict):
                all_valid = True
                for g in elements:
                    try:
                        val = eval_f(f, g)
                        # Check if the value can be interpreted as a complex number
                        complex(val)
                    except Exception:
                        all_valid = False
                        break
                h2 = all_valid
    except Exception:
        h2 = False

    # ¬Q: f is constant on each conjugacy class iff f is a linear combination of Irr(G) over C
    try:
        if not h1 or not h2:
            neg_q = False
        else:
            # Part A: f is constant on each conjugacy class
            part_a = True
            for g in elements:
                val = eval_f(f, g)
                for h in elements:
                    conj = (~h) * g * h
                    if eval_f(f, conj) != val:
                        part_a = False
                        break
                if not part_a:
                    break
            
            # Part B: f is a linear combination of the characters in Irr(G) over C
            # Mathematically, the irreducible characters of G over C form a basis 
            # for the space of class functions. Thus, any function f: G -> C is a 
            # linear combination of Irr(G) if and only if it is a class function.
            part_b = part_a
            
            q = (part_a == part_b)
            neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: f: G -> C is a function",
    "¬Q: f is constant on conjugacy classes XOR f is a linear combination of Irr(G)"
]

N_HYP = 2
NEG_Q_INDEX = 2