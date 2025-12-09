# -*- coding: utf-8 -*-
"""몬스터 클래스 정의"""

import random


class Monster:
    """몬스터 상태와 행동을 관리하는 클래스"""
    
    def __init__(self, name: str, hp: int, min_attack: int, max_attack: int):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.min_attack = min_attack
        self.max_attack = max_attack
        
        # 상태이상
        self.is_burning = False
        self.burn_damage = 1
        self.burn_turns = 0
        
        self.is_frozen = False
        self.freeze_reduction = 0
    
    def attack(self) -> int:
        """공격 대미지 계산 (빙결 효과 적용)"""
        damage = random.randint(self.min_attack, self.max_attack)
        
        if self.is_frozen:
            damage -= self.freeze_reduction
            self.is_frozen = False  # 빙결은 1턴만 지속
            if damage < 0:
                damage = 0
        
        return damage
    
    def take_damage(self, amount: int):
        """대미지를 받음"""
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0
    
    def apply_burn(self, damage: int = 1, turns: int = 3):
        """화상 상태 적용"""
        self.is_burning = True
        self.burn_damage = damage
        self.burn_turns = turns
    
    def process_burn(self) -> int:
        """화상 대미지 처리, 입힌 대미지 반환"""
        if not self.is_burning:
            return 0
        
        self.burn_turns -= 1
        damage = self.burn_damage
        self.hp -= damage
        
        if self.burn_turns <= 0:
            self.is_burning = False
        
        return damage
    
    def apply_freeze(self, reduction: int):
        """빙결 상태 적용"""
        self.is_frozen = True
        self.freeze_reduction = reduction
    
    def is_dead(self) -> bool:
        """사망 여부 확인"""
        return self.hp <= 0
    
    def get_status(self) -> str:
        """몬스터 상태 문자열 반환"""
        status = f"상대 체력 : {self.hp} / {self.max_hp}"
        if self.is_burning:
            status += f" [화상 {self.burn_turns}턴]"
        if self.is_frozen:
            status += " [빙결]"
        return status


# 미리 정의된 몬스터 팩토리
class MonsterFactory:
    """몬스터 생성 팩토리"""
    
    @staticmethod
    def create_level1_monster() -> Monster:
        """레벨 1 몬스터 생성"""
        return Monster("슬라임", hp=30, min_attack=5, max_attack=10)
    
    @staticmethod
    def create_level2_monster() -> Monster:
        """레벨 2 몬스터 생성 (추후 구현)"""
        return Monster("고블린", hp=50, min_attack=8, max_attack=15)
