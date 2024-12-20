import hashlib, time, json, os, platform, subprocess

# Get the directory path of the current .py file
current_dir = os.path.dirname(os.path.abspath(__file__))

def cls():
    system = platform.system()
    if system == 'Windows':
        subprocess.run('cls', shell=True)
    elif system in ('Linux', 'Darwin'):
        subprocess.run('clear', shell=True)

class Blockchain:
    def __init__(self):
        self.chain = []
        self.difficulty = 1  # Initial difficulty set to the lowest possible
        self.block_time = 600  # Target block time in seconds (10 minutes)
        self.adjustment_interval = 2016  # Number of blocks between difficulty adjustments
        self.load_chain()

    def create_block(self, nonce, previous_hash, owner_address):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'nonce': nonce,  # This is the nonce
            'previous_hash': previous_hash,
            'difficulty': self.difficulty,
            'owner_address': owner_address
        }
        self.chain.append(block)
        self.adjust_difficulty()
        self.save_chain()
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_nonce):
        new_nonce = 1
        check_proof = False
        while not check_proof:
            # SHA-3 hashing
            hash_operation = hashlib.sha3_256(
                str(new_nonce**2 - previous_nonce**2).encode()
            ).hexdigest()
            if hash_operation[:self.difficulty] == "0" * self.difficulty:
                check_proof = True
            else:
                new_nonce += 1
        return new_nonce

    def hash(self, block):
        encoded_block = str(block).encode()
        return hashlib.sha3_256(encoded_block).hexdigest()

    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_nonce = previous_block['nonce']
            nonce = block['nonce']
            difficulty = block['difficulty']
            hash_operation = hashlib.sha3_256(
                str(nonce**2 - previous_nonce**2).encode()
            ).hexdigest()
            if hash_operation[:difficulty] != "0" * difficulty:
                return False
            previous_block = block
            block_index += 1
        return True

    def save_chain(self):
        try:
            if os.path.exists(os.path.join(current_dir, 'blockchain.json')):
                with open(os.path.join(current_dir, 'blockchain.json'), 'r') as file:
                    existing_chain = json.load(file)
                    self.chain = existing_chain + self.chain[len(existing_chain):]
            with open(os.path.join(current_dir, 'blockchain.json'), 'w') as file:
                json.dump(self.chain, file)
        except FileNotFoundError:
            with open(os.path.join(current_dir, 'blockchain.json'), 'w') as file:
                json.dump(self.chain, file)
        except Exception as e:
            print(f"Error saving blockchain: {e}")

    def load_chain(self):
        if os.path.exists(os.path.join(current_dir, 'blockchain.json')):
            try:
                with open(os.path.join(current_dir, 'blockchain.json'), 'r') as file:
                    self.chain = json.load(file)
                    if not self.chain:
                        self.create_block(nonce=1, previous_hash='0', owner_address='')
            except Exception as e:
                print(f"Error loading blockchain: {e}")
                self.chain = []
                self.create_block(nonce=1, previous_hash='0', owner_address='')
        else:
            self.create_block(nonce=1, previous_hash='0', owner_address='')

    def adjust_difficulty(self):
        if len(self.chain) % self.adjustment_interval == 0 and len(self.chain) != 0:
            expected_time = self.block_time * self.adjustment_interval
            actual_time = self.chain[-1]['timestamp'] - self.chain[-self.adjustment_interval]['timestamp']
            if actual_time < expected_time:
                self.difficulty += 1
            elif actual_time > expected_time:
                self.difficulty -= 1

# Crear blockchain
blockchain = Blockchain()
previous_block = blockchain.get_previous_block()

# Dirección del propietario
owner_address = "0xImaginateQueEstaEsTuDireccionDeWallet"

cls()
print(f"Python Blockchain Test: Running...\nMiner Address: {owner_address}\n")

# Minar bloques
while True:
    nonce = blockchain.proof_of_work(previous_block['nonce'])
    block = blockchain.create_block(nonce, blockchain.hash(previous_block), owner_address)
    cls()
    print(f"Python Blockchain Test: Running...\nMiner Address: {owner_address}\n\n" + json.dumps(block, indent=4))
    previous_block = block