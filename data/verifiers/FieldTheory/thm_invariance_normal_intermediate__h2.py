import sympy
from sympy import minpoly, sqrt, Rational, I, pi, exp, QQ
from sympy.abc import x
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup: Named objects for the witness namespace
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = PermutationGroup([Permutation()])

def conditions(witness):
    """
    Check if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (K, F, E) representing the fields or their Galois groups.
    """
    try:
        K, F, E = witness
    except Exception:
        return [False, False]

    # 1. Group theory branch (Galois correspondence)
    # F corresponds to the full Galois group G.
    # K corresponds to a subgroup N.
    # E corresponds to a subgroup H.
    if hasattr(F, 'is_subgroup'):
        try:
            G = F
            N = K
            H = E
            
            # H_1: K/F is normal <=> N is a normal subgroup of G
            h1 = bool(N.is_subgroup(G) and N.is_normal(G))
            
            # LHS: E/F is normal <=> H is a normal subgroup of G
            lhs = bool(H.is_subgroup(G) and H.is_normal(G))
            
            # RHS: E is a subfield of K AND σ(E) = E for all F-automorphisms of K
            # E <= K <=> N <= H. If N <= H, σ(E) = E <=> H is normal in G.
            rhs = bool(N.is_subgroup(H) and H.is_normal(G))
            
            neg_q = not (lhs == rhs)
            return [h1, neg_q]
        except Exception:
            pass

    # 2. Field theory branch (SymPy expressions over Q)
    # F is assumed to be Q (represented by 1 or any rational).
    # K and E are SymPy expressions representing primitive elements.
    try:
        # H_1: K/Q is normal. We restrict to degree <= 2 for deterministic evaluation.
        p_K = minpoly(K, x)
        d_K = p_K.degree()
        h1 = bool(d_K <= 2)
        
        # LHS: E/Q is normal. We restrict to degree <= 2.
        p_E = minpoly(E, x)
        d_E = p_E.degree()
        lhs = bool(d_E <= 2)
        
        # Check if E is a subfield of K
        try:
            if d_E == 1:
                is_subfield = True
            elif d_K == 1:
                is_subfield = False
            else:
                p_E_K = minpoly(E, x, domain=QQ.algebraic_field(K))
                is_subfield = bool(p_E_K.degree() == 1)
        except Exception:
            # Safe fallback to prevent false positive counterexamples if minpoly fails
            is_subfield = True
            
        # RHS: E is a subfield of K AND σ(E) = E.
        # If E is not a subfield of K, σ(E) is undefined, making the condition False.
        rhs = bool(is_subfield and lhs)
        
        neg_q = not (lhs == rhs)
        return [h1, neg_q]
    except Exception:
        pass

    return [False, False]

CONDITION_LABELS = [
    "H_1: K/F is a normal extension",
    "¬Q: E/F is normal iff σ(E) = E condition fails (e.g., E is not a subfield of K)"
]

N_HYP = 1
NEG_Q_INDEX = 1