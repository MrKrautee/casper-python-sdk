import base64
import pathlib
import secrets
import operator
from operator import itemgetter


def test_get_hash(LIB, vector_crypto_1):
    for data, hashes in [operator.itemgetter("data", "hashes")(i) for i in vector_crypto_1]:
        for algo, digest in [operator.itemgetter("algo", "digest")(j) for j in hashes]:
            algo = LIB.crypto.HashAlgorithm[algo]
            digest = bytes.fromhex(digest)
            assert digest == LIB.crypto.get_hash(data.encode("utf-8"), 32, algo)


def test_get_account(LIB, vector_crypto_2):
    for algo, pbk, account_key, accountHash in [operator.itemgetter("algo", "pbk", "accountKey", "accountHash")(i) for i in vector_crypto_2]:
        pbk = bytes.fromhex(pbk)
        account_key = bytes.fromhex(account_key)
        accountHash = bytes.fromhex(accountHash)
        algo = LIB.crypto.KeyAlgorithm[algo]
        assert algo == LIB.crypto.get_account_key_algo(account_key)
        assert account_key == LIB.crypto.get_account_key(algo, pbk)
        print(LIB.crypto.get_account_hash(account_key).hex())
        assert LIB.crypto.get_account_hash(account_key) == accountHash


def test_that_a_key_pair_can_be_generated(LIB, key_pair_specs):
    for key_algo, pvk_length, pbk_length in key_pair_specs:
        pvk, pbk = LIB.crypto.get_key_pair(key_algo)
        assert len(pvk) == pvk_length
        assert len(pbk) == pbk_length
        

def test_that_a_key_pair_can_be_deserialized_from_base64(LIB, key_pair_specs):
    for key_algo, _, _ in key_pair_specs:
        pvk, pbk = LIB.crypto.get_key_pair(key_algo)
        pvk_b64 = base64.b64encode(pvk)
        assert (pvk, pbk) == LIB.crypto.get_key_pair_from_base64(pvk_b64, key_algo)


def test_that_a_key_pair_can_be_deserialized_from_bytes(LIB, key_pair_specs):
    for key_algo, _, _ in key_pair_specs:
        pvk, pbk = LIB.crypto.get_key_pair(key_algo)
        pvk_pem = LIB.crypto.get_pvk_pem_from_bytes(pvk, key_algo)
        assert isinstance(pvk_pem, bytes)


def test_that_a_key_pair_can_be_deserialized_from_pem_file(LIB, key_pair_specs):
    for key_algo, _, _ in key_pair_specs:
        pvk, pbk = LIB.crypto.get_key_pair(key_algo)
        path_to_pvk_pem_file = LIB.crypto.get_pvk_pem_file_from_bytes(pvk, key_algo)
        assert pathlib.Path(path_to_pvk_pem_file).is_file()
        assert (pvk, pbk) == LIB.crypto.get_key_pair_from_pem_file(path_to_pvk_pem_file, key_algo)


def test_that_a_key_pair_can_be_deserialized_from_a_seed(LIB, key_pair_specs):
    for key_algo, pvk_length, pbk_length in key_pair_specs:
        seed = secrets.token_bytes(32)
        pvk, pbk = LIB.crypto.get_key_pair_from_bytes(seed, key_algo)
        assert len(pvk) == pvk_length
        assert len(pbk) == pbk_length


def test_that_a_public_key_can_be_deserialized_from_a_private_key_encoded_as_byte_array(LIB, vector_crypto_2):
    for fixture in vector_crypto_2:
        _, pbk = LIB.crypto.get_key_pair_from_bytes(
            bytes.fromhex(fixture["pvk"]),
            LIB.crypto.KeyAlgorithm[fixture["algo"]]
        )
        assert bytes.fromhex(fixture["pbk"]) == pbk


def test_that_a_public_key_can_be_deserialized_from_a_private_key_encoded_as_base64(LIB, vector_crypto_2):
    for fixture in vector_crypto_2:
        _, pbk = LIB.crypto.get_key_pair_from_base64(
            base64.b64encode(bytes.fromhex(fixture["pvk"])),
            LIB.crypto.KeyAlgorithm[fixture["algo"]]
        )
        assert bytes.fromhex(fixture["pbk"]) == pbk


def test_that_a_public_key_can_be_deserialized_from_a_private_key_encoded_as_hex(LIB, vector_crypto_2):
    for fixture in vector_crypto_2:
        _, pbk = LIB.crypto.get_key_pair_from_hex_string(
            fixture["pvk"],
            LIB.crypto.KeyAlgorithm[fixture["algo"]]
        )
        assert bytes.fromhex(fixture["pbk"]) == pbk


def test_get_signature(LIB, vector_crypto_3):
    for fixture in vector_crypto_3:
        data = fixture["data"].encode("utf-8")
        key_algo = LIB.crypto.KeyAlgorithm[fixture["signingKey"]["algo"]]
        key_pvk = bytes.fromhex(fixture["signingKey"]["pvk"])
        assert fixture["sig"] == LIB.crypto.get_signature(data, key_pvk, key_algo).hex()
