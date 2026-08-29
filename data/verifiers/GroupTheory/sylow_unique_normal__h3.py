import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

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

def is_normal_subgroup(G, P):
    try:
        if not isinstance(P, PermutationGroup):
            return False
        # Check if P is a subgroup of G
        try:
            if not P.is_subgroup(G):
                return False
        except Exception:
            # Fallback subgroup check
            for gen in P.generators:
                if gen not in G:
                    return False
        
        # Check normality: g * h * g^-1 in P for all generators g in G, h in P
        for g in G.generators:
            g_inv = g**-1
            for h in P.generators:
                if (g * h * g_inv) not in P:
                    return False
                if (g_inv * h * g) not in P:
                    return False
        return True
    except Exception:
        return False

def is_unique_sylow_p_subgroup(G, p, P):
    try:
        if not isinstance(P, PermutationGroup):
            return False
        # Check if P is a subgroup of G
        try:
            if not P.is_subgroup(G):
                return False
        except Exception:
            for gen in P.generators:
                if gen not in G:
                    return False
                    
        # Determine the order of a Sylow p-subgroup
        order_G = G.order()
        k = 0
        temp = order_G
        while temp > 0 and temp % p == 0:
            k += 1
            temp //= p
        sylow_order = p**k
        
        # P must be a Sylow p-subgroup
        if P.order() != sylow_order:
            return False
            
        # A Sylow p-subgroup is unique if and only if it is normal in G
        return is_normal_subgroup(G, P)
    except Exception:
        return False

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple: (G, p, P)
    """
    try:
        G, p, P = witness
    except Exception:
        return [False, False, False]
        
    # H_1: G is a finite group
    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False
        
    # H_2: p is a prime number
    try:
        h2_ok = sympy.isprime(p)
    except Exception:
        h2_ok = False
        
    # neg_Q: P is a normal subgroup of G if and only if P is the unique Sylow p-subgroup of G (must FAIL)
    try:
        is_normal = is_normal_subgroup(G, P)
        is_unique_sylow = is_unique_sylow_p_subgroup(G, p, P)
        # The conclusion is the biconditional (is_normal == is_unique_sylow).
        # We want the negated conclusion, so the biconditional must be False.
        neg_q_ok = (is_normal != is_unique_sylow)
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is a prime number",
    "¬Q: The equivalence between P being normal and P being the unique Sylow p-subgroup fails"
]

N_HYP = 2
NEG_Q_INDEX = 2