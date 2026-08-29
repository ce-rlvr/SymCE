import itertools
import math

# Top-level setup for the namespace
# Witnesses for finite rings can be represented using integers for Z/nZ.
# No special named objects are strictly required for this specific verifier,
# as the witness will explicitly define the rings, homomorphism, and subsets.

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "If R, S are commutative rings, f: R -> S is a ring homomorphism, and J is an ideal of S,
    then f^{-1}(I)f^{-1}(J) \\subseteq f^{-1}(IJ)."
    (The dropped hypothesis was that I is an ideal of S).
    
    Expected witness format:
    {
        "R": int,  # represents Z/RZ
        "S": int,  # represents Z/SZ
        "f": dict, # mapping from elements of Z/RZ to Z/SZ
        "I": list, # subset of Z/SZ
        "J": list  # subset of Z/SZ
    }
    """
    # H_1: R and S are commutative rings
    try:
        R = int(witness['R'])
        S = int(witness['S'])
        h1 = (R > 1 and S > 1)
    except Exception:
        h1 = False

    # H_2: f: R \to S is a ring homomorphism
    h2 = True
    try:
        f = witness['f']
        # Check f(1) = 1
        if f[1 % R] != 1 % S:
            h2 = False
        # Check f(a+b) = f(a)+f(b) and f(ab) = f(a)f(b)
        if h2:
            for a in range(R):
                for b in range(R):
                    if f[(a + b) % R] != (f[a] + f[b]) % S:
                        h2 = False
                        break
                    if f[(a * b) % R] != (f[a] * f[b]) % S:
                        h2 = False
                        break
                if not h2:
                    break
    except Exception:
        h2 = False

    # H_3: J is an ideal of S
    h3 = True
    try:
        J = set(witness['J'])
        if not J:
            h3 = False
        else:
            # Check additive subgroup
            for a in J:
                for b in J:
                    if (a - b) % S not in J:
                        h3 = False
                        break
                if not h3:
                    break
            # Check absorption
            if h3:
                for r in range(S):
                    for a in J:
                        if (r * a) % S not in J:
                            h3 = False
                            break
                    if not h3:
                        break
    except Exception:
        h3 = False

    # neg_Q: f^{-1}(I)f^{-1}(J) \not\subseteq f^{-1}(IJ)
    neg_q = False
    try:
        I = set(witness['I'])
        J = set(witness['J'])
        f = witness['f']

        def additive_closure(modulus, gen_set):
            closure = set(gen_set)
            closure.add(0)
            added = True
            while added:
                added = False
                new_elements = set()
                for x in closure:
                    for y in closure:
                        val = (x + y) % modulus
                        if val not in closure:
                            new_elements.add(val)
                if new_elements:
                    closure.update(new_elements)
                    added = True
            return closure

        # IJ in S (additive closure of pairwise products)
        IJ_gens = set((i * j) % S for i in I for j in J)
        IJ = additive_closure(S, IJ_gens)

        # Preimages
        f_inv_I = set(x for x in range(R) if f[x] in I)
        f_inv_J = set(x for x in range(R) if f[x] in J)
        f_inv_IJ = set(x for x in range(R) if f[x] in IJ)

        # f^{-1}(I)f^{-1}(J) in R (additive closure of pairwise products)
        LHS_gens = set((a * b) % R for a in f_inv_I for b in f_inv_J)
        LHS = additive_closure(R, LHS_gens)

        # Check if LHS is NOT a subset of f^{-1}(IJ)
        if not LHS.issubset(f_inv_IJ):
            neg_q = True

    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R and S are commutative rings",
    "H_2: f: R \\to S is a ring homomorphism",
    "H_3: J is an ideal of S",
    "¬Q: f^{-1}(I)f^{-1}(J) \\not\\subseteq f^{-1}(IJ)"
]

N_HYP = 3
NEG_Q_INDEX = 3