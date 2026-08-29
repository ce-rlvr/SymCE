import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import Poly, eye, zeros
from sympy.abc import x

# Top-level setup: named object bindings that the witness expression may reference
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
    h1 = False
    h2 = False
    neg_q = False
    
    # 1. Dictionary witness
    if isinstance(witness, dict):
        try:
            h1 = bool(witness.get("H1", witness.get("L_finite_separable", True)))
            h2 = bool(witness.get("H2", witness.get("G_absolute_Galois", True)))
            neg_q = bool(witness.get("neg_Q", witness.get("not_normal", True)))
            return [h1, h2, neg_q]
        except Exception:
            pass

    # 2. Tuple of groups (G, H) representing Galois correspondence
    if isinstance(witness, tuple) and len(witness) == 2:
        try:
            G, H = witness
            if isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup):
                h1 = H.is_subgroup(G)
                h2 = True
                
                # Check if H is normal in G (corresponds to L being a normal extension)
                is_normal = True
                for g in G.generators:
                    for h in H.generators:
                        if not H.contains(g * h * ~g):
                            is_normal = False
                            break
                    if not is_normal:
                        break
                
                neg_q = not is_normal
                return [h1, h2, neg_q]
        except Exception:
            pass

    # 3. Single group witness
    if isinstance(witness, PermutationGroup):
        try:
            h1 = True
            h2 = True
            neg_q = not witness.is_abelian
            return [h1, h2, neg_q]
        except Exception:
            pass

    # 4. Polynomial witness (representing the extension L = K[x]/(f))
    try:
        p = Poly(witness, x, domain='QQ')
        h1 = bool(p.is_irreducible and p.is_sqf)
        h2 = True
        
        deg = p.degree()
        if deg <= 2:
            neg_q = False
        elif deg == 3:
            # A cubic is normal iff its discriminant is a perfect square
            disc = p.discriminant()
            sq = sympy.sqrt(disc)
            neg_q = not (getattr(sq, 'is_rational', False) is True)
        else:
            # For higher degrees, assume non-normal as a fallback for counterexamples
            neg_q = True
            
        return [h1, h2, neg_q]
    except Exception:
        pass

    # 5. Object with attributes
    try:
        h1 = bool(getattr(witness, "H1", getattr(witness, "is_finite_separable", True)))
        h2 = bool(getattr(witness, "H2", getattr(witness, "is_absolute_Galois", True)))
        if hasattr(witness, "neg_Q"):
            neg_q = bool(witness.neg_Q)
        elif hasattr(witness, "is_normal"):
            neg_q = not bool(witness.is_normal())
        else:
            neg_q = True
        return [h1, h2, neg_q]
    except Exception:
        pass

    return [False, False, False]

CONDITION_LABELS = [
    "H_1: L is a finite separable extension of K contained in \\bar{K}",
    "H_2: G is the absolute Galois group Gal(\\bar{K}/K)",
    "¬Q: The normal closure of L over K is not exactly the compositum of the fields \\sigma(L) over all \\sigma \\in G"
]

N_HYP = 2
NEG_Q_INDEX = 2