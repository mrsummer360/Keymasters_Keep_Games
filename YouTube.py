from __future__ import annotations

import json
import os
import random
import re
import time
import xml.etree.ElementTree as ET
from typing import Dict, List

import requests
from dataclasses import dataclass

from Options import NamedRange, FreeText, OptionList, OptionSet

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms

DEFAULT_YOUTUBE_KEYWORDS = [
    "Archipelago Multiworld Randomizer",
    "gaming",
    "documentary",
]

YOUTUBE_SEARCH_KEYWORD_POOL = [
    "Archipelago Multiworld Randomizer",
    "multiworld randomizer",
    "speedrun",
    "challenge run",
    "esport",
    "esports",
    "competitive gaming",
    "gaming",
    "history",
    "video essay",
    "documentary",
    "animals",
    "retro gaming",
    "let's play",
    "game review",
    "game theory",
    "speedrun commentary",
    "randomizer run",
    "world news",
    "world news today",
    "cheeses of the world",
    "platformer",
    "RPG",
    "adventure game",
    "strategy game",
    "indie game",
    "simulation game",
    "action game",
    "puzzle game",
    "arcade game",
    "open world",
    "mushroom soup",
    "miniature train set",
    "antique radio restoration",
    "unusual architecture",
    "coffee brewing science",
    "tiny house tour",
    "surreal art process",
    "volcano experiment",
    "weird science",
    "super mario",
    "mario 64",
    "zelda",
    "pokemon",
    "minecraft",
    "factorio",
    "portal",
    "celeste",
    "hollow knight",
    "stardew valley",
    "animal crossing",
    "super metroid",
    "kingdom hearts",
    "final fantasy",
    "no man's sky",
    "rogue legacy",
    "touhou",
    "mario kart",
    "doom",
    "halo",
    "tetris",
    "smash bros",
    "wii sports",
    "metroidvania",
    "roguelike",
]

# Option Dataclass
@dataclass
class YouTubeOptions:
    youtube_api_key: YouTubeAPIKey
    youtube_keyword_mode: YouTubeKeywordMode
    youtube_keywords: YouTubeKeywords
    youtube_keyword_pool_size_per_batch: YouTubeKeywordPoolSizePerBatch
    youtube_number_of_batches: YouTubeNumberOfBatches
    youtube_batch_size: YouTubeBatchSize
    youtube_min_length: YouTubeMinLength
    youtube_max_length: YouTubeMaxLength
    youtube_channel_name: YouTubeChannelName
    youtube_keyword_dictionary_path: YouTubeKeywordDictionaryPath
    youtube_region_code: YouTubeRegionCode
    youtube_language: YouTubeLanguage

