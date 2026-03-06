from __future__ import annotations

import functools, random
from typing import List, Dict, Set

from dataclasses import dataclass

from Options import Toggle, Option, DefaultOnToggle, TextChoice, NamedRange

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms

@dataclass
class NoMansSkyArchipelagoOptions:
    # Include Categories
    nms_include_scanning: NmsIncludeScanning
    nms_include_elements: NmsIncludeElements
    nms_include_languages: NmsIncludeLanguages
    nms_include_animals: NmsIncludeAnimals
    nms_include_freighters: NmsIncludeFreighters
    nms_include_upgrades: NmsIncludeUpgrades
    nms_include_exploration: NmsIncludeExploration
    nms_include_vehicle: NmsIncludeVehicle
    nms_include_base: NmsIncludeBase
    nms_include_junk: NmsIncludeJunk
    nms_include_landmarks: NmsIncludeLandmarks
    nms_include_combat: NmsIncludeCombat
    nms_include_artifacts: NmsIncludeArtifacts
    nms_include_harvesting: NmsIncludeHarvesting
    nms_include_special: NmsIncludeSpecial
    nms_include_missions: NmsIncludeMissions
    nms_include_quests: NmsIncludeQuests
    nms_include_galaxy_center: NmsIncludeCenter
    nms_include_fishing: NmsIncludeFishing
    nms_include_cooking: NmsIncludeCooking
    nms_include_settlement: NmsIncludeSettlements
    nms_include_corvette: NmsIncludeCorvette
    nms_include_crafting: NmsIncludeCrafting
    
    #advanced toggles
    nms_generate_portal_sequence: NmsGeneratePortalSequence
    
    # numeric limits
    nms_min_element_num: NmsMinElementNum
    nms_max_element_num: NmsMaxElementNum
    nms_min_scan_num: NmsMinScanNum
    nms_max_scan_num: NmsMaxScanNum
    nms_min_words_num: NmsMinWordsNum
    nms_max_words_num: NmsMaxWordsNum
    nms_min_inventory_upgrade_num: NmsMinInventoryUpgradeNum
    nms_max_inventory_upgrade_num: NmsMaxInventoryUpgradeNum
    nms_min_blueprint_num: NmsMinBlueprintNum
    nms_max_blueprint_num: NmsMaxBlueprintNum
    nms_min_taming_num: NmsMinTamingNum
    nms_max_taming_num: NmsMaxTamingNum
    nms_min_combat_kills_num: NmsMinCombatKillsNum
    nms_max_combat_kills_num: NmsMaxCombatKillsNum
    nms_min_recruit_num: NmsMinRecruitNum
    nms_max_recruit_num: NmsMaxRecruitNum
    nms_min_exploration_num: NmsMinExplorationNum
    nms_max_exploration_num: NmsMaxExplorationNum
    nms_min_build_num: NmsMinBuildNum
    nms_max_build_num: NmsMaxBuildNum
    nms_min_artifact_num: NmsMinArtifactNum
    nms_max_artifact_num: NmsMaxArtifactNum
    nms_min_harvesting_num: NmsMinHarvestingNum
    nms_max_harvesting_num: NmsMaxHarvestingNum
    nms_min_special_num: NmsMinSpecialNum
    nms_max_special_num: NmsMaxSpecialNum
    nms_min_missions_num: NmsMinMissionsNum
    nms_max_missions_num: NmsMaxMissionsNum
    nms_min_fishing_num: NmsMinFishingNum
    nms_max_fishing_num: NmsMaxFishingNum
    
    
