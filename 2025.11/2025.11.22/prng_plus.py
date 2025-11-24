#!/usr/bin/env python3
# local test: `./task.py` + `nc 127.0.0.1 12600`

import random
import signal
import socketserver
import string
from hashlib import sha256
from os import urandom
from Crypto.Util.number import getStrongPrime

FLAG = [b"ZJUCTF{test1}"]
LEAK_LIMIT = [6]
TIME_LIMIT = [3]
TOTAL = 20

BITS = [512]

BANNER = b"""
          _____                    _____                    _____                    _____                            _____                    _____            _____                    _____          
         /\    \                  /\    \                  /\    \                  /\    \                          /\    \                  /\    \          /\    \                  /\    \         
        /::\    \                /::\    \                /::\____\                /::\    \                        /::\    \                /::\____\        /::\____\                /::\    \        
       /::::\    \              /::::\    \              /::::|   |               /::::\    \                      /::::\    \              /:::/    /       /:::/    /               /::::\    \       
      /::::::\    \            /::::::\    \            /:::::|   |              /::::::\    \                    /::::::\    \            /:::/    /       /:::/    /               /::::::\    \      
     /:::/\:::\    \          /:::/\:::\    \          /::::::|   |             /:::/\:::\    \                  /:::/\:::\    \          /:::/    /       /:::/    /               /:::/\:::\    \     
    /:::/__\:::\    \        /:::/__\:::\    \        /:::/|::|   |            /:::/  \:::\    \                /:::/__\:::\    \        /:::/    /       /:::/    /               /:::/__\:::\    \    
   /::::\   \:::\    \      /::::\   \:::\    \      /:::/ |::|   |           /:::/    \:::\    \              /::::\   \:::\    \      /:::/    /       /:::/    /                \:::\   \:::\    \   
  /::::::\   \:::\    \    /::::::\   \:::\    \    /:::/  |::|   | _____    /:::/    / \:::\    \            /::::::\   \:::\    \    /:::/    /       /:::/    /      _____    ___\:::\   \:::\    \  
 /:::/\:::\   \:::\____\  /:::/\:::\   \:::\____\  /:::/   |::|   |/\    \  /:::/    /   \:::\ ___\          /:::/\:::\   \:::\____\  /:::/    /       /:::/____/      /\    \  /\   \:::\   \:::\    \ 
/:::/  \:::\   \:::|    |/:::/  \:::\   \:::|    |/:: /    |::|   /::\____\/:::/____/  ___\:::|    |        /:::/  \:::\   \:::|    |/:::/____/       |:::|    /      /::\____\/::\   \:::\   \:::\____\
\::/    \:::\  /:::|____|\::/   |::::\  /:::|____|\::/    /|::|  /:::/    /\:::\    \ /\  /:::|____|        \::/    \:::\  /:::|____|\:::\    \       |:::|____\     /:::/    /\:::\   \:::\   \::/    /
 \/_____/\:::\/:::/    /  \/____|:::::\/:::/    /  \/____/ |::| /:::/    /  \:::\    /::\ \::/    /          \/_____/\:::\/:::/    /  \:::\    \       \:::\    \   /:::/    /  \:::\   \:::\   \/____/ 
          \::::::/    /         |:::::::::/    /           |::|/:::/    /    \:::\   \:::\ \/____/                    \::::::/    /    \:::\    \       \:::\    \ /:::/    /    \:::\   \:::\    \     
           \::::/    /          |::|\::::/    /            |::::::/    /      \:::\   \:::\____\                       \::::/    /      \:::\    \       \:::\    /:::/    /      \:::\   \:::\____\    
            \::/____/           |::| \::/____/             |:::::/    /        \:::\  /:::/    /                        \::/____/        \:::\    \       \:::\__/:::/    /        \:::\  /:::/    /    
             ~~                 |::|  ~|                   |::::/    /          \:::\/:::/    /                          ~~               \:::\    \       \::::::::/    /          \:::\/:::/    /     
                                |::|   |                   /:::/    /            \::::::/    /                                             \:::\    \       \::::::/    /            \::::::/    /      
                                \::|   |                  /:::/    /              \::::/    /                                               \:::\____\       \::::/    /              \::::/    /       
                                 \:|   |                  \::/    /                \::/____/                                                 \::/    /        \::/____/                \::/    /        
                                  \|___|                   \/____/                                                                            \/____/          ~~                       \/____/                                                                                                                                                                                                                 
"""


