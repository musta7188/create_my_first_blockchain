#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  3 14:29:26 2021

@author: musta
"""


import datetime
import hashlib
import json
from flask import Flask, jsonify, request
import requests
from uuid import uuid4
from urllib.parse import urlparse

#part 1  create a Cryptocurrency

class Blockchain:
     
    def __init__(self):
        self.chain = [];
        self.transactions= [] #transaction has to be added before and later create the block and add the transactions 
        self.create_block(proof = 1, previous_hash = '0')
        self.nodes = set()
        
    def create_block(self, proof, previous_hash):
        block = {'index': len(self.chain) +1 ,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash,
                 'transactions': self.transactions
                 }
        self.transactions = []; #after adding the transaction to the block we need to empty the list as no the same transaction goas in all the blocks
        self.chain.append(block)
        return block
        
    
    def get_previous_block(self):
        return self.chain[-1] 
    

    
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        
        while check_proof is False:

            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            
            if hash_operation[:4] == '0000':
                check_proof = True
            
            else:
                new_proof += 1
                
        return new_proof
                
                
            
    def hash(self, block):
        
        
        
        encoded_block = json.dumps(block, sort_keys = True).encode() 
        
        return hashlib.sha256(encoded_block).hexdigest() 
    
    

    
    def is_chain_valid(self, chain):
        previous_block = self.chain[0]
        block_index = 1
        
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
                
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            
            if hash_operation[:4] != '0000':
                return False
            
            previous_block = block
            block_index+=1
            
        return True
    
    
    
    def add_transactions(self, sender, receiver, amount):
        self.transactions.append({'sender': sender,
                                  'receiver': receiver,
                                  'amount': amount})
        previous_block = self.get_previous_block()
        
        return previous_block['index']+1
        
        
    def add_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)
        
        
    
    #the below function check what is the longest chain the blockchain between nodes, and if it found one which is longest that the current one it replace it 
    #and return true....the method use the request to male a call to the nodes using the IP addess of each node which is saved in the set of the ndoe
        
        
    def replace_chain(self):#find the longest chain in the nodes and replace the other nodes one with that one
        network = self.nodes
        longest_chain = None
        max_length = leng(self.chain)#current chain the blockchain, if we find one that is longer we going to replace it
         for nodes in network:
             response = requests.get(f'http://{node}/get_chain')
             if response.status_code == 200:
                 length = response.json()['length']
                 chain = response.json()['chain']
                 if length > max_length and self.is_chain_valid(chain):
                     max_length = length
                     longest_chain = chain
        
        if longest_chain:
            self.chain = longest_chain
            return True
    
        return False
        
        
        
        
        
#########################################################################################################################################################################################

#part 2 Mining our blockchain


#Creating a Web App


#Running on http://127.0.0.1:5000/
app = Flask(__name__)


app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

# Creating a Blockchain

blockchain = Blockchain()#create instance of the class blockchain

# Mining a new block

@app.route('/mine_block', methods=['GET'])#declare the route and the request method get



def mine_block():
    previous_block  = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    
    response = {'message':'Congratulations, you just mined a block!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash']
                }
    return jsonify(response), 200





# Getting the full Blockchain

@app.route('/get_chain', methods=['GET'])

def get_chain():
    response = {'chain':blockchain.chain,
                'length':len(blockchain.chain)}
    return jsonify(response), 200



#check validity of the blockchain


@app.route('/is_valid', methods=['GET'])


def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    
    if is_valid:
        response = {'message': 'All good. The Blockchain is valid.'}
    else:
        response = {'message': 'Huston, we have a problem. The Blockchain is not valid.'}
        
    return jsonify(response), 200
    


# Part 3 - Decentralizing our Blockchain 









    

# Running the app

app.run(host = '0.0.0.0', port = 5000)