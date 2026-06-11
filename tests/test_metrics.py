from analytics.metrics import calculate_ctr, calculate_cpc, calculate_roas

def test_calculate_ctr():
    assert calculate_ctr(50, 1000) == 5.0
    assert calculate_ctr(0, 500) == 0.0

def test_calculate_cpc():
    assert calculate_cpc(100.0, 50) == 2.0

def test_calculate_roas():
    assert calculate_roas(200.0, 50.0) == 4.0
