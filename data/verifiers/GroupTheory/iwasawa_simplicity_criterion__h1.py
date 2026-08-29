import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
from itertools import combinations

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

def conditions(witness):
    """
    Checks if the given witness (a PermutationGroup) satisfies the hypotheses
    and falsifies the conclusion of the modified Iwasawa's Simplicity Criterion.
    """
    try:
        # Fast fail for invalid or excessively large groups to prevent timeouts
        if not hasattr(witness, 'order') or witness.order() > 1000:
            return [False, False, False, False, False]
    except Exception:
        return [False, False, False, False, False]

    G = witness

    # H_1: X is a non-empty set
    try:
        h1 = G.degree > 0
    except Exception:
        h1 = False

    # H_2: G acts faithfully and primitively on X
    try:
        h2 = G.is_primitive()
    except Exception:
        h2 = False

    # H_3: There exists an element x in X such that the stabilizer G_x contains an abelian normal subgroup A of G_x
    # H_4: The conjugates of A in G generate the group G
    h3 = False
    h4 = False
    try:
        elements_G = list(G.generate())
        for x in range(G.degree):
            try:
                Gx = G.stabilizer(x)
                elements_Gx = list(Gx.generate())
            except Exception:
                continue
                
            # Limit combination size to keep execution fast
            max_r = min(3, len(elements_Gx) + 1) if len(elements_Gx) <= 16 else 2
            for r in range(1, max_r):
                for gens in combinations(elements_Gx, r):
                    try:
                        A = PermutationGroup(*gens)
                        if not A.is_abelian:
                            continue
                        
                        # Check if A is normal in Gx
                        is_normal = True
                        A_elements = list(A.generate())
                        for h in elements_Gx:
                            for a in A_elements:
                                if (h * a * ~h) not in A_elements:
                                    is_normal = False
                                    break
                            if not is_normal:
                                break
                        
                        if is_normal:
                            h3 = True
                            # Check if conjugates of A in G generate G
                            conjugate_gens = []
                            for g in elements_G:
                                for a in gens:
                                    conjugate_gens.append(g * a * ~g)
                            K = PermutationGroup(*conjugate_gens)
                            if K.order() == G.order():
                                h4 = True
                                break
                    except Exception:
                        pass
                if h4:
                    break
            if h4:
                break
    except Exception:
        pass

    # ¬Q: The group G is not a simple group
    try:
        if G.order() <= 1:
            is_simple_group = False
        else:
            is_simple_group = True
            elements = list(G.generate())
            for g in elements:
                # Skip the identity element
                if not g.support():
                    continue
                # The normal closure of any non-identity element in a simple group must be the whole group
                conjugates = [h * g * ~h for h in elements]
                K = PermutationGroup(*conjugates)
                if K.order() < G.order():
                    is_simple_group = False
                    break
        neg_q = not is_simple_group
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(h4), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: X is a non-empty set",
    "H_2: G acts faithfully and primitively on X",
    "H_3: There exists an element x in X such that the stabilizer G_x contains an abelian normal subgroup A of G_x",
    "H_4: The conjugates of A in G generate the group G",
    "¬Q: The group G is not a simple group"
]

N_HYP = 4
NEG_Q_INDEX = 4