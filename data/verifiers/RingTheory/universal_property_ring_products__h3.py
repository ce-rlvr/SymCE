import sympy
import itertools

# Top-level setup
# Rings can be represented by their order n (for Z_n)
Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            R = int(witness['R'])
            S1 = int(witness['S1'])
            S2 = int(witness['S2'])
            f1 = witness['f1']
            f2 = witness['f2']
        else:
            R, S1, S2, f1, f2 = witness
            R = int(R)
            S1 = int(S1)
            S2 = int(S2)

        # H1: R, S1, S2 are rings
        h1 = (R > 0 and S1 > 0 and S2 > 0)

        # H2: pi_1, pi_2 are canonical projections
        # We verify that f1 and f2 are well-defined functions from R to S1 and S2
        h2 = True
        for x in range(R):
            try:
                v1 = f1[x]
                v2 = f2[x]
                if not (0 <= v1 < S1) or not (0 <= v2 < S2):
                    h2 = False
                    break
            except Exception:
                h2 = False
                break

        # neg_Q: There does NOT exist a unique ring homomorphism f: R -> S1 x S2
        # such that pi_1 o f = f1 and pi_2 o f = f2.
        # This means the map x |-> (f1(x), f2(x)) is NOT a valid ring homomorphism.
        is_hom = True
        if h2:
            # Check f(1) = 1
            if f1[1 % R] != 1 % S1 or f2[1 % R] != 1 % S2:
                is_hom = False

            # Check addition and multiplication
            if is_hom:
                for x in range(R):
                    for y in range(R):
                        sum_xy = (x + y) % R
                        prod_xy = (x * y) % R

                        if f1[sum_xy] != (f1[x] + f1[y]) % S1:
                            is_hom = False
                        if f2[sum_xy] != (f2[x] + f2[y]) % S2:
                            is_hom = False

                        if f1[prod_xy] != (f1[x] * f1[y]) % S1:
                            is_hom = False
                        if f2[prod_xy] != (f2[x] * f2[y]) % S2:
                            is_hom = False
        else:
            is_hom = False

        neg_q = not is_hom

        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R, S1, and S2 are rings",
    "H_2: pi_1 and pi_2 are canonical projection homomorphisms",
    "¬Q: There does not exist a unique ring homomorphism f such that pi_1 o f = f_1 and pi_2 o f = f_2"
]

N_HYP = 2
NEG_Q_INDEX = 2