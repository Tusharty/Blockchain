#!/usr/bin/env python
#Blackchain class whose constructor creates an initial empty list(to store our blockchain)
#!flask/bin/python
#!/usr/bin/env python

import hashlib
import json
from time import time
from uuid import uuid4
from textwrap import dedent
from flask import Flask, jsonify, request
import requests

class Blockchain(object):

    def __init__(self):
        self.chain = []
        self.current_transactions = []

        #create the genesis block
        self.new_block(previous_hash = '1', proof = 100)


    def new_block(self, proof, previous_hash):
        #create a new block and add it to the chain
        """
        create a new block in the Blockchain
         :param : <int> the proof give by the 3proof of the work algorithm
         :param previous_hash: (optional) <str> hash of previous block
        :return: <dict> new Block
        """
        block  = {
            'index' : len(self.chain) + 1,
            'timestamp' : time(),
            'transactions' : self.current_transactions,
            'proof' : proof,
            'previous_hash' : previous_hash or self.hash(self.chain[-1]),
        }

        #reset the current list of transactions
        self.current_transactions = []

        self.chain.append(block)

        return block


    def new_transaction(self, sender, recipient, amount):
        #adds new transaction to the list of transactions

        """
        CREATE a new transaction to go into the next mined block

        :param sender : <str> address of the sender
        :param recipient: <str> address of the recipient
        :param amount: <int> amount
        :return: <int> the index of the block that will hold this transaction
        """

        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.last_block['index'] + 1

    @property
    def last_block(self):
        #return the last block in chain
        return self.chain[-1]


    @staticmethod
    def hash(block):
        #hashes a block

        """
        create a SHA-256 hash of a block

        :param block : <dict> Block
        :return: <str>
        """

        # we must be sure that the dictionary is ordered or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys= True).encode()
        return hashlib.sha256(block_string).hexdigest()



    def proof_of_work(self, last_proof):
        """
        simple proof of work algorithm
         -find a number p' such that hash(pp') contains leading 4 zeros, where p is the previous p'
         -p is the previous proof, and p' is the new proof

         :param last_proof : <int>
         :return: <int>
        """

        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof


    @staticmethod
    def valid_proof(last_proof, proof):
        """
        validate the proof : Does hash(last_proof, proof) contains 4 leading zeroe?
        :param last_proof: <int> previous proof
        :param proof: <int> current proof
        :return: <bool> True  if correct, False if not.

        """
        guess = f'{last_proof}{proof}{last_hash}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

#instantiate the node
app = Flask(__name__)

#create a globally unique address for this node
node_identifier = str(uuid4()).replace(('-',''))

#initiating the blockchain
blockchain = Blockchain



@app.route('/mine', methods = ['GET'])
def mine():
    # we need to run the proof of work algorithm to get the next work
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)


    #rewarding 1 coin for finding the proof
    # the sender is 0 to signifies that this node has mined a new coin.

    blockchain.new_transaction(
        sender="0",
        recipient= node_identifier,
        amount=1,
    )

    #forge the new block by adding it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)
    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200


@app.route('/transactions/new',methods = ['POST'])
def new_transaction():

    values = request.get_json()

    #check for required field in posted data

    required = ['sender','recipient','amount']
    if not all (k in values for k in required):
        return 'missing values', 400

    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message':f'Transaction will be added to block {index}'}
    return jsonify(response), 201


@app.route('/chain',methods = ['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }

    return jsonify(response), 200


if __name__ == '__main__':
    app.run(host = '0.0.0.0', port=5000)























