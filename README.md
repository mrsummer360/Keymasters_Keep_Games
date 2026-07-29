# Keymasters_Keep_Games
mrsummer360's game implementations for [Keymaster's Keep](https://github.com/SerpentAI/Archipelago/releases?q=keymaster%27s+keep), a game mode for [Archipelago Multiworld](https://www.archipelago.gg)

## Installation

1. [Install Archipelago](https://archipelago.gg/tutorial/Archipelago/setup_en).
2. Add the [Keymaster's Keep `.apworld` file](https://github.com/silasary/Archipelago/releases?q=keymaster%27s&expanded=true) into Archipelago's `worlds/` folder.
3. Run the Archipelago Launcher. A new `keymasters_keep/` folder will be created.
4. Download the `.py` files for the games you wish to add to the game pool, and place them into the `keymasters_keep/` folder.
5. Restart the Archipelago Launcher and open 'Generate Template Options'. The `Players/Templates/Keymaster's Keep.yaml` file will now contain the customisable settings for each implementation installed.

## KMK Codex Entries
### No Man's Sky
__Version:__ 1.0  
__Download:__ [LINK](https://github.com/mrsummer360/Keymasters_Keep_Games/blob/main/nms.py)  
__Description:__  
No Man's Sky is a vast science fiction survival and exploration game set in a procedurally generated universe containing over 18 quintillion unique planets. Players take on the role of a space explorer, hopping between worlds to gather resources, upgrade their ship and equipment, uncover ancient alien lore, and gradually unravel the mysteries at the heart of the cosmos. Each planet offers its own distinct ecosystem, creatures, and hazards, ensuring no two worlds feel quite alike. The game supports both solo and multiplayer experiences, and has evolved dramatically since its 2016 launch — with Hello Games continuously releasing free updates that have added base building, underwater exploration, living ships, and much more.

__KMK Implementation:__  
The implementation includes various challenges across all areas of the gameplay. They are divided into categories, that can be individually activated and configured with minimum and maximum boundaries. 
For more background on some of the goals (like interactions with certain animal categories or portal sequences) see [No Man's Sky wiki](https://nomanssky.fandom.com/wiki/Product)

#### Objectives
1. Scanning
    - Scan QUANTITY SCANTYPE
    - Visit QUANTITY planets and scan at least one SCANTYPE
    - Scan all Wildlife on QUANTITY planets
2. Elements
    - Gather or Synthesize QUANTITY ELEMENT
3. Languages
    - Learn QUANTITY words in any language
    - Learn QUANTITY words of LANGUAGE (common languages)
    - Learn QUANTITY words of LANGUAGE (special languages like Atlas)
4. Upgrades
    - Install a UPGRADECLASS UPGRADETYPE upgrade
    - Upgrade your UPGRADETYPE inventory QUANTITY times
    - Install a Survey Device in any Multitool
    - Get QUANTITY BLUEPRINTTYPE Blueprints
    - Learn QUANTITY Blueprints of any kind
5. Animals
    - Tame QUANTITY different animal species
    - Breed QUANTITY eggs
    - ACTION QUANTITY ANIMALTYPE
    - Collect QUANTITY of animal dung from any animal
6. Freighters
    - Recruit a UPGRADECLASS Freighter Flagship
    - Fully explore (all rooms and goals) a derelict freighter
    - Discover and loot a crashed freighter
    - Discover and loot a crashed freighter under water
    - Recruit QUANTITY frigates of any type
    - Recruit QUANTITY TYPE frigates
7. Exploration
    - Visit QUANTITY different systems
    - Visit a TYPE star system
    - Discover an interstellar anomaly
    - Fly through a black hole
    - Meet an abysmal horror in space
    - Travel through a portal to LOCATION (specific locations can be deactivated, see wiki for portal glyph nomination)
    - Land on a TYPE planet
8. Vehicles
    - Get an Exo-Vehicle
    - Get a TYPE Exo-Vehicle
9. Bases
    - Build a base teleporter
    - Build or extend a TYPE base with at least QUANTITY base parts
    - Unlock QUANTITY base blueprints
    - Build a working Energy Extractor
    - Build a working Gas Extractor
    - Build a working Mineral Extractor
10. Junk
    - Gather or Synthesize QUANTITY ELEMENT (junk only)
11. Landmarks
    - Visit a TYPE on any planet
12. Combat
    - Kill at least QUANTITY of TYPE
    - Save a Freighter from Pirates
    - Destroy a pirate Dreadnaught
    - Raid a freighter
    - Kill QUANTITY creatures and/or security bots on derelict freighters
13. Artifacts
    - Gather QUANTITY RARITY TYPE
    - Obtain a RARITY ancient skeleton
14. Harvesting
    - Harvest QUANTITY TYPE (Regular crops)
    - Harvest QUANTITY TYPE (Special plants like Nipnip or Gravitino Balls)
15. Special
    - Harvest QUANTITY TYPE (special elements like Hexite)
16. Missions
    - Complete QUANTITY missions for the FACTION
    - Complete QUANTITY TYPE missions
17. Quests
    - Complete the quest line TYPE 
18. Galaxy Center
    - Reach the center of the galaxy without deliberately teleporting close to it
19. Fishing
    - Catch at least QUANTITY SIZE TYPE
    - Fish up at least QUANTITY flotsam
20. Cooking
    - Cook TYPE
21. Settlement
    - Become Overseer of a Settlement
    - Clear your Settlement's debt
    - Make a settlement decision
    - Build a TYPE in your settlement
    - Upgrade a TYPE in your settlement to RANK
22. Corvette
    - Build a corvette
    - Build a RANK corvette
23. Crafting
    - Craft all Atlas Passes
    - Craft a fusion ignitor

### Spoonacular
__Version:__ 1.0  
__Download:__ [LINK](https://github.com/mrsummer360/Keymasters_Keep_Games/blob/main/spoonacular.py)  
__Description:__   
The Spoonacular API is a comprehensive food and recipe data platform that gives developers access to an extensive database of recipes, ingredients, nutritional information, and meal planning tools. It enables applications to search and filter recipes by cuisine, diet, allergens, and available ingredients, as well as retrieve detailed nutritional breakdowns, wine pairings, and even grocery product data. Whether you're building a meal planner, a fitness tracker, or a cooking app, Spoonacular provides the data infrastructure to power rich, food-focused experiences with minimal effort.

__KMK Implementation:__  
This implementation uses the random_recipe API to fetch random recipes which should be cooked in order to fulfill the objective. The API call supports basic caching to limit API credit usage, the calls can be made with included and excluded tags. 

#### Objectives
Cook RECIPE
Cook anything or set API key and try again (is generated when invalid or no API key is set)

RECIPE is split into recipe name and a link to the recipe itself.


### Two Point Campus
__Version:__ 1.0
__Description:__
Two Point Campus is a management and simulation game about building and running your own university. Players design campuses, construct and upgrade rooms, hire and train staff, and offer a wide range of courses (from Wizardry and Spy School to Robotics and Gastronomy) to attract and educate students. Success is measured through Prestige, reputation, and star ratings as campuses grow from modest single-course schools into sprawling, fully-equipped institutions. Three expansions, Space Academy, School Spirits, and Medical School, add their own courses, skills, and mechanics on top of the base game. The game supports both a structured Career mode and a fully customizable Sandbox mode, where starting funds, disasters, invasions, and other conditions can all be tuned by the player.
__KMK Implementation:__
The implementation covers staff training, room and campus progression, course leveling, competitions, finances, and sandbox/challenge-specific goals. Objectives are split so the base game and each DLC can be individually included or excluded, and skill/room/course pools are weighted so that shorter DLC lists aren't drowned out by the much larger base game list. Some objective ranges are further split into Standard, Time Consuming, and Difficult bands based on how much of a system's cap they demand. Sandbox goals can additionally be paired with a set of Additional Optional Challenges drawn from the game's own Sandbox customization settings (disasters, invasions, starting funds, income multiplier, temperature, and more)
The Objectives are optimized for play in a Sandbox setting, but all goals should be generic enough to be achieved in any game mode. Challenge mode and Sandbox specific goals and constraints can be deactivated through the configuration. 
The configuration also allows deactivation of DLC content by pack.

#### Objectives
1. Staff Objectives
 - Train a staff member to LEVEL in SKILL (DLC Skills are added if the pack is activated)
 - Hire a specific staff member
2. Level and Prestige (Some level goals are separate and marked as Time Consuming / Difficult)
 - Reach LEVEL Prestige in ROOMTYPE (DLC Rooms are added if the pack is activated)
 - Reach LEVEL Campus Level (any map)
 - Reach LEVEL Campus Level on MAP (DLC Campuses are added if the pack is activated)
 - Level up COURSE to LEVEL (DLC Courses are added, if the pack is activated)
3. Events
 - Win COMPETITION (Space Battle is added, if Space Academy DLC is activated)
 - Catch all intruders during an invasion
4. Finances
 - Have more than AMOUNT money
5. Sandbox Progress (Can be separately enabled in the YAML)
 - Get STARS on MAP with GOAL (DLC campuses are added, if the pack is activated, 3 Stars is considered Time Consuming)
6. Challenges (Can be separately enabled in the YAML)
 - Get a MEDAL Medal in CHALLENGE (Gradeyard Shift is added, if School Spirit DLC is activated)

#### Optional Challenges
The Optional Challenges are currently revolving around playing in Sandbox mode, and are therefore only available if the Sandbox mode is activated in the YAML.
 - Disasters enabled
 - Invaders enabled
 - VIP Visits enabled / disabled
 - Staff Requests enabled / disabled
 - Start with CASH amount
 - Start with KUDOSH amount
 - Start with INCOME Income Multiplier
 - Start with ALLOWANCE monthly allowance
 - Start with Specific Temperature
 - Start with CP Course Points
 - Use a specific Sandbox mode Custom setting (includes all of the settings above)