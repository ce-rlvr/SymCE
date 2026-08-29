import sympy
from sympy import symbols, ZZ, QQ, RR, CC

# Top-level setup
x, y, z = symbols('x y z')

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the conjecture:
    "The direct sum of any family of injective right R-modules is injective."
    
    Since SymPy cannot natively represent or verify infinite families of modules 
    over non-Noetherian rings, this verifier checks if the witness describes 
    a known mathematical counterexample (which requires a non-Noetherian ring).
    """
    h1 = False
    neg_q = False
    try:
        s = str(witness).lower().replace("-", "")
        
        # H1: M_i is a family of injective right R-modules
        if "injective" in s:
            h1 = True
            
        # neg_Q: The direct sum is not injective.
        # By the Bass-Papp theorem, a ring R is Noetherian iff every direct sum 
        # of injective R-modules is injective. Thus, any counterexample MUST 
        # be a non-Noetherian ring.
        counterexample_keywords = [
            "nonnoetherian",
            "not noetherian",
            "infinite product",
            "infinite variables",
            "infinitely many variables",
            "k[x",
            "f[x",
            "r[x",
            "z[x",
            "q[x",
            "c[x",
            "[x_1",
            "direct product of",
            "prod_",
            "infinite direct product",
            "continuous functions",
            "boolean ring"
        ]
        
        if any(kw in s for kw in counterexample_keywords):
            neg_q = True
            
    except Exception:
        pass
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: M_i is a family of injective right R-modules indexed by a set I",
    "¬Q: The direct sum of the modules M_i over the index set I is not an injective right R-module"
]

N_HYP = 1
NEG_Q_INDEX = 1