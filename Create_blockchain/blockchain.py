#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  3 14:29:26 2021

@author: musta
"""
import datetime
import hashlib
import json
from flask import Flask, jsonify

#part 1  create the blockchain

class Blockchain:
     
    def __init__(self):
        self.chain = [];#difference blocks mined
        self.create_block(proof = 1, previous_hash = '0') #genesis block the first block 1
        
    def create_block(self, proof, previous_hash): #proof is the solution of the alog from the mining proccess 
        block = {'index': len(self.chain) +1 ,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash}
        #here where we define all the data that our block need to contain 
        
        self.chain.append(block)
        return block
        
    
    def get_previous_block(self):
        return self.chain[-1] #return the last block in the chain
    
    
    # this is the proof of work function, where we need to define a problem that is challange to solve but easy to verify 
    
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        
        while check_proof is False:
            #has_opearton using the new_proof will try to create random hexdechimal format which the first 3 charactar are 4 zeros if is not will increament new_proof by 1 and try
            #until it get the write one
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest() #this contain the problem to solve #encode add b infront of 
             
            if hash_operation[:4] == '0000':#leading zero condition is our condition that has to be meet for the algotihm 
                check_proof = True
            
            else:
                new_proof += 1
                
        return new_proof
                
                
            
    def hash(self, block):
        
        #convert the dictionary block into a string using the json.dumps library
        
        encoded_block = json.dumps(block, sort_keys = True).encode() #it will sort the block dictionary is sorted by key 
        
        return hashlib.sha256(encoded_block).hexdigest() #return the cryptografic hash of the block
    
    
    #check if our block chain is valid, and we need to check 2 things
    # 1- check that the previous hash of each block is equal to the hash of its previous block
    # 2 - check that the proof of the each block is valid according to our proof of work function
    
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

@app.route('/get_chain', methods=['GET'])#declare the route and the request method get

def get_chain():#display the full chain of the blockchain
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
    

    

# Running the app

app.run(host = '0.0.0.0', port = 5000)







