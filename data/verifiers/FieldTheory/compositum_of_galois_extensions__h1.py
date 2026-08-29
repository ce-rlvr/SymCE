import sympy
from sympy.combinatorics import PermutationGroup, Permutation
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
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: K and L are finite field extensions of F",
    "H_2: K and L are contained in a common extension field",
    "H_3: K/F is a Galois extension",
    "H_4: L/F is a Galois extension",
    "¬Q: The compositum field KL is not a Galois extension of F"
]

N_HYP = 4
NEG_Q_INDEX = 4

def conditions(witness):
    # Support for mock objects (dictionary)
    if isinstance(witness, dict):
        try:
            h1 = bool(witness.get("K_finite", witness.get("K_finite_extension", False))) and \
                 bool(witness.get("L_finite", witness.get("L_finite_extension", False)))
            h2 = bool(witness.get("common_extension", witness.get("contained_in_common_extension", False)))
            h3 = bool(witness.get("K_galois", witness.get("K_is_galois", False)))
            h4 = bool(witness.get("L_galois", witness.get("L_is_galois", False)))
            neg_q = not bool(witness.get("KL_galois", witness.get("KL_is_galois", True)))
            return [h1, h2, h3, h4, neg_q]
        except Exception:
            pass

    # Support for mock objects (attributes)
    if hasattr(witness, "K_finite") or hasattr(witness, "K_finite_extension"):
        try:
            h1 = bool(getattr(witness, "K_finite", getattr(witness, "K_finite_extension", False))) and \
                 bool(getattr(witness, "L_finite", getattr(witness, "L_finite_extension", False)))
            h2 = bool(getattr(witness, "common_extension", getattr(witness, "contained_in_common_extension", False)))
            h3 = bool(getattr(witness, "K_galois", getattr(witness, "K_is_galois", False)))
            h4 = bool(getattr(witness, "L_galois", getattr(witness, "L_is_galois", False)))
            neg_q = not bool(getattr(witness, "KL_galois", getattr(witness, "KL_is_galois", True)))
            return [h1, h2, h3, h4, neg_q]
        except Exception:
            pass

    # Support for Galois correspondence via PermutationGroups
    # witness = (G, H_K, H_L) where G is the Galois group of a large extension,
    # and H_K, H_L are subgroups corresponding to fields K and L.
    try:
        G, H_K, H_L = witness
    except Exception:
        return [False, False, False, False, False]

    # H1: K and L are finite field extensions of F
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(H_K, PermutationGroup) and isinstance(H_L, PermutationGroup)
        if h1:
            for gen in H_K.generators:
                if gen not in G:
                    h1 = False
                    break
            if h1:
                for gen in H_L.generators:
                    if gen not in G:
                        h1 = False
                        break
    except Exception:
        h1 = False

    # H2: K and L are contained in a common extension field
    try:
        h2 = h1 
    except Exception:
        h2 = False

    # H3: K/F is a Galois extension (H_K is normal in G)
    try:
        h3 = False
        if h1:
            h3 = True
            for h in H_K.generators:
                for g in G.generators:
                    if (g * h * ~g) not in H_K or (~g * h * g) not in H_K:
                        h3 = False
                        break
                if not h3:
                    break
    except Exception:
        h3 = False

    # H4: L/F is a Galois extension (H_L is normal in G)
    try:
        h4 = False
        if h1:
            h4 = True
            for h in H_L.generators:
                for g in G.generators:
                    if (g * h * ~g) not in H_L or (~g * h * g) not in H_L:
                        h4 = False
                        break
                if not h4:
                    break
    except Exception:
        h4 = False

    # neg_Q: KL is NOT a Galois extension of F (H_K \cap H_L is NOT normal in G)
    try:
        neg_q = False
        if h1:
            elements_K = set(H_K.generate())
            elements_L = set(H_L.generate())
            elements_KL = elements_K.intersection(elements_L)
            H_KL = PermutationGroup(list(elements_KL))
            
            is_normal_KL = True
            for h in H_KL.generators:
                for g in G.generators:
                    if (g * h * ~g) not in H_KL or (~g * h * g) not in H_KL:
                        is_normal_KL = False
                        break
                if not is_normal_KL:
                    break
            neg_q = not is_normal_KL
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]