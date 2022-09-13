from string import ascii_lowercase
import json
import re

class Sigaba():

    def __init__(self):
        self.alphabet = ascii_lowercase
        self.numbers = "0123456789"

        self.largeRotors = {"I":    "pwjvdrgtmbholyxuzfqeainkcs",
                            "II":   "mklwaibxruygtncspdfqhzjvoe",
                            "III":  "wvylijamxztsuroendkqhcfbpg",
                            "IV":   "zrmqwnitbjukhofpeydxavlsgc",
                            "V":    "lgbazwmipqtfhevuyjncrskdox",
                            "VI":   "ygowzxpcbjtiarkhmelndfvusq",
                            "VII":  "uzgkpdqrjtfcyoinvmalhexwsb",
                            "VIII": "oqrtdbuzgphwnjfelkcixvsaym",
                            "IX":   "hledcotjmuawfzqigrbvypsnkx",
                            "X":    "qkciypwlznhtjvfdursxebgmoa"}


        self.smallRotors = {"I":   "9438705162",
                            "II":  "8135624097",
                            "III": "5901284736",
                            "IV":  "1953742680",
                            "V":   "6482359170"}

        self.indwiring = {"a": 9, "b": 1, "c": 2, "d": 3, "e": 3, "f": 4,
                          "g": 4, "h": 4, "i": 5, "j": 5, "k": 5, "l": 6,
                          "m": 6, "n": 6, "o": 6, "p": 7, "q": 7, "r": 7,
                          "s": 7, "t": 7, "u": 8, "v": 8, "w": 8, "x": 8,
                          "y": 8, "z": 8}

    def rotor(self, alphabet, letter,key,pos,invert=False):
        alpha = alphabet
        entry = alpha.index(letter)
        
        if invert == False:
            inner = key[(entry+pos-1)%len(alpha)]
            outer = (alpha.index(inner)-pos+1)%len(alpha)
            return alpha[outer]
        if invert == True:
            inner = alpha[(entry+pos-1)%len(alpha)]
            outer = (key.index(inner)-pos+1)%len(alpha)
            return alpha[outer]


    def encrypt(self, text=None, keys = None, settings_file = None, file = None):
        
        if file:
            try:
                f=open(file)

            except IOError:
                print("Sigaba Error 3: There is not such a file for encrypte")
            
            text = f.read()
        elif text:
            text = text
        else:
            text = "Hello World"
        
        text = re.sub(r'[^a-zA-Z ]', "", text)  
        text = text.lower()

        text = text.replace("z","x")
        text = text.replace(" ","z")
        
        if settings_file:
            try:
                data_settings_file = json.load(open(settings_file, "r"))

            except IOError:
                print("Sigaba Error 1: There is not such a settings file")
            
            cipherRotorsSet = data_settings_file["cipher"]
            controlRotorsSet = data_settings_file["control"]
            indexRotorsSet = data_settings_file["index"]

            indicator1 = data_settings_file["indicator"]
            indicator2 = data_settings_file["controlPos"]
            indicator3 = data_settings_file["indexPos"]

            orientationControl = data_settings_file["orientationControl"]
            orientationCipher =  data_settings_file["orientationCipher"]

            
        elif len(keys) == 8 and keys[0] != None and keys[1] != None and keys[2] != None and keys[3] != None and keys[4] != None:

            cipherRotorsSet = keys[0].copy()
            controlRotorsSet = keys[1].copy()
            indexRotorsSet = keys[2].copy()

            indicator1 = keys[3]
            indicator2 = keys[4]
            indicator3 = keys[5]

            orientationControl = keys[6]
            orientationCipher = keys[7]
        else:
            cipherRotorsSet = ["I","II","III","IV","V"]
            controlRotorsSet = ["VI","VII","VIII","IX","X"]
            indexRotorsSet = ["I","II","III","IV","V"]

            indicator1 = "aaaaa"
            indicator2 = "aaaaa"
            indicator3 = "00000"

            orientationControl = ["F", "F", "F", "F", "F"]
            orientationCipher = ["F", "F", "F", "F", "F"]
        
        
        cipherRotors = []
        cipherPos = []
        for ctr,num in enumerate(cipherRotorsSet):
            cipherRotors.append(self.largeRotors[num])
            if orientationCipher[ctr] == "R":
                cipherRotors[ctr] = cipherRotors[ctr][::-1]
            cipherPos.append(cipherRotors[ctr].index(indicator1[ctr]))
        
        
        
        
        controlRotors = []
        controlPos = []
        for ctr, num in enumerate(controlRotorsSet):
            controlRotors.append(self.largeRotors[num])
            if orientationControl[ctr] == "R":
                controlRotors[ctr] = controlRotors[ctr][::-1]
            controlPos.append(controlRotors[ctr].index(indicator2[ctr]))
        
       
            

        indexRotors = []
        indexPos = []
        for ctr, num in enumerate(indexRotorsSet):
            indexRotors.append(self.smallRotors[num])
            indexPos.append(self.smallRotors[num].index(indicator3[ctr]))
                      
        out = []
        for ctr,letter in enumerate(text,1):
            
            T = letter
            for R,P in zip(cipherRotors,cipherPos):
                T = self.rotor(self.alphabet, T,R,P)
            out.append(T)
                        
            L = ["f","g","h","i"]
            for R,P in zip(controlRotors,controlPos):
                for i in range (4):
                    L[i] = self.rotor(self.alphabet, L[i],R,P)
            
            controlPos[2] = (controlPos[2] + 1) % 26
            if ctr % 26 == 0:
                controlPos[3] = (controlPos[3] + 1) % 26
            if ctr % 676 == 0:
                controlPos[1] = (controlPos[1] + 1) % 26     
            
            for i in range(4):
                L[i] = str(self.indwiring[L[i]])
            
            for R,P in zip(indexRotors,indexPos):
                for i in range(4):
                    L[i] = self.rotor(self.numbers, L[i], R, P)  
            
            for i in range(4):
                if int(L[i]) == 1 or int(L[i]) == 2:
                    L[i] = 4
                elif  int(L[i]) == 3 or int(L[i]) == 4:
                    L[i] = 3
                elif  int(L[i]) == 5 or int(L[i]) == 6:
                    L[i] = 2
                elif  int(L[i]) == 7 or int(L[i]) == 8:
                    L[i] = 1
                elif  int(L[i]) == 0 or  int(L[i]) == 9:
                    L[i] = 0
            


            for rtr in set(L):
                cipherPos[rtr] = (cipherPos[rtr] + 1) % 26
            

        outtext = "".join(out)


        f = open("encrypt.txt", "w")
        f.write(outtext)
        return outtext


    def decrypt(self, text = None, keys = None, settings_file = None, encrypte_file = None):
        
        if encrypte_file:
            try:
                f=open(encrypte_file)
                text = f.read()
                
            except IOError:
                print("Sigaba Error 2: There is not such a encrypte file")
            
            
        elif text:
            text = text

        else:
            text = "plaxglppajb"

        text = re.sub(r'[^a-zA-Z]', "", text)    
        text = text.lower()


        if settings_file:
            try:
                data_settings_file = json.load(open(settings_file, "r"))

            except IOError:
                print("Sigaba Error 1: There is not such a settings file")
            
            cipherRotorsSet = data_settings_file["cipher"]
            controlRotorsSet = data_settings_file["control"]
            indexRotorsSet = data_settings_file["index"]

            indicator1 = data_settings_file["indicator"]
            indicator2 = data_settings_file["controlPos"]
            indicator3 = data_settings_file["indexPos"]

            orientationControl = data_settings_file["orientationControl"]
            orientationCipher =  data_settings_file["orientationCipher"]

            
        elif len(keys) == 8 and keys[0] != None and keys[1] != None and keys[2] != None and keys[3] != None and keys[4] != None:

            cipherRotorsSet = keys[0].copy()
            controlRotorsSet = keys[1].copy()
            indexRotorsSet = keys[2].copy()

            indicator1 = keys[3]
            indicator2 = keys[4]
            indicator3 = keys[5]

            orientationControl = keys[6]
            orientationCipher = keys[7]
        else:
            cipherRotorsSet = ["I","II","III","IV","V"]
            controlRotorsSet = ["VI","VII","VIII","IX","X"]
            indexRotorsSet = ["I","II","III","IV","V"]

            indicator1 = "aaaaa"
            indicator2 = "aaaaa"
            indicator3 = "00000"

            orientationControl = ["F", "F", "F", "F", "F"]
            orientationCipher = ["F", "F", "F", "F", "F"]


        cipherRotors = []
        cipherPos = []
        for ctr,num in enumerate(cipherRotorsSet):
            cipherRotors.append(self.largeRotors[num])
            if orientationCipher[ctr] == "R":
                cipherRotors[ctr] = cipherRotors[ctr][::-1]
            cipherPos.append(cipherRotors[ctr].index(indicator1[ctr]))
        

        cipherRotorsRev = cipherRotors[::-1]

        controlRotors = []
        controlPos = []
        for ctr, num in enumerate(controlRotorsSet):
            controlRotors.append(self.largeRotors[num])
            if orientationControl[ctr] == "R":
                controlRotors[ctr] = controlRotors[ctr][::-1]
            controlPos.append(controlRotors[ctr].index(indicator2[ctr]))

        indexRotors = []
        indexPos = []
        for ctr, num in enumerate(indexRotorsSet):
            indexRotors.append(self.smallRotors[num])
            indexPos.append(self.smallRotors[num].index(indicator3[ctr]))
        
        out = []
        for ctr,letter in enumerate(text,1):

            cipherPosRev = cipherPos[::-1]

            T = letter
            for R,P in zip(cipherRotorsRev,cipherPosRev):
                T = self.rotor(self.alphabet, T,R,P,invert=True)
            out.append(T)

            L = ["f","g","h","i"]
            for R,P in zip(controlRotors,controlPos):
                for i in range (4):
                    L[i] = self.rotor(self.alphabet, L[i],R,P)

            controlPos[2] = (controlPos[2] + 1) % 26
            if ctr % 26 == 0:
                controlPos[3] = (controlPos[3] + 1) % 26
            if ctr % 676 == 0:
                controlPos[1] = (controlPos[1] + 1) % 26     

            for i in range(4):
                L[i] = str(self.indwiring[L[i]])
            
            for R,P in zip(indexRotors,indexPos):
                for i in range(4):
                    L[i] = self.rotor(self.numbers, L[i], R, P)
            
            for i in range(4):
                if int(L[i]) == 1 or int(L[i]) == 2:
                    L[i] = 4
                elif  int(L[i]) == 3 or int(L[i]) == 4:
                    L[i] = 3
                elif  int(L[i]) == 5 or int(L[i]) == 6:
                    L[i] = 2
                elif  int(L[i]) == 7 or int(L[i]) == 8:
                    L[i] = 1
                elif  int(L[i]) == 0 or  int(L[i]) == 9:
                    L[i] = 0

            for rtr in set(L):
                cipherPos[rtr] = (cipherPos[rtr] + 1) % 26

        outtext = "".join(out)

        outtext = outtext.replace("z"," ")
        
        f = open("decrypt.txt", "w")
        f.write(outtext)

        return outtext



def SIGABAExample():

    cipher =     ["V","IX","II","IV","III"]
    control =    ["IX","VI","I","VII","VIII"]
    index =      ["II","I","V","IV","III"]
    indicator =  "table"
    controlPos = "graph"
    indexPos =   "02367"
    orientationControl = ["F", "R", "F", "R", "F"]
    orientationCipher = ["F", "R", "R", "R", "F"]

   
    sigaba = Sigaba()
    ctext = sigaba.encrypt(file="text.txt", settings_file = "settings.json")
    dtext = sigaba.decrypt(encrypte_file="encrypt.txt", settings_file = "settings.json")
        
    
    
SIGABAExample()