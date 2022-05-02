import annotated_types


def test_gt():
    gt = annotated_types.Gt(4)
    assert gt.bound == 4
