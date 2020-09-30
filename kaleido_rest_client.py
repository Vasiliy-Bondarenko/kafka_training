import base64
from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware


class KaleidoEthereumProvider:
    w3: Web3

    def __init__(self):
        # FIXME
        USER = "xxxxxxxx"
        PASS = "xxxxxxxxxxxxxxxxx"
        RPC_ENDPOINT = "https://e0u9yrfjnc-e0v6nvzwc3-rpc.de0-aws.kaleido.io"

        # Encode the username and password from the app creds into USER:PASS base64 encoded string
        auth = USER + ":" + PASS
        encodedAuth = base64.b64encode(auth.encode('ascii')).decode('ascii')

        # Build the header object with the Basic auth and the standard headers
        headers = {'headers': {
            'Authorization': 'Basic %s' % encodedAuth,
            'Content-Type': 'application/json',
            'User-Agent': 'kaleido-web3py'
        }}

        # Construct a Web3 object by constructing and passing the HTTP Provider
        provider = HTTPProvider(
            endpoint_uri=RPC_ENDPOINT,
            request_kwargs=headers
        )
        self.w3 = Web3(provider)

        # Add the Geth POA middleware needed for ExtraData Header size discrepancies between consensus algorithms
        # See: http://web3py.readthedocs.io/en/stable/middleware.html#geth-style-proof-of-authority
        # ONLY for GETH/POA; If you are using quorum, comment out the line below
        self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    def getLatestBlock(self):
        return self.w3.eth.getBlock("latest")

    def transact(self, abi, contract_address, from_address, function_name, *args):
        contract = self.w3.eth.contract(
            address=self.w3.toChecksumAddress(contract_address),
            abi=abi,
        )

        contract_func = contract.functions[function_name]

        tx_hash = contract_func(*args).transact({
            "from": self.w3.toChecksumAddress(from_address)
        })

        return tx_hash

    def getTransactionReceipt(self, tx_hash):
        return self.w3.eth.waitForTransactionReceipt(tx_hash)

    def  call(self, abi, contract_address, function_name, *args):
        contract = self.w3.eth.contract(
            address=self.w3.toChecksumAddress(contract_address),
            abi=abi,
        )

        contract_function = contract.functions[function_name]

        return contract_function(*args).call()


if __name__ == '__main__':
    '''
    this is a little demo with SimpleStorage contract deployed on Kaleido
    '''

    p = KaleidoEthereumProvider()

    abi = """[
    {
      "constant": true,
      "inputs": [],
      "name": "storedData",
      "outputs": [
        {
          "name": "",
          "type": "uint256"
        }
      ],
      "payable": false,
      "stateMutability": "view",
      "type": "function"
    },
    {
      "anonymous": false,
      "inputs": [
        {
          "indexed": false,
          "name": "_message",
          "type": "string"
        }
      ],
      "name": "StorageSet",
      "type": "event"
    },
    {
      "constant": false,
      "inputs": [
        {
          "name": "x",
          "type": "uint256"
        }
      ],
      "name": "set",
      "outputs": [],
      "payable": false,
      "stateMutability": "nonpayable",
      "type": "function"
    }
  ]"""

    contract_address = "0xb286cdce944a22b162ccb639902e58c60d843be1"
    from_address = "0xd45ea2ab710e94667f234f4cd2a20800f10c9062"

    hash = p.transact(abi, contract_address, from_address, "set", 998)
    receipt = p.getTransactionReceipt(hash)
    print(receipt)

    print(p.call(abi, contract_address, "storedData"))
