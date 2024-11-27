import random
import struct
from tabulate import tabulate
import os

DECODE_DIR = "decoded/"
CODES_DIR = "codes/"
ENCODE_PREFIX = "encoded_"
DECODE_PREFIX = "decoded_"

if not os.path.exists(CODES_DIR):
    os.makedirs(CODES_DIR)
if not os.path.exists(DECODE_DIR):
    os.makedirs(DECODE_DIR)

class FanoEncoder:
    def __init__(self, f_name):
        self.f_name = f_name
        with open(f_name, "r", encoding="ASCII") as f:
            self.message = "".join(f.readlines())
        self.probs = self.get_probabilities(self.message)
        self.encoding = [[x[0],""] for x in self.probs]
        
        
    @staticmethod
    def get_probabilities(message):
        enters = {}
        for c in message:
            if c not in enters.keys():
                enters[c] = 1
            else:
                enters[c] += 1
        probs = []
        n = len(message)
        for c, count in enters.items():
            probs.append((c, count/n))
        probs.sort(key=lambda x: x[1], reverse=True)
        return probs   
     
     
    @staticmethod
    def med(b, e, probs):
        sb = 0
        for i in range(b, e):
            sb += probs[i][1]
        se = probs[e][1]

        m = e
        d = abs(sb-se)
    
        while abs(sb-se) <= d:    
            d = abs(sb-se)
            m -= 1
            sb -= probs[m][1]
            se += probs[m][1]     
        return m
    
    
    def encode(self, b=0, e=None, k=0):
        stack = [(b,e,k)]
        if(len(self.probs) == 1):
            self.encoding[0][1] = '0' 
            
        while stack:
            b, e, k = stack.pop()
            if e is None:
                e = len(self.probs)-1

            if(b < e):
                k += 1
                m = self.med(b,e,self.probs)
                for i in range(b, e+1):
                    self.encoding[i][1] += str(int(i>m))
                stack.append((b,m,k))
                stack.append((m+1,e,k))
        

    
    
    def print_encoding(self):
        table = []
        for el in self.encoding:
            table.append(el.copy())
        smooth_ef = 0
        for i in range(len(table)):
            smooth_cost = 8*self.probs[i][1]
            table[i].append(self.probs[i][1])
            table[i].append(len(table[i][1]))
            table[i].append(len(table[i][1])*self.probs[i][1])
            table[i].append(smooth_cost)
            table[i][0] = repr(table[i][0])
            smooth_ef += smooth_cost
        if(len(table) > 20):
            table = table[:10] + table[-5:]
        table.append(["Summary effectiveness", '', '', '', self.count_effectiveness(), smooth_ef])
        print(tabulate(table, headers=["Symbol", "Encoding", "Probability", "Length", "P*L", "Smooth P*L"],tablefmt="grid"))
    
    
    def _encoding_to_dict(self):
        d = {}
        for el in self.encoding:
            d[el[0]] = el[1]
        return d
    
    def count_effectiveness(self):
        pl = 0
        for i in range(len(self.encoding)):
            pl += self.probs[i][1]*len(self.encoding[i][1])
        return pl
    
    def write_codes(self):
        enc = self._encoding_to_dict()

        with open(CODES_DIR + self.f_name.replace(".bin", ".txt"), "w+") as out_tree_file:
            
            for symbol, code in enc.items():
                if symbol == '\n':
                    out_tree_file.write(f"bn\t{code}\n")
                elif symbol == ' ':
                    out_tree_file.write(f"sp\t{code}\n")
                elif symbol == '\t':
                    out_tree_file.write(f"bt\t{code}\n")
                else:
                    out_tree_file.write(f"{symbol}\t{code}\n")

    
    def write_translation(self):
        enc = self._encoding_to_dict()
        encoded_string = ''.join(enc[c] for c in self.message if c in enc.keys())
        encoded_bytes = bytearray()
    
        encoded_bytes.extend(struct.pack(">I", len(self.message)))
        
        for i in range(0, len(encoded_string), 8):
            byte = encoded_string[i:i + 8]
            encoded_bytes.append(int(byte.ljust(8, '0'), 2))
        
        with open(ENCODE_PREFIX + self.f_name.replace(".txt", ".bin"), "wb+") as f:
            
            f.write(encoded_bytes)
                
            
class FanoDecoder:
    def __init__(self, f_name:str):
        name = f_name.split("_")[-1]
        self.name = name
        self.f_name = f_name
        self.codes = {}
        
        with open(f_name, "rb") as f:
            self.message = b"".join(f.readlines())

        with open(CODES_DIR + name.replace(".bin", ".txt"), 'r') as f:
            for line in f:
                symbol, code = line.strip().split('\t')
                if symbol == "bn":
                    symbol = '\n'
                elif symbol == "sp":
                    symbol = ' '
                elif symbol == "bt":
                    symbol = "\t"
                self.codes[code] = symbol
    
    def decode(self):
        decoded_message = ""
        current_code = ""

        length = struct.unpack(">I", self.message[:4])[0]
        encoded_bits = ''.join(f'{byte:08b}' for byte in self.message[4:])
        print(encoded_bits)
        for bit in encoded_bits:
            current_code += bit
            if current_code in self.codes.keys():
                decoded_message += self.codes[current_code]
                current_code = ""
                if len(decoded_message) == length:
                    break
                
        self.decoded_message = decoded_message
    
    
    def write_translation(self):
        path = DECODE_DIR + DECODE_PREFIX + self.name
        with open(DECODE_DIR + DECODE_PREFIX + self.name.replace(".bin", ".txt"), "w+") as f:
            f.write(self.decoded_message)
        return path
            
            
        
def generate_random_text(n):
    ascii_chars = [chr(i) for i in range(128)]
    ret = ""
    times = random.randint(10,n/10)
    ind = random.randint(0,127)
    for i in range(n):
 
        times -= 1
        if(times == 0):
            ind = random.randint(0,127)
            times = random.randint(10,n/10)
        
        ret += ascii_chars[ind]
    return ret


def run_interface():
    try:
        print("Fano encoder/decoder (to exit - Ctrl+C)")
        while(1):
            
            opt = input("Enter:\n1 - encode file\n2 - decode file\n3 - encode 3 messages of lengths 100 1000 10000\n\n")
            match opt:
                case '1':
                    path = input("Enter filename (txt) to process: ")
                    fe = FanoEncoder(path)
                    fe.encode()
                    fe.print_encoding()
                    fe.write_translation()
                    fe.write_codes()
                    
                    print(f'''\n\nEncoded file:"{ENCODE_PREFIX + path}"
                          \nFile with codes: "{CODES_DIR + path}"\n\n''')
                case '2':
                    path = input("Enter filename (txt) to process: ")
                    fd = FanoDecoder(path)
                    fd.decode()
                    res_path = fd.write_translation()
                    
                    print(f'\n\n Decoded file: "{res_path.replace(".bin", ".txt")}"\n\n')
                case '3':
                    ls = [100, 1000, 10000]
                    for l in ls:
                        message = generate_random_text(l)
                        path = f"random{l}.txt"
                        print(f"\n\nCase {l}\n")
                        with open(path, "w+") as f:
                            f.write(message)                 
                        fe = FanoEncoder(path)
                        fe.encode()
                        fe.print_encoding()
                        fe.write_translation()
                        fe.write_codes()
                case _:
                    print("Wrong option")
    except KeyboardInterrupt:
        print("\n\nProcess is terminated")
    

def main():
    run_interface()
        
if __name__ == "__main__":
    main()