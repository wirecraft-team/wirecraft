from wirecraft_server import utils


def test_id_to_mac():
    # Test with a known ID
    id = 7983034
    mac = utils.id_to_mac(id)
    expected_mac = "79:cf:ba"

    # Check if the last three bytes match the expected values
    assert mac.endswith(expected_mac), f"Expected MAC to end with {expected_mac}, got {mac}"

    mac2 = utils.id_to_mac(id)
    # Check if the function is idempotent
    assert mac == mac2, f"Expected idempotency, got {mac} and {mac2}"

    id_from_mac = utils.mac_to_id(mac)
    # Check if we can revert the MAC address back to the original ID
    assert id == id_from_mac, f"Expected ID {id}, got {id_from_mac}"
