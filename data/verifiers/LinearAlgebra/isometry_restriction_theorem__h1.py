import z3
from sympy import eye, zeros

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

# The witness should be a callable that takes a z3.Int 'n' (representing the basis index e_n)
# and returns a tuple (T_n, W_n):
#   - T_n: a z3 expression for the index m such that T(e_n) = e_m
#   - W_n: a z3 boolean expression indicating whether e_n is in the subspace W
# Example for right shift on l^2(Z) with W = l^2(N):
#   lambda n: (n + 1, n >= 0)

def conditions(witness):
    try:
        if not callable(witness):
            return [False, False, False]
            
        n = z3.Int('n')
        m = z3.Int('m')
        n1 = z3.Int('n1')
        n2 = z3.Int('n2')
        
        T_n, W_n = witness(n)
        T_n1, _ = witness(n1)
        T_n2, _ = witness(n2)
        _, W_Tn = witness(T_n)
        _, W_m = witness(m)
        
        # H1: T is an isometry on V (bijective and preserves inner product)
        # Since T maps basis to basis, preserving inner product means T is injective.
        # Isometry on V also requires surjectivity on V.
        solver1 = z3.Solver()
        solver1.set("timeout", 1000)
        solver1.add(n1 != n2)
        solver1.add(T_n1 == T_n2)
        is_injective = (solver1.check() == z3.unsat)
        
        solver2 = z3.Solver()
        solver2.set("timeout", 1000)
        solver2.add(z3.ForAll([n], T_n != m))
        is_surjective = (solver2.check() == z3.unsat)
        
        h1 = is_injective and is_surjective
        
        # H2: W is a subspace of V that is invariant under T
        solver3 = z3.Solver()
        solver3.set("timeout", 1000)
        solver3.add(W_n)
        solver3.add(z3.Not(W_Tn))
        h2 = (solver3.check() == z3.unsat)
        
        # neg_Q: The restriction operator T|_W is NOT an isometry on W
        # Since T preserves inner product, T|_W preserves inner product.
        # Thus, T|_W fails to be an isometry iff it is NOT surjective on W.
        solver4 = z3.Solver()
        solver4.set("timeout", 1000)
        solver4.add(W_m)
        solver4.add(z3.ForAll([n], z3.Implies(W_n, T_n != m)))
        neg_q = (solver4.check() == z3.sat)
        
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: T is an isometry on V",
    "H_2: W is a subspace of V that is invariant under T",
    "¬Q: The restriction operator T|_W is not an isometry on W"
]

N_HYP = 2
NEG_Q_INDEX = 2