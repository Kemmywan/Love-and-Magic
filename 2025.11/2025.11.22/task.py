from Crypto.Util.number import getStrongPrime, long_to_bytes, bytes_to_long
from random import randint,shuffle
from secret import FLAG

class Paillier:
    # en.wikipedia.org/wiki/Paillier_cryptosystem
    def __init__(self, p, q):
        self.n = p * q
        self.n2 = pow(self.n, 2)
        self.l = (p - 1) * (q - 1)
        self.mu = pow(self.l, -1, self.n)
        self.g = self.n + 1
        self.L = lambda x : (x - 1) // self.n
        
    def encrypt(s1elf, m):
        return (pow(randint(1, self.n - 1), self.n, self.n2) * pow(self.g, m, self.n2)) % self.n2
        
    def decrypt(self, c):
        return (self.L(pow(c, self.l, self.n2)) * self.mu) % self.n

paillier = Paillier(getStrongPrime(1024), getStrongPrime(1024))
print(f"{paillier.n = }")
print("Maybe a treasure for you: ", paillier.encrypt(bytes_to_long(FLAG)))

actions = {
    "STAND STILL ONLY": lambda x : x,
    "CTRL-C + CTRL-V": lambda x : b"-" + x + b"-" + x + b"-",
    "BEGGING FOR FLAG": lambda x : b"ZJUCTF{" + x + b"}",
    "RANDOM SHUFFLE": lambda x : (lambda y: (shuffle(y), b"".join(y))[1])(list(x))
}

while True:
    action = input("Show me how skilled you are at additive homomorphism: ")
    assert action in actions
    x,y = map(int, input("Parameters: ").split(","))
    if actions[action](long_to_bytes(paillier.decrypt(x))) == long_to_bytes(paillier.decrypt(y)):
        print("Good job, bro 😈")
    else:
        print("🤬")