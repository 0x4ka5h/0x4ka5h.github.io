+++
title = "InvaderCTF writeups"
description = " My approch towards the CTF challanges authored by Team Invaders"
date = 2022-08-17T07:34:48+08:30
featured = false
draft = false
comment = false
toc = false
reward = true
categories = [ "CTF", "WriteUps", "Security"
]
tags = [ "Web", "Reverse", "pwn", "Crypto", "Misc"
]
series = []
images = ["images/compose.png"]
+++


### Introduction 
Hello mate, Sup?

Long time, no see ah? Don't worry, I'm coming. Here we go, Our new blog but this time with a different topic 🙃. Me, entering the world of CTFs and Application security. Playing “InvaderCTF” is my first step toward the path that I have chosen. And, at the end of the day, it’s a 🥳BANG! I'm able to secure my position in the Top 3.

Actually, I'm studying at RGUKT. Some of the alumni of our college called [Team Invaders](https://ctf.pwn.af/) conducted this CTF. 

There is a list of categories in this CTF such as “web”, “pwn”, “reverse”, “cryptography”, and “miscellaneous”. During CTF I was mostly dedicated to Web and Reverse categories. This CTF was conducted with a very basic level of challenges to encourage the students.. 

Randon Reader(RR): "Quick!"

Okay okay, let me explain the approch that I have followed to solve those challenges.

### MISC

