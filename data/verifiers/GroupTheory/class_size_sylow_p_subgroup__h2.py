from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import isprime

# Top-level setup: named object bindings for witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    # Unpack witness
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) != 3:
            return [False, False, False]
        G, p, x = witness
    except Exception:
        return [False, False, False]

    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: p is a prime number
    try:
        h2 = isprime(p)
    except Exception:
        h2 = False

    # ¬Q: The size of the conjugacy class of x in G is coprime to p XOR the centralizer C_G(x) contains a Sylow p-subgroup of G
    try:
        # Normalize x to a set of elements
        if hasattr(x, 'elements'):
            x_elems = set(x.elements)
        elif isinstance(x, (list, set, tuple)):
            x_elems = set(x)
        else:
            x_elems = {x}

        G_elems = list(G.elements)

        # Compute the size of the centralizer C_G(x)
        C_G_x_len = 0
        for g in G_elems:
            if all(g * h == h * g for h in x_elems):
                C_G_x_len += 1

        # Compute the size of the normalizer N_G(x)
        if len(x_elems) == 1:
            N_G_x_len = C_G_x_len
        else:
            N_G_x_len = 0
            for g in G_elems:
                g_inv = ~g
                conj_set = {g * h * g_inv for h in x_elems}
                if conj_set == x_elems:
                    N_G_x_len += 1

        # The size of the conjugacy class of x is [G : N_G(x)]
        conj_size = len(G_elems) // N_G_x_len
        is_coprime = (conj_size % p != 0)

        # Find the highest power of p dividing |G|
        highest_power = 1
        temp = len(G_elems)
        while temp % p == 0:
            highest_power *= p
            temp //= p

        # C_G(x) contains a Sylow p-subgroup of G iff its order is divisible by the highest power of p dividing |G|
        contains_sylow = (C_G_x_len % highest_power == 0)

        # The conclusion is an iff statement; its negation is an XOR
        neg_q = (is_coprime != contains_sylow)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is a prime number",
    "¬Q: The size of the conjugacy class of x in G is coprime to p XOR the centralizer C_G(x) contains a Sylow p-subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2