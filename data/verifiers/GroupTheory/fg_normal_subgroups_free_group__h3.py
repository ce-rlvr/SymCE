import sympy
from sympy.combinatorics import free_group
from sympy import Matrix

# Top-level setup: named object bindings that the witness expression may reference.
F2, x, y = free_group("x, y")
F3, a, b, c = free_group("a, b, c")

def conditions(witness) -> list[bool]:
    # Extract F and relators from the witness
    F = None
    relators = None
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            F, relators = witness
        elif hasattr(witness, 'free_group') and hasattr(witness, 'relators'):
            F = witness.free_group
            relators = witness.relators
    except Exception:
        pass

    # H_1: F is a non-abelian free group
    try:
        # Check if F is a free group by checking its type against F2's type
        h1 = type(F) is type(F2) and len(F.generators) >= 2
    except Exception:
        h1 = False

    # H_2: N is a normal subgroup of F
    # By definition, the normal closure of any set of elements in F is a normal subgroup.
    # We verify that the witness provides a valid list of elements in F.
    try:
        if h1 and isinstance(relators, (list, tuple)):
            h2 = all(hasattr(w, 'group') and w.group == F for w in relators)
        else:
            h2 = False
    except Exception:
        h2 = False

    # ¬Q: N is not the trivial subgroup AND N does not have finite index in F
    try:
        if not (h1 and h2):
            neg_q = False
        else:
            if not relators:
                # No relators means N is the trivial subgroup
                neg_q = False
            else:
                # N is trivial iff all relators are the identity
                is_trivial = all(w == F.identity for w in relators)
                not_trivial = not is_trivial

                # To check if N has infinite index, we check if the abelianization of F/N is infinite.
                # This is a sufficient condition: if the rank of the exponent sum matrix is less 
                # than the number of generators, the abelianization has free rank > 0, meaning F/N 
                # maps onto Z, so F/N is infinite.
                num_gens = len(F.generators)
                rows = []
                for w in relators:
                    sums = {str(g): 0 for g in F.generators}
                    for gen, exp in w.array_form:
                        sums[str(gen)] += exp
                    rows.append([sums[str(g)] for g in F.generators])
                
                if rows:
                    M = Matrix(rows)
                    infinite_index = M.rank() < num_gens
                else:
                    infinite_index = True
                
                neg_q = not_trivial and infinite_index
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a non-abelian free group",
    "H_2: N is a normal subgroup of F",
    "¬Q: N is not the trivial subgroup and does not have finite index in F"
]

N_HYP = 2
NEG_Q_INDEX = 2