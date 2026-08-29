import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import Matrix
from itertools import combinations

# Top-level setup: named object bindings for witness expressions
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

def conditions(witness):
    """
    Checks if the witness is a counterexample to the false conjecture.
    The witness should be a tuple (G, n, R) where:
      - G is a sympy PermutationGroup
      - n is the number of generators of the presentation (integer >= 0)
      - R is a list of relations, where each relation is a list of non-zero integers
        representing generators (1 to n) and their inverses (-1 to -n).
    """
    try:
        G, n, R = witness
    except Exception:
        return [False, False]
        
    # H_1: Let G^{ab} = G / [G,G] be the abelianization of G.
    # This is a definitional hypothesis, so it always holds for any valid witness.
    h1 = True
    
    try:
        if not isinstance(n, int) or n < 0:
            return [False, False]
            
        # Compute the abelian invariants of the presentation < X | R >
        if n == 0:
            P_inv = []
        else:
            M = []
            for rel in R:
                row = [0] * n
                for symbol in rel:
                    if symbol == 0:
                        return [False, False]
                    if symbol > 0:
                        if symbol > n: return [False, False]
                        row[symbol - 1] += 1
                    elif symbol < 0:
                        if -symbol > n: return [False, False]
                        row[-symbol - 1] -= 1
                M.append(row)
            
            m = len(M)
            if n > 8 or m > 8:
                # Prevent timeout for large matrices
                return [False, False]
                
            mat = Matrix(M)
            
            D = [1] * (n + 1)
            for k in range(1, n + 1):
                if k > m:
                    D[k] = 0
                    continue
                    
                minors_gcd = 0
                for rows in combinations(range(m), k):
                    for cols in combinations(range(n), k):
                        submat = mat[list(rows), list(cols)]
                        det = abs(submat.det())
                        minors_gcd = sympy.gcd(minors_gcd, det)
                        if minors_gcd == 1:
                            break
                    if minors_gcd == 1:
                        break
                D[k] = minors_gcd
                
            P_inv = []
            for k in range(1, n + 1):
                if D[k] == 0:
                    P_inv.append(0)
                else:
                    if D[k-1] != 0:
                        d = D[k] // D[k-1]
                        if d != 1:
                            P_inv.append(d)
                    else:
                        P_inv.append(0)
                        
        # Convert P_inv (invariant factors) to prime-power invariants
        P_prime_power = []
        for val in P_inv:
            if val == 0:
                P_prime_power.append(0)
            elif val > 1:
                factors = sympy.factorint(val)
                for p, e in factors.items():
                    P_prime_power.append(p**e)
        P_prime_power.sort()
        
        # Get prime-power invariants of G
        if hasattr(G, 'abelian_invariants'):
            G_inv = sorted(G.abelian_invariants())
            is_iso = (G_inv == P_prime_power)
        else:
            # Fallback if G doesn't have abelian_invariants
            if hasattr(G, 'derived_subgroup'):
                G_ab_order = G.order() // G.derived_subgroup().order()
            elif hasattr(G, 'order'):
                if getattr(G, 'is_abelian', False):
                    G_ab_order = G.order()
                else:
                    G_ab_order = G.order() // G.derived_subgroup().order()
            else:
                G_ab_order = None
                
            P_ab_order = 1
            for val in P_inv:
                if val == 0:
                    P_ab_order = 0
                    break
                P_ab_order *= val
                
            if G_ab_order is not None:
                is_iso = (G_ab_order == P_ab_order)
            else:
                is_iso = True
                
        neg_q = not is_iso
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G^{ab} is the abelianization of G",
    "¬Q: G^{ab} is not isomorphic to < X | R U {commutators} >"
]

N_HYP = 1
NEG_Q_INDEX = 1