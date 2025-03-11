
# -*- coding: euc-kr -*-

import random as r
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')


game_on = 1

player_HP = 100
player_HP_adder = 0
player_max_HP = 100

monster_max_HP = 0
monster_HP = 0

player_max_attack = 5
player_min_attack = 1
player_attack = 0

player_max_MP = 30
player_MP = 30
player_MP_fill = 5

player_skill_damage = 0
player_skill_base = 0


monster_max_attack = 0
monster_min_attack = 0
monster_attack = 0
gold = 10000

player_choice = 0
monster_choice = 0

level = 1
battles = 1

player_max_attack_up = 0
player_min_attack_up = 0
gold_up = 0

fire_tick = False
fire_tick_damage = 1
fire_tick_damage_plus = 0
fire_tick_turn = 0

freeze = False
freeze_power = 0
freeze_power_up = 0

gamble = 0

skill_list = []
relics_list = []

def item_list(item):
    global gold
    global player_max_attack
    global player_max_HP
    global player_HP

    
    if item == '긴 검':
        gold += 24
        player_max_attack -= 2
        print("팔렸다.")
        input()
    elif item == '작은 지팡이':
        gold += 35
        player_max_attack -= 3
        print("팔렸다.")
        input()
    elif item == '천 갑옷':
        gold += 21
        player_max_HP -= 10
        player_HP -= 10
        if player_HP < 0:
            player_HP = 1
        print("팔렸다.")
        input()
        

def death():
    score = 0
    
    print("죽었습니다.")
    print("-"*15)
    print("당신의 정보")
    print("레벨 : %d" %level)
    print("공격력 : %d ~ %d" %(player_min_attack, player_max_attack))
    print("최대 체력 : %d" %player_max_HP)
    print("최대 마나 : %d" %player_max_MP)
    print("소유 스킬: ",skill_list)
    print("소유 유물: ",relics_list)
    print("소유 돈: %d" %gold)
    print("-"*15)
    print("끝")
    game_on = 0

    
    score = score + ((player_min_attack * 3) + (player_max_attack * 3) + (level * 10) + ((player_max_HP/10) * 5) + (len(relics_list) * 5) + gold)
    print("당신의 점수 %d" %score)
    
    input("")

def battle():
    print("")
    print("상대 체력 : %d / %d" %(monster_HP,monster_max_HP))

    print("체력 : %d / %d" %(player_HP,player_max_HP))
    print("마나 : %d / %d" %(player_MP,player_max_MP))
    
    print("-"*15)
    player_choice = input("1. 공격 2. 스킬 3. 스텟 4. 스킬정보 \n")
    print("")
    
    if player_choice == '1':
        real_battle()
    elif player_choice == '2':
        skill_lists()
    elif player_choice == '3':
        information()
        battle()
    elif player_choice == '4':
        if len(skill_list) == 0:
            print("보유한 스킬이 없습니다.")
            input()
            battle()
        else:
            print("정보를 알고 싶은 스킬 번호를 입력하세요")
            for i in range(len(skill_list)):
                print("%d. %s" %(i+1, skill_list[i]))
            
            player_choice = input("")
        
            if player_choice.isdigit():
                player_choice = int(player_choice)
                if player_choice > len(skill_list):
                    battle()
                else:
                    player_choice = int(player_choice)
                    print("선택한 스킬 : ", skill_list[player_choice-1])
                    input()
                    skill_info(skill_list[player_choice-1])
                    battle()
            else:
                battle()
        
    else:
        battle()


def information():

    print("-"*15)
    print("당신의 정보")
    print("레벨 : %d" %level)
    print("공격력 : %d ~ %d" %(player_min_attack, player_max_attack))
    print("체력 : %d / %d" %(player_HP,player_max_HP))
    print("마나 : %d / %d" %(player_MP,player_max_MP))
    print("턴당 마나 회복량: %d" %player_MP_fill)
    print("소유 스킬: ",skill_list)
    print("소유 유물: ",relics_list)
    print("소유 돈: %d" %gold)
    print("-"*15)
    print("")
    input("")

