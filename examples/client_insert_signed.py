# https://github.com/tgrospic/rnode-client-js/blob/master/src/nodejs/client-insert-signed.js
# the logic below mostly copied from the logic of the link above

from rchain.client import RClient
from rchain.crypto import PrivateKey
from rchain.pb.RhoTypes_pb2 import (
    Bundle, ETuple, Expr, GPrivate, GUnforgeable, Par,
)

host = "localhost"
port = 40402

deployKey = PrivateKey.generate()
timestamp = 1559156356769
nonce = 9223372036854775807
publicKey = deployKey.get_public_key()

with RClient(host, port) as client:
    ret = client.previewPrivateNames(publicKey, timestamp, 3)
    unforgeable = ret.payload.ids[0]

print(unforgeable)
dataToSign = Par(
    exprs=[
        Expr(e_tuple_body=
        ETuple(ps=[
            Par(exprs=[Expr(g_int=nonce)]),
            Par(bundles=[
                Bundle(body=Par(unforgeables=[GUnforgeable(g_private_body=GPrivate(id=unforgeable))]),
                       writeFlag=True,
                       readFlag=False)])
        ])
        )
    ]
)
sigArray = deployKey.sign_deterministic(dataToSign.SerializeToString())
signatureHex = sigArray.hex()
publicKeyHex = publicKey.to_hex()

contract = """
    new MyContract, rs(`rho:registry:insertSigned:secp256k1`), uriOut, out(`rho:io:stdout`)
    in {{
      contract MyContract(ret) = {{
        ret!("Hello Arthur!")
      }} |
      rs!(
        "{publicKeyHex}".hexToBytes(),
        ({nonce}, bundle+{{*MyContract}}),
        "{signatureHex}".hexToBytes(),
        *uriOut
      ) |
      for(@uri <- uriOut) {{
        out!(("Registered", uri))
      }}
    }}
""".format(publicKeyHex=publicKeyHex, nonce=nonce, signatureHex=signatureHex)

print(contract)
