# -*- coding: utf-8 -*-
"""전투 시스템 정의"""

from player import Player
from monster import Monster
from skill import SKILLS


class Combat:
    """전투 관리 클래스"""
    
    def __init__(self, player: Player, monster: Monster):
        self.player = player
        self.monster = monster
        self.is_battle_active = True
    
    def player_basic_attack(self) -> dict:
        """
        플레이어 기본 공격
        Returns: 공격 결과 정보
        """
        damage = self.player.attack()
        self.monster.take_damage(damage)
        
        result = {
            'damage': damage,
            'monster_hp': self.monster.hp,
            'burn_damage': 0
        }
        
        # 화상 대미지 처리
        if self.monster.is_burning:
            burn_dmg = self.monster.process_burn()
            result['burn_damage'] = burn_dmg
            result['burn_ended'] = not self.monster.is_burning
        
        return result
    
    def player_skill_attack(self, skill_name: str) -> dict:
        """
        플레이어 스킬 공격
        Returns: 공격 결과 정보
        """
        if skill_name not in SKILLS:
            return {'success': False, 'message': '존재하지 않는 스킬입니다.'}
        
        if skill_name not in self.player.skills:
            return {'success': False, 'message': '보유하지 않은 스킬입니다.'}
        
        skill = SKILLS[skill_name]
        
        # 마나 체크
        if not self.player.use_mp(skill.effect.mp_cost):
            return {'success': False, 'message': '마나가 모자릅니다.'}
        
        # 대미지 계산 (스킬 대미지 + 보너스)
        total_damage = skill.effect.damage + self.player.skill_damage_bonus
        self.monster.take_damage(total_damage)
        
        result = {
            'success': True,
            'damage': total_damage,
            'monster_hp': self.monster.hp,
            'skill_name': skill_name
        }
        
        # 화상 적용
        if skill.effect.apply_burn:
            burn_damage = skill.effect.burn_damage + self.player.fire_tick_damage_bonus
            self.monster.apply_burn(burn_damage, 3)
            result['applied_burn'] = True
            result['burn_damage'] = burn_damage
        
        # 빙결 적용
        if skill.effect.apply_freeze:
            freeze_reduction = skill.effect.freeze_reduction + self.player.freeze_power_bonus
            self.monster.apply_freeze(freeze_reduction)
            result['applied_freeze'] = True
            result['freeze_reduction'] = freeze_reduction
        
        return result
    
    def monster_attack(self) -> dict:
        """
        몬스터 공격 및 턴 종료 처리
        Returns: 공격 결과 정보
        """
        was_frozen = self.monster.is_frozen
        freeze_reduction = self.monster.freeze_reduction if was_frozen else 0
        
        damage = self.monster.attack()
        original_damage = damage + freeze_reduction if was_frozen else damage
        
        self.player.take_damage(damage)
        self.player.regen_mp()
        
        return {
            'damage': damage,
            'original_damage': original_damage,
            'was_frozen': was_frozen,
            'freeze_reduction': freeze_reduction,
            'player_hp': self.player.hp,
            'player_mp': self.player.mp
        }
    
    def check_battle_end(self) -> tuple:
        """
        전투 종료 조건 확인
        Returns: (ended: bool, player_won: bool or None)
        """
        if self.player.is_dead():
            self.is_battle_active = False
            return True, False
        
        if self.monster.is_dead():
            self.is_battle_active = False
            return True, True
        
        return False, None
    
    def get_battle_status(self) -> str:
        """현재 전투 상태 문자열 반환"""
        lines = [
            "",
            self.monster.get_status(),
            f"체력 : {self.player.hp} / {self.player.max_hp}",
            f"마나 : {self.player.mp} / {self.player.max_mp}",
            "-" * 15
        ]
        return "\n".join(lines)
