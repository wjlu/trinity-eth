#!/usr/bin/env python
# coding=utf-8

import time
import pymysql
import requests

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Numeric, Boolean, create_engine, or_
from sqlalchemy.orm import sessionmaker
from config import setting
from logzero import logger,logfile

# logfile("store_erc20_tx.log", maxBytes=1e6, backupCount=3)

pymysql.install_as_MySQLdb()
engine = create_engine('mysql://%s:%s@%s/%s' %(setting.MYSQLDATABASE["user"],
                                               setting.MYSQLDATABASE["passwd"],
                                               setting.MYSQLDATABASE["host"],
                                               setting.MYSQLDATABASE["db"]),
                       pool_size=5)

Session = sessionmaker(bind=engine)
Base = declarative_base()
session=Session()

class Erc20Tx(Base):
    __tablename__ = 'erc20_tx'
    id = Column(Integer, primary_key=True)
    tx_id = Column(String(256),unique=True)
    block_number = Column(Integer)
    contract = Column(String(64))
    address_from = Column(String(64),index=True)
    address_to = Column(String(64),index=True)
    value = Column(Numeric(16,8))
    block_timestamp=Column(Integer)
    hash_pushed=Column(Boolean,default=False)


    def save(self):
        session.add(self)
        session.commit()


def push_transfer(txId,addressFrom,addressTo,value,blockTimestamp):
    data = {
        "txId":txId,
        "addressFrom": addressFrom,
        "addressTo": addressTo,
        "value": value,
        "blockTimestamp":blockTimestamp
    }
    try:
        res = requests.post(setting.WEBAPI, json=data).json()
        return res["Code"]
    except:
        return None

def TransferMonitor():


    while True:
        exist_instance = session.query(Erc20Tx).filter(
            or_(Erc20Tx.address_from == setting.FUNDING_ADDRESS,
                Erc20Tx.address_to == setting.FUNDING_ADDRESS),
            Erc20Tx.has_pushed==False
        ).first()
        if exist_instance:
            res=push_transfer(exist_instance.tx_id,
                              exist_instance.address_from,
                              exist_instance.address_to,
                              exist_instance.value,
                              exist_instance.block_timestamp)
            if res==0:
                exist_instance.has_pushed=True
                exist_instance.save()
                # time.sleep(3)
        else:
            time.sleep(30)

if __name__ == "__main__":
    TransferMonitor()