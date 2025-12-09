# -*- coding: utf-8 -*-
"""스킬 시스템 정의"""

import random
from dataclasses import dataclass
from typing import Optional


@dataclass
class SkillEffect:
    """스킬 효과 데이터"""
    damage: int = 0
    mp_cost: int = 0
    apply_burn: bool = False
    burn_damage: int = 0
    apply_freeze: bool = False
    freeze_reduction: int = 0


class Skill:
    """개별 스킬 정의"""
    
    def __init__(self, name: str, description: str, effect: SkillEffect, rarity: str = "일반"):
        self.name = name
        self.description = description
        self.effect = effect
        self.rarity = rarity
    
    def get_info(self, player_skill_bonus: int = 0, fire_bonus: int = 0, freeze_bonus: int = 0) -> str:
        """스킬 정보 문자열 반환"""
        info_lines = [self.description]
        
        total_damage = self.effect.damage + player_skill_bonus
        info_lines.append(f"상대방에게 {total_damage} 대미지를 준다")
        
        if self.effect.apply_burn:
            total_burn = self.effect.burn_damage + fire_bonus
            info_lines.append(f"화상 대미지 {total_burn}를 입힌다")
        
        if self.effect.apply_freeze:
            total_freeze = self.effect.freeze_reduction + freeze_bonus
            info_lines.append(f"상대방의 대미지를 1턴동안 {total_freeze} 감소시킨다")
        
        info_lines.append(f"MP {self.effect.mp_cost} 소요")
        
        return "\n".join(info_lines)


# 미리 정의된 스킬들
SKILLS = {
    "파이어볼": Skill(
        name="파이어볼",
        description="거의 모든 판타지에 등장하는 기초 마법\n가장 흔하고 누구나 쓸 수 있지만 위험한 마법이다.",
        effect=SkillEffect(
            damage=5,
            mp_cost=20,
            apply_burn=True,
            burn_damage=1
        ),
        rarity="일반"
    ),
    "썬더볼트": Skill(
        name="썬더볼트",
        description="배울 수 있는 기초 마법중에 가장 위험한 마법\n썬더볼트로 핸드폰을 충전하다 폭팔사고가 많이 일어난다.",
        effect=SkillEffect(
            damage=10,
            mp_cost=30
        ),
        rarity="일반"
    ),
    "프로즌오브": Skill(
        name="프로즌오브",
        description="얼음구체로 상대방을 타격하는 마법\n매우 차가워서 손에서 자주 놓친다.",
        effect=SkillEffect(
            damage=3,
            mp_cost=20,
            apply_freeze=True,
            freeze_reduction=3
        ),
        rarity="일반"
    )
}


class SkillShop:
    """스킬 상점 시스템"""
    
    DRAW_COST = 100
    REFUND_RATE = 0.5
    
    # 등급별 확률
    RARITY_CHANCES = {
        "일반": (1, 80),    # 1~80
        "희귀": (81, 95),   # 81~95
        "전설": (96, 100)   # 96~100
    }
    
    NORMAL_SKILLS = ["파이어볼", "썬더볼트", "프로즌오브"]
    RARE_SKILLS = []  # 미구현
    LEGENDARY_SKILLS = []  # 미구현
    
    @classmethod
    def draw_skill(cls, player_gold: int, player_skills: list) -> tuple:
        """
        스킬 뽑기
        Returns: (success: bool, skill_name: str or None, gold_change: int, message: str)
        """
        if player_gold < cls.DRAW_COST:
            return False, None, 0, "돈이 없습니다."
        
        roll = random.randint(1, 100)
        
        # 등급 결정
        if roll <= 80:
            rarity = "일반"
            skill_pool = cls.NORMAL_SKILLS
        elif roll <= 95:
            rarity = "희귀"
            skill_pool = cls.RARE_SKILLS
        else:
            rarity = "전설"
            skill_pool = cls.LEGENDARY_SKILLS
        
        # 스킬 풀이 비어있으면 (미구현)
        if not skill_pool:
            return False, None, 0, f"{rarity} 등급의 스킬 - 미구현"
        
        # 랜덤 스킬 선택
        skill_name = random.choice(skill_pool)
        
        # 중복 체크
        if skill_name in player_skills:
            refund = int(cls.DRAW_COST * cls.REFUND_RATE)
            return True, None, refund, f"{skill_name} 습득\n중복되는 스킬입니다.\n{refund} gold를 돌려받았습니다."
        
        return True, skill_name, -cls.DRAW_COST, f"{rarity} 등급의 스킬\n{skill_name} 습득!"
