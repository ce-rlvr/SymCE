import math
from sympy.combinatorics import SymmetricGroup, PermutationGroup, Permutation
from sympy.combinatorics.named_groups import AlternatingGroup, CyclicGroup, DihedralGroup

# Top-level setup for potential witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

CONDITION_LABELS = [
    "H_1: P is a Sylow p-subgroup of the symmetric group S_p",
    "H_2: N(P) is the normalizer of P in S_p",
    "¬Q: The order of N(P) is not p(p-1)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        # Handle different witness formats
        if isinstance(witness, int):
            p = witness
            if p == 1:
                P = SymmetricGroup(1)
                N = SymmetricGroup(1)
            elif p == 4:
                P = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
                N = SymmetricGroup(4)
            else:
                return [False, False, False]
        elif isinstance(witness, dict):
            p = witness.get('p')
            P = witness.get('P')
            N = witness.get('N')
        else:
            p, P, N = witness
            
        if not isinstance(p, int) or p < 1:
            return [False, False, False]
            
        Sp = SymmetricGroup(p)
        id_p = Permutation(list(range(p)))
        
        # Helper to safely resize permutations to degree p
        def resize(perm, size):
            if perm.size == size:
                return perm
            elif perm.size < size:
                return Permutation(perm.array_form + list(range(perm.size, size)))
            else:
                for i in range(size, perm.size):
                    if perm(i) != i:
                        raise ValueError("Permutation moves points beyond p")
                return Permutation(perm.array_form[:size])
                
        # Check if P is a subgroup of Sp
        try:
            P_gens = [resize(g, p) for g in P.generators]
            P_Sp = PermutationGroup(*P_gens) if P_gens else PermutationGroup(id_p)
            is_p_subgroup = True
        except (ValueError, AttributeError):
            is_p_subgroup = False

        # Check if N is a subgroup of Sp
        try:
            N_gens = [resize(g, p) for g in N.generators]
            N_Sp = PermutationGroup(*N_gens) if N_gens else PermutationGroup(id_p)
            is_n_subgroup = True
        except (ValueError, AttributeError):
            is_n_subgroup = False

        # Helper to find the highest power of 'base' dividing 'n'
        def highest_power(n, base):
            if base == 1:
                return 1
            power = 1
            while n % (power * base) == 0:
                power *= base
            return power

        # H1: P is a Sylow p-subgroup of Sp
        # (Interpreted literally for composite p: order is the highest power of p dividing |Sp|)
        try:
            if is_p_subgroup:
                expected_order = highest_power(math.factorial(p), p)
                h1 = P_Sp.order() == expected_order
            else:
                h1 = False
        except Exception:
            h1 = False

        # H2: N is the normalizer of P in Sp
        try:
            if is_n_subgroup and is_p_subgroup:
                if p <= 8:  # Limit p to avoid excessive computation time
                    actual_normalizer_order = 0
                    is_N_correct = True
                    
                    # Verify N normalizes P
                    for g in N_Sp.generators:
                        for x in P_Sp.generators:
                            if not P_Sp.contains(g * x * (~g)):
                                is_N_correct = False
                                break
                        if not is_N_correct:
                            break
                    
                    # Verify N is maximal (i.e., it is the full normalizer)
                    if is_N_correct:
                        for g in Sp.generate():
                            normalizes = True
                            for x in P_Sp.generators:
                                if not P_Sp.contains(g * x * (~g)):
                                    normalizes = False
                                    break
                            if normalizes:
                                actual_normalizer_order += 1
                        
                        h2 = N_Sp.order() == actual_normalizer_order
                    else:
                        h2 = False
                else:
                    h2 = False
            else:
                h2 = False
        except Exception:
            h2 = False

        # ¬Q: The order of N(P) is not p(p-1)
        try:
            expected_N_order = p * (p - 1)
            neg_q = N.order() != expected_N_order
        except Exception:
            neg_q = False

        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]