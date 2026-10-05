from pricer import (black_scholes, mc_price, delta_closed_form,
                    delta_bump, parity_check, implied_vol)

S = 100
K = 100
r = 0.05
sigma = 0.2
T = 1
seed = 42


def test_black_scholes_call():
    price = black_scholes(S, K, r, sigma, T, "call")
    assert abs(price - 10.4506) < 0.0001


def test_black_scholes_put():
    price = black_scholes(S, K, r, sigma, T, "put")
    assert abs(price - 5.5735) < 0.0001


def test_mc_close_to_black_scholes():
    for option_type in ["call", "put"]:
        bs_price = black_scholes(S, K, r, sigma, T, option_type)
        price, std_error = mc_price(S, K, r, sigma, T, 1000000, option_type, seed)
        assert abs(price - bs_price) < 3 * std_error


def test_put_call_parity():
    call_price, call_se = mc_price(S, K, r, sigma, T, 1000000, "call", seed)
    put_price, put_se = mc_price(S, K, r, sigma, T, 1000000, "put", seed)
    left_side, right_side = parity_check(S, K, r, T, call_price, put_price)
    allowed = 3 * (call_se + put_se)
    assert abs(left_side - right_side) < allowed


def test_delta_bump_close_to_closed_form():
    exact = delta_closed_form(S, K, r, sigma, T, "call")
    bumped = delta_bump(S, K, r, sigma, T, 1000000, "call", seed)
    assert abs(exact - bumped) < 0.01


def test_implied_vol_round_trip():
    for strike in [80, 90, 100, 110, 120]:
        for option_type in ["call", "put"]:
            price = black_scholes(S, strike, r, 0.25, T, option_type)
            recovered = implied_vol(price, S, strike, r, T, option_type)
            assert abs(recovered - 0.25) < 0.0001


def test_implied_vol_below_intrinsic():
    failed_cleanly = False
    try:
        implied_vol(5.0, 100, 90, 0.05, 1, "call")
    except ValueError as error:
        failed_cleanly = "intrinsic" in str(error)
    assert failed_cleanly


all_tests = [
    test_black_scholes_call,
    test_black_scholes_put,
    test_mc_close_to_black_scholes,
    test_put_call_parity,
    test_delta_bump_close_to_closed_form,
    test_implied_vol_round_trip,
    test_implied_vol_below_intrinsic,
]

passed = 0
for test in all_tests:
    try:
        test()
        print("PASS", test.__name__)
        passed += 1
    except AssertionError:
        print("FAIL", test.__name__)

print(f"{passed} of {len(all_tests)} tests passed")
