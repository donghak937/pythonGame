# -*- coding: utf-8 -*-
"""플레이어 클래스 정의"""

import random


class Player:
    """플레이어 상태와 행동을 관리하는 클래스"""
    
    def __init__(self):
        # 기본 스탯
        self.hp = 100
        self.max_hp = 100
        self.mp = 30
        self.max_mp = 30
        self.mp_regen = 10  # 턴당 마나 회복량
        
        # 공격력
        self.min_attack = 5
        self.max_attack = 10
        
        # 레벨 & 골드
        self.level = 1
        self.gold = 50
        
        # 스킬 대미지 보너스
        self.skill_damage_bonus = 0
        
        # 인벤토리
        self.skills = []
        self.relics = []
        
        # 상태이상 관련
        self.fire_tick_damage_bonus = 0
        self.freeze_power_bonus = 0
    
    def attack(self) -> int:
        """기본 공격 대미지 계산"""
        return random.randint(self.min_attack, self.max_attack)
    
    def take_damage(self, amount: int):
        """대미지를 받음"""
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0
    
    def heal(self, amount: int):
        """체력 회복"""
        self.hp += amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp
    
    def use_mp(self, amount: int) -> bool:
        """마나 사용, 성공 여부 반환"""
        if self.mp >= amount:
            self.mp -= amount
            return True
        return False
    
    def regen_mp(self):
        """턴 종료시 마나 회복"""
        self.mp += self.mp_regen
        if self.mp > self.max_mp:
            self.mp = self.max_mp
    
    def is_dead(self) -> bool:
        """사망 여부 확인"""
        return self.hp <= 0
    
    def level_up(self) -> dict:
        """레벨업 처리, 증가된 스탯 정보 반환"""
        self.level += 1
        
        # 스탯 증가량
        attack_up = 3
        gold_reward = random.randint(30, 100)
        hp_recover = round(self.max_hp * 0.3)
        
        # 적용
        self.max_attack += attack_up
        self.min_attack += attack_up
        self.gold += gold_reward
        self.hp += hp_recover
        if self.hp > self.max_hp:
            self.hp = self.max_hp
        self.mp = self.max_mp
        
        return {
            'attack_up': attack_up,
            'gold_reward': gold_reward,
            'hp_recover': hp_recover
        }
    
    def add_skill(self, skill_name: str) -> bool:
        """스킬 추가, 중복 시 False 반환"""
        if skill_name in self.skills:
            return False
        self.skills.append(skill_name)
        return True
    
    def add_relic(self, relic_name: str) -> bool:
        """유물 추가, 중복 시 False 반환"""
        if relic_name in self.relics:
            return False
        self.relics.append(relic_name)
        return True
    
    def remove_relic(self, relic_name: str) -> bool:
        """유물 제거"""
        if relic_name in self.relics:
            self.relics.remove(relic_name)
            return True
        return False
    
    def get_info(self) -> str:
        """플레이어 정보 문자열 반환"""
        info = [
            "-" * 15,
            "당신의 정보",
            f"레벨 : {self.level}",
            f"공격력 : {self.min_attack} ~ {self.max_attack}",
            f"체력 : {self.hp} / {self.max_hp}",
            f"마나 : {self.mp} / {self.max_mp}",
            f"턴당 마나 회복량: {self.mp_regen}",
            f"소유 스킬: {self.skills}",
            f"소유 유물: {self.relics}",
            f"소유 돈: {self.gold}",
            "-" * 15
        ]
        return "\n".join(info)
    
    def get_death_info(self) -> tuple:
        """사망 시 점수와 함께 정보 반환"""
        score = (
            (self.min_attack * 3) + 
            (self.max_attack * 3) + 
            (self.level * 10) + 
            ((self.max_hp / 10) * 5) + 
            (len(self.relics) * 5) + 
            self.gold
        )
        return self.get_info(), int(score)