# Main Class
class YouTubeGame(Game):

    name = "YouTube"

    platform = KeymastersKeepGamePlatforms.WEB

    is_adult_only_or_unrated = False

    options_cls = YouTubeOptions

    # This is a flag for the current design: YouTube search terms are currently
    # expected for interesting randomized results, since the API does not expose
    # a true random-video endpoint.
    search_terms_required = True

    def resolve_keywords(self) -> List[str]:
        custom_keywords = list(self.keywords or [])
        recommended_keywords = list(YOUTUBE_SEARCH_KEYWORD_POOL)

        selected_sources = list(self.keyword_mode or [])
        if not selected_sources:
            selected_sources = ["Recommended"]

        trending_keywords: List[str] = []
        if "Trending" in selected_sources:
            trending_keywords = get_trending_keywords(
                region=self.region_code,
                language=self.language,
            )

        dictionary_keywords: List[str] = []
        if "Dictionary" in selected_sources:
            dictionary_keywords = get_keyword_dictionary(self.keyword_dictionary_path)

        keyword_sources = {
            "Custom": custom_keywords,
            "Recommended": recommended_keywords,
            "Trending": trending_keywords,
            "Dictionary": dictionary_keywords,
        }

        combined_keywords: List[str] = []
        for source_name in selected_sources:
            if source_name in keyword_sources:
                combined_keywords.extend(keyword_sources[source_name])

        deduped_keywords = list(dict.fromkeys(combined_keywords))
        if deduped_keywords:
            return deduped_keywords

        return recommended_keywords

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        game_objective_templates: List[GameObjectiveTemplate] = list()

        print("[YouTube] Initializing...")
        if self.api_key and (self.number_of_batches == 0 or not hasattr(self, 'video_list')):
            keywords = self.resolve_keywords()
            if not keywords:
                print("[YouTube] Search terms are required for the current random video generator.")
                game_objective_templates = [
                    GameObjectiveTemplate(
                        label="Watch something random on YouTube or add search terms and try again.",
                        data={},
                        is_time_consuming=False,
                        is_difficult=False,
                    ),
                ]
                print("[YouTube] Objectives generated.")
                return game_objective_templates

            print(
                "[YouTube] generating video list... ",
            #   "Keywords:",
            #    keywords,
            #    "; Keyword Pool Size Per Batch:",
            #    self.keyword_pool_size_per_batch,
            #    "; Number of Batches:",
            #    self.number_of_batches,
            #    "; Batch Size:",
            #    self.batch_size,
            #    "; Length Between",
            #    self.min_length,
            #    "and",
            #    self.max_length,
            #    "seconds; Channel:",
            #    self.channel_name,
            #    "; Region:",
            #    self.region_code or "default",
            #    "; Language:",
            #    self.language or "default", 
            )
            holder = YouTubeVideoHolder(
                api_key=self.api_key,
                keywords=keywords,
                keyword_pool_size_per_batch=self.keyword_pool_size_per_batch,
                number_of_batches=self.number_of_batches,
                batch_size=self.batch_size,
                min_length=self.min_length,
                max_length=self.max_length,
                channel_name=self.channel_name,
                region_code=self.region_code,
                language=self.language,
            )
            video_dict = holder.get_videos()
            print("[YouTube] Video list generated, moving on...")
            self.video_list = list(video_dict.values())

        if not self.api_key:
            print("[YouTube] YouTube API key is not set, generating generic objective")
            game_objective_templates = [
                GameObjectiveTemplate(
                    label="Watch something random on YouTube or set API key and try again.",
                    data={},
                    is_time_consuming=False,
                    is_difficult=False,
                ),
            ]
        else:
            print("[YouTube] Generating objectives...")
            game_objective_templates = [
                GameObjectiveTemplate(
                    label="Watch VIDEO",
                    data={
                        "VIDEO": (self.video_list, 1)
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                ),
            ]

        print("[YouTube] Objectives generated.")
        return game_objective_templates

    # Property checks
    @property
    def api_key(self) -> bool:
        return self.archipelago_options.youtube_api_key.value

    @property
    def keyword_mode(self) -> List[str]:
        return list(self.archipelago_options.youtube_keyword_mode.value or [])

    @property
    def keywords(self) -> List[str]:
        return self.archipelago_options.youtube_keywords.value

    @property
    def keyword_pool_size_per_batch(self) -> int:
        return self.archipelago_options.youtube_keyword_pool_size_per_batch.value

    @property
    def number_of_batches(self) -> int:
        return self.archipelago_options.youtube_number_of_batches.value

    @property
    def batch_size(self) -> int:
        return self.archipelago_options.youtube_batch_size.value

    @property
    def min_length(self) -> int:
        return self.archipelago_options.youtube_min_length.value

    @property
    def max_length(self) -> int:
        return self.archipelago_options.youtube_max_length.value

    @property
    def channel_name(self) -> str:
        return self.archipelago_options.youtube_channel_name.value

    @property
    def keyword_dictionary_path(self) -> str:
        return self.archipelago_options.youtube_keyword_dictionary_path.value

    @property
    def region_code(self) -> str:
        return self.archipelago_options.youtube_region_code.value

    @property
    def language(self) -> str:
        return self.archipelago_options.youtube_language.value


class YouTubeAPIKey(FreeText):
    """
    API Key used to access the YouTube Data API.
    You can create one in the Google Cloud Console.
    """
    display_name = "YouTube API Key"
    default = ""


class YouTubeKeywordMode(OptionSet):
    """
    Controls which keyword sources are used to build the video search pool.
    The selected values are combined into one keyword pool.
    Allowed values: Custom, Recommended, Trending, Dictionary
    """
    display_name = "Keyword Mode"
    valid_keys = [
        "Custom",
        "Recommended",
        "Trending",
        "Dictionary",
    ]
    default = frozenset({"Recommended"})


class YouTubeKeywords(OptionList):
    """
    Search terms used to build the random video pool for the Custom setting.
    The selected values are combined into one YouTube search query.
    Leave empty to use a default set of keywords. 
    Example values: gaming, speedrun, documentary, cats
    """
    display_name = "Keywords"
    default = DEFAULT_YOUTUBE_KEYWORDS


class YouTubeKeywordPoolSizePerBatch(NamedRange):
    """
    How many keywords are randomly selected for each YouTube batch query.
    """
    display_name = "Keyword Pool Size Per Batch"
    default = 5
    range_start = 1
    range_end = 50


class YouTubeNumberOfBatches(NamedRange):
    """
    How many search batches are issued. A value of 0 means no cache is used and
    a fresh query is made every time with the configured keyword pool size.
    """
    display_name = "Number of Batches"
    default = 3
    range_start = 0
    range_end = 20


class YouTubeBatchSize(NamedRange):
    """
    How many matching video results are retained from each batch.
    """
    display_name = "Batch Size"
    default = 10
    range_start = 1
    range_end = 50


class YouTubeMinLength(NamedRange):
    """
    The minimum allowed video duration in seconds.
    """
    display_name = "Minimum Length (seconds)"
    default = 30
    range_start = 1
    range_end = 36000


class YouTubeMaxLength(NamedRange):
    """
    The maximum allowed video duration in seconds.
    """
    display_name = "Maximum Length (seconds)"
    default = 600
    range_start = 1
    range_end = 360000


class YouTubeChannelName(FreeText):
    """
    Optional channel filter. When set, it is used as an extra query hint.
    """
    display_name = "Channel Name"
    default = ""


class YouTubeKeywordDictionaryPath(FreeText):
    """
    Optional absolute file path to a keyword dictionary.
    The file must contain one keyword per line.
    Example dictionary powered by 1000words.com is provided on GitHub
    """
    display_name = "YouTube Keyword Dictionary Path"
    default = ""


class YouTubeRegionCode(FreeText):
    """
    Optional region code for Google Trends and YouTube search requests.
    Accepts a single value or a comma-separated list of region codes.
    Examples: US, GB, DE, IN, BR.
    """
    display_name = "YouTube Region Code"
    default = ""


class YouTubeLanguage(FreeText):
    """
    Optional language preference for Google Trends and YouTube search requests.
    Accepts a single value or a comma-separated list of language codes.
    Examples: en, en-US, fr, es, de.
    """
    display_name = "YouTube Language"
    default = ""


def get_keyword_dictionary(keyword_file_path: str) -> List[str]:
    if not keyword_file_path:
        return []

    dictionary_path = keyword_file_path.strip()
    if not os.path.isabs(dictionary_path):
        print("[YouTube] Keyword dictionary path must be an absolute file path.")
        return []

    if not os.path.exists(dictionary_path):
        print(f"[YouTube] Keyword dictionary file not found: {dictionary_path}")
        return []

    try:
        with open(dictionary_path, "r", encoding="utf-8") as handle:
            keywords = [
                line.strip()
                for line in handle
                if line.strip()
            ]
        if keywords:
            print(f"[YouTube] Loaded {len(keywords)} keywords from dictionary file: {dictionary_path}")
        return keywords
    except OSError as exc:
        print(f"[YouTube] Failed to read keyword dictionary file {dictionary_path}: {exc}")
        return []


def _split_multi_value(value: str) -> List[str]:
    if not value:
        return []
    parts = re.split(r"[,;|\n]+", value)
    return [part.strip() for part in parts if part and part.strip()]


def _iter_preference_pairs(region: str = "", language: str = "") -> List[tuple[str, str]]:
    region_values = _split_multi_value(region)
    language_values = _split_multi_value(language)

    if not region_values and not language_values:
        return [("", "")]

    pairs: List[tuple[str, str]] = []
    if not region_values:
        region_values = [""]
    if not language_values:
        language_values = [""]

    for region_value in region_values:
        normalized_region = region_value.strip().upper() if region_value else ""
        for language_value in language_values:
            pairs.append((normalized_region, language_value.strip()))
    return pairs


def _is_safe_trending_keyword(keyword: str) -> bool:
    banned_terms = {
        "election",
        "vote",
        "campaign",
        "president",
        "government",
        "congress",
        "senate",
        "politics",
        "political",
        "religion",
        "religious",
        "church",
        "prayer",
        "islam",
        "christian",
        "judaism",
        "hinduism",
        "buddhism",
        "allah",
        "jesus",
        "quran",
        "bible",
    }
    lowered = keyword.lower()
    return not any(term in lowered for term in banned_terms)


def get_trending_keywords(region: str = "", language: str = "") -> List[str]:
    headers = {"User-Agent": "Mozilla/5.0"}
    all_keywords: List[str] = []
    seen_keywords = set()

    for region_code, language_code in _iter_preference_pairs(region, language):
        query_params = {}
        if region_code:
            query_params["geo"] = region_code
        if language_code:
            query_params["hl"] = language_code

        print(
            f"[YouTube] Fetching trending keywords for region={region_code or 'default'} language={language_code or 'default'}..."
        )
        try:
            # NOTE: The Google Trends JSON Daily Trends endpoint is not publicly
            # available yet. Keep the code below as a commented reference until
            # the official endpoint becomes accessible; RSS remains the active
            # standard fallback for now.
            # response = requests.get(
            #     "https://trends.google.com/trends/api/dailytrends",
            #     params=query_params,
            #     timeout=10,
            #     headers=headers,
            # )
            # if response.status_code == 200:
            #     text = response.text
            #     if text.startswith(")]}'"):
            #         text = text[4:]
            #
            #     payload = json.loads(text)
            #     keywords: List[str] = []
            #     for entry in payload:
            #         for trend_day in entry.get("trendingSearchesDays", []):
            #             for trend in trend_day.get("trendingSearches", []):
            #                 if isinstance(trend.get("title"), dict):
            #                     keyword = trend.get("title", {}).get("query")
            #                 else:
            #                     keyword = trend.get("title")
            #                 if keyword and _is_safe_trending_keyword(keyword) and keyword not in seen_keywords:
            #                     keywords.append(keyword)
            #                     seen_keywords.add(keyword)
            #     if keywords:
            #         all_keywords.extend(keywords)
            #         print(f"[YouTube] Trending keywords found: {keywords}")
            #         continue

            rss_params = {}
            if region_code:
                rss_params["geo"] = region_code

            rss_response = requests.get(
                "https://trends.google.com/trending/rss",
                params=rss_params,
                timeout=10,
                headers=headers,
            )
            if rss_response.status_code != 200:
                print("[YouTube] Trending keyword search returned no usable keywords.")
                continue

            root = ET.fromstring(rss_response.content)
            keywords = []
            for item in root.findall(".//item"):
                title = item.findtext("title")
                if title and _is_safe_trending_keyword(title) and title not in seen_keywords:
                    keywords.append(title)
                    seen_keywords.add(title)

            if keywords:
                all_keywords.extend(keywords)
                print(f"[YouTube] Trending keywords found via RSS fallback: {keywords}")
                continue

            print("[YouTube] Trending keyword search returned no usable keywords.")
        except Exception:
            print("[YouTube] Trending keyword search failed and returned no usable keywords.")

    return all_keywords


class YouTubeVideoHolder:
    _video_cache: Dict[tuple, Dict[str, str]] = {}

    def __init__(self, api_key, keywords, keyword_pool_size_per_batch, number_of_batches, batch_size, min_length, max_length, channel_name, region_code=None, language=None):
        self.api_key = api_key
        self.keywords = keywords
        self.keyword_pool_size_per_batch = keyword_pool_size_per_batch
        self.number_of_batches = number_of_batches
        self.batch_size = batch_size
        self.min_length = min_length
        self.max_length = max_length
        self.channel_name = channel_name
        self.region_code = (region_code or "").strip().upper()
        self.language = (language or "").strip()

    def _request_with_retry(self, url: str, params: Dict[str, str], *, timeout: int = 20):
        max_retries = 5
        for attempt in range(max_retries + 1):
            response = requests.get(url, params=params, timeout=timeout)
            if response.status_code != 429:
                return response

            retry_after = response.headers.get("Retry-After") or response.headers.get("retry-after")
            if retry_after:
                try:
                    wait_seconds = max(1, int(float(retry_after)))
                except ValueError:
                    wait_seconds = min(2 ** attempt, 60)
            else:
                wait_seconds = min(2 ** attempt, 60)

            print(
                f"[YouTube] API rate limit hit (429). Waiting {wait_seconds}s before retrying "
                f"request to {url} (attempt {attempt + 1}/{max_retries + 1})."
            )
            time.sleep(wait_seconds)

        raise RuntimeError("[YouTube] YouTube API rate limit persisted after repeated retries.")

    def _parse_duration(self, duration: str) -> int:
        duration = duration or ""
        hours_match = re.search(r"(\d+)H", duration)
        minutes_match = re.search(r"(\d+)M", duration)
        seconds_match = re.search(r"(\d+)S", duration)

        hours = int(hours_match.group(1)) if hours_match else 0
        minutes = int(minutes_match.group(1)) if minutes_match else 0
        seconds = int(seconds_match.group(1)) if seconds_match else 0
        return hours * 3600 + minutes * 60 + seconds

    def _sample_keywords(self) -> List[str]:
        if not self.keywords:
            return []

        sample_count = min(self.keyword_pool_size_per_batch, len(self.keywords))
        return random.sample(self.keywords, sample_count)

    def get_videos(self) -> Dict[str, str]:
        if not self.api_key:
            raise RuntimeError("[YouTube] API key is not set")

        if self.min_length > self.max_length:
            raise RuntimeError(
                "[YouTube] Minimum Length must be less than or equal to Maximum Length. "
                f"Received minimum={self.min_length} and maximum={self.max_length}."
            )

        cache_key = (
            self.api_key,
            tuple(self.keywords),
            self.keyword_pool_size_per_batch,
            self.number_of_batches,
            self.batch_size,
            self.min_length,
            self.max_length,
            self.channel_name,
            self.region_code,
            self.language,
        )

        if self.number_of_batches > 0 and cache_key in YouTubeVideoHolder._video_cache:
            print("[YouTube] Using cached videos from YouTube...")
            return YouTubeVideoHolder._video_cache[cache_key]

        print("[YouTube] Fetching videos from YouTube...")
        filtered_videos: Dict[str, str] = {}
        batch_count = self.number_of_batches if self.number_of_batches > 0 else 1

        preference_pairs = _iter_preference_pairs(self.region_code, self.language)
        max_keyword_pool_retries = max(3, min(10, len(self.keywords) or 1))

        for batch_index in range(batch_count):
            batch_success = False
            for attempt_index in range(max_keyword_pool_retries):
                batch_query_terms = self._sample_keywords()
                if not batch_query_terms:
                    break

                print(
                    f"[YouTube] Batch {batch_index + 1} keyword pool attempt {attempt_index + 1}: {batch_query_terms}"
                )

                if self.channel_name:
                    batch_query_terms.append(self.channel_name)

                batch_found_results = False
                for region_code, language_code in preference_pairs:
                    search_params = {
                        "part": "snippet",
                        "type": "video",
                        "maxResults": min(self.batch_size, 50),
                        "order": "relevance",
                        "safeSearch": "none",
                        "key": self.api_key,
                        "q": " ".join(batch_query_terms).strip(),
                    }
                    if region_code:
                        search_params["regionCode"] = region_code
                    if language_code:
                        search_params["relevanceLanguage"] = language_code

                    print(
                        f"[YouTube] Searching with region={region_code} language={language_code} for query={search_params['q']}"
                    )

                    search_response = self._request_with_retry(
                        "https://www.googleapis.com/youtube/v3/search",
                        params=search_params,
                    )
                    if search_response.status_code != 200:
                        raise RuntimeError(
                            f"[YouTube] YouTube search API returned {search_response.status_code}"
                        )

                    search_data = search_response.json()
                    video_ids = [
                        item["id"]["videoId"]
                        for item in search_data.get("items", [])
                        if item.get("id", {}).get("videoId")
                    ]

                    if not video_ids:
                        continue

                    batch_found_results = True
                    details_response = self._request_with_retry(
                        "https://www.googleapis.com/youtube/v3/videos",
                        params={
                            "part": "snippet,contentDetails",
                            "id": ",".join(video_ids),
                            "key": self.api_key,
                        },
                    )
                    if details_response.status_code != 200:
                        raise RuntimeError(
                            f"[YouTube] YouTube video details API returned {details_response.status_code}"
                        )

                    details_data = details_response.json()
                    batch_results = {}
                    for item in details_data.get("items", []):
                        duration_seconds = self._parse_duration(item.get("contentDetails", {}).get("duration", ""))
                        if self.min_length <= duration_seconds <= self.max_length:
                            video_id = item["id"]
                            if video_id in filtered_videos:
                                continue
                            title = item.get("snippet", {}).get("title", "Untitled Video")
                            batch_results[video_id] = f"{title} | https://www.youtube.com/watch?v={video_id}"

                    for video_id, label in list(batch_results.items())[: self.batch_size]:
                        filtered_videos[video_id] = label

                if batch_found_results:
                    batch_success = True
                    break

            if not batch_success:
                print(
                    f"[YouTube] Batch {batch_index + 1} produced no usable results after retrying with new keyword subsets."
                )

        if not filtered_videos:
            raise RuntimeError(
                "[YouTube] No videos in the search results matched the requested duration range."
            )

        if self.number_of_batches > 0:
            YouTubeVideoHolder._video_cache[cache_key] = filtered_videos
        return filtered_videos
