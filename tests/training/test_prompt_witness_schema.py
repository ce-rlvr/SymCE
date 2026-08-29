from __future__ import annotations

from training.common.prompts import build_v2_user_message


def test_build_v2_user_message_appends_witness_schema():
    record = {
        "remaining_hypotheses": ["G is finite", "G is non-abelian"],
        "conclusion": "G is cyclic",
        "witness_schema": "Python tuple (G, H) of SymPy permutation groups. Example: (S3, A4)",
    }

    message = build_v2_user_message(record)

    assert "Claim: For all mathematical objects satisfying:" in message
    assert "Witness schema hint:" in message
    assert record["witness_schema"] in message
    assert message.endswith(
        "Use this structural hint when constructing the [COUNTEREXAMPLE: ...] expression."
    )


def test_build_v2_user_message_without_schema_remains_clean():
    record = {
        "remaining_hypotheses": ["G is finite"],
        "conclusion": "G is solvable",
    }

    message = build_v2_user_message(record)

    assert "Witness schema hint:" not in message
    assert "G is solvable" in message