class NoMansSkyGame(Game):
    name = "No Man's Sky"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.PS5,
        KeymastersKeepGamePlatforms.SW,
        KeymastersKeepGamePlatforms.XONE,
        KeymastersKeepGamePlatforms.XSX,
        KeymastersKeepGamePlatforms.VR,
        KeymastersKeepGamePlatforms.SW2,
    ]

    is_adult_only_or_unrated = False

    options_cls = NoMansSkyArchipelagoOptions
    
    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        game_objective_templates: List[GameObjectiveTemplate] = list()
        
        # scanning templates
        if self.include_scanning:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Scan QUANTITY SCANTYPE",
                    data={
                        "QUANTITY": (self.scan_quantities, 1),
                        "SCANTYPE": (self.scan_types, 1)
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Visit QUANTITY Planets and scan at least one SCANTYPE there",
                    data={
                        "QUANTITY": (self.scan_quantities, 1),
                        "SCANTYPE": (self.scan_types, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Scan all Wildlife on QUANTITY Planets",
                    data={
                        "QUANTITY": (self.scan_quantities, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=2,
                ),                
            ])
        
        
        # element templates
        if self.include_elements:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Gather or Synthesize QUANTITY ELEMENT",
                    data={
                        "QUANTITY": (self.element_quantities, 1),
                        "ELEMENT": (self.element_types, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=3,
                ),
            ])    
        # language templates
        if self.include_languages:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Learn QUANTITY words in any language",
                    data={
                        "QUANTITY": (self.words_quantities, 1)
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Learn QUANTITY words of LANGUAGE",
                    data={
                        "QUANTITY": (self.words_quantities, 1),
                        "LANGUAGE": (self.languages_types, 1)
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),                
                GameObjectiveTemplate(
                    label="Learn QUANTITY words of LANGUAGE",
                    data={
                        "QUANTITY": (self.words_quantities, 1),
                        "LANGUAGE": (self.special_languages_types, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
            ])
            
        # upgrade templates
        if self.include_upgrades:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Install a UPGRADECLASS UPGRADETYPE upgrade",
                    data={
                        "UPGRADECLASS": (self.upgrades_class_types, 1),
                        "UPGRADETYPE": (self.upgrades_types,1)
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Upgrade your UPGRADETYPE inventory QUANTITY times",
                    data={
                        "UPGRADETYPE": (self.upgrades_types,1),
                        "QUANTITY": (self.inventory_upgrade_quantities, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),                
                GameObjectiveTemplate(
                    label="Install a Survey Device in any Multitool",
                    data={},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Get QUANTITY BLUEPRINTTYPE Blueprints",
                    data={
                        "QUANTITY": (self.blueprint_quantities, 1),
                        "BLUEPRINTTYPE": (self.blueprint_type,1),
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Learn QUANTITY Blueprints of any kind",
                    data={
                        "QUANTITY": (self.blueprint_quantities, 1)
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
            ])
        # animals templates
        if self.include_animals:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Tame QUANTITY different animal species",
                    data={
                        "QUANTITY": (self.taming_quantities, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Breed QUANTITY eggs",
                    data={
                        "QUANTITY": (self.taming_quantities, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="ACTION QUANTITY ANIMALTYPE",
                    data={
                        "ACTION": (self.animal_action_type,1),
                        "QUANTITY": (self.taming_quantities, 1),
                        "ANIMALTYPE": (self.animal_type,1)
                    },
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),                
                GameObjectiveTemplate(
                    label="Collect QUANTITY of animal dung from any animal",
                    data={
                        "QUANTITY": (self.taming_quantities, 1),
                    },                    
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                ),
            ])            
        # Freighters templates
        if self.include_freighters:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Recruit a UPGRADECLASS Freighter Flagship",
                    data={
                        "UPGRADECLASS": (self.upgrades_class_types, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Fully explore (all rooms and goals) a derelict freighter",
                    data={},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Discover and loot a crashed freighter",
                    data={},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                ),                
                GameObjectiveTemplate(
                    label="Discover and loot a crashed freighter under water",       
                    data={},          
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Recruit QUANTITY frigates of any type",  
                    data={
                        "QUANTITY": (self.recruit_quantities, 1),
                    },                    
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=3,
                ),                
                GameObjectiveTemplate(
                    label="Recruit QUANTITY TYPE frigates",  
                    data={
                        "QUANTITY": (self.recruit_quantities, 1),
                        "TYPE": (self.frigate_types, 1)
                    },                    
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
            ])     
    
        # Exploration templates
        if self.include_exploration:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Visit QUANTITY different Systems",
                    data={
                        "QUANTITY": (self.exploration_quantities, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Visit a TYPE star system",
                    data={
                        "TYPE": (self.star_system_types, 1),
                    },                    
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Discover an interstellar anomaly",
                    data={},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                ),                
                GameObjectiveTemplate(
                    label="Fly through a black hole",        
                    data={},         
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Meet an abysmal horror in space",    
                    data={},               
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),                
                GameObjectiveTemplate(
                    label="Travel through a portal to LOCATION",
                    data={
                        "LOCATION": (self.portal_location, 1),
                    },   
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Land on a TYPE planet",
                    data={
                        "TYPE": (self.planet_types, 1),
                    },   
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                ),                   
            ])
        # Vehicle templates
        if self.include_vehicle:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Get any Exo-Vehicle",
                    data={},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Get a TYPE Exo-Vehicle",
                    data={
                        "TYPE": (self.exo_vehicle_types, 1),
                    },                    
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),         
                
            ])  
        # Base templates
        if self.include_base:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Build a base teleporter",
                    data={},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Build or extend a TYPE base with at least QUANTITY base parts",
                    data={
                        "TYPE": (self.base_types, 1),
                        "QUANTITY": (self.build_quantities, 1)
                    },                    
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Unlock QUANTITY base blueprints",
                    data={
                        "QUANTITY": (self.blueprint_quantities, 1)
                    },                    
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),                
                GameObjectiveTemplate(
                    label="Build a working Energy Extractor",
                    data={},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                ),   
                GameObjectiveTemplate(
                    label="Build a working Gas Extractor",
                    data={},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                ),  
                GameObjectiveTemplate(
                    label="Build a working Mineral Extractor",  
                    data={},                 
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                ),                                
            ]) 
        # junk templates
        if self.include_junk:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Gather or Synthesize QUANTITY ELEMENT",
                    data={
                        "QUANTITY": (self.element_quantities, 1),
                        "ELEMENT": (self.junk_types, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=3,
                ),
            ]) 

        # landmark templates
        if self.include_landmarks:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Visit a TYPE on any planet",
                    data={
                        "TYPE": (self.landmark_types, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=3,
                ),
            ])    

        # combat templates
        if self.include_combat:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Kill at least QUANTITY of TYPE",
                    data={
                        "QUANTITY": (self.combat_kill_quantities, 1),
                        "TYPE": (self.combat_types, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=3,
                ),            
                GameObjectiveTemplate(
                    label="Save a Freigther from Pirates",
                    data={},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Destroy a Pirate Dreadnaught",
                    data={},
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Raid a freighter",
                    data={},
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=2,
                ),
                 GameObjectiveTemplate(
                    label="Kill QUANTITY creatures and/or security bots on derelict freighters",
                    data={
                        "QUANTITY": (self.combat_kill_quantities, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                ),    
            ])
        # Artifact templates
        if self.include_artifacts:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Gather QUANTITY RARITY TYPE",
                    data={
                        "RARITY": (self.artifact_rarity, 1),
                        "QUANTITY": (self.artifact_quantities, 1),
                        "TYPE": (self.artifact_types, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Obtain a RARITY ancient skeleton",
                    data={
                        "RARITY": (self.artifact_rarity, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=3,
                ),
            ])        
        # harvesting templates
        if self.include_harvesting:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Harvest QUANTITY TYPE",
                    data={
                        "QUANTITY": (self.harvesting_quantities, 1),
                        "TYPE": (self.harvesting_types, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Harvest QUANTITY TYPE",
                    data={
                        "QUANTITY": (self.harvesting_quantities, 1),
                        "TYPE": (self.harvesting_special_types, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
            ])
        # special templates
        if self.include_special:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Gather QUANTITY TYPE",
                    data={
                        "QUANTITY": (self.special_quantities, 1),
                        "TYPE": (self.special_types, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=3,
                ),
            ]) 
        # mission templates
        if self.include_missions:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Complete QUANTITY missions for the FACTION",
                    data={
                        "QUANTITY": (self.missions_quantities, 1),
                        "FACTION": (self.factions_types, 1)
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Complete QUANTITY TYPE missions",
                    data={
                        "QUANTITY": (self.missions_quantities, 1),
                        "TYPE": (self.missions_types, 1)
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
            ])
        # quests templates
        if self.include_quests:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Complete the quest line TYPE",
                    data={
                        "TYPE": (self.quest_types, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=3,
                ),
            ])
        # galaxy center templates
        if self.include_galaxy_center:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Reach the center of the galaxy without deliberately teleporting close to it using portals",
                    data={},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=3,
                ),
            ]) 
        # fishing templates
        if self.include_fishing:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Catch at least QUANTITY SIZE TYPE",
                    data={
                        "QUANTITY": (self.fishing_quantities, 1),
                        "SIZE": (self.fish_size, 1),
                        "TYPE": (self.fish_types, 1)
                    },                    
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Fish up at least QUANTITY flotsam",
                    data={
                        "QUANTITY": (self.fishing_quantities, 1),
                    },                    
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=3,
                ),
            ]) 
        # cooking templates
        if self.include_cooking:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Cook TYPE",
                    data={
                        "TYPE": (self.cooking_types, 1)
                    },                    
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
            ]) 
        # settlement templates
        if self.include_settlement:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Become Overseer of a Settlement",
                    data={},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Clear your Settlement's debt",
                    data={},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Make a settlement Decision",
                    data={},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Build a TYPE in your settlement",
                    data={
                        "TYPE": (self.settlement_building_types, 1)
                    },                    
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Upgrade a TYPE in your settlement to RANK",
                    data={
                        "TYPE": (self.settlement_building_types, 1),
                        "RANK": (self.upgrades_class_types, 1)
                    },                    
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),            
            ])
        # corvette templates
        if self.include_corvette:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Build a Corvette",
                    data={},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Build a RANK corvette",
                    data={
                        "RANK": (self.upgrades_class_types, 1)
                    },                    
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),            
            ])
        # crafting templates
        if self.include_crafting:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Craft all Atlas Passes",
                    data={},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Craft a Fusion Ignitor",
                    data={},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),            
            ]) 
        return game_objective_templates
            
    # Property checks
    @property
    def include_scanning(self) -> bool:
        return self.archipelago_options.nms_include_scanning.value
    @property
    def include_elements(self) -> bool:
        return self.archipelago_options.nms_include_elements.value    
    @property
    def include_junk(self) -> bool:
        return self.archipelago_options.nms_include_junk.value            
    @property
    def include_languages(self) -> bool:
        return self.archipelago_options.nms_include_languages.value
    @property
    def include_animals(self) -> bool:
        return self.archipelago_options.nms_include_animals.value
    @property
    def include_freighters(self) -> bool:
        return self.archipelago_options.nms_include_freighters.value
    @property
    def include_upgrades(self) -> bool:
        return self.archipelago_options.nms_include_upgrades.value
    @property
    def include_exploration(self) -> bool:
        return self.archipelago_options.nms_include_exploration.value
    @property
    def include_vehicle(self) -> bool:
        return self.archipelago_options.nms_include_vehicle.value
    @property
    def include_base(self) -> bool:
        return self.archipelago_options.nms_include_base.value
    @property
    def include_landmarks(self) -> bool:
        return self.archipelago_options.nms_include_landmarks.value
    @property
    def include_combat(self) -> bool:
        return self.archipelago_options.nms_include_combat.value    
    @property
    def include_artifacts(self) -> bool:
        return self.archipelago_options.nms_include_artifacts.value
    @property
    def include_harvesting(self) -> bool:
        return self.archipelago_options.nms_include_harvesting.value
    @property
    def include_special(self) -> bool:
        return self.archipelago_options.nms_include_special.value
    @property
    def include_missions(self) -> bool:
        return self.archipelago_options.nms_include_missions.value
    @property
    def include_quests(self) -> bool:
        return self.archipelago_options.nms_include_quests.value
    @property
    def include_galaxy_center(self) -> bool:
        return self.archipelago_options.nms_include_galaxy_center.value    
    @property
    def include_fishing(self) -> bool:
        return self.archipelago_options.nms_include_fishing.value
    @property
    def include_corvette(self) -> bool:
        return self.archipelago_options.nms_include_corvette.value
    @property
    def include_cooking(self) -> bool:
        return self.archipelago_options.nms_include_cooking.value
    @property
    def include_settlement(self) -> bool:
        return self.archipelago_options.nms_include_settlement.value
    @property
    def include_crafting(self) -> bool:
        return self.archipelago_options.nms_include_crafting.value
    @property
    def generate_portal_sequence(self) -> bool:
        return self.archipelago_options.nms_generate_portal_sequence.value
        
    @property
    def min_scan_num(self) -> int:
        return self.archipelago_options.nms_min_scan_num.value
    @property
    def max_scan_num(self) -> int:
        return self.archipelago_options.nms_max_scan_num.value
    @property
    def min_element_num(self) -> int:
        return self.archipelago_options.nms_min_element_num.value
    @property
    def max_element_num(self) -> int:
        return self.archipelago_options.nms_max_element_num.value
    @property
    def min_words_num(self) -> int:
        return self.archipelago_options.nms_min_words_num.value
    @property
    def max_words_num(self) -> int:
        return self.archipelago_options.nms_max_words_num.value
    @property
    def min_inventory_upgrade_num(self) -> int:
        return self.archipelago_options.nms_min_inventory_upgrade_num.value
    @property
    def max_inventory_upgrade_num(self) -> int:
        return self.archipelago_options.nms_max_inventory_upgrade_num.value        
    @property
    def min_blueprint_num(self) -> int:
        return self.archipelago_options.nms_min_blueprint_num.value
    @property
    def max_blueprint_num(self) -> int:
        return self.archipelago_options.nms_max_blueprint_num.value
    @property
    def min_taming_num(self) -> int:
        return self.archipelago_options.nms_min_taming_num.value
    @property
    def max_taming_num(self) -> int:
        return self.archipelago_options.nms_max_taming_num.value   
    @property
    def min_combat_kill_num(self) -> int:
        return self.archipelago_options.nms_min_combat_kills_num.value
    @property
    def max_combat_kill_num(self) -> int:
        return self.archipelago_options.nms_max_combat_kills_num.value
    @property
    def min_recruit_num(self) -> int:
        return self.archipelago_options.nms_min_recruit_num.value
    @property
    def max_recruit_num(self) -> int:
        return self.archipelago_options.nms_max_recruit_num.value        
    @property
    def min_exploration_num(self) -> int:
        return self.archipelago_options.nms_min_exploration_num.value
    @property
    def max_exploration_num(self) -> int:
        return self.archipelago_options.nms_max_exploration_num.value        
    @property
    def min_build_num(self) -> int:
        return self.archipelago_options.nms_min_build_num.value 
    @property
    def max_build_num(self) -> int:
        return self.archipelago_options.nms_max_build_num.value   
    @property
    def min_artifact_num(self) -> int:
        return self.archipelago_options.nms_min_artifact_num.value 
    @property
    def max_artifact_num(self) -> int:
        return self.archipelago_options.nms_max_artifact_num.value 
    @property
    def min_harvesting_num(self) -> int:
        return self.archipelago_options.nms_min_harvesting_num.value 
    @property
    def max_harvesting_num(self) -> int:
        return self.archipelago_options.nms_max_harvesting_num.value        
    @property
    def min_special_num(self) -> int:
        return self.archipelago_options.nms_min_special_num.value 
    @property
    def max_special_num(self) -> int:
        return self.archipelago_options.nms_max_special_num.value
    @property
    def min_missions_num(self) -> int:
        return self.archipelago_options.nms_min_missions_num.value 
    @property
    def max_missions_num(self) -> int:
        return self.archipelago_options.nms_max_missions_num.value  
    @property
    def min_fishing_num(self) -> int:
        return self.archipelago_options.nms_min_fishing_num.value 
    @property
    def max_fishing_num(self) -> int:
        return self.archipelago_options.nms_max_fishing_num.value        
       
    # Ranges
    def scan_quantities(self) -> range:
        return range(self.min_scan_num, self.max_scan_num, 5)        
    def element_quantities(self) -> range:
        return range(self.min_element_num, self.max_element_num, 50)
    def words_quantities(self) -> range:
        return range(self.min_words_num, self.max_words_num, 5)        
    def inventory_upgrade_quantities(self) -> range:
        return range(self.min_inventory_upgrade_num, self.max_inventory_upgrade_num, 1)
    def blueprint_quantities(self) -> range:
        return range(self.min_blueprint_num, self.max_blueprint_num, 1)        
    def taming_quantities(self) -> range:
        return range(self.min_taming_num, self.max_taming_num, 1)
    def combat_kill_quantities(self) -> range:
        return range(self.min_combat_kill_num, self.max_combat_kill_num, 1)  
    def recruit_quantities(self) -> range:
        return range(self.min_recruit_num, self.max_recruit_num, 1)          
    def exploration_quantities(self) -> range:
        return range(self.min_exploration_num, self.max_exploration_num, 1)    
    def build_quantities(self) -> range:
        return range(self.min_build_num, self.max_build_num, 1)    
    def artifact_quantities(self) -> range:
        return range(self.min_artifact_num, self.max_artifact_num, 1)
    def special_quantities(self) -> range:
        return range(self.min_special_num, self.max_special_num, 1)    
    def harvesting_quantities(self) -> range:
        return range(self.min_harvesting_num, self.max_harvesting_num, 10) 
    def missions_quantities(self) -> range:
        return range(self.min_missions_num, self.max_missions_num, 1) 
    def fishing_quantities(self) -> range:
        return range(self.min_fishing_num, self.max_fishing_num, 1) 
        
    # Stringbuilders
    def portal_location(self) -> List[str]:
        portal_address = ["any location"]
        if self.generate_portal_sequence:
            random.seed()
            sequence_str = ""
            for i in range(16):                
                if (i > 0):
                    sequence_str += ", "
                sequence_str += random.choice(self.glyphs())
            portal_address.append(sequence_str)
        return portal_address
            
    # Data lists
    @staticmethod
    def scan_types() -> List[str]:
        return [
            "Plants","Minerals","Land Animals","Air Animals","Underwater Animals", "Underground Animals"
        ]    
    @staticmethod
    def frigate_types() -> List[str]:
        return [
            "Combat", "Expedition", "Industrial", "Trade", "Support"
        ]            
    @staticmethod
    def element_types() -> List[str]:
        return [
            "Silicate Powder", "Carbon", "Di-Hydrogen", "Tritium", "Oxygen", "Ferrite Dust", "Faecium", "Condensed Carbon", "Pure Ferrite", "Salt", "Cobalt", "Gold", "Copper", "Sodium", "Chlorite", "Magnetized Ferrite", "Cyto Phosphate", "Silver", "Cadmium", "Mordite", "Paraffinium", "Ionized Cobalt", "Ammonia", "Pyrite", "Platinum", "Activated Cadmium", "Dioxide", "Activated Copper", "Emeril", "Phosphorous", "Sodium Nitrate", "Uranium", "Activated Emeril", "Deuterium", "Chromatic Metal", "Indium", "Activated Indium", "Nitrogen", "Radon", "Sulphurine", "Basalt","Quartzite","Activated Quartzite", "Crystallised Helium", "Methane", "Lithium", "Chlorine", "Tainted Metal", "Pugneum"
        ]
    @staticmethod
    def junk_types() -> List[str]:
        return [
            "Living Slime", "Residual Goop", "Rusted Metal", "Runaway Mold", "Viscous Fluids"
        ]        
    @staticmethod
    def languages_types() -> List[str]:
        return [
            "Korvax", "Gek", "Vykeen"
        ]
    @staticmethod
    def special_languages_types() -> List[str]:
        return [
            "Autophage", "Atlas"
        ]
        
    @staticmethod
    def upgrades_class_types() -> List[str]:
        return [
            "C-Class", "B-Class", "A-Class", "S-Class"
        ]
    @staticmethod
    def upgrades_types() -> List[str]:
        return [
            "Ship", "Suit", "Freighter", "Multitool", "Vehicle" 
        ]    
    @staticmethod
    def blueprint_type() -> List[str]:
        return [
            "Base", "Freighter Rooms", "Freighter", "Multitool", "Vehicle" 
        ]          
    @staticmethod
    def animal_action_type() -> List[str]:
        return [
            "Kill", "Milk", "Feed", "photograph"
        ]    
    @staticmethod
    def star_system_types() -> List[str]:
        return [
            "Red","Green","Blue","Purple","Outlaw","Abandoned","Uncharted","Atlas"
        ]
    @staticmethod
    def planet_types() -> List[str]:
        return [
            "Lush", "Barren", "Dead", "Exotic", "Mega Exotic", "Scorched", "Frozen", "Toxic", "Irradiated", "Marsh", "Volcanic", "Waterworld", "Gas Giant", "Infested", "Water"
        ]          
    @staticmethod
    def animal_type() -> List[str]:
        return [
            "Anastomus - Striders (the bipedal species with long legs and no arms), uncommon","Anomalous - Creatures that can only be found on planets with exotic biome, rare", "Arthropodae - Giant insectoid critters", "Bos - Spiders, uncommon, floating spiders, rare", "Bosoptera - Crawling beetles, may be capable of flight", "Conokinis - Swarming beetles, common", "Felidae - Cats, common", "Felihex - Hexapodal cat, uncommon", "Floradae - Hybrids of flora and fauna", "Hexungulatis - Hexapodal cow, uncommon", "Lok - Blobs, common", "Mechanoceris - Robot antelopes", "Mogara - Grunts, the bipedal species which often look like the Gek, rare", "Osteofelidae - Bonecats", "Prionterrae - Ploughs, generally digging species", "Procavya - Rodents, common", "Protosphaeridae - Protorollers, orb-shaped species", "Prototerrae - Protodiggers, the clusters of protrusions that pop out of the ground", "Rangifae - Diplos (long neck dinosaurs), uncommon", "Reococcyx - Bipedal antelopes, uncommon", "Shaihuluda - Sandworms, immortal giant worms", "Spiralis - Drills", "Structurae - Synthetic lifeforms with buildings as their body", "Talpidae - Moles", "Tetraceris - Antelopes, common", "Theroma - Triceratops, uncommon", "Tyranocae - Tyrannosaurus rex-like species, uncommon", "Ungulatis - Cow, common", "Bosaquatica - Underwater crabs, common (community-labeled genus)", "Chrysaora - Jellyfish, common", "Crustacea - Prawns", "Hippocampus - Seahorses", "Ictaloris - Fish, common", "Krakenidae - Giant squids", "Mobula - Manta rays", "Prionace - Sharks, eels, seasnakes, common", "Prionacefda - Swimming cows, rare", "Procavaquatica - Swimming rodents, rare (community-labeled genus)", "Agnelis - Birds, common", "Cycromys - ID says FlyingLizard, the winged species that are much larger than Agnelis, common", "Oxyacta - Wraiths / flying snake-like organisms, rare", "Protocaeli - Protoflyers", "Rhopalocera - Pygmy butterflies, Anomalous butterflies, Large butterflies, common"
        ]  
    @staticmethod
    def exo_vehicle_types() -> List[str]:
        return [
            "Roamer", "Nomad", "Colossus", "Pilgrim", "Nautilon", "Minotaur"
        ]
    @staticmethod
    def base_types() -> List[str]:
        return [
            "land", "underwater"
        ]        
    @staticmethod
    def glyphs() -> List[str]:
        return [
            "Star Over Water (sunset)", "Hunter (bird)", "Reflection (face)", "Ancient Giant (diplo)", "Obscured Champion (eclipse)", "Ascending Orb (balloon)", "Sailor (boat)", "Lowly Insect (bug)", "dragonfly", "Spiral of Reality (Galaxy)", "Anomaly (voxel)", "Ocean King (fish)", "tent", "Vessel To Beyond (rocket)", "tree", "atlas"
        ]         
    @staticmethod
    def landmark_types() -> List[str]:
        return [
            "Plaque", "Ruins", "Monolith", "Portal", "Boundary Failure", "Manufacturing Facility", "Operation Center", "Depot", "Habitable Base by another player", "Shelter", "Minor Settlement", "Observatory", "Trading Post", "Transmission Tower", "Colossal Archive", "Harmonic Camp", "Autophage Camp", "Crashed Ship", "Crashed Freighter", "Abandoned Building", "Holo Terminus", "Waypoint", "Beacon", "Drop Pod", "Galactic Trade Terminal", "Space Station"
        ]         
    @staticmethod
    def combat_types() -> List[str]:
        return [
            "Sentinels", "Biological Horrors", "Abyssal Horrors", "Predators", "Titan Worms"
        ]         
    @staticmethod
    def space_combat_types() -> List[str]:
        return [
            "Space Pirates", "Sentinel Ships"
        ]            
    @staticmethod
    def artifact_types() -> List[str]:
        return [
            "Aquatic Treasure", "Biological Sample", "Delicate Flora", "Excavated Bones", "Fossil Sample", "Historical Document", "Lost Artifact", "Salvaged Scrap", "Terrifying Sample", "Unearthed Treasure"
        ]                    
    @staticmethod
    def artifact_rarity() -> List[str]:
        return [
            "Common", "Uncommon", "Rare"
        ]                                
    @staticmethod
    def harvesting_types() -> List[str]:
        return [
            "Cactus Flesh", "Faecium", "Frost Crystal", "Fungal Mold", "Gamma Root", "Marrow Bulb", "Solanium", "Star Bulb", "Mordite"
        ]
    @staticmethod
    def harvesting_special_types() -> List[str]:
        return [
            "Kelp Sac", "Albumen Pearl", "Gravitino Ball", "NipNip", "Sac Venom"
        ]
    @staticmethod
    def special_types() -> List[str]:
        return [
            "Somnal Dust", "Atlantideum", "Liquid Sun", "Hexite"
        ]     
    @staticmethod
    def factions_types() -> List[str]:
        return [
            "Korvax", "Gek", "Vy'Keen", "Autophage", "Explorers Guild", "Merchants Guild", "Mercenaries Guild", "Outlaws"
        ]
    @staticmethod
    def missions_types() -> List[str]:
        return [
            "Collect Item", "Delivery", "Destroy Sentinels", "Kill Creatures", "Feed Creatures", "Find Missing Person", "Hunt Pirates", "Take A Photo", "Raid a facility", "Assault a Freighter", "Defend a Freighter", "Repair a damaged item", "scan objects", "Anomaly"
        ]
    @staticmethod
    def quest_types() -> List[str]:
        return [
            "Artemis", "Atlas", "Collecting Fossiles", "Dreams of the Deep", "Starbirth", "The Settlers", "They Who Returned", "Under a Rebel Star", "A Trace of Metal", "In Stellar Multitudes"
        ] 
    @staticmethod
    def fish_types() -> List[str]:
        return [
            "fish", "night-active fish", "storm-active fish", "day-active fish", "fish inhabiting only toxic planets", "fish inhabiting only irradiated planets", "fish inhabiting only scorching planets", "fish inhabiting only frozen planets", "fish inhabiting only lush planets", "fish inhabiting only barren planets", "fish inhabiting only Mega Exotic planets", "fish inhabiting only underwater planets", "fish inhabiting only Gas Giants"
        ]
    @staticmethod
    def fish_rarity() -> List[str]:
        return [
            "any", "common", "uncommon", "rare", "legendary"
        ]
    @staticmethod
    def fish_size() -> List[str]:
        return [
            "any", "small", "medium-sized", "large", "colossal"
        ]
    @staticmethod
    def settlement_building_types() -> List[str]:
        return [
            "Distribution Centre", "Factory Module", "Farm Module", "Fishing Pond", "Marketplace", "Residence", "Saloon", "Starship Dock", "Tower", "Utility Module", "Warehouse"
        ]    
    @staticmethod
    def cooking_types() -> List[str]:
        return [
            "Wild Yeast", "Meat Flakes", "Silicon Egg", "Meaty Chunks", "Steamed Vegetables", "Processed Meat", "Smoked Meat", "Processed Sugar", "Synthetic Honey", "Purged Ribs", "Nourishing Slime", "Cream", "Proto-Cream", "Churned Butter", "Proto-Butter", "Pastry", "Bone Milk", "Bone Butter", "Bone Cream (Cheese)", "Very Thick Custard", "Bone Cream", "Viscous Custard", "Salty Custard", "Monstrous Custard", "Stellar Custard", "Delicate Meringue", "Sweetened Butter", "Sweetened Proto-Butter", "Honey Butter", "Honied Proto-Butter", "Gooey Butter", "Gooey ProtoButter", "Tangy Cheese", "ProtoCheese", "Dough", "Sugar Dough", "Butter Syrup", "Syrupy Proto-Butter", "Crunchy Caramel", "Clarified Oil", "Proto-Oil", "Iced Screams", "Ice Cream", "Briney Rime", "Deathly-Cold Ice Cream", "Stellar Ice Cream", "Chocolate Ice Cream", "Caramel Ice Cream", "Fruity Ice Cream", "Apple Ice Cream", "Honey Ice Cream", "Perpetual Ice Cream", "Vy'ice Cream", "Icey Marrow", "Spiced Ice", "Slime Pop", "Bread", "Cake Batter", "Proto-Batter", "Thick, Sweet Batter", "Wailing Batter", "Extra-Fluffy Batter", "Writhing, Roiling Butter", "Syrupy Butter", "Horrifying Mush", "Baked Eggs", "Omelette", "Whispering Omelette", "Proto-Omelette", "Parasitic Omelette", "Scrambled Marrow", "Fungal Omelette", "Bugs-in-a-Blanket", "Root Juice", "Pilgrim's Tonic", "Fire Water", "Refreshing Drink", "Salty Juice", "Flavoursome Sauce", "Scorching Sauce", "Creamy Sauce", "Partially-Liquid Cheese", "Mystery Meat Stew", "Fibrous Stew", "Stewed Organs", "Crystalline Soup", "Well-Stirred Stew", "Gelatinous Goop", "Soiled Soup", "Chewy Dumpling Stew", "Abyssal Stew", "Tangy Orange Surprise", "Tangy Vegetable Stew", "Cheese-and-Flesh Stew", "Creamed Organ Soup", "Cream of Vegetable Soup", "Thick Meat Stew", "Devilled Organs", "Fiery Vegetable Stew", "Spicy Fleshballs", "Flavoursome Organs", "Delicious Vegetable Stew", "Herb-Encrusted Flesh", "Popping Stew", "The Worst Stew", "Syrupy Viscera", "Bone Broth", "Anomalous Jam", "Ever-burning Jam", "Grahj'am", "Cactus Jelly", "Furball Jelly", "Wriggling Jam", "Sweetened Mucous", "Lumpen Doughnut", "Proto-Beignet", "Custard Doughnut", "Salty Doughnut", "Monstrous Doughnut", "The Stellarator", "Honey Doughnut", "Honeybutter Doughnut", "Gooey ProtoDoughnut", "Caramel Doughnut", "Cocoa Doughnut", "Proteinous Doughnut", "Jam Doughnut", "Wriggling Doughnut", "Anomalous Doughnut", "Mucal Doughnut", "Pollen Puffball", "Pie Case", "Mystery Meat Pie", "Smokey Meat Pie", "High-Fibre Pie", "Fish Pie", "Chewy Organ Pie", "Proto-Sausage Pie", "Legs-in-Pastry", "Glowing Pie", "Mushed Root Pie", "Solidified Grease Pie", "Cheesy Vegetable Pie", "Gristle Pie", "Leathery Tart", "The Pie of Knowledge", "Gritty Meat Pie", "Earthy Pie", "Haunted Pie", "The Spawning Tart", "The Toothbreaker", "Fruity Pudding", "Fungal Tart", "Jam Tart", "Anomalous Tart", "Spikey Tart", "Honey Tart", "Jellied Fur Tart", "Wriggling Tart", "Cocoa Tart", "Caramel Tart", "Custard Tart", "Stellar Custard Tart", "Baked Cheese Tart", "Creamy Treat", "Muculent Tart", "Seeping Pie", "Burning Jam Surprise", "Cream Buns", "Esophageal Surpsrise", "Custard Fancy", "Briney Delight", "Interstellar Fancy", "Cream Curiosity", "Chocolate Curiosity", "Caramel Curiosity", "Apple Curiosity", "Prickly Curiosity", "Jam Curiosity", "Startling Fancy", "Unsolvable Jam Turnover", "Custard Curiosity", "Salty Surprise", "Intestellar Curiosity", "Chocolate Dream", "Glittering Honey Cake", "Questionably Sweet Cake", "Chocolate Cake", "Caramal-Encrusted Cake", "Spiced Apple Cake", "Traditional Cake", "Ever-Boiling Cake", "Perpetual Cake", "Honied Angel Cake", "Extra-Fluffy Cream Cake", "Fluffy Caramel Delight", "Angelic Fruit Cake", "Soft and Spiky Surprise", "Jam Fluffer", "Burning Jam Fluffer", "Perpetual Jam Fluffer", "Soft Custard Fancy", "Monstrous Honey Cake", "Honied Proto-Cake", "Horrifying Gooey Delight", "Haunted Chocolate Dreams", "Unbound Cream Horn", "Volatile Chocolate Fancy", "Fluffy Throatripper", "Writhing Jam Puff", "Gooey Screamer", "Most Curious Cake", "Honey-Soaked Fancy", "Sweet Cream Dreams", "Gooey Chocolate Cake", "Gooey Caramel Cake", "Gooey Fruit Surprise", "Honied Throat-Sticker", "Jam Oozers", "Gooey Mouthburner", "Perpetual Honeycake", "Gooey Custard Fancy", "Salt-Laced Honey Cake", "Starbirth Delight", "Gooey Honey Puff", "Doomed Cream Cake", "Wailing Caramel Cake", "Apple Cake of Lost Souls", "Choking Monstrosity Cake", "Appalling Jam Sponge", "Cake of Burning Dread", "Cake of Glass", "Tortured Honey Cake", "Itching Creeping Honey Sponge", "Cake of Sin", "Cake of the Lost", "Caramelised Nightmare", "Unbound Monstrosity", "Mucal Curiosity", "Ambrosial Curse", "Squirming Fancy", "Primordial Sponge", "Gelatinous Sponge", "Nourishing Oozer", "Frosted Mire", "Nectar Islands", "Cake of Eternal Sleep", "Syrup-Drenched Delight", "Nectar Sponge Cake", "Creamy Clouds of Nectar", "Chocolate Oozer", "Syrupy Caramel Slice", "Ambrosial Wonder", "Candied Apples", "Hybrid Cake", "Sponge of Ambrosia", "Sweet and Salty Puff", "Starpollen Surprise", "Xeno-Sponge", "Syrupy Tingler", "Jammy Burster", "Splicers Delight", "Simple Biscuit", "Apple Roll", "Baked Anomaly", "Burning Surprise", "Chewy Biscuit", "Cocoa Creams", "Cough Biscuits", "Cream Fingers", "Curdy Cracker", "Enriched Biscuit", "Fish Biscuit", "Floral Wafer", "Haunted Wafer", "Healthy Wheatblock", "Herbal Crunchie", "Honey Waffle", "Jammy Rounds", "Questionable Biscuit", "Salty Cruncher", "Spore Dunkers", "Sticky Finger", "Tooth Pickers", "Well-Smoked Biscuit", "Wriggling Tack", "Fleshy Cylinder", "Mollusc Flesh", "Pickled Fish", "Edible Chum", "Jellymeat", "Marine Steak", "Boiled Flipper", "Snail Fillet", "Grilled Tentacle", "Steamed Rubber", "Shell Puree", "Delicate Legs", "Fish Fry", "Whitebait", "Grilled Fillet", "Smoked Fish", "Poached Worms", "Brined Flesh", "Seafood Feast", "Peeled Claws", "Seared Fillet", "Fishy Slab", "Whole Roast Fish", "Horrifying Mush", "Haunted Fillet", "Starched Fish", "Marine Pie", "Fish and Rice", "Jellied Eel", "Seafood Stew", "Sea's Bounty", "Assorted Roe", "Salty Platter"
        ]        
        
        
