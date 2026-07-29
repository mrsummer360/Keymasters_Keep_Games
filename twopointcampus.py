from __future__ import annotations

import functools, random
from typing import List, Dict, Set

from dataclasses import dataclass

from Options import Toggle, Option, DefaultOnToggle, TextChoice, NamedRange

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms

@dataclass
class TwoPointCampusArchipelagoOptions:
    # Modes
    tpc_include_sandbox: TpcIncludeSandbox
    tpc_include_challenges: TpcIncludeChallenges

    # DLC
    tpc_include_space_academy: TpcIncludeSpaceAcademy
    tpc_include_school_spirits: TpcIncludeSchoolSpirits
    tpc_include_medical_school: TpcIncludeMedicalSchool
   
    
class TwoPointCampusGame(Game):
    name = "Two Point Campus"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.PS5,
        KeymastersKeepGamePlatforms.SW,
        KeymastersKeepGamePlatforms.XONE,
        KeymastersKeepGamePlatforms.XSX,
    ]

    is_adult_only_or_unrated = False

    options_cls = TwoPointCampusArchipelagoOptions

    # Constraints
    def optional_game_constraint_templates(self) -> list[GameObjectiveTemplate]:
        tpc_constraint_list: list[GameObjectiveTemplate]

        tpc_constraint_list = []

        if self.include_sandbox:
            tpc_constraint_list.extend([
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
                    label="Play in Custom Sandbox Mode with Invaders enabled",
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
                    label="Play in Custom Sandbox Mode with Monthly Allowance ALLOWANCE",
                    data={
                        "ALLOWANCE": (self.monthly_allowance, 1)
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
                    label="Play in Custom Sandbox Mode and start with COURSEPOINTS Course Points",
                    data={
                        "COURSEPOINTS": (self.course_points, 1)
                    },
                    weight=1
                ),
                GameObjectiveTemplate(    
                    label="Play in Custom Sandbox Mode with CASH $, KUDOSH K, INCOME x Income, Monthly ALLOWANCE, TEMPERATURE temperature and COURSEPOINTS starting CP",
                    data={
                        "TEMPERATURE": (self.temperatures, 1),
                        "ALLOWANCE": (self.monthly_allowance, 1),
                        "INCOME": (self.income_multiplier_str, 1),
                        "KUDOSH": (self.starting_kudosh, 1),
                        "CASH": (self.starting_cash, 1),
                        "COURSEPOINTS": (self.course_points, 1)
                    },
                    weight=10
                ),
            ])        
        return tpc_constraint_list

    
    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        game_objective_templates: List[GameObjectiveTemplate] = list()

        self.skill_list = self.skills_no_dlc()
        if self.include_space_academy:
            self.skill_list.extend(self.skills_space_academy())
        if self.include_school_spirits: 
            self.skill_list.extend(self.skills_school_spirits())
        if self.include_medical_school: 
            self.skill_list.extend(self.skills_medical_school())
        if self.include_school_spirits or self.include_medical_school:
            self.skill_list.append("Ghost Capture")
        

        self.room_list = self.rooms_no_dlc()
        if self.include_space_academy:
            self.room_list.extend(self.rooms_space_academy())
        if self.include_school_spirits: 
            self.room_list.extend(self.rooms_school_spirits())
        if self.include_medical_school: 
            self.room_list.extend(self.rooms_medical_school())


        
        self.course_list = self.courses_no_dlc()
        if self.include_space_academy:
            self.course_list.extend(self.courses_space_academy())
        if self.include_school_spirits: 
            self.course_list.extend(self.courses_school_spirits())
        if self.include_medical_school: 
            self.course_list.extend(self.courses_medical_school())
        

        self.campus_list = self.campuses_no_dlc()
        if self.include_space_academy:
            self.campus_list.extend(self.campuses_space_academy())
        if self.include_school_spirits: 
            self.campus_list.extend(["Lifeless Estate"])
        if self.include_medical_school: 
            self.campus_list.extend(self.campuses_medical_school())

        self.competition_list = self.competitions_no_dlc()
        if self.include_space_academy:
            self.competition_list.extend(["Space Battle"])

        self.challenge_list = self.challenges_no_dlc()
        if self.include_school_spirits:
            self.challenge_list.extend(["Gradeyard Shift"])
        
        # Plan: 
        # Generic Objectives:
        #  - Training in specific skills (excluding DLC, 3-5)
        #  - Training in specific skills (one per DLC, 3-5)
        #  - Training in specific skills (excluding DLC, 6-10, Time Consuming)
        #  - Training in specific skills (one per DLC, 6-10, Time Consuming)
        #  - Prestige Level of a specific room type (excluding DLC, 5-11) 
        #  - Prestige Level of a specific room type (one per DLC, 5-11)
        #  - Reach Campus Level (5-15)
        #  - Reach Campus Level (16-84, Time Consuming)
        #  - Reach Campus Level (85-100, Time Consuming, Difficult)
        #  - Reach Campus Level on Map (Excluding DLC, 5-15)
        #  - Reach Campus Level on Map (One per DLC, 5-15)
        #  - Reach Campus Level on Map (Excluding DLC, 16-84, Time Consuming)
        #  - Reach Campus Level on Map (One per DLC, 16-84, Time Consuming)
        #  - Reach Campus Level on Map (Excluding DLC, 85-100, Time Consuming, Difficult)
        #  - Reach Campus Level on Map (One per DLC, 85-100, Time Consuming, Difficult)
        #  - Win specific competition (excluding DLC)
        #  - Win a Space Battle (Space Academy DLC)
        #  - Catch all intruders during an invasion
        #  - Level up a specific course (excluding DLC, 3-5)
        #  - Level up a specific course (one per DLC, 3-5)
        #  - Level up a specific course (excluding DLC, 6-10, Time Consuming)
        #  - Level up a specific course (one per DLC, 6-10, Time Consuming)
        #  - Have 750,000-1,000,000 $ (50k steps, Time Consuming)
        #  - Have 2,000,000-5,000,000 $ (100k steps, Time Consuming, Difficult)
        # 
        # Sandbox Objectives:
        #  - Get Stars in a specific map with a specific goal setting (excluding DLC, 1-2 stars, sandbox custom goal option)
        #  - Get Stars in a specific map with a specific goal setting (one per DLC, 1-2 stars, sandbox custom goal option)
        #  - Get Stars in a specific map with a specific goal setting (excluding DLC, 3 stars, sandbox custom goal option, Time Consuming)
        #  - Get Stars in a specific map with a specific goal setting (one per DLC, 3 stars, sandbox custom goal option, Time Consuming)
        #
        # Challenge Objectives:
        #  - Get Medal in a specific challenge (excluding DLC, Bronze or Silver Medal)
        #  - Get Medal in Gradeyard Shift (Bronze or Silver Medal)
        #  - Get Gold Medal in a specific challenge (excluding DLC, Gold Medal, Difficult)
        #  - Get Gold Medal in a Gradeyard Shift (Gold Medal, Difficult)
        # 
        # KMK Room Challenges: 
        #  - Disasters enabled
        #  - No Auto-unlocks
        #  - Invaders enabled
        #  - VIP Visits enabled / disabled
        #  - Staff Requests enabled / disabled
        #  - starting cash (0-2,000,000, 10k steps)
        #  - starting Kudosh (0-15,000, 100 steps)
        #  - Income Multiplier (0-5, 0.1 steps)
        #  - Monthly Allowance (0-100,000, 1k steps)
        #  - Temperature (Normal, Cold, Hot)
        #  - Course Points (10-500, 10 step)


        # general goals
        game_objective_templates.extend([
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
                label="Reach Campus Level LEVEL",
                data={
                    "LEVEL": (self.campus_level_low, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Reach Campus Level LEVEL",
                data={
                    "LEVEL": (self.campus_level_mid, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Reach Campus Level LEVEL",
                data={
                    "LEVEL": (self.campus_level_high, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Reach Campus Level LEVEL on CAMPUS",
                data={
                    "LEVEL": (self.campus_level_low, 1),
                    "CAMPUS": (self.campus_list, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Reach Campus Level LEVEL on CAMPUS",
                data={
                    "LEVEL": (self.campus_level_mid, 1),
                    "CAMPUS": (self.campus_list, 1)
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Reach Campus Level LEVEL on CAMPUS",
                data={
                    "LEVEL": (self.campus_level_high, 1),
                    "CAMPUS": (self.campus_list, 1)
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Win a COMPETITION",
                data={
                    "COMPETITION": (self.competition_list, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Catch all intruders during an invasion",
                data={
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Level up COURSE to LEVEL",
                data={
                    "LEVEL": (self.course_level_low, 1),
                    "COURSE": (self.course_list, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Level up COURSE to LEVEL",
                data={
                    "LEVEL": (self.course_level_high, 1),
                    "COURSE": (self.course_list, 1)
                },
                is_time_consuming=True,
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
                        "MAP": (self.campus_list, 1),
                        "GOAL": (self.sandbox_goals, 1)
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Get 3 Stars in MAP with GOAL",
                    data={
                        "MAP": (self.campus_list, 1),
                        "GOAL": (self.sandbox_goals, 1)
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
            ])

        # Challenge Goals
        if self.include_challenges:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Get MEDAL in CHALLENGE",
                    data={
                        "MEDAL": (self.challenge_medals, 1),
                        "CHALLENGE": (self.challenge_list, 1)
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                )
            ])

        return game_objective_templates
            
    # Property checks
    @property
    def include_sandbox(self) -> bool:
        return self.archipelago_options.tpc_include_sandbox.value
    @property
    def include_challenges(self) -> bool:
        return self.archipelago_options.tpc_include_challenges.value    
    @property
    def include_space_academy(self) -> bool:
        return self.archipelago_options.tpc_include_space_academy.value            
    @property
    def include_school_spirits(self) -> bool:
        return self.archipelago_options.tpc_include_school_spirits.value
    @property
    def include_medical_school(self) -> bool:
        return self.archipelago_options.tpc_include_medical_school.value
       
    # Ranges
    def skill_training_low(self) -> range:
        return range(3, 5, 1)        
    def skill_training_high(self) -> range:
        return range(6, 10, 1)
    def prestige_level(self) -> range:
        return range(5, 11, 1)        
    def campus_level_low(self) -> range:
        return range(5, 15, 1)
    def campus_level_mid(self) -> range:
        return range(16, 84, 1)        
    def campus_level_high(self) -> range:
        return range(85, 100, 1)
    def course_level_low(self) -> range:
        return range(3, 5, 1)  
    def course_level_high(self) -> range:
        return range(6, 10, 1)
    def cash_low(self) -> range:
        return range(750000, 1000000, 50000)    
    def cash_high(self) -> range:
        return range(2000000, 5000000, 100000)    
    def stars_easy(self) -> range:
        return range(1, 2, 1)
    # KMK Challenges
    def starting_cash(self) -> range:
        return range(0, 2000000, 10000)    
    def starting_kudosh(self) -> range:
        return range(0, 15000, 100) 
    def income_multiplier(self) -> range:
        return range(0, 50, 1) 
    def monthly_allowance(self) -> range:
        return range(0, 100000, 1000)
    def course_points(self) -> range:
        return range(10, 500, 10) 

    def income_multiplier_str(self) -> str:
        return [str(float(x) / 10) for x in self.income_multiplier()]
    
    # Data lists
    @staticmethod
    def skills_no_dlc() -> List[str]:
        return [
            "Academic Exercise", "Archeology", "Countercultural Studies", "Dark Art", "Funny Business", "Gastronomy", "General Knowledge", "Internet History", "Knight School", "Money Wangling", "Musicality", "Scientography", "Spy School", "Wizardry", "Robotics", "School of Thought", "Virtual Normality", "Private Tuition", "Research", "First Aid", "Library Management", "Marketing", "Pastoral Care", "Maintentance", "Mechanics", "Security", "Aerodynamics", "Comic Timing", "Happy Thoughts", "Inspirational Speaking"
        ]    
    @staticmethod
    def skills_space_academy() -> List[str]:
        return [
            "Astrology", "Cheese-Moongery", "Cosmic Expansion", "Humanities", "Space Academy", "Space-Knight School", "Space Mining"
        ]            
    @staticmethod
    def skills_school_spirits() -> List[str]:
        return [
            "Paranormal Detection", "School Spirits"
        ]
    @staticmethod
    def skills_medical_school() -> List[str]:
        return [
            "Medical School", "Nursing", "Fire Resistance"
        ]       
    @staticmethod
    def campuses_no_dlc() -> List[str]:
        return [
            "Two Point University", "Mitton University", "Urban Bungle", "Blundergrad", "Freshleigh Meadows", "Breaking Point", "Piazza Lanatra", "Fluffborough", "Freshleigh Meadows", "Noblestead", "Pebberley Ruins", "Spiffinmoore", "Upper Etching"
        ]
    @staticmethod
    def campuses_space_academy() -> List[str]:
        return [
            "Cape Shrapnull", "Cheesy Heap: Delta-Rye", "Universe City"
        ]        
    @staticmethod
    def campuses_medical_school() -> List[str]:
        return [
            "Pointy Peak", "Molten Rock", "Lake Tumble"
        ]
    @staticmethod
    def competitions_no_dlc() -> List[str]:
        return [
            "Campus Cook-Off", "County Cook-Off", "Celebrity Cook-Off", "Jousting Tournament", "The Grand Joust", "Cheeseball: Smogley Salamanders", "Cheeseball: Hogsport Porthogs", "Cheeseball: Bungle Technicals", "Cheeseball: Flemington Flobtrotters", "Cheeseball: Jumbo Mega Team", "Talent Show"
        ]    
    @staticmethod
    def temperatures() -> List[str]:
        return [
            "Normal", "Cold", "Hot"
        ]          
    @staticmethod
    def challenges_no_dlc() -> List[str]:
        return [
            "The Siege of Noblestead", "Pumpkin High", "Two Point Krampus", "The L-Bomb", "Egg & Silver-Spoon Race", "Summer School", "Destitute Institute", "Pebberly Puzzler"
        ] 
    @staticmethod
    def rooms_no_dlc() -> List[str]:
        return [
            "Battle Ground", "Cheeseball Field", "Dig Site", "Jousting Field", "Lecture Theatre", "Library", "Computer Lab", "Dig Site", "Gadget Lab", "Gym", "Panic Room", "Potions Room"
        ] 
    @staticmethod
    def rooms_space_academy() -> List[str]:
        return [
            "Rocket Lab", "Anti-Gravity Chamber", "Battle Space", "Command Room", "Creamatorium", "Living Room", "Recording Studio", "Robo Construction", "Robo Design", "Savoury Kitchen", "Science Lab", "Spells Room", "Sweet Kitchen", "VR Lab", "Bathroom", "Dormitory", "Shower Room", "Student Lounge", "Cafeteria", "Marketing Office", "Medical Office", "Pastoral Support", "Private Tuition Room", "Research Lab", "Staff Room", "Student Union", "Training Room"
        ] 
    @staticmethod
    def rooms_medical_school() -> List[str]:
        return [
            "Head Clinic", "Injection Room", "Psychiatry", "Rocket Lab", "Surgery", "Thumping Therapy", "Ward"
        ] 
    @staticmethod
    def rooms_school_spirits() -> List[str]:
        return [
            "Detection Office", "Ghost Storage"
        ] 
    @staticmethod
    def courses_no_dlc() -> List[str]:
        return [
            "Academic Exercise", "Archeology", "Countercultural Studies", "Dark Arts", "Funny Business", "Gastronomy", "General Knowledge", "Internet History", "Knight School", "Money Wangling", "Musicality", "Robotics", "School of Thought", "Scientography", "Spy School", "Virtual Normality", "Wizardry"
        ]
    @staticmethod
    def courses_space_academy() -> List[str]:
        return [
            "Astrology", "Cheese-Moongery", "Cosmic Expansion", "Humanities", "Space Academy", "Space-Knight School"
        ]
    @staticmethod
    def courses_medical_school() -> List[str]:
        return [
            "Medical School", "Nursing"
        ]
    @staticmethod
    def courses_school_spirits() -> List[str]:
        return [
            "Paranormal Detection", "School Spirits"
        ]
    @staticmethod
    def sandbox_goals() -> List[str]:
        return [
            "Variety", "Academic", "Financial", "Social", "Staff"
        ]
    @staticmethod
    def challenge_medals() -> List[str]:
        return [
            "Bronze", "Silver"
        ]

#Archipelago Options 
class TpcIncludeSandbox(DefaultOnToggle):
    """Include Sandbox Mode Goals"""
    display_name = "Include Sandbox Mode Goals"
class TpcIncludeChallenges(DefaultOnToggle):
    """Include Challenge Mode Goals"""
    display_name = "Include Challenge Mode Goals"
class TpcIncludeSpaceAcademy(DefaultOnToggle):
    """Include Campuses, Skills and Competitions from the Space Academy DLC"""
    display_name = "Include Space Academy Content"
class TpcIncludeSchoolSpirits(DefaultOnToggle):
    """Include Lifeless Estate, Gradeyard Shift and Skills from School Spirits DLC"""
    display_name = "Include School Spirits Content"
class TpcIncludeMedicalSchool(DefaultOnToggle):
    """Include Campuses and Skills from Medical School DLC"""
    display_name = "Include Medical School Content"