##### Sniff
![chall_1](images/sniff_Chall.png)
Challenge - [misc2.pcapng](https://ctf.pwn.af/files/1898a74ff07d1d8a9a8ad81886bd2730/misc2.pcapng?token=eyJ1c2VyX2lkIjo2LCJ0ZWFtX2lkIjpudWxsLCJmaWxlX2lkIjoyOX0.YwMhtA.hidJXLnP2WPA0SG7-qHlGyQjZS4), here is the file (sniffed packet).

1. Open .pcap file with wireshark, filter with http.
2. Found some captured traffic data, filter with "flag". We'll found a packet with /flag_in_authorization_header
3. Extract Authorization header value and decrypt with base64, got it! done.

```py
#Extracted header value 
token = "SW52YWRlckNURntOaWNlX3BjYXBfYW5hbHlzaW5nX3NraWxsc30="
import base64
flag = base64.b64decode(token)
print(flag)

# b'InvaderCTF{Nice_pcap_analysing_skills}'
```

##### Python2
![chall_2](images/python2_chall.png)
```py
## This is the code that was given in chall.py
#!/usr/bin/python2

import flag
import sys

sys.stdout.write('''\t +++++ Even/Odd Calculator +++++
Enter a number: ''')
sys.stdout.flush()
inp = input()
sys.stdout.write('The number you entered is ' + str(inp))
if inp % 2 == 0:
    sys.stdout.write(' and it is even!')
else:
    sys.stdout.write(' and it is odd!')
sys.stdout.write('\n')
sys.stdout.flush()

exit()

```

Let me explain you about python2.* input.
In python2 there two ways to take an input from the user using input funtion. 
1. input() -> This function takes the value and type of the input you enter as it is without modifying any type.
2. raw_input() -> This function explicitly converts the input you give to type string.

Guess, what we can do. We can call funtions directly. Noice.

```bash
$ python2 chall.py
+++++ Even/Odd Calculator +++++
Enter a number: 1==1
The number you entered is True and it is even!

$ # wow it print resultant value, puck we catch it :P
$ # If you see in the code, the flag is being imported and the flag also in string format
$ # so we can see doc-strings and built-in function of flag module, lets try it
$ python2 chall.py
+++++ Even/Odd Calculator +++++
Enter a number: dir(flag)
The number you entered is ['__builtins__', '__doc__', '__file__', '__name__', '__package__','here_is_your_flag'] and it is odd!

$ # Yay, our flag is stored in here_is_your_flag, so can call it with flag.here_is_your_flag
$ python2 chall.py
+++++ Even/Odd Calculator +++++
Enter a number: flag.here_is_your_flag
The number you entered is InvaderCTF{python2_is_vulnerable_huh!} and it is odd!
```
##### Mnemonics
![chall_3](images/mnemonics_chall.png)
```py
## This is the code that was given in chall.py
#!/usr/bin/python3

list_of_words = ['abc', 'def', 'ghi']

flag = 'Dummy_FLAG' # Real flag is on the server

print('''Let's play a game :)
	Guess the words that comes to my mind.
	And if you guess it correctly everytime, 
	you will get the flag as reward!''')

WORD_COUNT = len(list_of_words)

index = 0
while (input('Enter the word (%s/%s): '%(index + 1, WORD_COUNT)) 
	== list_of_words[index]):
	index += 1
	if index == WORD_COUNT: 
		exit('Here is your flag: ' + flag)

exit('Nah, you got it wrong! The word is ' + list_of_words[index])

```
Boom, we got that.

Random Reader (RR) : What boom?

Me: See that last line, if we guess the wrong word, correct word is printing.

RR : Boom!


Haha!, Lets write a program cause there are 500 words to guess.
```py
from pwn import *
# for netcat connection
h = "198.199.123.169"
port = "9390"
conn = remote(h,port)
recvd = conn.recv()
conn.sendline(b'puck')
crct_ans = conn.recv()
print(crct_ans.split()[-1])
## prints correct word.
```

Now, if we are able to store the correct value in a list and then we can send it again to the program
cause if we made a false guess, then the program will end.
```py
from pwn import *
# for netcat connection
h = "198.199.123.169"
port = "9390"

crct_words = []
for i in range(500):
	conn = remote(h,port)
	recvd = conn.recv()
	for word in crct_words:
		conn.sendline(word.decode('utf-8'))
		flag = conn.recv()
	conn.sendline(b'puck')
	crct_ans = conn.recv()
	crct_words.append(crct_ans.split()[-1])
print(flag)
## prints flag -> InvaderCTF{Test_FLAG_123_Mnemonics}
```

### PWN

##### Food_Court_OverFlow
![chall_4](images/pwn_overflow.png)
Challenge [court.zip,](https://ctf.pwn.af/files/48243982f9e28ccc05f9847405311322/court.zip?token=eyJ1c2VyX2lkIjo2LCJ0ZWFtX2lkIjpudWxsLCJmaWxlX2lkIjoyN30.YwOl9w.4cxtmv3vqgYytXVIGmAAOIVghXA) here you can download the challange zip file.

```c 
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>

int wallet = 200;

int order(char *item, int cost) {
    int n;
    printf("Input the number of %s you want to buy?\n", item);
    printf("> ");
    scanf("%d", &n);

    if (n > 0) {
        cost = cost * n;
        printf("That will cost Rs%d.\n", cost);
        if (cost <= wallet) {
            puts("Order placed!");
            wallet -= cost;
        } else {
            puts("Ah man, you don't have enough money to buy this order");
            n = 0;
        }
    } else {
        puts("Nah, buy something.");
    }

    return n;
}
void initialize()
{
  alarm(60);
  setvbuf(stdout, NULL, _IONBF, 0);
  setvbuf(stderr, NULL, _IONBF, 0);
  setvbuf(stdin, NULL, _IONBF, 0);
}

int main() {
    int item;
    puts("Welcome to RGUKT Food Court!");
    puts("We are giving free 200 RS wallet amount to our online customers.");
    puts("Sadly, you don't have enough money to buy the tastiest dish named Flag :/? Or is it? \n");

    while (1) {

        printf("Wallet Amount Rs%d.\n", wallet);
        puts("Menu: ");
        puts("1. Noodles: 50");
        puts("2. Biryani: 100");
        puts("3. Soft Drink: 20");
        puts("4. Flag: Rs 1000");
        puts("0. Logout\n");
        puts("Which item would you like to Order?");

        printf("> ");
        scanf("%d", &item);

        switch (item) {
            case 0:
                printf("Logging out");
                return 0;
            case 1:
                order("Nooooodles", 50);
                break;
            case 2:
                order("Dum Biryani", 100);
                break;
            case 3:
                order("Soft Drink", 1);
                break;
            case 4:
                if (order("buy the today's special dish - flag", 1000) > 0) {
                    FILE *fp = fopen("flag.txt", "r");
                    char flag[100];

                    if (fp == NULL) {
                        puts("Create flag.txt in the current working directory");
                        puts("Please report to admin if you saw this error on remote");
                        exit(1);
                    }

                    fgets(flag, sizeof(flag), fp);
                    puts(flag);
                }
                break;
            default:
                puts("Please select a valid item.");
        }
    }
}
```
The challenge name itself a big hint! lol🫂, the interger is declared as ```int```. 
we just need to give a number that belongs to out of the ```signed int``` range.

singed int range for 

- 2 or 4 bytes	(-32,768 to 32,767 or -2,147,483,648 to 2,147,483,647)

Lets understand the program, once input is taken, the program multiplied it with 1000,
and stores in int.

The overflow happens iff we give a number and when 1000 is multipled with it, the resultant must be greater than 2,147,483,647.

So we if input 21474836, then 21474836*1000 >> 2,147,483,647.
BAMM, done.

```sh
$ gcc court.c
$ ./a.out
Welcome to RGUKT Food Court!
We are giving free 200 RS wallet amount to our online customers.
Sadly, you dont have enough money to buy the tastiest dish named Flag :/? Or is it? 

Wallet Amount Rs200.
Menu: 
1. Noodles: 50
2. Biryani: 100
3. Soft Drink: 20
4. Flag: Rs 1000
0. Logout

Which item would you like to Order?
> 4
Input the number of buy the todays special dish - flag you want to buy?
> 21474836
That will cost Rs-480.
Order placed!
InvaderCTF{this_is_not_flag_flag_is_on_the_remote_server}
Wallet Amount Rs680.
Menu: 
1. Noodles: 50
2. Biryani: 100
3. Soft Drink: 20
4. Flag: Rs 1000
0. Logout

Which item would you like to Order?
> 

# BAMM, InvaderCTF{this_is_not_flag_flag_is_on_the_remote_server} here is our flag
```

### REV

##### pyencryptor
![chall_5](images/pyencrypter.png)
```py
#this is the code in chall.py
import random

# Two byte hash
def myHash(string):
    random.seed("H4shS33d" + string)
    num = random.getrandbits(16)
    return hex(num)[2:].zfill(4)

def encryptFlag(flag):
    enc = ""
    for char in flag:
        enc += myHash(char)
    return enc

flag = input("Enter flag : ")
enc = encryptFlag(flag)
print("Encrypted flag is : ", enc)

## Encrpted flag
# 08ef07973844262cd256a8635295ad53ece7518ae30f1fb9bdbfbfa9529526
# 2c1fb917ac757352956685500ebfa9cf347573d2566685bdbfbfa9cf34bdbff
# 2a30797b15a66856217cf34668507287573262c908276b5
```

Now, we need to write a reverse code to decrypt the flag. We already know, our flag contains InvaderCTF{ at beginning.

```py
import random

random.seed("H4shS33d"+"I") 
num = random.getrandbits(16)
print(number)
# 2287, is always generate same

h = hex(2287)[2:].zfill[4]
print(h)
# 08ef -> front [0:4] slice part of decrypted flag

# if we print 0x08ef -> 2287
```
BOOM, BAAMM, it done bro 🥲.

If we iterate a loop over all printable values, we can get our flag back

```py
import random
import string
flag = "08ef07973844262cd256a8635295ad53ece7518ae30f1fb9bdbfbfa95295262c" + \
"1fb917ac757352956685500ebfa9cf347573d2566685bdbfbfa9cf" + \
"34bdbff2a30797b15a66856217cf34668507287573262c908276b5"

flag = [flag[i:i+4] for i in range(0,len(flag),4)]
for j in flag:
	for i in string.printable:
		random.seed("H4shS33d"+i) 
		num = random.getrandbits(16)
		if int(j,16)==num:
			print(i,end="")
			break

# InvaderCTF{ch4ract3r_b4s3d_h4sh1ng_is_w3ak}
```

##### Crack_ME

![crack_me](images/crack_me.png)
challegen - [crack_me.pyc](https://ctf.pwn.af/files/9029de2a8b3fe1f3c73f8af512e6b673/crack.zip?token=eyJ1c2VyX2lkIjo2LCJ0ZWFtX2lkIjpudWxsLCJmaWxlX2lkIjoyM30.YwO4cg.W_dEqy4Gkgv8RCGSQs4Mtfp1lHU) is given in the zip file. 


1. I have used online decompiler to reverse .pyc file

```py
import random
random.seed(u'[5\x80E\x1d\x1aX\x91Z\x8f')

def encrypt(string):
    enc = []
    for char in string:
        temp = ord(char) + 120 ^ random.getrandbits(7)
        enc.append(temp)

    return bytearray(enc)


flag = input('Enter flag : ')
encFlag = encrypt(flag)
if encFlag == '\xd1\xe0\xb3\x9e\x80\xbf\xd3\x97\xa1\xda\x97\xdd\xe4\xef\xc9\xdf\x92\xff\xa2\xd5\x95\xfc\x99\xe6\xbc\xfa\xf5\xab\xd1\x89\xae\xd4\xe0\x94\xbb\x80\x96\x97\xa4\xd5\xd1\xe6\xce':
    print('Flag was right :)')
else:
    print('Nope')
```

This is the code we got it from decompiler, if our input matches to
``` 
'\xd1\xe0\xb3\x9e\x80\xbf\xd3\x97\xa1\xda\x97\xdd\xe4\xef\xc9\xdf\x92\xff\xa2\xd5\x95\xfc\x99\xe6\xbc\xfa\xf5\xab\xd1\x89\xae\xd4\xe0\x94\xbb\x80\x96\x97\xa4\xd5\xd1\xe6\xce'
``` 
this, then our input is the flag.

2. If you observe that, the seed is common for all bits. It means, how many time we run ```random.getrandbits(7)``` after seeding we get the same sequence values.

3. Now we just need to find which printable char is satisfied the condition  ```ord(i) + 120 ^ p == encFlag[]```

```py  
import random
import string

st = b'\xd1\xe0\xb3\x9e\x80\xbf\xd3\x97\xa1\xda\x97\xdd\xe4\xef\xc9\xdf\x92\xff\xa2\xd5\x95\xfc\x99\xe6\xbc\xfa\xf5\xab\xd1\x89\xae\xd4\xe0\x94\xbb\x80\x96\x97\xa4\xd5\xd1\xe6\xce'
random.seed(u'[5\x80E\x1d\x1aX\x91Z\x8f')
flag = []
j = 0
while j<43:
	p = random.getrandbits(7)
	for i in string.printable:
		temp = ord(i) + 120 ^ p
		
		if temp == st[j]:
			print(i,end="")
			break
	j+=1

# InvaderCTF{d3c0mpilati0n_m4kes_l1f3_e4si3r}
```

##### Binary

![chall_6](images/binary.png)
```py
```

### CRYPt


##### Thanks for reading! {align=center}