#Archipelago Options 
class NmsIncludeScanning(DefaultOnToggle):
    """Include Scanning Goals (Scan X Plants/Animals/Minerals)"""
    display_name = "Include No Man's Sky Scanning Objectives"
class NmsIncludeElements(DefaultOnToggle):
    """Include Element collection Goals (Collect X of ELEMENT)"""
    display_name = "Include No Man's Sky Scanning Objectives"
class NmsIncludeLanguages(DefaultOnToggle):
    """Include Language Learning Goals (Learn X Words of Language)"""
    display_name = "Include No Man's Sky Language Learning Objectives"
class NmsIncludeAnimals(DefaultOnToggle):
    """Include Animal Goals (Taming / Milking / Killing / ...)"""
    display_name = "Include No Man's Sky Animal Objectives"
class NmsIncludeFreighters(DefaultOnToggle):
    """Include Freighter Goals (Obtaining / Upgrading / ...)"""
    display_name = "Include No Man's Sky Freighter Objectives"
class NmsIncludeUpgrades(DefaultOnToggle):
    """Include Upgrade Goals (Multitool / Suit / Inventory / Vehicles / ...)"""
    display_name = "Include No Man's Sky Upgrading Objectives"
class NmsIncludeExploration(DefaultOnToggle):
    """Include Exploration Goals"""
    display_name = "Include No Man's Sky Exploration Objectives"
