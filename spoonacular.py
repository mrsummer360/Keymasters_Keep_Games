from __future__ import annotations

import functools
from typing import List, Dict

import requests
from dataclasses import dataclass

from Options import Option, NamedRange, FreeText, OptionList, Toggle

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms

# Option Dataclass
@dataclass
class SpoonacularOptions:
    spoonacular_api_key: SpoonacularAPIKey
    spoonacular_include_tags: SpoonacularIncludeTags
    spoonacular_exclude_tags: SpoonacularExcludeTags
    spoonacular_recipe_count: SpoonacularRecipeCount
    spoonacular_ignore_cache: SpoonacularIgnoreCache

# Main Class
class SpoonacularGame(Game):

    name = "Spoonacular"

    platform = KeymastersKeepGamePlatforms.META

    is_adult_only_or_unrated = False
    
    options_cls = SpoonacularOptions
    
    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        game_objective_templates: List[GameObjectiveTemplate] = list()

        print("[Spoonacular] Initializing...")
        if self.api_key and not hasattr(self, 'recipe_list'):
            print("[Spoonacular] generating recipe list... Include tags:", self.include_tags, "Exclude tags:", self.exclude_tags, "Recipe count:", self.recipe_count)
            holder = SpoonacularRecipeHolder(
                api_key=self.api_key,
                include_tags=self.include_tags,
                exclude_tags=self.exclude_tags,
                recipe_count=self.recipe_count,
                ignore_cache=self.ignore_cache
            )
            recipes_dict = holder.get_recipes()
            print("[Spoonacular] recipe list generated, moving on...")
            self.recipe_list = list(recipes_dict.values())
        
        if not self.api_key:
            print("[Spoonacular] Spoonacular API key is not set, generating generic objective")
            game_objective_templates = [
                GameObjectiveTemplate(
                    label="Cook Anything or set API key and try again.",
                    data={
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                ),
            ]
        else:        
            print("[Spoonacular] Generating objectives...")
            game_objective_templates = [
                GameObjectiveTemplate(
                    label="Cook RECIPE",
                    data={
                        "RECIPE": (self.recipe_list, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                ),
            ]
        
        print("[Spoonacular] Objectives generated.")
        return game_objective_templates

    # Property checks
    @property
    def api_key(self) -> bool:
        return self.archipelago_options.spoonacular_api_key.value
    @property
    def include_tags(self) -> List[str]:
        return self.archipelago_options.spoonacular_include_tags.value
    @property
    def exclude_tags(self) -> List[str]:
        return self.archipelago_options.spoonacular_exclude_tags.value
    @property
    def recipe_count(self) -> int:
        return self.archipelago_options.spoonacular_recipe_count.value
    @property
    def ignore_cache(self) -> bool:
        return self.archipelago_options.spoonacular_ignore_cache.value


class SpoonacularAPIKey(FreeText):
    """
        API Key used to access the Spoonacular API. You can get one for free at https://spoonacular.com/food-api
        Calls cost credits, the free plan has 50 credits per day, which should be enough for most users. 
    """
    display_name = "Spoonacular API Key"
    default = ""

class SpoonacularIncludeTags(OptionList):
    """
        Tags that have to be included in the recipe. 
        Examples: vegan, vegetarian, gluten free, ...
    """
    display_name = "Include Tags"
    default = []

class SpoonacularExcludeTags(OptionList):
    """
        Tags to exclude from the recipe search.
        Examples: dairy
    """
    display_name = "Exclude Tags"
    default = []

class SpoonacularRecipeCount(NamedRange):
    """
        The number of recipes to fetch from the API. 
        Recipes are randomly selected from the results. 
        Note: Higher recipe count results in higher API credit usage.
    """
    display_name = "Recipe Count"
    default = 50
    range_start = 1
    range_end = 500

class SpoonacularIgnoreCache(Toggle):
    """
        If enabled, the game will ignore the cached recipes and fetch new ones from the API every time. 
        This can be useful if you want to get new recipes without changing the other parameters, but it will result in higher API credit usage.
    """
    display_name = "Ignore Cache"
    default = False

class SpoonacularRecipeHolder:
    _recipe_cache: Dict[tuple, Dict[int, str]] = {}
    
    def __init__(self, api_key, include_tags, exclude_tags, recipe_count, ignore_cache):
        self.api_key = api_key
        self.include_tags = include_tags
        self.exclude_tags = exclude_tags
        self.recipe_count = recipe_count
        self.ignore_cache = ignore_cache

    def get_recipes(self) -> Dict[int, str]:
        if not self.api_key:
            raise RuntimeError("[Spoonacular] API key is not set")
        
        # Create cache key from parameters
        cache_key = (
            self.api_key,
            tuple(self.include_tags),
            tuple(self.exclude_tags),
            self.recipe_count
        )
        
        # Check if already cached
        if self.ignore_cache == False and cache_key in SpoonacularRecipeHolder._recipe_cache:
            print("[Spoonacular] Using cached recipes from Spoonacular...")
            return SpoonacularRecipeHolder._recipe_cache[cache_key]
        
        print("[Spoonacular] Fetching recipes from Spoonacular...")
        spoonacular_response = requests.get("https://api.spoonacular.com/recipes/random",
                                      params={
                                        "apiKey": self.api_key,
                                        "includeNutrition": False,
                                        "include-tags": self.include_tags,
                                        "exclude-tags": self.exclude_tags,
                                        "number": self.recipe_count
                                      })
        if spoonacular_response.status_code != 200:
            raise RuntimeError(f"[Spoonacular] Spoonacular API returned {spoonacular_response.status_code}")
        recipe_data = spoonacular_response.json()
        print(f"[Spoonacular] Received {len(recipe_data['recipes'])} recipes from Spoonacular.")
        recipes_dict = {
            recipe["id"]: f"{recipe['title']} | {recipe['sourceUrl']}"
            for recipe in recipe_data["recipes"]
        }
        
        # Cache the result
        SpoonacularRecipeHolder._recipe_cache[cache_key] = recipes_dict
        return recipes_dict
