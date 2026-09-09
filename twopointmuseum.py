from __future__ import annotations

import functools, random
from typing import List, Dict, Set

from dataclasses import dataclass

from Options import Toggle, Option, DefaultOnToggle, TextChoice, NamedRange

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms

@dataclass
class TwoPointMuseumArchipelagoOptions:
    # Modes
    tpm_include_challenges: TpmIncludeChallenges
    tpm_challenge_sandbox: TpmChallengeSandbox

    # DLC
    tpm_include_explorer: TpmIncludeExplorer
    tpm_include_zooseum: TpmIncludeZooseum
    tpm_include_fantasy: TpmIncludeFantasy
    tpm_include_artyfacts: TpmIncludeArtyfacts

    #Digiverse
    tpm_include_digiverse: TpmIncludeDigiverse

    #Max Levels
    tpm_max_curator_level: TpmMaxCuratorLevel
    tpm_max_museum_level: TpmMaxMuseumLevel
    tpm_max_stars: TpmMaxStars


class TwoPointMuseumGame(Game):
    name = "Two Point Museum"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.PS5,
        KeymastersKeepGamePlatforms.SW,
        KeymastersKeepGamePlatforms.XONE,
        KeymastersKeepGamePlatforms.XSX,
    ]

    is_adult_only_or_unrated = False

    options_cls = TwoPointMuseumArchipelagoOptions

    # Constraints
    def optional_game_constraint_templates(self) -> list[GameObjectiveTemplate]:
        tpm_constraint_list: list[GameObjectiveTemplate]

        tpm_constraint_list = []

        tpm_constraint_list.extend([
            GameObjectiveTemplate(    
                label="Play in Sandbox Mode on Creative Difficulty",
                data={}, 
                weight=1
            ),
            GameObjectiveTemplate(
                label="Play in Sandbox Mode on Career Difficulty",
                data={},
                weight=1
            ),
            GameObjectiveTemplate(    
                label="Play in Sandbox Mode on Hardcore Difficulty",
                data={},
                weight=1
            ),
            GameObjectiveTemplate(    
                label="Custom Sandbox: GOAL, THIEVES, LOTS, CASH, KUDOSH, DONATIONS, SALARIES, MIN_GRANT, MAX_GRANT, CURATOR, UNLOCK_K, UNLOCK_ENLIGHTENMENT, UNLOCK_WORKSHOP, UNLOCK_POI, SURVEY_LEVEL",
                data={
                    "GOAL": (self.sandbox_goal, 1),
                    "THIEVES": (self.thief_threat, 1),
                    "LOTS": (self.lot_status, 1),
                    "CASH": (self.starting_cash, 1),
                    "KUDOSH": (self.starting_kudosh, 1),
                    "DONATIONS": (self.donation_multiplier, 1),
                    "SALARIES": (self.salary_multiplier, 1),
                    "MIN_GRANT": (self.minimum_monthly_grant, 1),
                    "MAX_GRANT": (self.maximum_monthly_grant, 1),
                    "CURATOR": (self.disable_curator_objectives, 1),
                    "UNLOCK_K": (self.unlock_kudosh_items, 1),
                    "UNLOCK_ENLIGHTENMENT": (self.unlock_enlightenment_items, 1),
                    "UNLOCK_WORKSHOP": (self.unlock_workshop_contraptions, 1),
                    "UNLOCK_POI": (self.unlock_all_pois, 1),
                    "SURVEY_LEVEL": (self.start_max_survey_level, 1),
                },
                weight=1
            ),
        ])        
        return tpm_constraint_list

    
    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        game_objective_templates: List[GameObjectiveTemplate] = list()

        self.skill_list = self.skills_no_dlc()
        if self.include_digiverse:
            self.skill_list.extend(self.skills_digiverse())
        if self.include_zooseum: 
            self.skill_list.extend(self.skills_zooseum())
        if self.include_fantasy: 
            self.skill_list.extend(self.skills_fantasy())
        if self.include_artyfacts: 
            self.skill_list.extend(self.skills_artyfacts())

        self.challenge_list = self.museums_popup()
        if self.include_explorer:
            self.challenge_list.extend(["Plywood Island"])

        self.museum_list = self.museums_no_dlc()
        if self.challenge_sandbox:
            self.museum_list.extend(self.museums_popup())
        if self.include_explorer and self.challenge_sandbox:
            self.museum_list.extend(["Plywood Island"])
        if self.include_zooseum:
            self.museum_list.extend(["Silverbottom Park"])
        if self.include_artyfacts:
            self.museum_list.extend(["Undee Docks"])


        self.expedition_list = self.expeditions_no_dlc()
        if self.include_fantasy:
            self.expedition_list.extend(self.expeditions_fantasy())
        if self.include_zooseum:
            self.expedition_list.extend(self.expeditions_zooseum())
        if self.include_artyfacts:
            self.expedition_list.extend(self.expeditions_artyfacts())
        if self.include_digiverse:
            self.expedition_list.extend(self.expeditions_digiverse())

        # general goals
        game_objective_templates.extend([
            GameObjectiveTemplate(
                label="Train a staff member to level LEVEL in SKILL",
                data={
                    "LEVEL": (self.skill_training, 1),
                    "SKILL": (self.skill_list, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Reach Museum Level LEVEL",
                data={
                    "LEVEL": (self.museum_level, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Reach Museum Level LEVEL on MUSEUM",
                data={
                    "LEVEL": (self.museum_level, 1),
                    "MUSEUM": (self.museum_list, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Reach Curator Level LEVEL",
                data={
                    "LEVEL": (self.curator_level, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
        ])

        # Sandbox Goals
        game_objective_templates.extend([
            GameObjectiveTemplate(
                label="Get STARS Stars in MAP",
                data={
                    "STARS": (self.museum_stars, 1),
                    "MAP": (self.museum_list, 1),
                },
                is_time_consuming=True,
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

        # POI Goals
        game_objective_templates.extend([
            GameObjectiveTemplate(
                label="Unlock POI Points of Interest on MAP",
                data={
                    "POI": (self.number_points_of_interest, 1),
                    "MAP": (self.expedition_list, 1)
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=3,
            )
        ])

        # Special DLC Goals
        if self.include_fantasy:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Defeat the Dragon King in Scorched Earth",
                    data={},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=3,
                )
            ])

        if self.include_digiverse:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Clear all Points of Interest in DIGIVERSE",
                    data={
                        "DIGIVERSE": (self.digiverse_list, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=3,
                )
            ])

        return game_objective_templates
            
    # Property checks
    @property
    def include_digiverse(self) -> bool:
        return self.archipelago_options.tpm_include_digiverse.value
    @property
    def include_zooseum(self) -> bool:
        return self.archipelago_options.tpm_include_zooseum.value    
    @property
    def include_fantasy(self) -> bool:
        return self.archipelago_options.tpm_include_fantasy.value            
    @property
    def include_artyfacts(self) -> bool:
        return self.archipelago_options.tpm_include_fantasy.value
    @property
    def include_explorer(self) -> bool:
        return self.archipelago_options.tpm_include_explorer.value
    @property
    def include_challenges(self) -> bool:
        return self.archipelago_options.tpm_include_challenges.value
    @property
    def challenge_sandbox(self) -> bool:
        return self.archipelago_options.tpm_challenge_sandbox.value
    @property
    def max_curator_level(self) -> int:
        return self.archipelago_options.tpm_max_curator_level.value
    @property
    def max_museum_level(self) -> int:
        return self.archipelago_options.tpm_max_museum_level.value
    @property
    def max_stars(self) -> int:
        return self.archipelago_options.tpm_max_stars.value
    
       
    # Ranges
    def sandbox_goal(self) -> List[str]:
        return ["Total Buzz", "Traditional"]    
    def thief_threat(self) -> List[str]:
        return ["None", "Low", "Medium", "High"]
    def lot_status(self) -> List[str]:
        return ["Locked", "Unlocked"]
    def starting_cash(self) -> range:
        return range(0, 100000, 10000)   
    def starting_kudosh(self) -> range:
        return range(0, 500, 50) 
    def donation_multiplier(self) -> range:
        return range(0, 200, 2) 
    def salary_multiplier(self) -> range:
        return range(0, 200, 2)
    def minimum_monthly_grant(self) -> range:
        return range(0, 10000, 1000)
    def maximum_monthly_grant(self) -> range:
        return range(0, 10000, 1000)
    def skill_training(self) -> range:
        return range(1, 3, 1)
    def curator_level(self) -> range:
        return range(1, self.max_curator_level, 1)
    def museum_level(self) -> range:
        return range(5, self.max_museum_level, 1)
    def museum_stars(self) -> range:
        return range(1, self.max_stars, 1)
    def number_points_of_interest(self) -> range:
        return range(1, 16, 1)
    


    
    # Data lists
    @staticmethod    
    def disable_curator_objectives() -> List[str]:
        return ["Enabled", "Disabled"]
    @staticmethod
    def unlock_kudosh_items() -> List[str]:
        return ["Locked", "Unlocked"]
    @staticmethod
    def unlock_enlightenment_items() -> List[str]:
        return ["Locked", "Unlocked"]
    @staticmethod
    def unlock_workshop_contraptions() -> List[str]:
        return ["Locked", "Unlocked"]
    @staticmethod
    def unlock_all_pois() -> List[str]:
        return ["Locked", "Unlocked"]
    @staticmethod
    def start_max_survey_level() -> range:
        return ["Normal", "Maximum"]
    @staticmethod
    def skills_no_dlc() -> List[str]:
        return [
            "Aerodynamics", "Happy Thoughts", "Pilot Wings", "Analysis", "Fish Whispering", "Rapid Restauration", "Spirit Whispering", "Survey Skills", "Survival Skills", "Tour Guidelines", "Accomplished Admission", "Customer Service", "Marketing", "Fire-Resistance", "Ghost Capture", "Mechanics", "Workshop", "Camera Room", "Strolling Surveillance"
        ]    
    @staticmethod
    def skills_digiverse() -> List[str]:
        return [
            "Cult of the Museum", "Button Master"
        ]            
    @staticmethod
    def skills_artyfacts() -> List[str]:
        return [
            "2D Art", "3D Art", "Emotional Intelligence", "Modelling"
        ]
    @staticmethod
    def skills_zooseum() -> List[str]:
        return [
            "Animal Analysis", "Macro Zoology", "Micro-Zoology"
        ] 
         
    @staticmethod
    def skills_fantasy() -> List[str]:
        return [
            "Potion Master"
        ]     
    
    @staticmethod
    def museums_no_dlc() -> List[str]:
        return [
            "Memento Mile", "Passwater Cove", "Wailon Lodge", "Bungle Wastelands", "Pebberley Heights", "Pointy Mountains"
        ]
    @staticmethod
    def museums_popup() -> List[str]:
        return [
            "County Archives", "Remote Rock", "Elementary Shoal"
        ]            
    @staticmethod
    def challenge_medals() -> List[str]:
        return [
            "Bronze", "Silver", "Gold"
        ]

    @staticmethod
    def expeditions_no_dlc() -> List[str]:
        return [
            "Bone Belt", "Two Point Sea", "Netherworld", "Bungle Burrows", "Known Universe"
        ]
    @staticmethod
    def expeditions_digiverse() -> List[str]:
        return [
            "Digiverse"
        ]
    @staticmethod
    def expeditions_zooseum() -> List[str]:
        return [
            "Farflung Isles"
        ]
    @staticmethod
    def expeditions_fantasy() -> List[str]:
        return [
            "Scorched Earth"
        ]
    @staticmethod
    def expeditions_artyfacts() -> List[str]:
        return [
            "Zara's Sketchbook"
        ]
    @staticmethod
    def digiverse_list() -> List[str]:
        return [
            "Meat Wizard", "Dredge", "Vampire Survivors", "Revenge of the savage Planet", "Angry Birds", "Dave The Diver", "Cult of the Lamb"
        ]


# Archipelago Options 
class TpmIncludeChallenges(DefaultOnToggle):
    """Include Challenge Mode Goals"""
    display_name = "Include Challenge Mode Goals"
class TpmChallengeSandbox(DefaultOnToggle):
    """Include the Pop-Up Museums for Star Goals in Sandbox Mode"""
    display_name = "Include Challenges in Sandbox"
class TpmIncludeExplorer(DefaultOnToggle):
    """Include Explorer Add On Content"""
    display_name = "Include Explorer Add On Content"
class TpmIncludeZooseum(DefaultOnToggle):
    """Include Farflung Isles, Silverbottom Park, Zooology Exhibits and Skills."""
    display_name = "Include Zooseum Content"
class TpmIncludeFantasy(DefaultOnToggle):
    """Include Fantasy Experts, Scorched Earth and Exhibits"""
    display_name = "Include Fantasy Finds Content"
class TpmIncludeArtyfacts(DefaultOnToggle):
    """Include Artyfacts Exhibits and Skills"""
    display_name = "Include Artyfacts Content"
class TpmIncludeDigiverse(DefaultOnToggle):
    """Include Digiverse Exhibits and Skills"""
    display_name = "Include Digiverse Content"    

class TpmMaxCuratorLevel(NamedRange):
    """
    Highest Curator Level for Objectives 
    """
    display_name = "Highest Curator Level"
    default = 15
    range_start = 1
    range_end = 50
class TpmMaxMuseumLevel(NamedRange):
    """
    Highest Museum Level for Objectives 
    """
    display_name = "Highest Museum Level"
    default = 50
    range_start = 10
    range_end = 100
class TpmMaxStars(NamedRange):
    """
    Highest Stars for Objectives 
    """
    display_name = "Highest Stars"
    default = 5
    range_start = 1
    range_end = 50


