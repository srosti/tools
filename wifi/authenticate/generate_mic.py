#Used for computing HMAC
import hmac
#Used to convert from hex to binary
from binascii import a2b_hex, b2a_hex
#Used for computing PMK
from hashlib import pbkdf2_hmac, sha1, md5

 
#Pseudo-random function for generation of
#the pairwise transient key (PTK)
#key:       The PMK
#A:         b'Pairwise key expansion'
#B:         The apMac, cliMac, aNonce, and sNonce concatenated
#           like mac1 mac2 nonce1 nonce2
#           such that mac1 < mac2 and nonce1 < nonce2
#return:    The ptk
def PRF(key, A, B):
    #Number of bytes in the PTK
    nByte = 64
    i = 0
    R = b''
    #Each iteration produces 160-bit value and 512 bits are required
    while(i <= ((nByte * 8 + 159) / 160)):
        hmacsha1 = hmac.new(key, A + chr(0x00).encode() + B + chr(i).encode(), sha1)
        R = R + hmacsha1.digest()
        i += 1
    return R[0:nByte]
 
#Make parameters for the generation of the PTK
#aNonce:        The aNonce from the 4-way handshake
#sNonce:        The sNonce from the 4-way handshake
#apMac:         The MAC address of the access point
#cliMac:        The MAC address of the client
#return:        (A, B) where A and B are parameters
#               for the generation of the PTK
def MakeAB(aNonce, sNonce, apMac, cliMac):
    A = b"Pairwise key expansion"
    B = min(apMac, cliMac) + max(apMac, cliMac) + min(aNonce, sNonce) + max(aNonce, sNonce)
    return (A, B)
 
#Compute the 1st message integrity check for a WPA 4-way handshake
#pwd:       The password to test
#ssid:      The ssid of the AP
#A:         b'Pairwise key expansion'
#B:         The apMac, cliMac, aNonce, and sNonce concatenated
#           like mac1 mac2 nonce1 nonce2
#           such that mac1 < mac2 and nonce1 < nonce2
#data:      A list of 802.1x frames with the MIC field zeroed
#return:    (x, y, z) where x is the mic, y is the PTK, and z is the PMK
def MakeMIC(pwd, ssid, A, B, data, wpa = False):
    #Create the pairwise master key using 4096 iterations of hmac-sha1
    #to generate a 32 byte value
    pmk = pbkdf2_hmac('sha1', pwd.encode('ascii'), ssid.encode('ascii'), 4096, 32)
    #Make the pairwise transient key (PTK)
    ptk = PRF(pmk, A, B)
    #WPA uses md5 to compute the MIC while WPA2 uses sha1
    hmacFunc = md5 if wpa else sha1
    #Create the MICs using HMAC-SHA1 of data and return all computed values
    mics = [hmac.new(ptk[0:16], i, hmacFunc).digest() for i in data]
    return (mics, ptk, pmk)


#Run a brief test showing the computation of the PTK, PMK, and MICS
#for a 4-way handshake
def RunTest():
    #the pre-shared key (PSK)
    psk = "12345678"
    #ssid name
    ssid = "blah"
    #ANonce
    aNonce = a2b_hex("f13374aea3749a0834591d0ca351b993181d5d75b02e41dd1eec9716ce479725")

    #SNonce
    sNonce = a2b_hex("862a4af51180f0715650906a3ac42842d68b2bde34099a0a08dde848801b4bdb")


    #Authenticator MAC (AP)
    apMac = a2b_hex("003044167b07")
    #Station address: MAC of client
    cliMac = a2b_hex("9801a79a63f3")
    #The first MIC
    mic1 = "fed4073e157107718a105b801fcc10ca"
    #The entire 802.1x frame of the second handshake message with the MIC field set to all zeros
    data1 = a2b_hex("0103007502010a00000000000000000001862a4af51180f0715650906a3ac42842d68b2bde34099a0a08dde848801b4bdb000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001630140100000fac040100000fac040100000fac020000")


    #The second MIC
    mic2 = "5b22728430c4a8ade8aae96b720e2872"
    #The entire 802.1x frame of the third handshake message with the MIC field set to all zeros
    data2 = a2b_hex("020300af0213ca00100000000000000002f13374aea3749a0834591d0ca351b993181d5d75b02e41dd1eec9716ce4797250000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000050a26db0bc52202983e3b7fad7b196246fccec4e043644b8f83523765575b75a0d3cc5015cbbef6bf2502176ec9484d156f987ced5ad2022ee3c6130fa26b80744ac00b4852943777ffde2586fa6477aed")

    #The third MIC
    mic3 = "c0a2374b4d578559fb7cf1d431086501"
    #The entire 802.1x frame of the forth handshake message with the MIC field set to all zeros
    data3 = a2b_hex("0103005f02030a00000000000000000002862a4af51180f0715650906a3ac42842d68b2bde34099a0a08dde848801b4bdb0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000")

    #Create parameters for the creation of the PTK, PMK, and MICs
    A, B = MakeAB(aNonce, sNonce, apMac, cliMac)
    #Generate the MICs, the PTK, and the PMK
    mics, ptk, pmk = MakeMIC(psk, ssid, A, B, [data1, data2, data3])
    #Display the pairwise master key (PMK)
    pmkStr = b2a_hex(pmk).decode().upper()
    print("pmk:\t\t" + pmkStr + '\n')
    #Display the pairwise transient key (PTK)
    ptkStr = b2a_hex(ptk).decode().upper()
    print("ptk:\t\t" + ptkStr + '\n')
    #Display the desired MIC1 and compare to target MIC1
    mic1Str = mic1.upper()
    print("desired mic:\t" + mic1Str)
    #Take the first 128-bits of the 160-bit SHA1 hash
    micStr = b2a_hex(mics[0]).decode().upper()[:-8]
    print("actual mic:\t" + micStr)
    print('MATCH\n' if micStr == mic1Str else 'MISMATCH\n')
    #Display the desired MIC2 and compare to target MIC2
    mic2Str = mic2.upper()
    print("desired mic:\t" + mic2Str)
    #Take the first 128-bits of the 160-bit SHA1 hash
    micStr = b2a_hex(mics[1]).decode().upper()[:-8]
    print("actual mic:\t" + micStr)
    print('MATCH\n' if micStr == mic2Str else 'MISMATCH\n')
    #Display the desired MIC3 and compare to target MIC3
    mic3Str = mic3.upper()
    print("desired mic:\t" + mic3Str)
    #Take the first 128-bits of the 160-bit SHA1 hash
    micStr = b2a_hex(mics[2]).decode().upper()[:-8]
    print("actual mic:\t" + micStr)
    print('MATCH\n' if micStr == mic3Str else 'MISMATCH\n')
    return

RunTest()
