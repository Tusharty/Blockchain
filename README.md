# Blockchain


Grind and learn


1:) Blockchain is an immutable, sequential chain of records called blocks
2:) they can contain transactions , files and any data
3:) they are chained together using Hashes


4:) Each block should has an index, a timestamp, a list of transactions, a proof and hash of the privious block


5:)
sample block
--------------

    block = {
        'index': 1,
        'timestamp': 1506057125.900785,
        'transactions': [
            {
                'sender':"845454sdf84564654654s6d5f4s6df4sj5",
                'recipient':"546dfsfsd5f4sd5fsd4f5sd4f6s45f6ds4f",
                'amount':5,
            }
        ],
        'proof': 5565654665,
        'previous_hash': "2sdfs54f65sd4fs5d4f6dfd4f42d4fd46d5f46s5d4f6sd54f6sd5f46s5df45ds4fd"
    }


6:) create a new transactio that will contain sender, recipient, amount and index of block

    def new_transaction(self, sender, recipient, amount):

        self.current_transaction.append({
                'sender': sender,
                'recipient': recipient,
                'amount': amount,
            })

        return self.last_block['index'] + 1

7:) when a new Blockchain is initiated we need to seed it with a genesis block (a block with no predecessors)
8:) we also need to add a proof to our genesis block which is the result of mining

9:) we need to create a genesis block in our constructor



UNDERSTANDING proof of Work
-----------------------------
10: A proof of work algorithm  is how new Blocks are created pr mined on the blockchain
11: the PoW is to discover a number which solves a problem(difficult to find but easy to verify)




let hash of some integer x multiplied by another y must end in 0

so (x*y) = 464654654sd56sdsd5.....0

=============================
lets fix x = 5


-------------------------------
from hashlib import sha256

x = 5
y = 0 # we dont know what y should be yet...

while sha256(f'{x*y}'.encode()).hexdigest()[-1] != "0":
    y += 1

print (f'the solution is y = {y}')

--------------------------------------

the solution is y  = 21 since the produced hash ends in 0:


hash(5 * 21) = 1253e936546e.....sdf54sdf54sd6f45sd6f46dfds54f20

===========================================

12:) In bitcoin the proof of work algorithm is called Hashcash
    the level of difficulty is determined by the no of character searched for in a string