def first_battle():
    global monster_max_attack
    global monster_min_attack
    global monster_HP
    global monster_max_HP

    monster_max_HP = 30
    monster_HP = 30
    monster_max_attack = 10
    monster_min_attack = 5
    
    while battles == 1:
        if player_HP <= 0:
            death()
            break
        battle()
        if monster_HP <= 0:
            print("승리!")
            level_up()
            break
        monster_fight()
        
def real_battle():
    global monster_HP
    global fire_tick
    global fire_tick_damage
    global fire_tick_turn
    
    
    player_attack = r.randint(player_min_attack,player_max_attack)
    print("당신은 몬스터를 %d 의 대미지로 공격했다." %player_attack)
    monster_HP -= player_attack
    if fire_tick == True:
        if fire_tick_turn == 3:
            fire_tick = False
            print("몬스터의 불이 꺼졌다.")
        else:
            fire_tick_turn += 1
            print("몬스터는 화상 대미지 %d 를 받았다." %(fire_tick_damage + fire_tick_damage_plus))
            monster_HP -= fire_tick_damage + fire_tick_damage_plus
    print("몬스터는 %d 의 체력이 남았다." %monster_HP)
        
    input("")

def monster_fight():
    global player_HP
    global player_MP
    global player_max_MP
    global freeze
    global freeze_power
    
    monster_attack = r.randint(monster_min_attack,monster_max_attack)

    if freeze:
        print("얼음속성 마법으로 인해 몬스터의 대미지가 한턴동안 %d + %d 감소했다." %(freeze_power, freeze_power_up))
        print("%d --> " %monster_attack, end='')
        monster_attack = monster_attack - (freeze_power + freeze_power_up)
        print(monster_attack)
        freeze = False
        if monster_attack < 0:
            monster_attack = 0
    print("몬스터는 당신을 %d 의 대미지로 공격했다." %monster_attack)
    player_HP -= monster_attack
    print("당신은 %d 의 체력이 남았다." %player_HP)
    player_MP += player_MP_fill
    if player_MP > player_max_MP:
        player_MP = player_max_MP
    
    input("")

def start():

    player_choice = input("1. 게임시작 2. 스텟 3. 상점 4.스킬구매 5. 스킬정보 6. 나가기 \n")

    if player_choice == '1':
        if level == 1:
            first_battle()
        elif level == 2:
            print("미구현")
    elif player_choice == '2':
        information()
    elif player_choice == '3':
        print("상점에 오신것을 환영합니다")
        input("")
        shop()
    elif player_choice == '4':
        skill_draw()
    elif player_choice == '5':
        
        if len(skill_list) == 0:
            print("보유한 스킬이 없습니다.")
            input()
            start()
        else:
            print("정보를 알고 싶은 스킬 번호를 입력하세요")
            for i in range(len(skill_list)):
                print("%d. %s" %(i+1, skill_list[i]))
                
            player_choice = input("")
            
            if player_choice.isdigit():
                player_choice = int(player_choice)
                if player_choice > len(skill_list):
                    start()
                else:
                    player_choice = int(player_choice)
                    print("선택한 스킬 : ", skill_list[player_choice-1])
                    input()
                    skill_info(skill_list[player_choice-1])

    elif player_choice == '6':
        sys.exit()

def level_up():

    global player_max_attack_up
    global player_min_attack_up
    global player_max_attack
    global player_min_attack
    global gold_up
    global player_max_HP
    global level
    global gold
    global player_HP
    global player_MP
    global player_max_MP
    global player_MP

    player_max_attack_up = 3
    player_min_attack_up = 3
    gold_up = r.randint(30,100)
    
    print("레벨업!")
    input("")
    print("LV%d > LV%d" %(level, level+1))
    level += 1
    input("")
    print("최대 공격력이 %d 올랐다!" %player_max_attack_up)
    input("")
    print("최소 공격력이 %d 올랐다!" %player_min_attack_up)
    input("")
    print("돈을 %d원 줬다!" %gold_up)
    gold += gold_up
    input("")
    player_max_attack += player_max_attack_up
    player_min_attack += player_min_attack_up
    player_HP_adder = round(player_max_HP * 0.3)
    player_HP = player_HP + player_HP_adder
    player_MP = player_max_MP
    print("체력을 %d 회복했다." %player_HP_adder)
    if player_HP >= 100:
          player_HP = 100
    input("")
    
