from math import log2 
import random
from tabulate import tabulate

DECODE_DIR = "decoded/"
CODES_DIR = "codes/"
ENCODE_PREFIX = "encoded_"
DECODE_PREFIX = "decoded_"


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
        if(e == None):
            e = len(self.probs)-1
        
        if(b < e):
            k += 1
            m = self.med(b,e,self.probs)
            for i in range(b, e+1):
                self.encoding[i][1] += str(int(i>m))
            self.encode(b, m, k)
            self.encode(m+1, e, k)
    
    def print_encoding(self):
        table = []
        for el in self.encoding:
            table.append(el.copy())
        smooth_ef = 0
        for i in range(len(table)):
            smooth_cost = int(log2(len(table)) + 1)*self.probs[i][1]
            table[i].append(self.probs[i][1])
            table[i].append(len(table[i][1]))
            table[i].append(len(table[i][1])*self.probs[i][1])
            table[i].append(smooth_cost)
            table[i][0] = repr(table[i][0])
            smooth_ef += smooth_cost
            
        table.append(["Summary effectiveness", '', '', '', self.count_effectiveness(), smooth_ef])
        print(tabulate(table, headers=["Symbol", "Encoding", "Probability", "Length", "P*L", "Smooth P*L"],tablefmt="grid"))
    
    
    def _encoding_to_dict(self):
        d = {}
        for el in self.encoding:
            d[el[0]] = el[1]
        return d
    
    
    def write_codes(self):
        with open(CODES_DIR + self.f_name, "w+") as f:
            for el in self.encoding:
                sym = repr(el[0])
                line = f"{sym.strip()} {el[1]}"
                f.write(line)
                f.write("\n")
            
    
    def write_translation(self):
        enc = self._encoding_to_dict()
        encoded_message = ""
        for c in self.message:
            encoded_message += enc[c]
            
        with open(ENCODE_PREFIX + self.f_name, "w+") as f:
            f.write(encoded_message)
    
    def count_effectiveness(self):
        pl = 0
        for i in range(len(self.encoding)):
            pl += self.probs[i][1]*len(self.encoding[i][1])
        return pl
                
            
class FanoDecoder:
    def __init__(self, f_name:str):
        name = f_name.split("_")[-1]
        self.name = name
        self.f_name = f_name
        try:
            with open(f_name, "r") as f:
                self.message = "".join(f.readlines())
        except FileNotFoundError:
            print("Message is not found")
        try:
            with open(CODES_DIR + name, "r") as f:
                lines = [line.rstrip() for line in f]
        except FileNotFoundError:
            print("Codes of this message are not found")
            lines = []
            
        self.codes = {}
        for line in lines:
            sym = ""
            is_sym = False
            i = 0
            while i < len(line):
                
                if(line[i] == "'" and not is_sym):
                    is_sym = True
                    i+=1
                    continue
                elif (line[i] == "'" and is_sym):
                    is_sym = False
                    i+=2
                    break
                if is_sym:
                    sym += line[i]
                i+=1
            code = line[i:]
            self.codes[code] = sym
            
        self.decoded_message = ""
    
    def decode(self):
        buffer = ""
        i = 0
        decoded_message = ""
        while i<len(self.message):
            buffer += self.message[i]
            i+=1
            
            if buffer in self.codes.keys():
                decoded_message += self.codes[buffer]
                buffer = ''
        self.decoded_message = decoded_message
    
    def write_translation(self):
        path = DECODE_DIR + DECODE_PREFIX + self.name
        with open(DECODE_DIR + DECODE_PREFIX + self.name, "w+") as f:
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
                    
                    print(f'\n\n Decoded file: "{res_path}"\n\n')
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