class NmsGeneratePortalSequence(DefaultOnToggle):
    """Demand a specific Portal Sequence for the Exploration goal 'Travel through a portal' (Does nothing if Exploration Objectives are not active)"""
    display_name = "Allow specific Portal Sequence Objectives"
class NmsIncludeVehicle(DefaultOnToggle):
    """Include Vehicle Goals"""
    display_name = "Include No Man's Sky Vehicle Objectives"
class NmsIncludeBase(DefaultOnToggle):
    """Include Base Building Goals"""
    display_name = "Include No Man's Sky Base Building Objectives"
class NmsIncludeJunk(DefaultOnToggle):
    """Include Junk Collection Goals"""
    display_name = "Include No Man's Sky Junk Collection Objectives"
class NmsIncludeLandmarks(DefaultOnToggle):
    """Include specific Landmark Visiting Goals"""
    display_name = "Include No Man's Sky Landmark Visiting Objectives"
class NmsIncludeCombat(DefaultOnToggle):
    """Include Combat oriented Goals"""
    display_name = "Include No Man's Sky Combat Objectives"
class NmsIncludeArtifacts(DefaultOnToggle):
    """Include Artifact Goals"""
    display_name = "Include No Man's Sky Artifact Objectives"
class NmsIncludeHarvesting(DefaultOnToggle):
    """Include Harvesting Goals"""
    display_name = "Include No Man's Sky Harvesting Objectives"
