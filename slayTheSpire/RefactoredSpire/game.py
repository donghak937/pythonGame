# -*- coding: utf-8 -*-
"""게임 메인 로직"""

import sys
from player import Player
from monster import Monster, MonsterFactory
from combat import Combat
from skill import SKILLS, SkillShop
from item import ITEMS, Shop


class Game:
    """게임 전체를 관리하는 클래스"""
    
    def __init__(self):
        self.player = Player()
        self.is_running = True
        self.current_combat = None
    
    def run(self):
        """게임 메인 루프"""
        print("=" * 30)
        print("      Slay the Spire")
        print("=" * 30)
        
        while self.is_running:
            self.main_menu()
    
    def main_menu(self):
        """메인 메뉴"""
        print("\n1. 게임시작 2. 스텟 3. 상점 4. 스킬구매 5. 스킬정보 6. 나가기")
        choice = input()
        
        if choice == '1':
            self.start_battle()
        elif choice == '2':
            self.show_player_info()
        elif choice == '3':
            self.visit_shop()
        elif choice == '4':
            self.visit_skill_shop()
        elif choice == '5':
            self.show_skill_info()
        elif choice == '6':
            self.quit_game()
    
    def start_battle(self):
        """전투 시작"""
        if self.player.level == 1:
            monster = MonsterFactory.create_level1_monster()
        elif self.player.level == 2:
            monster = MonsterFactory.create_level2_monster()
        else:
            print("미구현")
            return
        
        self.current_combat = Combat(self.player, monster)
        self.battle_loop()
    
    def battle_loop(self):
        """전투 루프"""
        while self.current_combat.is_battle_active:
            # 플레이어 사망 체크
            if self.player.is_dead():
                self.game_over()
                return
            
            # 전투 상태 출력 및 행동 선택
            print(self.current_combat.get_battle_status())
            print("1. 공격 2. 스킬 3. 스텟 4. 스킬정보")
            choice = input()
            
            if choice == '1':
                self.execute_basic_attack()
            elif choice == '2':
                self.execute_skill_menu()
            elif choice == '3':
                self.show_player_info()
                continue  # 턴 소모 안함
            elif choice == '4':
                self.show_skill_info_in_battle()
                continue  # 턴 소모 안함
            else:
                continue
            
            # 몬스터 사망 체크
            ended, player_won = self.current_combat.check_battle_end()
            if ended:
                if player_won:
                    self.victory()
                return
            
            # 몬스터 턴
            self.execute_monster_turn()
            
            # 다시 플레이어 사망 체크
            if self.player.is_dead():
                self.game_over()
                return
    
    def execute_basic_attack(self):
        """기본 공격 실행"""
        result = self.current_combat.player_basic_attack()
        
        print(f"당신은 몬스터를 {result['damage']}의 대미지로 공격했다.")
        
        if result.get('burn_damage', 0) > 0:
            print(f"몬스터는 화상 대미지 {result['burn_damage']}를 받았다.")
            if result.get('burn_ended'):
                print("몬스터의 불이 꺼졌다.")
        
        print(f"몬스터는 {result['monster_hp']}의 체력이 남았다.")
        input()
    
    def execute_skill_menu(self):
        """스킬 메뉴"""
        if not self.player.skills:
            print("보유한 스킬이 없습니다.")
            input()
            return
        
        for i, skill_name in enumerate(self.player.skills, 1):
            print(f"{i}. {skill_name}")
        
        print("사용할 스킬의 번호를 적어주세요 (0: 취소)")
        choice = input()
        
        if choice == '0':
            return
        
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(self.player.skills):
                skill_name = self.player.skills[idx]
                self.execute_skill_attack(skill_name)
            else:
                print("잘못된 번호입니다.")
    
    def execute_skill_attack(self, skill_name: str):
        """스킬 공격 실행"""
        result = self.current_combat.player_skill_attack(skill_name)
        
        if not result['success']:
            print(result['message'])
            input()
            return
        
        print(f"당신은 몬스터를 {result['damage']}의 대미지로 공격했다.")
        
        if result.get('applied_burn'):
            print("몬스터는 불타고 있다.")
        
        if result.get('applied_freeze'):
            print(f"몬스터는 얼어붙었다. (대미지 {result['freeze_reduction']} 감소)")
        
        print(f"몬스터는 {result['monster_hp']}의 체력이 남았다.")
        input()
    
    def execute_monster_turn(self):
        """몬스터 턴 실행"""
        result = self.current_combat.monster_attack()
        
        if result['was_frozen']:
            reduction = result['freeze_reduction']
            print(f"얼음속성 마법으로 인해 몬스터의 대미지가 {reduction} 감소했다.")
            print(f"{result['original_damage']} --> {result['damage']}")
        
        print(f"몬스터는 당신을 {result['damage']}의 대미지로 공격했다.")
        print(f"당신은 {result['player_hp']}의 체력이 남았다.")
        input()
    
    def victory(self):
        """승리 처리"""
        print("승리!")
        input()
        
        level_info = self.player.level_up()
        
        print("레벨업!")
        input()
        print(f"LV{self.player.level - 1} > LV{self.player.level}")
        input()
        print(f"최대 공격력이 {level_info['attack_up']} 올랐다!")
        input()
        print(f"최소 공격력이 {level_info['attack_up']} 올랐다!")
        input()
        print(f"돈을 {level_info['gold_reward']}원 줬다!")
        input()
        print(f"체력을 {level_info['hp_recover']} 회복했다.")
        input()
    
    def game_over(self):
        """게임 오버 처리"""
        print("죽었습니다.")
        info, score = self.player.get_death_info()
        print(info)
        print("끝")
        print(f"당신의 점수 {score}")
        input()
        self.is_running = False
    
    def show_player_info(self):
        """플레이어 정보 표시"""
        print(self.player.get_info())
        input()
    
    def show_skill_info(self):
        """스킬 정보 표시 (메인 메뉴)"""
        if not self.player.skills:
            print("보유한 스킬이 없습니다.")
            input()
            return
        
        print("정보를 알고 싶은 스킬 번호를 입력하세요")
        for i, skill_name in enumerate(self.player.skills, 1):
            print(f"{i}. {skill_name}")
        
        choice = input()
        
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(self.player.skills):
                skill_name = self.player.skills[idx]
                self._display_skill_info(skill_name)
    
    def show_skill_info_in_battle(self):
        """스킬 정보 표시 (전투 중)"""
        if not self.player.skills:
            print("보유한 스킬이 없습니다.")
            input()
            return
        
        print("정보를 알고 싶은 스킬 번호를 입력하세요")
        for i, skill_name in enumerate(self.player.skills, 1):
            print(f"{i}. {skill_name}")
        
        choice = input()
        
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(self.player.skills):
                skill_name = self.player.skills[idx]
                self._display_skill_info(skill_name)
    
    def _display_skill_info(self, skill_name: str):
        """실제 스킬 정보 출력"""
        if skill_name in SKILLS:
            skill = SKILLS[skill_name]
            info = skill.get_info(
                self.player.skill_damage_bonus,
                self.player.fire_tick_damage_bonus,
                self.player.freeze_power_bonus
            )
            print(f"[{skill_name}]")
            print(info)
            input()
    
    def visit_shop(self):
        """상점 방문"""
        print("상점에 오신것을 환영합니다")
        input()
        
        while True:
            print(f"당신의 돈 : {self.player.gold}")
            print("-" * 21)
            
            items = Shop.get_item_list()
            for i, (name, price) in enumerate(items, 1):
                print(f"{i}. {name} : {price} gold")
            
            print("99. 판매")
            print("0. 나가기")
            print()
            
            choice = input()
            
            if choice == '0':
                print("돌아갔다")
                input()
                break
            elif choice == '99':
                self.sell_item_menu()
            elif choice.isdigit():
                idx = int(choice) - 1
                item_names = list(ITEMS.keys())
                if 0 <= idx < len(item_names):
                    self.buy_item_menu(item_names[idx])
    
    def buy_item_menu(self, item_name: str):
        """아이템 구매 메뉴"""
        item = ITEMS[item_name]
        print()
        print(item.get_info())
        print("1. 산다 2. 안 산다")
        
        choice = input()
        if choice == '1':
            success, message = Shop.buy_item(item_name, self.player)
            print(message)
            input()
    
    def sell_item_menu(self):
        """아이템 판매 메뉴"""
        if not self.player.relics:
            print("판매할 아이템이 없습니다.")
            input()
            return
        
        print("판매할 아이템")
        for i, relic in enumerate(self.player.relics, 1):
            sell_price = ITEMS[relic].sell_price if relic in ITEMS else 0
            print(f"{i}. {relic} ({sell_price} gold)")
        
        print("판매할 아이템의 번호를 적어주세요 (0: 취소)")
        choice = input()
        
        if choice == '0':
            return
        
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(self.player.relics):
                relic_name = self.player.relics[idx]
                
                print(f"선택한 아이템 : {relic_name}")
                print("1. 판다 2. 안 판다")
                confirm = input()
                
                if confirm == '1':
                    success, message = Shop.sell_item(relic_name, self.player)
                    print(message)
                    input()
    
    def visit_skill_shop(self):
        """스킬 상점 방문"""
        print("스킬 상점에 오신것을 환영합니다.")
        print("스킬을 랜덤적으로 구매할 수 있습니다.")
        print("중복되는 스킬은 소멸하고 돈은 반값만 돌려줍니다.")
        print(f"비용: {SkillShop.DRAW_COST} gold")
        input()
        
        print("1. 산다 2. 안 산다")
        choice = input()
        
        if choice == '1':
            success, skill_name, gold_change, message = SkillShop.draw_skill(
                self.player.gold, 
                self.player.skills
            )
            
            print(message)
            
            if success:
                self.player.gold += gold_change
                if skill_name:
                    self.player.add_skill(skill_name)
            
            input()
    
    def quit_game(self):
        """게임 종료"""
        print("게임을 종료합니다.")
        self.is_running = False
        sys.exit()