def skill_lists():
    if len(skill_list) == 0:
        print("보유한 스킬이 없습니다.")
        input()
        battle()
    else:
        for i in range(len(skill_list)):
            print("%d. %s" %(i+1, skill_list[i]))
            
        print("사용할 스킬의 번호를 적어주세요")
        player_choice = input("")

        if player_choice == '0':
            print("0번째 스킬은 없습니다.")
            
        elif player_choice == player_choice:
            player_choice = int(player_choice)
            print("선택한 스킬 : ", skill_list[player_choice-1])
            input()
            skill_attack(skill_list[player_choice-1])
            
        else:
             print("치명적 오류")

def skill_attack(skill):

    global skill_base
    global player_skill_damage
    global monster_HP
    global fire_tick
    global player_MP
    global freeze_power
    global freeze

    if skill == '파이어볼':
        if player_MP < 20:
            print("마나가 모자릅니다.")
            input()
            battle()
        else:
            skill_base = 5
            print("당신은 몬스터를 %d 의 대미지로 공격했다." %(skill_base + player_skill_damage))
            monster_HP -= skill_base + player_skill_damage
            print("몬스터는 %d 의 체력이 남았다." %monster_HP)
            print("몬스터는 불타고 있다.")
            fire_tick = True
            fire_tick_turn = 0
            player_MP -= 20
            input("")
    elif skill == '썬더볼트':
        if player_MP < 30:
            print("마나가 모자릅니다.")
            input()
            battle()
        else:
            skill_base = 10
            print("당신은 몬스터를 %d 의 대미지로 공격했다." %(skill_base + player_skill_damage))
            monster_HP -= skill_base + player_skill_damage
            player_MP -= 30
            input("")
    elif skill == '프로즌오브':
        if player_MP < 20:
            print("마나가 모자릅니다.")
            input()
            battle()
        else:
            skill_base = 3
            freeze_power = 3
            freeze = True
            print("당신은 몬스터를 %d 의 대미지로 공격했다." %(skill_base + player_skill_damage))
            monster_HP -= skill_base + player_skill_damage
            player_MP -= 30
            input("")


def shop():
    global player_max_attack
    global gold
    global player_max_HP
    global player_HP
    
    print("당신의 돈 : %d" %gold)
    input("--------------------- \n")
    print("1. 긴 검 : 35 gold")
    print("2. 작은 지팡이 : 50 gold")
    print("3. 천 갑옷 : 30 gold")
    print("99. 판매")
    print("아무키나 눌러서 나가기")
    print("")
    player_choice = input("")

    if player_choice == '1':
        print("")
        print("낡은 긴 검. 너무 오래되어서 실전성은 떨어져 보인다.")
        print("최대 대미지를 2 올려준다.")
        print("1. 산다 2. 안 산다")
        player_choice = input("")

        if player_choice == '1':
            shop_buy('긴 검')
            input()
        elif player_choice == '2':
            shop()
        else:
            shop()
    elif player_choice == '2':
        print("")
        print("작은 지팡이. 너무 작아서 들기도 힘들다. 위협적으로 보인다.")
        print("최대 대미지를 3 올려준다.")
        print("1. 산다 2. 안 산다")
        player_choice = input("")

        if player_choice == '1':
            shop_buy('작은 지팡이')
            input()
        elif player_choice == '2':
            shop()
        else:
            shop()
    elif player_choice == '3':
        print("")
        print("천 갑옷. 천으로 만들었지만 지나치게 무게감이 느껴진다.")
        print("최대 체력을 10 올려준다.")
        print("1. 산다 2. 안 산다")
        player_choice = input("")

        if player_choice == '1':
            shop_buy('천 갑옷')
            input()
        elif player_choice == '2':
            shop()
        else:
            shop()
    elif player_choice == '99':

        if len(relics_list) != 0:
            print("판매할 아이템")
            for i in range(len(relics_list)):
                print("%d. %s" %(i+1, relics_list[i]))
            print("판매할 아이템의 번호를 적어주세요")
            player_choice = input("")
            
            try:
                if player_choice == '0':
                    print("0번째 물건은 없습니다.")
                    
                elif player_choice == player_choice:
                    player_choice = int(player_choice)
                    print("선택한 아이템 : ", relics_list[player_choice-1], " 1. 판다 2. 안 판다")
                    player_choice = input("")

                    if player_choice == player_choice:
                        player_choice = int(player_choice)
                        item_list(relics_list[player_choice-1])
                        del relics_list[player_choice-1]
                
            
                else:
                     print("판매할 아이템이 없습니다.")
                     print("")
                     shop()
            except:
                print("숫자를 입력해 주세요")
                input()
                    
        
    else:
        print("돌아갔다")
        input("")