class NmsIncludeSpecial(DefaultOnToggle):
    """Include Special Resource Goals"""
    display_name = "Include No Man's Sky Special Resource Objectives"
class NmsIncludeMissions(DefaultOnToggle):
    """Include Faction Mission Goals"""
    display_name = "Include No Man's Sky Faction Mission Objectives"
class NmsIncludeQuests(DefaultOnToggle):
    """Include Story Quest Goals"""
    display_name = "Include No Man's Sky Story Quest Objectives"
class NmsIncludeCenter(DefaultOnToggle):
    """Include Reach the center of the Galaxy as Goal"""
    display_name = "Include No Man's Sky Reach Center of the Galaxy Objective"
class NmsIncludeFishing(DefaultOnToggle):
    """Include Fishing Goals"""
    display_name = "Include No Man's Sky Fishing Objectives"
class NmsIncludeCooking(DefaultOnToggle):
    """Include Cooking Goals"""
    display_name = "Include No Man's Sky Cooking Objectives"
class NmsIncludeSettlements(DefaultOnToggle):
    """Include Settlement Goals"""
    display_name = "Include No Man's Sky Settlement Objectives"
class NmsIncludeCorvette(DefaultOnToggle):
    """Include Corvette Goals"""
    display_name = "Include No Man's Sky Corvette Objectives"
