import time

from rchain.client import RClient
from rchain.crypto import PrivateKey
from rchain.vault import VaultAPI
from .utils_test import BlockSee, wait_using_wall_clock_time_or_fail

term = "Nil"
p1 = PrivateKey.from_hex("016120657a8f96c8ee5c50b138c70c66a2b1366f81ea41ae66065e51174e158e")
p2 = PrivateKey.from_hex("61e594124ca6af84a5468d98b34a4f3431ef39c54c6cf07fe6fbf8b079ef64f6")
p3 = PrivateKey.from_hex("34d969f43affa8e5c47900e6db475cb8ddd8520170ee73b2207c54014006ff2b")
p4 = PrivateKey.from_hex("5438ac0bde91bb813c7b4b17f215cd6ad52b19e7bcbf1f7907adb1d69c8aa7b1")
p5 = PrivateKey.from_hex("304b2893981c36122a687c1fd534628d6f1d4e9dd8f44569039ea762dae2d3e7")


def test_grpc_client():
    with RClient("localhost", 40402) as client:
        block_infos = client.show_blocks(depth=10)
        assert len(block_infos) > 0

        deploy_1_timestamp = int(time.time() * 1000)
        deploy_id_1 = client.deploy(p1, "Nil", 1, 10000, 1, deploy_1_timestamp)

        block_hash_1 = client.propose()

        block_info_1 = client.find_deploy(deploy_id_1)
        assert block_info_1.blockHash == block_hash_1
        block_info_1_detailed = client.show_block(block_info_1.blockHash)
        assert block_info_1_detailed.blockInfo.blockHash == block_hash_1
        deploy =  block_info_1_detailed.deploys[0]
        assert deploy.term == "Nil"
        assert deploy.timestamp == deploy_1_timestamp
        assert deploy.deployer == p1.get_public_key().to_hex()

        deploy_2_timestamp = int(time.time() * 1000)
        deploy_id_2 = client.deploy_with_vabn_filled(p1, "Nil", 1, 10000, deploy_2_timestamp)

        block_hash_2 = client.propose()

        last_finalized = client.last_finalized_block()
        is_finalized_block_hash_2 = client.is_finalized(block_hash_2)

def test_vault_api():
    init_amount = 100000000
    transfer_amount = 500000
    wait_timeout = 300
    not_exist = PrivateKey.generate()
    not_exist_2 = PrivateKey.generate()
    with RClient("localhost", 40402) as client:
        with RClient("localhost", 30302) as read_client:
            vault = VaultAPI(client)
            read_vault = VaultAPI(read_client)

            # transfer to an existing vault
            vault.transfer(p1.get_public_key().get_rev_address(), p2.get_public_key().get_rev_address(), transfer_amount, p1)
            b1 = client.propose()
            wait_using_wall_clock_time_or_fail(BlockSee(read_client, b1), wait_timeout)

            assert read_vault.get_balance(p2.get_public_key().get_rev_address()) == init_amount + transfer_amount

            # transfer to not existing vault
            vault.transfer(p3.get_public_key().get_rev_address(), not_exist.get_public_key().get_rev_address(), transfer_amount, p3)
            b2 = client.propose()
            wait_using_wall_clock_time_or_fail(BlockSee(read_client, b2), wait_timeout)
            assert read_vault.get_balance(p3.get_public_key().get_rev_address()) == init_amount

            # create the not existing vault
            vault.create_vault(not_exist.get_public_key().get_rev_address(), p1)
            b3 = client.propose()
            wait_using_wall_clock_time_or_fail(BlockSee(read_client, b3), wait_timeout)
            assert read_vault.get_balance(not_exist.get_public_key().get_rev_address()) == transfer_amount

            # transfer ensure
            vault.transfer_ensure(p4.get_public_key().get_rev_address(), not_exist_2.get_public_key().get_rev_address(), transfer_amount, p4)
            b4 = client.propose()
            wait_using_wall_clock_time_or_fail(BlockSee(read_client, b4), wait_timeout)
            assert read_vault.get_balance(p4.get_public_key().get_rev_address()) < init_amount - transfer_amount