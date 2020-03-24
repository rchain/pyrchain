from rchain.client import RClient
from rchain.crypto import PrivateKey
from rchain.vault import VaultAPI

not_exist = PrivateKey.from_hex('7697cf972024cee7186decc5afcd52905d28e357087e3626038d7c6f5927fb49')

a = PrivateKey.from_hex("304b2893981c36122a687c1fd534628d6f1d4e9dd8f44569039ea762dae2d3e7")
b = PrivateKey.from_hex("5438ac0bde91bb813c7b4b17f215cd6ad52b19e7bcbf1f7907adb1d69c8aa7b1")
not_exist_2 = PrivateKey.from_hex('f3db47a958af0ba81fda8503bb13e60acd083177e6440859efade003c8fb44a3')

origin = 100000000
def pKey(k: PrivateKey):
    print(k.to_hex())
    print(k.get_public_key().to_hex())
    print(k.get_public_key().get_rev_address())
    print(k.get_public_key().get_eth_address())

# pKey(a)
# pKey(b)
# with RClient("localhost", 40402) as client:
#     vault = VaultAPI(client)
#     vault.transfer(a.get_public_key().get_rev_address(), b.get_public_key().get_rev_address(), int(origin/2), a)
#     successful = client.propose()
#
#     vault.transfer(a.get_public_key().get_rev_address(), not_exist.get_public_key().get_rev_address(), 10000, a)
#     not_ = client.propose()
#
#     vault.transfer(a.get_public_key().get_rev_address(), b.get_public_key().get_rev_address(), 2 * origin, a)
#     en = client.propose()
#
#     print(successful)
#     print(not_)
#     print(en)

successfulB = "a5160a2074f9892ab26913ee897fabde9c3851c610f693aa6583392d82018b73"
hangB = "d67be972179df2ffa0f28b7aa5f08521e78540919f855e4d48e6f0b8655a0bc9"
not_enough = "b4b009b46d5964f5b9ce5c64f1766ff94c397a400d707ad7d288e476ac1de436"
genesis = "603f6650895e84f9d63939e7877195805d4036499f5f5cf34538d6139f62b8ed"

class Report:
    def __init__(self, pre, user, refund):
        self.pre = pre
        self.user = user
        self.refund = refund

class GenesisReport:
    def __init__(self, deploys):
        self.registry = deploys[0]
        self.list_ops = deploys[1]
        self.either = deploys[2]
        self.nonNegativeNumber = deploys[3]
        self.makeMint = deploys[4]
        self.authKey = deploys[5]
        self.revVault = deploys[6]
        self.multiSigRevVault = deploys[7]

class Transaction:
    def __init__(self, from_addr, to_addr, amount, ret_unforgeable):
        self.from_addr = from_addr
        self.to_addr = to_addr
        self.amount = amount
        self.ret_unforgeable = ret_unforgeable
        self.success = None

def get_report(client, block_hash):
    b = client.show_block(block_hash)
    resp_successfully = client.get_event_data(block_hash)
    deploys = resp_successfully.result.deploys
    d = deploys[0]
    reports = d.report
    precharge = reports[0]
    user_d = reports[1]
    refund = reports[2]
    return Report(precharge, user_d, refund)

def get_genesis_report(client, block_hash):
    b = client.show_block(block_hash)
    resp_successfully = client.get_event_data(block_hash)
    deploys = resp_successfully.result.deploys
    return deploys

def analyse_revVault_deploy(deploy):
    r = deploy.report[0]
    produce, consume, comm = catagory_events(r.events)
    transfer_template_unfor = find_transfer_template(consume)
    return transfer_template_unfor[0].channels[0]

def find_transfer_comm(report, transfer_template_unforgeable):
    transfers = []
    transactions = []
    for event in report.events:
        report_type = event.WhichOneof('report')
        if report_type == 'comm':
            channel = event.comm.consume.channels[0]
            if channel == transfer_template_unforgeable:
                transfers.append(event)
                from_addr = event.comm.produces[0].data.pars[0].exprs[0].g_string
                to_addr = event.comm.produces[0].data.pars[2].exprs[0].g_string
                amount = event.comm.produces[0].data.pars[3].exprs[0].g_int
                ret = event.comm.produces[0].data.pars[5]
                transactions.append(Transaction(from_addr, to_addr, amount, ret))
    for transaction in transactions:
        for event in report.events:
            report_type = event.WhichOneof('report')
            if report_type == 'produce':
                channel = event.produce.channel
                if channel == transaction.ret_unforgeable:
                    data = event.produce.data
                    transaction.success = data
    return transactions


def find_transfer_template(consumes):
    result = []
    deposit = []
    for consume in consumes:
        consume = consume.consume
        patterns = consume.patterns
        if patterns[0].freeCount == 6:
            result.append(consume)
        if patterns[0].freeCount == 3:
            deposit.append(consume)
    return result

def find_first_string_pattern(comms, g_string):
    for comm in comms:
        consume = comm.comm.consume
        patterns = consume.patterns
        for p in patterns:
            t = p.patterns[0]
            if len(t.exprs) > 0 and t.exprs[0].g_string==g_string:
                return comm
    return None

def find_consume_channel_unforgeable(comms, unforge):
    for comm in comms:
        consume = comm.comm.consume
        patterns = consume.patterns
        channel = consume.channels
        for c in channel:
            if len(c.unforgeables) > 0 and c.unforgeables[0].g_private_body == unforge.unforgeables[0].g_private_body:
                return comm
    return None
def catagory_events(events):
    produce = []
    consume = []
    comm = []
    for event in events:
        report_type = event.WhichOneof('report')
        if report_type == "produce":
            produce.append(event)
        elif report_type == 'consume':
            consume.append(event)
        elif report_type == 'comm':
            comm.append(event)
        else:
            raise
    return (produce, consume, comm)

with RClient("localhost", 40402) as client:
    # reports = get_report(client, successfulB)
    reports = get_genesis_report(client, "603f6650895e84f9d63939e7877195805d4036499f5f5cf34538d6139f62b8ed")
    # produce, consume, comm = analyse_revVault_deploy(reports[6])
    transfer_template = analyse_revVault_deploy(reports[6])
    successful = get_report(client, successfulB)
    successfule_transfer = find_transfer_comm(successful.user, transfer_template)

    hangB_r = get_report(client, hangB)
    hang_trans = find_transfer_comm(hangB_r.user, transfer_template)

    not_enough_r = get_report(client, not_enough)
    not_enough_trans = find_transfer_comm(not_enough_r.user, transfer_template)
    # r = reports[6].report[0]
    # produce, consume, comm = catagory_events(r.events)
    # report_not_exist_ = get_report(client, hangB)
    # report_not_enough= get_report(client, not_enough)

    # produce, consume, comm = catagory_events(reports.user.events)
    # for c in comm:
    #     consume = c.comm.consume
    #     patterns = consume.patterns
    #     for p in patterns:
    #         t = p.patterns[0]
    #         if len(t.exprs) > 0 and t.exprs[0].g_string=='transfer':
    #             transfer_comm = c
    #
    # vault_unforgeable = transfer_comm.comm.consume.channels[0]
    # k = client.get_continuation(vault_unforgeable, 1)
    # data = client.get_data_at_name(d.comm.produces[0].data.pars[0], 1)
    print(1)
