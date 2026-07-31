from __future__ import annotations

import functools, random
from typing import List, Dict, Set

from dataclasses import dataclass

from Options import Toggle, Option, DefaultOnToggle, TextChoice, NamedRange

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms

@dataclass
class TwoPointHospitalArchipelagoOptions:
    # Modes
    tph_include_sandbox: TphIncludeSandbox

    # DLC
    tph_include_bigfoot: TphIncludeBigfoot
    tph_include_pebberley_island: TphIncludePebberleyIsland
    tph_include_close_encounters: TphIncludeCloseEncounters
    tph_include_off_the_grid: TphIncludeOffTheGrid
    tph_include_culture_shock: TphIncludeCultureShock
    tph_include_a_stitch_in_time: TphIncludeAStitchInTime
    tph_include_speedy_recovery: TphIncludeSpeedyRecovery

   
    
class TwoPointHospitalGame(Game):
    name = "Two Point Hospital"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.PS5,
        KeymastersKeepGamePlatforms.SW,
        KeymastersKeepGamePlatforms.XONE,
        KeymastersKeepGamePlatforms.XSX,
    ]

    is_adult_only_or_unrated = False

    options_cls = TwoPointHospitalArchipelagoOptions

    # Constraints
    def optional_game_constraint_templates(self) -> list[GameObjectiveTemplate]:
        tph_constraint_list: list[GameObjectiveTemplate]

        self.illness_list = self.sandbox_illness_settings()
        if self.include_bigfoot:
            self.illness_list.extend("Bigfoot")
        if self.include_a_stitch_in_time: 
            self.illness_list.extend("A Stitch in Time")
        if self.include_close_encounters: 
            self.illness_list.extend("Close Encounters")
        if self.include_culture_shock:
            self.illness_list.append("Culture Shock")
        if self.include_off_the_grid:
            self.illness_list.append("Off the Grid")
        if self.include_pebberley_island:
            self.illness_list.append("Pebberley Island")
        if self.include_speedy_recovery:
            self.illness_list.append("Speedy Recovery")



        tph_constraint_list = [
                GameObjectiveTemplate(    
                    label="Finish all objectives on one map",
                    data={}, 
                    weight=1
                ),
                GameObjectiveTemplate(    
                    label="Finish each objective on a different map",
                    data={}, 
                    weight=1
                ),
        ]

        if self.include_sandbox:
            tph_constraint_list.extend([
                GameObjectiveTemplate(    
                    label="Play in Custom Sandbox Mode with Desasters enabled",
                    data={}, 
                    weight=1
                ),
                GameObjectiveTemplate(
                    label="Play in Custom Sandbox Mode with Auto-Unlocks disabled",
                    data={},
                    weight=1
                ),
                GameObjectiveTemplate(    
                    label="Play in Custom Sandbox Mode with Epidemics enabled",
                    data={},
                    weight=1
                ),
                GameObjectiveTemplate(    
                    label="Play in Custom Sandbox Mode with VIP Visits enabled",
                    data={},
                    weight=1
                ),
                GameObjectiveTemplate(    
                    label="Play in Custom Sandbox Mode with VIP Visits disabled",
                    data={},
                    weight=1
                ),
                GameObjectiveTemplate(    
                    label="Play in Custom Sandbox Mode with Staff Requests enabled",
                    data={},
                    weight=1
                ),
                GameObjectiveTemplate(    
                    label="Play in Custom Sandbox Mode with Staff Requests disabled",
                    data={},
                    weight=1
                ),
                GameObjectiveTemplate(    
                    label="Play in Custom Sandbox Mode with starting cash of CASH $",
                    data={
                        "CASH": (self.starting_cash, 1)
                    },
                    weight=1
                ),
                GameObjectiveTemplate(    
                    label="Play in Custom Sandbox Mode with KUDOSH starting Kudosh",
                    data={
                        "KUDOSH": (self.starting_kudosh, 1)
                    },
                    weight=1
                ),
                GameObjectiveTemplate(    
                    label="Play in Custom Sandbox Mode with Income Multiplier INCOME",
                    data={
                        "INCOME": (self.income_multiplier_str, 1)
                    },
                    weight=1
                ),
                GameObjectiveTemplate(    
                    label="Play in Custom Sandbox Mode with TEMPERATURE Temperature setting",
                    data={
                        "TEMPERATURE": (self.temperatures, 1)
                    },
                    weight=1
                ),
                GameObjectiveTemplate(    
                    label="Play in Custom Sandbox Mode with CASH $, KUDOSH K, INCOME x Income, TEMPERATURE temperature, STAFF staff and ILLNESS illness setting",
                    data={
                        "TEMPERATURE": (self.temperatures, 1),
                        "INCOME": (self.income_multiplier_str, 1),
                        "KUDOSH": (self.starting_kudosh, 1),
                        "CASH": (self.starting_cash, 1),
                        "STAFF": (self.sandbox_staff_settings, 1),
                        "ILLNESS": (self.illness_list, 1)
                    },
                    weight=10
                ),
            ])        
        return tph_constraint_list

    
    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        game_objective_templates: List[GameObjectiveTemplate] = list()

        self.skill_list = self.skills_no_dlc()
        if self.include_speedy_recovery:
            self.skill_list.extend(self.skills_speedy_recovery())
        if self.include_a_stitch_in_time: 
            self.skill_list.extend(self.skills_a_stitch_in_time())        

        self.room_list = self.rooms_no_dlc()
        self.hospital_list = self.hospitals_no_dlc()
        if self.include_bigfoot:
            self.room_list.extend(self.rooms_bigfoot())
            self.hospital_list.extend(self.hospitals_bigfoot())
        if self.include_a_stitch_in_time: 
            self.room_list.extend(self.rooms_a_stitch_in_time())
            self.hospital_list.extend(self.hospitals_a_stitch_in_time())
        if self.include_speedy_recovery: 
            self.room_list.extend(self.rooms_speedy_recovery())
            self.hospital_list.extend(self.hospitals_speedy_recovery())
        if self.include_pebberley_island:
            self.room_list.extend(self.rooms_pebberley_island())
            self.hospital_list.extend(self.hospitals_pebberley_island())
        if self.include_off_the_grid: 
            self.room_list.extend(self.rooms_off_the_grid())
            self.hospital_list.extend(self.hospitals_off_the_grid())
        if self.include_culture_shock: 
            self.room_list.extend(self.rooms_culture_shock())
            self.hospital_list.extend(self.hospitals_culture_shock())
        if self.include_close_encounters: 
            self.room_list.extend(self.rooms_close_encounters())
            self.hospital_list.extend(self.hospitals_close_encounters())
        
        # Plan: 
        # Generic Objectives:
        #  - Training in specific skills (1-3)
        #  - Training in specific skills (4-5, Time Consuming)
        #  - Prestige Level of a specific room type (3-5) 
        #  - Have 750,000-1,000,000 $ (50k steps, Time Consuming)
        #  - Have 2,000,000-5,000,000 $ (100k steps, Time Consuming, Difficult)
        #  - Reach Hospital Level (1-30)
        # 
        # Sandbox Objectives:
        #  - Get Stars in a specific map with a specific goal setting (1-2 stars, sandbox custom goal option: Staff Development, Cure Patients, Cure & Expand, Moneymaker, Research & Training)
        #  - Get Stars in a specific map with a specific goal setting (3 stars, sandbox custom goal option, Time Consuming)
        #
        # 
        # KMK Room Challenges: 
        #  - Specific illness settings (Easy, Medium, Hard, Visible Symptoms Only, All From the Start, DLCs)
        #  - Specific Hiring Setting (Default, Medical Students, All Junior)
        #  - Disasters enabled
        #  - No Auto-unlocks
        #  - Epidemics enabled
        #  - VIP Visits enabled / disabled
        #  - Staff Requests enabled / disabled
        #  - starting cash (-20,000 - 10,000,000, 5k steps)
        #  - starting Kudosh (0 - 20,000, 100 steps)
        #  - Income Multiplier (0 - 2, 0.01 steps)
        #  - Temperature (Normal, Cold, Hot)


        # general goals
        game_objective_templates.extend([
            GameObjectiveTemplate(
                            label="Get Hospital Level LEVEL",
                            data={
                                "LEVEL": (self.hospital_level_low, 1),
                            },
                            is_time_consuming=False,
                            is_difficult=False,
                            weight=3,
                        ),
            GameObjectiveTemplate(
                            label="Get Hospital Level LEVEL on map MAP",
                            data={
                                "LEVEL": (self.hospital_level_low, 1),
                                "MAP": (self.hospital_list, 1),
                            },
                            is_time_consuming=False,
                            is_difficult=False,
                            weight=3,
                        ),
            GameObjectiveTemplate(
                            label="Get Hospital Level LEVEL",
                            data={
                                "LEVEL": (self.hospital_level_mid, 1),
                            },
                            is_time_consuming=True,
                            is_difficult=False,
                            weight=3,
                        ),
            GameObjectiveTemplate(
                            label="Get Hospital Level LEVEL on map MAP",
                            data={
                                "LEVEL": (self.hospital_level_mid, 1),
                                "MAP": (self.hospital_list, 1),
                            },
                            is_time_consuming=True,
                            is_difficult=False,
                            weight=3,
                        ),
            GameObjectiveTemplate(
                            label="Get Hospital Level LEVEL",
                            data={
                                "LEVEL": (self.hospital_level_high, 1),
                            },
                            is_time_consuming=True,
                            is_difficult=True,
                            weight=3,
                        ),
            GameObjectiveTemplate(
                            label="Get Hospital Level LEVEL on map MAP",
                            data={
                                "LEVEL": (self.hospital_level_high, 1),
                                "MAP": (self.hospital_list, 1),
                            },
                            is_time_consuming=True,
                            is_difficult=True,
                            weight=3,
                        ),

            GameObjectiveTemplate(
                label="Train a staff member to level LEVEL in SKILL",
                data={
                    "LEVEL": (self.skill_training_low, 1),
                    "SKILL": (self.skill_list, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Train a staff member to level LEVEL in SKILL",
                data={
                    "LEVEL": (self.skill_training_high, 1),
                    "SKILL": (self.skill_list, 1)
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Train a staff member in SKILL",
                data={
                    "SKILL": (self.skills_no_level, 1)
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Reach Prestige Level LEVEL with ROOM",
                data={
                    "LEVEL": (self.prestige_level, 1),
                    "ROOM": (self.room_list, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Clear an Epidemic",
                data={
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Have CASH $",
                data={
                    "CASH": (self.cash_low, 1)
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Have CASH $",
                data={
                    "CASH": (self.cash_high, 1)
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=3,
            ),
            ])

        # Sandbox Goals
        if self.include_sandbox:  
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Get STARS Stars in MAP with GOAL",
                    data={
                        "STARS": (self.stars_easy, 1),
                        "MAP": (self.hospital_list, 1),
                        "GOAL": (self.sandbox_goals, 1)
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Get 3 Stars in MAP with GOAL",
                    data={
                        "MAP": (self.hospital_list, 1),
                        "GOAL": (self.sandbox_goals, 1)
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
            ])

        return game_objective_templates
          
    # Property checks
    # tph_include_bigfoot: TphIncludeBigfoot
    # tph_include_pebberley_island: TphIncludePebberlyIsland
    # tph_include_close_encounters: TphIncludeCloseEncounters
    # tph_include_off_the_grid: TphIncludeOffTheGrid
    # tph_include_culture_shock: TphIncludeCultureShock
    # tph_include_a_stitch_in_time: TphIncludeAStitchInTime
    # tph_include_speedy_recovery: TphIncludeSpeedyRecovery
    @property
    def include_sandbox(self) -> bool:
        return self.archipelago_options.tph_include_sandbox.value
    @property
    def include_bigfoot(self) -> bool:
        return self.archipelago_options.tph_include_bigfoot.value            
    @property
    def include_pebberley_island(self) -> bool:
        return self.archipelago_options.tph_include_pebberley_island.value
    @property
    def include_close_encounters(self) -> bool:
        return self.archipelago_options.tph_include_close_encounters.value
    @property
    def include_off_the_grid(self) -> bool:
        return self.archipelago_options.tph_include_off_the_grid.value
    @property
    def include_culture_shock(self) -> bool:
        return self.archipelago_options.tph_include_culture_shock.value            
    @property
    def include_a_stitch_in_time(self) -> bool:
        return self.archipelago_options.tph_include_a_stitch_in_time.value
    @property
    def include_speedy_recovery(self) -> bool:
        return self.archipelago_options.tph_include_speedy_recovery.value

    # Ranges
    def skill_training_low(self) -> range:
        return range(1, 3, 1)        
    def skill_training_high(self) -> range:
        return range(4, 5, 1)
    def prestige_level(self) -> range:
        return range(3, 5, 1)        
    def cash_low(self) -> range:
        return range(750000, 1000000, 50000)    
    def cash_high(self) -> range:
        return range(2000000, 5000000, 100000)    
    def stars_easy(self) -> range:
        return range(1, 2, 1)
    # KMK Challenges
    def starting_cash(self) -> range:
        return range(-20000, 10000000, 5000)    
    def starting_kudosh(self) -> range:
        return range(0, 20000, 100) 
    def income_multiplier(self) -> range:
        return range(0, 200, 1) 
    def income_multiplier_str(self) -> str:
        return [str(float(x) / 100) for x in self.income_multiplier()]
    def hospital_level_low(self) -> range:
        return range(5, 10, 1)
    def hospital_level_mid(self) -> range:
        return range(11, 25, 1)
    def hospital_level_high(self) -> range:
        return range(26, 30, 1)
    
    
    # Data lists
    @staticmethod
    def skills_no_dlc() -> List[str]:
        return [
            "Diagnostics", "General Practice", "Maintenance", "Treatment", "Ward Management", "Marketing", "Mechanics", "Psychiatry", "Research", "Surgery", "", "Scientography", "Spy School", "Wizardry", "Robotics", "School of Thought", "Virtual Normality", "Private Tuition", "Research"
        ]    
    @staticmethod
    def skills_no_level() -> List[str]:
        return [
            "Genetics*", "Ghost Capture*", "Injection Administration*", "Pharmacy Management*", "Radiology*", "Bedside Manner*", "Emotional Intelligence*", "Motivation*", "Stamina Training*", "Training Masterclass*"
        ]    
    @staticmethod
    def skills_speedy_recovery() -> List[str]:
        return [
            "Driving", "Flying", "Vehicular Mechanics"
        ]            
    @staticmethod
    def skills_a_stitch_in_time() -> List[str]:
        return [
            "Yesterization"
        ]
    @staticmethod
    def hospitals_no_dlc() -> List[str]:
        return [
            "Hogsport", "Lower Bullocks", "Flottering", "Mitton University", "Tumble", "Flemington", "Melt Downs", "Smogley", "Duckworth-Upon-Bilge", "Grockle Bay", "Sweaty Palms", "Blighton", "Pelican Wharf", "Rotting Hill", "Croquembouche"
        ]
    @staticmethod
    def hospitals_bigfoot() -> List[str]:
        return [
            "Underlook Hotel", "Swelbard", "Roquefort Castle"
        ]        
    @staticmethod
    def hospitals_pebberley_island() -> List[str]:
        return [
            "Pebberley Reef", "Overgrowth", "Topless Mountain"
        ]
    @staticmethod
    def hospitals_close_encounters() -> List[str]:
        return [
            "Goldpan", "Camouflage Falls", "Chasm 24"
        ]    
    @staticmethod
    def hospitals_off_the_grid() -> List[str]:
        return [
            "Wanderoff", "Old Newpoint", "Windsock"
        ]    
    @staticmethod
    def hospitals_culture_shock() -> List[str]:
        return [
            "Plywood Studios", "Mudbury Festival", "Fitzpocket Academy"
        ]    
    @staticmethod
    def hospitals_a_stitch_in_time() -> List[str]:
        return [
            "Clockwise-Upon-Thyme", "Clockwise-Before-Thyme", "Clockwise-Above-Thyme"
        ]    
    @staticmethod
    def hospitals_speedy_recovery() -> List[str]:
        return [
            "Ailing", "Betts Shore", "Pointy Pass"
        ]    


    @staticmethod
    def temperatures() -> List[str]:
        return [
            "Normal", "Cold", "Hot"
        ]          
    @staticmethod
    def rooms_no_dlc() -> List[str]:
        return [
            "Cardiology", "DNA Lab", "Fluid Analysis", "General Diagnostics", "GP's Office", "M.E.G.A. Scan", "Psychiatry", "Ward", "X-Ray", "Chromatherapy", "Clown Clinic", "Cryptology", "De-Lux Clinic", "Fracture Ward", "Head Office", "Injection Room", "Pans Lab", "Pest Control", "Pharmacy", "Recurvery Room", "Resolution Lab", "Shock Clinic", "Surgery", "Café", "Marketing", "Reception", "Research", "Staff Room", "Toilets", "Training"
        ] 
    @staticmethod
    def rooms_bigfoot() -> List[str]:
        return [
            "Doghouse", "Urban Mythology", "Reanimation"
        ] 
    @staticmethod
    def rooms_pebberley_island() -> List[str]:
        return [
            "Indentification", "Escape Room", "Correcting Pool"
        ] 
    @staticmethod
    def rooms_close_encounters() -> List[str]:
        return [
            "Self-Assembly", "Toad Hall", "Personification"
        ] 
    @staticmethod
    def rooms_off_the_grid() -> List[str]:
        return [
            "Woordwork", "Herb Garden", "Farmacology", "Tech Support"
        ] 
    @staticmethod
    def rooms_culture_shock() -> List[str]:
        return [
            "Danger Zone", "Wash Pit", "War Room"
        ] 
    @staticmethod
    def rooms_a_stitch_in_time() -> List[str]:
        return [
            "Speed Dating"
        ] 
    @staticmethod
    def rooms_speedy_recovery() -> List[str]:
        return [
            "Cloud Computing", "Wax Works", "Powder Room"
        ] 
    @staticmethod
    def sandbox_goals() -> List[str]:
        return [
            "Staff Development", "Cure Patients", "Cure & Expand", "Moneymaker", "Research & Training"
        ]
    @staticmethod
    def sandbox_illness_settings() -> List[str]:
        return [
            "Easy", "Medium", "Hard", "Visible Symptoms Only", "All from the start"
        ]
    @staticmethod
    def sandbox_staff_settings() -> List[str]:
        return [
            "Default", "Medical Students", "All Junior"
        ]

    
#Archipelago Options 
class TphIncludeSandbox(DefaultOnToggle):
    """Include Sandbox Mode Goals"""
    display_name = "Include Sandbox Mode Goals"
class TphIncludeBigfoot(DefaultOnToggle):
    """Include Bigfoot DLC"""
    display_name = "Include Bigfoot DLC"
class TphIncludePebberleyIsland(DefaultOnToggle):
    """IncludePebberley Island DLC"""
    display_name = "IncludePebberley Island DLC"
class TphIncludeCloseEncounters(DefaultOnToggle):
    """Include Close Encounters DLC"""
    display_name = "Include Close Encounters DLC"
class TphIncludeOffTheGrid(DefaultOnToggle):
    """Include Off the Grid DLC"""
    display_name = "Include Off the Grid DLC"
class TphIncludeCultureShock(DefaultOnToggle):
    """Include Culture Shock DLC"""
    display_name = "Include Culture Shock Grid DLC"
class TphIncludeAStitchInTime(DefaultOnToggle):
    """Include A Stitch in Time DLC"""
    display_name = "Include A Stitch in Time DLC"
class TphIncludeSpeedyRecovery(DefaultOnToggle):
    """Include Speedy Recovery DLC"""
    display_name = "Include Speedy Recovery DLC"


