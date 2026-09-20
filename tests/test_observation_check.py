from procejour.observation_check import observation_meets_spec


def test_observation_meets_spec_with_range():
    assert not observation_meets_spec("1.39", "decimal:2", "[1.40, 1.60]")
    assert not observation_meets_spec("1.61", "decimal:2", "[1.40, 1.60]")

    assert observation_meets_spec("1.40", "decimal:2", "[1.40, 1.60]")
    assert observation_meets_spec("1.50", "decimal:2", "[1.40, 1.60]")
    assert observation_meets_spec("1.60", "decimal:2", "[1.40, 1.60]")
