import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

# Standard algebra objects
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
    """
    Given a witness, checks if it satisfies the remaining hypotheses and falsifies the conclusion.
    The witness can be a tuple (G, G_prime, N), a tuple (G, N), or a dictionary.
    """
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            N = witness.get('N')
            if 'G_prime' in witness:
                G_prime = witness['G_prime']
            else:
                G_prime = G.derived_subgroup() if hasattr(G, 'derived_subgroup') else None
        elif isinstance(witness, tuple):
            if len(witness) == 3:
                G, G_prime, N = witness
            elif len(witness) == 2:
                G, N = witness
                G_prime = G.derived_subgroup() if hasattr(G, 'derived_subgroup') else None
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    def is_subgroup(H, Grp):
        try:
            if not hasattr(H, 'generators') or not hasattr(Grp, 'generators'):
                return False
            return all(g in Grp for g in H.generators)
        except Exception:
            return False

    def is_normal_subgroup(N_sub, Grp):
        if not is_subgroup(N_sub, Grp):
            return False
        try:
            for n in N_sub.generators:
                for g in Grp.generators:
                    if (g * n * ~g) not in N_sub:
                        return False
            return True
        except Exception:
            return False

    # H1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H2: G' is the commutator subgroup of G
    try:
        if G_prime is None:
            h2 = False
        else:
            derived = G.derived_subgroup()
            h2 = is_subgroup(G_prime, derived) and is_subgroup(derived, G_prime)
    except Exception:
        h2 = False

    # neg_Q: The quotient group G/N is abelian if and only if G' \le N
    try:
        if G_prime is None or N is None:
            neg_q = False
        else:
            g_prime_le_n = is_subgroup(G_prime, N)
            
            # G/N is a valid quotient group only if N is a normal subgroup of G
            if is_normal_subgroup(N, G):
                quotient_is_abelian = True
                # G/N is abelian iff the commutator of any two generators of G is in N
                for g1 in G.generators:
                    for g2 in G.generators:
                        commutator = g1 * g2 * ~g1 * ~g2
                        if commutator not in N:
                            quotient_is_abelian = False
                            break
                    if not quotient_is_abelian:
                        break
            else:
                # If N is not a normal subgroup, G/N is not a group, so it cannot be an abelian group
                quotient_is_abelian = False
                
            # The conclusion Q is the biconditional
            q = (quotient_is_abelian == g_prime_le_n)
            neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: G' is the commutator subgroup of G",
    "¬Q: The biconditional (G/N is abelian iff G' <= N) fails"
]

N_HYP = 2
NEG_Q_INDEX = 2