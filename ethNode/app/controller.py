

from . import jsonrpc
from . import service

from .utils import response_wrap

@response_wrap
@jsonrpc.method("constructTx")
def construct_tx(addressFrom,addressTo,value):
    return service.construct_tx(addressFrom,addressTo,value)

@response_wrap
@jsonrpc.method("constructERC20Tx")
def construct_erc20_tx(addressFrom,addressTo,value):
    return service.construct_erc20_tx(addressFrom,addressTo,value)

@response_wrap
@jsonrpc.method("sign")
def sign(txData,privtKey):
    return service.sign(txData,privtKey)

@response_wrap
@jsonrpc.method("broadcast")
def broadcast(rawTx,signature):
    return service.broadcast(rawTx,signature)



@response_wrap
@jsonrpc.method("getBalance")
def get_balance(address,erc20):
    if erc20!="ERC20TNC":
        return None
    return service.get_balance(address,erc20)


@response_wrap
@jsonrpc.method("invokeContract")
def invoke_contract(invoker,contractAddress,method,args):
    return service.invoke_contract(invoker,contractAddress,method,args)