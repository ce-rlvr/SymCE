import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
    def eval_f(f, x):
        if isinstance(f, dict):
            return f.get(x, None)
        return f(x)

    # H_1: A is an abelian group
    try:
        G, A, f = witness
        h1 = bool(A.is_abelian)
    except Exception:
        h1 = False

    # H_2: f: G -> A is a group homomorphism
    try:
        G, A, f = witness
        elements_G = list(G.generate())
        
        h2 = True
        for x in elements_G:
            fx = eval_f(f, x)
            if fx not in A:
                h2 = False
                break
                
        if h2:
            for x in elements_G:
                for y in elements_G:
                    if eval_f(f, x * y) != eval_f(f, x) * eval_f(f, y):
                        h2 = False
                        break
                if not h2:
                    break
    except Exception:
        h2 = False

    # ¬Q: The commutator subgroup is not contained in the kernel of f
    try:
        G, A, f = witness
        elements_G = list(G.generate())
        id_G = elements_G[0]**0
        id_A = eval_f(f, id_G)
        
        C = G.derived_subgroup()
        
        neg_q = False
        for x in C.generate():
            if eval_f(f, x) != id_A:
                neg_q = True
                break
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A is an abelian group",
    "H_2: f is a group homomorphism",
    "¬Q: The commutator subgroup is not contained in the kernel of f"
]

N_HYP = 2
NEG_Q_INDEX = 2