class NmsIncludeCrafting(DefaultOnToggle):
    """Include Crafting Goals"""
    display_name = "Include No Man's Sky Crafting Objectives"

class NmsMinElementNum(NamedRange):
    """
    Minimum Number of Elements to collect for Element and Resource Collection Goals
    """

    display_name = "Resource collection minimum"
    default = 50
    range_start = 50
    range_end = 600
class NmsMaxElementNum(NamedRange):
    """
    Maximum Number of Elements to collect for Element and Resource Collection Goals
    """

    display_name = "Resource collection maximum"
    default = 250
    range_start = 50
    range_end = 600
    
class NmsMinScanNum(NamedRange):
    """
    Minimum Number of Items to scan for Scanning Goals
    """

    display_name = "Scan Goal minimum"
    default = 1
    range_start = 1
    range_end = 100
class NmsMaxScanNum(NamedRange):
    """
    Maximum Number of Items to scan for Scanning Goals
    """

    display_name = "Scan Goal maximum"
    default = 10
    range_start = 1
    range_end = 100
    
class NmsMinWordsNum(NamedRange):
    """
    Minimum Number of words to learn for language goals
    """

    display_name = "Word Learn minimum"
    default = 1
    range_start = 1
    range_end = 100
class NmsMaxWordsNum(NamedRange):
    """
    Maximum Number of words to learn for language goals
    """

    display_name = "Word Learn maximum"
    default = 10
    range_start = 1
    range_end = 100
    
