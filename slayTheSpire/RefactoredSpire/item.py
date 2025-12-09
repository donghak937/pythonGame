# -*- coding: utf-8 -*-
"""아이템/유물 시스템 정의"""

from dataclasses import dataclass
from typing import Callable


@dataclass
class ItemEffect:
    """아이템 효과 데이터"""
    max_attack_bonus: int = 0
    min_attack_bonus: int = 0
    max_hp_bonus: int = 0
    hp_bonus: int = 0


class Item:
    """개별 아이템 정의"""
    
    def __init__(self, name: str, description: str, price: int, sell_price: int, effect: ItemEffect):
        self.name = name
        self.description = description
        self.price = price
        self.sell_price = sell_price
        self.effect = effect
    
    def get_info(self) -> str:
        """아이템 정보 반환"""
        info_lines = [self.description]
        
        if self.effect.max_attack_bonus:
            info_lines.append(f"최대 대미지를 {self.effect.max_attack_bonus} 올려준다.")
        if self.effect.min_attack_bonus:
            info_lines.append(f"최소 대미지를 {self.effect.min_attack_bonus} 올려준다.")
        if self.effect.max_hp_bonus:
            info_lines.append(f"최대 체력을 {self.effect.max_hp_bonus} 올려준다.")
        
        return "\n".join(info_lines)


# 미리 정의된 아이템들
ITEMS = {
    "긴 검": Item(
        name="긴 검",
        description="낡은 긴 검. 너무 오래되어서 실전성은 떨어져 보인다.",
        price=35,
        sell_price=24,
        effect=ItemEffect(max_attack_bonus=2)
    ),
    "작은 지팡이": Item(
        name="작은 지팡이",
        description="작은 지팡이. 너무 작아서 들기도 힘들다. 위협적으로 보인다.",
        price=50,
        sell_price=35,
        effect=ItemEffect(max_attack_bonus=3)
    ),
    "천 갑옷": Item(
        name="천 갑옷",
        description="천 갑옷. 천으로 만들었지만 지나치게 무게감이 느껴진다.",
        price=30,
        sell_price=21,
        effect=ItemEffect(max_hp_bonus=10, hp_bonus=10)
    )
}


class Shop:
    """상점 시스템"""
    
    @staticmethod
    def get_item_list() -> list:
        """판매 중인 아이템 목록 반환"""
        return [
            (name, item.price) 
            for name, item in ITEMS.items()
        ]
    
    @staticmethod
    def buy_item(item_name: str, player) -> tuple:
        """
        아이템 구매
        Returns: (success: bool, message: str)
        """
        if item_name not in ITEMS:
            return False, "존재하지 않는 아이템입니다."
        
        item = ITEMS[item_name]
        
        if item_name in player.relics:
            return False, "중복되는 아이템은 구매할 수 없습니다."
        
        if player.gold < item.price:
            return False, "돈이 부족합니다."
        
        # 구매 처리
        player.gold -= item.price
        player.relics.append(item_name)
        player.max_attack += item.effect.max_attack_bonus
        player.min_attack += item.effect.min_attack_bonus
        player.max_hp += item.effect.max_hp_bonus
        player.hp += item.effect.hp_bonus
        
        return True, "구매했다."
    
    @staticmethod
    def sell_item(item_name: str, player) -> tuple:
        """
        아이템 판매
        Returns: (success: bool, message: str)
        """
        if item_name not in ITEMS:
            return False, "존재하지 않는 아이템입니다."
        
        if item_name not in player.relics:
            return False, "소유하지 않은 아이템입니다."
        
        item = ITEMS[item_name]
        
        # 판매 처리 (효과 제거)
        player.gold += item.sell_price
        player.relics.remove(item_name)
        player.max_attack -= item.effect.max_attack_bonus
        player.min_attack -= item.effect.min_attack_bonus
        player.max_hp -= item.effect.max_hp_bonus
        player.hp -= item.effect.hp_bonus
        
        if player.hp < 1:
            player.hp = 1
        
        return True, "팔렸다."
