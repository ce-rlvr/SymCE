import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.matrices
import sympy.ntheory

S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)
I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2,2)
O3 = sympy.matrices.zeros(3,3)

def contains_perm(group, perm):
    if perm.is_Identity:
        return True
    try:
        if perm.size > group.degree:
            for i in range(group.degree, perm.size):
                if perm(i) != i:
                    return False
            perm = sympy.combinatorics.Permutation(perm.array_form[:group.degree])
        elif perm.size < group.degree:
            perm = sympy.combinatorics.Permutation(perm, size=group.degree)
        return group.contains(perm)
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            N = witness.get('N')
            P = witness.get('P')
            p = witness.get('p')
        else:
            G, N, P, p = witness
    except Exception:
        return [False, False, False]

    # H1: G is a finite group
    try:
        h1 = isinstance(G, sympy.combinatorics.PermutationGroup)
    except Exception:
        h1 = False

    # H2: N is a normal p-subgroup of G
    h2 = False
    try:
        if isinstance(N, sympy.combinatorics.PermutationGroup) and isinstance(p, (int, sympy.Integer)) and sympy.ntheory.isprime(p):
            is_sub = True
            for n in N.generators:
                if not contains_perm(G, n):
                    is_sub = False
                    break
            if is_sub:
                is_norm = True
                for n in N.generators:
                    for g in G.generators:
                        conj = g * n * ~g
                        if not contains_perm(N, conj):
                            is_norm = False
                            break
                    if not is_norm:
                        break
                if is_norm:
                    order = N.order()
                    is_p = True
                    if order > 1:
                        temp = order
                        while temp % p == 0:
                            temp //= p
                        if temp != 1:
                            is_p = False
                    h2 = is_p
    except Exception:
        h2 = False

    # neg_Q: N is NOT a subgroup of P
    neg_q = False
    try:
        is_sub_P = True
        if not isinstance(P, sympy.combinatorics.PermutationGroup):
            is_sub_P = False
        else:
            for n in N.generators:
                if not contains_perm(P, n):
                    is_sub_P = False
                    break
        neg_q = not is_sub_P
    except Exception:
        neg_q = True

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: N is a normal p-subgroup of G",
    "¬Q: N is not a subgroup of P"
]

N_HYP = 2
NEG_Q_INDEX = 2