class NmsMinInventoryUpgradeNum(NamedRange):
    """
    Minimum Number of inventory upgrades for goals
    """

    display_name = "Inventory Upgrade minimum"
    default = 1
    range_start = 1
    range_end = 60
class NmsMaxInventoryUpgradeNum(NamedRange):
    """
    Maximum Number of inventory upgrades for goals
    """

    display_name = "Inventory Upgrade maximum"
    default = 10
    range_start = 1
    range_end = 60
    
class NmsMinBlueprintNum(NamedRange):
    """
    Minimum Number of base part blueprints to obtain for goals
    """

    display_name = "Base Part Blueprint minimum"
    default = 1
    range_start = 1
    range_end = 464
class NmsMaxBlueprintNum(NamedRange):
    """
    Maximum Number of base part blueprints to obtain for goals
    """

    display_name = "Base Part Blueprint maximum"
    default = 10
    range_start = 1
    range_end = 464
    
class NmsMinTamingNum(NamedRange):
    """
    Minimum Number for animal goals
    """

    display_name = "Animal minimum"
    default = 1
    range_start = 1
    range_end = 50
class NmsMaxTamingNum(NamedRange):
    """
    Maximum Number for animal goals
    """

    display_name = "Animal maximum"
    default = 10
    range_start = 1
    range_end = 50
    
