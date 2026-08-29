import sympy
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

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

x0, x1, x2, x3, x4, x5, x6, x7, x8, x9 = sympy.symbols('x0:10')

def conditions(witness) -> list[bool]:
    try:
        sigma, Delta = witness
    except Exception:
        return [False, False]
        
    try:
        h1 = isinstance(sigma, Permutation) and isinstance(Delta, sympy.Expr)
    except Exception:
        h1 = False
        
    try:
        n = sigma.size
        xs = [sympy.Symbol(f'x{i}') for i in range(n)]
        sub_dict = {xs[i]: xs[sigma(i)] for i in range(n)}
        acted_Delta = Delta.subs(sub_dict, simultaneous=True)
        
        sgn = 1 if sigma.is_even else -1
        
        diff = sympy.expand(acted_Delta - sgn * Delta)
        neg_q = bool(diff != 0)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: sigma is a permutation and Delta is an expression",
    "¬Q: The action of sigma on Delta does NOT yield sgn(sigma)*Delta"
]

N_HYP = 1
NEG_Q_INDEX = 1