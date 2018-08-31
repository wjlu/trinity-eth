"""Author: Trinity Core Team

MIT License

Copyright (c) 2018 Trinity

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""
from trinity import SUPPORTED_ASSET_TYPE


Configure = {
    "alias": "TrinityEthNode",# you can rename your node
    "GatewayURL": "http://localhost:8177",
    "AutoCreate": True, # if the wallet accept the create channel request automatically
    "Channel":{
               "TNC":{"CommitMinDeposit": 1,   # the min commit deposit
                       "CommitMaxDeposit": 5000,# the max commit deposit
                      "Fee": 0.01 # gateway fee
                      }
                      },#
    "MaxChannel":100, # the max number to create channel, if 0 , no limited
    "NetAddress":"localhost",
    "RpcListenAddress":"0.0.0.0",
    "NetPort":"21556",
    "GatewayTCP":"localhost:8189",
    "AssetType":{
        "TNC": SUPPORTED_ASSET_TYPE['TNC']
    },
    "BlockChain":{
        "EthNetUrl" : "https://ropsten.infura.io"
    },
    "DataBase":{"url": "http://localhost:20554"
    },
    "Version":"v0.2.1",
    "Magic":{
        "Block":5274657374,##binascii.b2a_hex(u"Rtest".encode("utf8"))
        "Trinity":19990331
    }
}