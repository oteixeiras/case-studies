#class of date 02/04/2025

import hashlib
import json
import datetime
from typing import cast

class Block:
    def __init__(self, index: int, data: str, prior_hash='') -> None:
        self.index = index
        self.data = data
        self.prior_hash = prior_hash
        self.timestamp = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S:%f")
        self.hash = self.create_hash()

    def create_hash(self)-> str:
        blockstring = f"{self.index}{self.prior_hash}{self.timestamp}{self.data}".encode()
        return hashlib.sha256(blockstring).hexdigest()

class StudentBlockChain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
    
    def create_genesis_block(self):
        return Block(
            index=0,
            data='MyFirstBlockChainUVV.br',
            prior_hash='0'
        )
    
    def get_last_block(self)-> Block | None:
        if len(self.chain) == 0:
            return None
        return self.chain[-1]
    
    def add_block(self, data: str)-> None:
        last_block = cast(Block, self.get_last_block())

        new_block = Block(
            index=last_block.index + 1,
            data=data,
            prior_hash=last_block.hash
        )
        self.chain.append(new_block)
    
    def validate_chain(self)-> bool:
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.create_hash():
                return False
            
            if current_block.prior_hash != previous_block.hash:
                return False
        
        return True

if __name__ == "__main__": 
    student_coin = StudentBlockChain()
    firstblock = student_coin.create_genesis_block()
    student_coin.add_block(data="SecondBlock")
    student_coin.add_block(data="ThirdBlock")
    print(json.dumps(student_coin.chain, default=lambda o: o.__dict__, indent=4))
    print(student_coin.validate_chain())