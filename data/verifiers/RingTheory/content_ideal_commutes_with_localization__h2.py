import sympy as sp
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros

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

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: f is a polynomial over R",
    "¬Q: The content ideal of the localized polynomial S^(-1)f in S^(-1)R is not equal to S^(-1)c(f)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if isinstance(witness, dict):
            R_vars = witness.get('R_vars', [])
            K_gens = witness.get('K_gens', [])
            S_gens = witness.get('S_gens', [])
            f_coeffs = witness.get('f_coeffs', [])
            S_inv_f_coeffs = witness.get('S_inv_f_coeffs', f_coeffs)
        else:
            R_vars = getattr(witness, 'R_vars', [])
            K_gens = getattr(witness, 'K_gens', [])
            S_gens = getattr(witness, 'S_gens', [])
            f_coeffs = getattr(witness, 'f_coeffs', [])
            S_inv_f_coeffs = getattr(witness, 'S_inv_f_coeffs', f_coeffs)

        if isinstance(R_vars, str):
            R_vars_sym = sp.symbols(R_vars)
            if not isinstance(R_vars_sym, tuple):
                R_vars_sym = (R_vars_sym,)
        else:
            R_vars_sym = tuple(sp.sympify(v) for v in R_vars)

        K_gens_sym = [sp.sympify(g) for g in K_gens]
        S_gens_sym = [sp.sympify(g) for g in S_gens]
        f_coeffs_sym = [sp.sympify(g) for g in f_coeffs]
        S_inv_f_coeffs_sym = [sp.sympify(g) for g in S_inv_f_coeffs]

        h1_ok = True
        h2_ok = True

        T_vars = sp.symbols(f't1:{len(S_gens_sym)+1}')
        if not isinstance(T_vars, tuple):
            T_vars = (T_vars,)

        all_vars = list(R_vars_sym) + list(T_vars)

        K_prime = list(K_gens_sym)
        for t, s in zip(T_vars, S_gens_sym):
            K_prime.append(t * s - 1)
            
        if not K_prime:
            K_prime_for_gb = [sp.Integer(0)]
        else:
            K_prime_for_gb = K_prime

        try:
            GB_K_prime = sp.groebner(K_prime_for_gb, all_vars)
            
            valid_S_inv = True
            max_len = max(len(f_coeffs_sym), len(S_inv_f_coeffs_sym))
            for i in range(max_len):
                c1 = f_coeffs_sym[i] if i < len(f_coeffs_sym) else sp.Integer(0)
                c2 = S_inv_f_coeffs_sym[i] if i < len(S_inv_f_coeffs_sym) else sp.Integer(0)
                if sp.reduced(c1 - c2, GB_K_prime)[1] != 0:
                    valid_S_inv = False
                    break
            
            if not valid_S_inv:
                neg_q_ok = False
            else:
                I_ideal = K_prime + f_coeffs_sym
                J_ideal = K_prime + S_inv_f_coeffs_sym

                if not I_ideal:
                    I_ideal = [sp.Integer(0)]
                if not J_ideal:
                    J_ideal = [sp.Integer(0)]

                GB_I = sp.groebner(I_ideal, all_vars)
                GB_J = sp.groebner(J_ideal, all_vars)

                I_subset_J = all(sp.reduced(a, GB_J)[1] == 0 for a in f_coeffs_sym)
                J_subset_I = all(sp.reduced(b, GB_I)[1] == 0 for b in S_inv_f_coeffs_sym)

                ideals_equal = I_subset_J and J_subset_I
                neg_q_ok = not ideals_equal

        except Exception:
            neg_q_ok = False

    except Exception:
        h1_ok = False
        h2_ok = False
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]