class PRNG_PLUS_1(object):
    """
    PRNG based on Quaternion.
    """

    def __init__(self, bits):
        self.p = getStrongPrime(bits)
        self.n = random.randrange(1, self.p)
        self.a = [random.randrange(1, self.p) for _ in range(4)]
        self.b = self.pow(self.a, self.n)

    def mul(self, x, y):
        return [
            (x[0] * y[0] - x[1] * y[1] - x[2] * y[2] - x[3] * y[3]) % self.p,
            (x[0] * y[1] + x[1] * y[0] + x[2] * y[3] - x[3] * y[2]) % self.p,
            (x[0] * y[2] - x[1] * y[3] + x[2] * y[0] + x[3] * y[1]) % self.p,
            (x[0] * y[3] + x[1] * y[2] - x[2] * y[1] + x[3] * y[0]) % self.p,
        ]

    def pow(self, x, n):
        tmp = x
        a = [1, 0, 0, 0]
        while n:
            if n & 1:
                a = self.mul(a, tmp)
            tmp = self.mul(tmp, tmp)
            n >>= 1
        return a

    def next(self):
        self.b = self.mul(self.b, self.a)
        return self.b[2]


class Task(socketserver.BaseRequestHandler):
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)

    def proof_of_work(self):
        random.seed(urandom(8))
        proof = "".join(
            [random.choice(string.ascii_letters + string.digits) for _ in range(20)]
        )
        digest = sha256(proof.encode()).hexdigest()
        self.dosend(str.encode(("sha256(XXXX + %s) == %s" % (proof[4:], digest))))
        self.dosend(str.encode("Give me XXXX:"))
        x = self.request.recv(10)
        x = (x.strip()).decode("utf-8")
        if len(x) != 4 or sha256((x + proof[4:]).encode()).hexdigest() != digest:
            return False
        return True

    def dosend(self, msg):
        try:
            self.request.sendall(msg + b"\n")
        except:
            pass

    def timeout_handler(self, signum, frame):
        raise TimeoutError

    def handle(self):
        try:
            signal.signal(signal.SIGALRM, self.timeout_handler)
            signal.alarm(60)
            if not self.proof_of_work():
                self.dosend(b"You must pass the PoW!")
                return
            self.dosend(BANNER)
            signal.alarm(3)
            self.dosend(b"Level: ")
            level = int(self.request.recv(2).strip())
            if level < 1 or level > 1:
                raise ValueError
            prng_list = [PRNG_PLUS_1]
            prng = prng_list[level - 1](BITS[level - 1])
            output = []
            for i in range(TOTAL):
                output.append(prng.next())
            known = output[: LEAK_LIMIT[level - 1]]
            hint = sha256("".join(map(str, output)).encode()).hexdigest()
            self.dosend(str(known).encode())
            self.dosend(str(hint).encode())
            signal.alarm(TIME_LIMIT[level - 1])
            for i in range(TOTAL):
                self.dosend(b"guess: ")
                guess = int(self.request.recv(1024).strip())
                if guess != output[i]:
                    self.dosend(b"Wrong!")
                    self.request.close()
                    return
            self.dosend(b"Congrats! Here is the flag: %s" % FLAG[level - 1])
        except TimeoutError:
            self.dosend(b"Timeout!")
            self.request.close()
        except:
            self.dosend(b"Wtf?")
            self.request.close()


class ThreadedServer(socketserver.ForkingMixIn, socketserver.TCPServer):
    pass


if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 12600
    server = ThreadedServer((HOST, PORT), Task)
    server.allow_reuse_address = True
    server.serve_forever()
