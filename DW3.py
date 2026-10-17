from __future__ import annotations

import functools, random
from typing import List, Dict, Set

from dataclasses import dataclass

from Options import Toggle, Option, DefaultOnToggle, TextChoice, NamedRange

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms

@dataclass
class DW3ArchipelagoOptions:
    dw3_include_xtreme_legends: Dw3IncludeXtremeLegends
    dw3_include_unique_items: Dw3IncludeUniqueItems


class DW3Game(Game):
    name = "Dynasty Warriors 3"
    platform = KeymastersKeepGamePlatforms.PS2

    platforms_other = [
        KeymastersKeepGamePlatforms.XBOX,
        KeymastersKeepGamePlatforms.PC
    ]

    is_adult_only_or_unrated = False

    options_cls = DW3ArchipelagoOptions

    # Constraints
    def optional_game_constraint_templates(self) -> list[GameObjectiveTemplate]:
       
        return []

    
    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        game_objective_templates: List[GameObjectiveTemplate] = list()

        # musuo modes
        game_objective_templates.extend([
            GameObjectiveTemplate(
                label="Play GENERAL in Musou Mode",
                data={
                    "GENERAL": (self.generals_musuo, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=10,
            ),
            GameObjectiveTemplate(
                label="Play GENERAL in Musou Mode on Easy or higher difficulty",
                data={
                    "GENERAL": (self.generals_musuo, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=10,
            ),
            GameObjectiveTemplate(
                label="Play GENERAL in Musou Mode on Normal or higher difficulty",
                data={
                    "GENERAL": (self.generals_musuo, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=10,
            ),
            GameObjectiveTemplate(
                label="Play GENERAL in Musou Mode on Hard or higher difficulty",
                data={
                    "GENERAL": (self.generals_musuo, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=10,
            ),                                    
            GameObjectiveTemplate(
                label="Play GENERAL in Free Play Mode on STAGE on Easy or higher difficulty", 
                data={
                    "GENERAL": (self.generals, 1),
                    "STAGE": (self.stages, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=10,
            ),
            GameObjectiveTemplate(
                label="Play GENERAL in Free Play Mode on STAGE on Normal or higher difficulty", 
                data={
                    "GENERAL": (self.generals, 1),
                    "STAGE": (self.stages, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=10,
            ),
            GameObjectiveTemplate(
                label="Play GENERAL in Free Play Mode on STAGE on Hard or higher difficulty", 
                data={
                    "GENERAL": (self.generals, 1),
                    "STAGE": (self.stages, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=10,
            ),
        ])

        if self.include_xtreme_legends:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Play GENERAL in Musou Mode", 
                    data={
                        "GENERAL": (self.generals_musuo_xl, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=10,
                ),
                GameObjectiveTemplate(
                    label="Play GENERAL in Musou Mode on Easy or higher difficulty", 
                    data={
                        "GENERAL": (self.generals_musuo_xl, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=10,
                ),                
                GameObjectiveTemplate(
                    label="Play GENERAL in Musou Mode Normal or higher difficulty", 
                    data={
                        "GENERAL": (self.generals_musuo_xl, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=10,
                ),
                GameObjectiveTemplate(
                    label="Play GENERAL in Musou Mode on Hard or higher difficulty", 
                    data={
                        "GENERAL": (self.generals_musuo_xl, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=10,
                ),
                GameObjectiveTemplate(
                    label="Play GENERAL in Musou Mode on XTreme or higher difficulty", 
                    data={
                        "GENERAL": (self.generals_musuo_xl, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=10,
                ),                
                GameObjectiveTemplate(
                    label="Play GENERAL in Musou Mode on XTreme or higher difficulty", 
                    data={
                        "GENERAL": (self.generals_musuo, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=10,
                ),
                GameObjectiveTemplate(
                    label="Play GENERAL in Free Play Mode on STAGE on Easy or higher difficulty", 
                    data={
                        "GENERAL": (self.generals, 1),
                        "STAGE": (self.stages_xl, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=10,
                ),
                GameObjectiveTemplate(
                    label="Play GENERAL in Free Play Mode on STAGE on Normal or higher difficulty", 
                    data={
                        "GENERAL": (self.generals, 1),
                        "STAGE": (self.stages_xl, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=10,
                ),
                GameObjectiveTemplate(
                    label="Play GENERAL in Free Play Mode on STAGE on Hard or higher difficulty", 
                    data={
                        "GENERAL": (self.generals, 1),
                        "STAGE": (self.stages_xl, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=10,
                ),
                GameObjectiveTemplate(
                    label="Play GENERAL in Free Play Mode on STAGE on XTreme or higher difficulty", 
                    data={
                        "GENERAL": (self.generals, 1),
                        "STAGE": (self.stages, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=10,
                ),
                GameObjectiveTemplate(
                    label="Play GENERAL in Free Play Mode on STAGE on XTreme or higher difficulty", 
                    data={
                        "GENERAL": (self.generals, 1),
                        "STAGE": (self.stages_xl, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=10,
                ),                
            ])

        if self.include_unique_items:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Obtain UNIQUE", 
                    data={
                        "UNIQUE": (self.uniques, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=10,
                ),
            ])

            if self.include_xtreme_legends:
                game_objective_templates.extend([
                    GameObjectiveTemplate(
                        label="Obtain UNIQUE", 
                        data={
                            "UNIQUE": (self.uniques_xl, 1),
                        },
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=10,
                    ),
                ])

        return game_objective_templates
            
    # Property checks
    @property
    def include_xtreme_legends(self) -> bool:
        return self.archipelago_options.dw3_include_xtreme_legends.value
    @property
    def include_unique_items(self) -> bool:
        return self.archipelago_options.dw3_include_unique_items.value

    # Data lists
    @staticmethod
    def generals() -> List[str]:
        return [
            "Zhao Yun", "Guan Yu", "Zhang Fei", "Zhuge Liang", "Liu Bei", "Ma Chao", "Huang Zhong", "Jiang Wei", "Wei Yan", "Pang Tong", "Xiahou Dun", "Dian Wei", "Xu Zhu", "Cao Cao", "Xiahou Yuan", "Zhang Liao", "Sima Yi", "Xu Huang", "Zhang He", "Zhen Ji", "Zhou Yu", "Lu Xun", "Taishi Ci", "Sun Shang Xiang", "Sun Jian", "Sun Quan", "Lu Meng", "Gan Ning", "Huang Gai", "Sun Ce", "Da Qiao", "Xiao Qiao", "Diao Chan", "Lu Bu", "Dong Zhuo", "Yuan Shao", "Zhang Jiao", "Meng Huo", "Zhu Rong", "Fu Xi", "Nu Wa"
        ]

    @staticmethod
    def generals_musuo() -> List[str]:
        return [
            "Zhao Yun", "Guan Yu", "Zhang Fei", "Zhuge Liang", "Liu Bei", "Ma Chao", "Huang Zhong", "Jiang Wei", "Wei Yan", "Pang Tong", "Xiahou Dun", "Dian Wei", "Xu Zhu", "Cao Cao", "Xiahou Yuan", "Zhang Liao", "Sima Yi", "Xu Huang", "Zhang He", "Zhen Ji", "Zhou Yu", "Lu Xun", "Taishi Ci", "Sun Shang Xiang", "Sun Jian", "Sun Quan", "Lu Meng", "Gan Ning", "Huang Gai", "Sun Ce", "Da Qiao", "Xiao Qiao"
        ]

    @staticmethod
    def generals_musuo_xl() -> List[str]:
        return [
            "Diao Chan", "Lu Bu", "Dong Zhuo", "Yuan Shao", "Zhang Jiao", "Meng Huo", "Zhu Rong"
        ]

    @staticmethod
    def stages() -> List[str]:
        return [
            "The Yellow Turban Rebellion (Han)", "The Yellow Turban Rebellion (Yellow Turbans)", "The Battle at Hu Lao Gate (Allied)", "The Battle at Hu Lao Gate (Dong Zhuo)", "Surprise Attack on Liu Biao", "The Batttle at Wan Castle(Cao Cao)", "The Battle at Wan Castle (Zhang Xiu)", "Assault on the Wu Territory (Sun Ce)", "Assault on the Wu Territory (Allied)", "The Battle at Guan Du (Cao Cao)", "The Battle at Guan Du (Yuan Shao)", "Guan Yu's Escape (Guan Yu)", "The Battle of Chang Ban (Liu Bei)", "The Battle of Chang Ban (Cao Cao)", "The Battle at Chi Bi (Allied)", "The Battle at Chi Bi (Cao Cao)", "Assault on Cheng Du", "The Battle at Tong Gate (Cao Cao)", "The Battle at Tong Gate (Allied)", "The Battle at He Fei (Wu)", "The Battle at He Fei (Wei)", "The Battle at Fan Castle (Allied)", "The Battle at Fan Castle (Shu)", "The Battle of Mt. Ding Jun (Shu)", "The Battle of Mt. Ding Jun (Wei)", "The Battle at Yi Ling (Wu)", "The Battle at Yi Ling (Shu)", "The Nanman Campaign (Wu)", "The Nanman Campaign (Nanman)", "The Battle of Jie Ting (Shu)", "The Battle of Jie Ting (Wei)", "The Battle at You Ting (Wu)", "The Battle at You Ting (Wei)", "The Siege of He DFei Castle (Wu)", "The Siege of He Fei Castle (Wei)", "The Battle at Wu Zhang Plains (Shu)", "The Battle at Wu Zhang Plains (Wei)", "The Mountain Bandit Campaign (Sun Quan)", "The Mountain Bandit Campaign (Bandits)", "Raid on the Rogue Fortress (Wu)", "Rait on the Rogue Fortress (Rogues)", "Pirate Attack on the High Seas (Sun Jian)", "Pirate Attack on the High Seas (Pirates)"
        ]

    @staticmethod
    def stages_xl() -> List[str]:
        return [
            "The Battle at Tong Gate (Dong Zhuo)", "The Battle at He Fei (Dong Zhuo)", "The Battle at Fan Castle (Yuan Shao)", "The Battle of Mt. Ding Jun (Dong Zhuo)", "The Battle at Yi Ling (Yellow Turbans)", "The Nanman Campaign (Shu)", "The Battle of Jie Ting (Yuan Shao)", "The Battle at You Ting (Nanman)", "The Siege of He Fei Castle (Dong Zhuo)", "The Battle at Wu Zhang Plains (Dong Zhuo)", "The Mountain Bandit Campaign (Yellow Turbans)", "Raid on the Rogue Fortress (Dong Zhuo)", "Wu Navy Skirmish (Nanman)", "Wu Navy Skirmish (Wu)"
        ]

    @staticmethod
    def uniques() -> List[str]:
        return [
            "Red Hare Saddle", "Hex Mark Saddle", "Imperial Saddle", "The Art of War", "Bodyguard Manual", "The Way of Musou", "Survival Guide", "Defender", "Fire Arrows", "Buckler", "Power Scroll", "Gold Harness"
        ]
    
    @staticmethod
    def uniques_xl() -> List[str]:
        return [
            "Divine Helmet", "Scroll of Accuracy", "Imperial Harness", "Seven Stars Blade", "Lightning Bow", "Seal of Darkness", "Beast Harness", "Marching Drum", "Divine Gauntlet", "Master's Cloak", "Legendary Scroll", "Musou Armor"
        ]



# Archipelago Options 
class Dw3IncludeXtremeLegends(DefaultOnToggle):
    """Include XTreme Legends Expansion"""
    display_name = "Include XTreme Legends Expansion"

class Dw3IncludeUniqueItems(DefaultOnToggle):
    """Include Getting Unique Items"""
    display_name = "Include Getting Unique Items"