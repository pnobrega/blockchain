"""
Created on Thu Oct  1 19:05:19 2020
First Blockchain
@author: Paulo
"""

# Libraries
import datetime
import hashlib
import json
from flask import Flask, jsonify

# 1 - Bilding the blockchain


class Blockchain:

    def __init__(self):
        self.chain = []
        self.create_block(proof=1, previous_hash='0')

    def create_block(self, proof, previous_hash):
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash}
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(
                str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(
                str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
            return True

# 2 - Mining the blockchain


# Crating Web App
app = Flask(__name__)

# Create a Blockchain
Blockchain = Blockchain()

# mining the block


@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = Blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = Blockchain.proof_of_work(previous_proof)
    previous_hash = Blockchain.hash(previous_block)
    block = Blockchain.create_block(proof, previous_hash)
    response = {'message': 'Congratulation you just mined a block!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash']}
    return jsonify(response), 200

# Getting the full blockchain


@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {'chain': Blockchain.chain,
                'length': len(Blockchain.chain)}
    return jsonify(response), 200

# checking if the blockchain is valid


@app.route('/is_valid', methods=['GET'])
def is_valid():
    is_valid = Blockchain.is_chain_valid(Blockchain.chain)
    if is_valid:
        response = {'message': 'All good. The Blockchain is valid.'}
    else:
        response = {'Message': 'The Blockchain is not valid.'}
    return jsonify(response), 200


# Running the app
app.run(host='0.0.0.0', port='5000')