def shop_buy(item):
    global player_max_attack
    global gold
    global player_max_HP
    global player_HP

    if item in relics_list:
        print("중복되는 아이템은 구매할 수 없습니다.")
        print("")
        shop()
    elif item == '긴 검':
        relics_list.append('긴 검')
        gold -= 35
        player_max_attack += 2
        print("구매했다.")
        input()
        shop()

    elif item == '작은 지팡이':
        relics_list.append('작은 지팡이')
        gold -= 50
        player_max_attack += 3
        print("구매했다.")
        input()
        shop()
        
    elif item == '천 갑옷':
        relics_list.append('천 갑옷')
        gold -= 30
        player_max_HP += 10
        player_HP += 10
        print("구매했다.")
        input()
        shop()

def skill_info(sk):

    if sk == '파이어볼':
        print("거의 모든 판타지에 등장하는 기초 마법")
        print("가장 흔하고 누구나 쓸 수 있지만 위험한 마법이다.")
        print("상대방에게 5 + %d 대미지를 주고 1 + %d 의 화상 대미지를 입힌다." %(player_skill_damage,fire_tick_damage_plus))
        print("MP 20 소요")
        input()
    elif sk == '썬더볼트':
        print("배울 수 있는 기초 마법중에 가장 위험한 마법")
        print("썬더볼트로 핸드폰을 충전하다 폭팔사고가 많이 일어난다.")
        print("상대방에게 5 + %d 대미지를 준다" %player_skill_damage)
        print("MP 30 소요")
        input()
    elif sk == '프로즌오브':
        print("얼음구체로 상대방을 타격하는 마법")
        print("매우 차가워서 손에서 자주 놓친다.")
        print("상대방에게 3 + %d 대미지를 준다" %player_skill_damage)
        print("상대방의 대미지를 1턴동안 3 + %d 감소 시킨다" %freeze_power_up)
        print("MP 20 소요")
        input()

    
def skill_draw():
    global gold
    print("스킬 상점에 오신것을 환영합니다.")
    print("스킬을 랜덤적으로 구매할 수 있습니다.")
    print("중복되는 스킬은 소멸하고 돈은 반값만 돌려줍니다.")
    input()
    print("1. 산다 2. 안 산다")
    
    player_choice = input()

    if player_choice == "1":
        if gold > 100:
            skilldraw = r.randint(1,100)
            if 1 <= skilldraw <= 80:
                print("일반 등급의 스킬")
                skilldraw = r.randint(1,3)
                if skilldraw == 1:
                    print("파이어볼 습득")
                    input()
                    if '파이어볼' in skill_list:
                        print("중복되는 스킬입니다.")
                        print("50 gold를 돌려받았습니다.")
                        input()
                        gold += 50
                    else:
                        gold -= 100
                        skill_list.append('파이어볼')
                elif skilldraw == 2:
                    print("썬더볼트 습득")
                    input()
                    if '썬더볼트' in skill_list:
                        print("중복되는 스킬입니다.")
                        print("50 gold를 돌려받았습니다.")
                        input()
                        gold += 50
                    else:
                        gold -= 100
                        skill_list.append('썬더볼트')
                elif skilldraw == 3:
                    print("프로즌오브 습득")
                    input()
                    if '프로즌오브' in skill_list:
                        print("중복되는 스킬입니다.")
                        print("50 gold를 돌려받았습니다.")
                        input()
                        gold += 50
                    else:
                        gold -= 100
                        skill_list.append('프로즌오브')

            elif 80 <= skilldraw <= 95:
                print("희귀 등급의 스킬")
                print("미구현")
            elif 95 <= skilldraw <= 100:
                print("전설 등급의 스킬")
                print("미구현")
        else:
            print("돈이 없습니다.")

while game_on == 1:    
    start()
