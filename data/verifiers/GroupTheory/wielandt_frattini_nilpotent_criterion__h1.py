import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
    # H_1: The commutator subgroup G' is a subgroup of the Frattini subgroup \Phi(G)
    h1_ok = False
    try:
        if hasattr(witness, 'commutator_in_frattini'):
            val = witness.commutator_in_frattini
            h1_ok = bool(val() if callable(val) else val)
        else:
            if hasattr(witness, 'derived_subgroup'):
                G_prime = witness.derived_subgroup() if callable(witness.derived_subgroup) else witness.derived_subgroup
            elif hasattr(witness, 'commutator_subgroup'):
                G_prime = witness.commutator_subgroup() if callable(witness.commutator_subgroup) else witness.commutator_subgroup
            else:
                G_prime = None

            if G_prime is not None:
                if hasattr(witness, 'frattini_subgroup'):
                    phi = witness.frattini_subgroup() if callable(witness.frattini_subgroup) else witness.frattini_subgroup
                    if hasattr(G_prime, 'is_subgroup'):
                        h1_ok = bool(G_prime.is_subgroup(phi))
                    elif hasattr(phi, 'contains_subgroup'):
                        h1_ok = bool(phi.contains_subgroup(G_prime))
                elif hasattr(witness, 'maximal_subgroups'):
                    max_subs = witness.maximal_subgroups() if callable(witness.maximal_subgroups) else witness.maximal_subgroups
                    is_sub = True
                    for M in max_subs:
                        if hasattr(G_prime, 'is_subgroup'):
                            if not G_prime.is_subgroup(M):
                                is_sub = False
                                break
                        elif hasattr(M, 'contains_subgroup'):
                            if not M.contains_subgroup(G_prime):
                                is_sub = False
                                break
                        elif hasattr(G_prime, 'generators') and hasattr(M, 'contains'):
                            gens = G_prime.generators() if callable(G_prime.generators) else G_prime.generators
                            for g in gens:
                                if not M.contains(g):
                                    is_sub = False
                                    break
                            if not is_sub:
                                break
                        else:
                            is_sub = False
                            break
                    h1_ok = is_sub
    except Exception:
        h1_ok = False

    # neg_Q: G is not a nilpotent group
    neg_q_ok = False
    try:
        if hasattr(witness, 'is_nilpotent'):
            val = witness.is_nilpotent
            is_nilp = val() if callable(val) else val
            neg_q_ok = not bool(is_nilp)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    r"H_1: The commutator subgroup G' is a subgroup of the Frattini subgroup \Phi(G)",
    "¬Q: G is not a nilpotent group"
]

N_HYP = 1
NEG_Q_INDEX = 1