class NmsMinCombatKillsNum(NamedRange):
    """
    Minimum Number for kill goals
    """

    display_name = "Combat Kill minimum"
    default = 1
    range_start = 1
    range_end = 50
class NmsMaxCombatKillsNum(NamedRange):
    """
    Maximum Number for kill goals
    """

    display_name = "Combat Kill maximum"
    default = 10
    range_start = 1
    range_end = 50
    
class NmsMinRecruitNum(NamedRange):
    """
    Minimum Number for Frigate Recruitment Goals
    """

    display_name = "Frigate Recruitment minimum"
    default = 1
    range_start = 1
    range_end = 30
class NmsMaxRecruitNum(NamedRange):
    """
    Maximum Number for Frigate Recruitment Goals
    """

    display_name = "Frigate Recruitment maximum"
    default = 10
    range_start = 1
    range_end = 30
    
class NmsMinExplorationNum(NamedRange):
    """
    Minimum Number of Systems to visit for Exploration Goals
    """

    display_name = "Exploration Goal minimum"
    default = 1
    range_start = 1
    range_end = 30
class NmsMaxExplorationNum(NamedRange):
    """
    Maximum Number of Systems to visit for Exploration Goals
    """

    display_name = "Exploration Goal maximum"
    default = 10
    range_start = 1
    range_end = 30
    
class NmsMinBuildNum(NamedRange):
    """
    Minimum Number of Base Parts for Building Goals
    """

    display_name = "Base Building Goal minimum"
    default = 1
    range_start = 1
    range_end = 50
class NmsMaxBuildNum(NamedRange):
    """
    Maximum Number of Base Parts for Building Goals
    """

    display_name = "Base Building Goal maximum"
    default = 10
    range_start = 1
    range_end = 50
    
class NmsMinArtifactNum(NamedRange):
    """
    Minimum Number of Artifacts to find for Goals
    """

    display_name = "Artifact Goal minimum"
    default = 1
    range_start = 1
    range_end = 50
class NmsMaxArtifactNum(NamedRange):
    """
    Maximum Number of Artifacts to find for Goals
    """

    display_name = "Artifact Goal maximum"
    default = 10
    range_start = 1
    range_end = 50
    
class NmsMinHarvestingNum(NamedRange):
    """
    Minimum Number of plants to harvest for Goals
    """

    display_name = "Plant Harvest Goal minimum"
    default = 10
    range_start = 1
    range_end = 300
class NmsMaxHarvestingNum(NamedRange):
    """
    Maximum Number of plants to harvest for Goals
    """

    display_name = "Plant Harvest Goal maximum"
    default = 100
    range_start = 1
    range_end = 300
    
class NmsMinSpecialNum(NamedRange):
    """
    Minimum Number of Special Elements to find for Goals
    """

    display_name = "Special Element Goal minimum"
    default = 10
    range_start = 1
    range_end = 300
class NmsMaxSpecialNum(NamedRange):
    """
    Maximum Number of Special Elements to find for Goals
    """

    display_name = "Special Element Goal maximum"
    default = 100
    range_start = 1
    range_end = 300
    
class NmsMinMissionsNum(NamedRange):
    """
    Minimum Number of Missions to complete for Goals
    """

    display_name = "Minimum number of missions to complete for goals"
    default = 1
    range_start = 1
    range_end = 100
class NmsMaxMissionsNum(NamedRange):
    """
    Maximum Number of Missions to complete for Goals
    """

    display_name = "Maximum number of missions to complete for goals"
    default = 10
    range_start = 1
    range_end = 100
    
class NmsMinFishingNum(NamedRange):
    """
    Minimum Number of Fish to catch for Goals
    """

    display_name = "Minimum number of Fish to catch for goals"
    default = 1
    range_start = 1
    range_end = 100
class NmsMaxFishingNum(NamedRange):
    """
    Maximum Number of Fish to catch for Goals
    """

    display_name = "Maximum number of Fish to catch for goals"
    default = 10
    range_start = 1
    range_end = 100

