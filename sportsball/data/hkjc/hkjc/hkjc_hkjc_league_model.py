"""The HKJC league model."""

# pylint: disable=line-too-long
import datetime
from typing import Iterator
import logging
import urllib.parse
from urllib.parse import urlparse
import io

import requests_cache
import tqdm
from bs4 import BeautifulSoup
import pandas as pd

from ...game_model import GameModel
from ...league import League
from ...league_model import LeagueModel
from .hkjc_hkjc_game_model import create_hkjc_hkjc_game_model, POST_TIME_KEY, RACE_RESULTS_KEY, RACE_TIME_KEY, DISTANCE_KEY, RACE_NUMBER_KEY, COUNTRY_KEY, RACE_TRACK_KEY, DESCRIPTION_KEY, RACE_COURSE_KEY, RUNNERS_KEY
from .hkjc_hkjc_team_model import SIRE_KEY

_HKJC_GRAPHQL_BASE_URL = "https://info.cld.hkjc.com/graphql/base/"
_SHA_TIN_VENUE_CODE = "ST"
_HAPPY_VALLEY_VENUE_CODE = "HV"


class HKJCHKJCLeagueModel(LeagueModel):
    """HKJC HKJC implementation of the league model."""

    def __init__(
        self, session: requests_cache.CachedSession, position: int | None = None
    ) -> None:
        super().__init__(League.HKJC, session, position=position)

    @classmethod
    def name(cls) -> str:
        return "hkjc-league-model"

    @property
    def games(self) -> Iterator[GameModel]:  # type: ignore
        def games_for_date(dt: datetime.date) -> Iterator[GameModel]:
            dt_str = dt.strftime("%Y-%m-%d")

            def games_for_venue(venue_code: str) -> Iterator[GameModel]:
                nonlocal dt_str
                response = self.session.post(
                    _HKJC_GRAPHQL_BASE_URL,
                    json={
                        "variables": {
                            "date": dt_str,
                            "venueCode": venue_code,
                        },
                        "query": "\n    query RaceResultsProfile($date: String, $venueCode: String) {\n      videoReplay(date: $date, venueCode: $venueCode) {\n        hkRaceDate\n        raceNo\n        overseasRaceIndicator\n        videoPresentOrNot\n        isVideoReplayOn\n        language\n      }\n      raceMeetingProfile(date: $date, venueCode: $venueCode) {\n        totalNumberOfRace\n        currentNumberOfRace\n        races {\n          id\n          no\n          status\n          runners {\n            horse {\n              id\n              name_en\n              name_ch\n            }\n            color\n            id\n            no\n            handicapWeight\n            jockey {\n              code\n              name_en\n              name_ch\n            }\n            trainer {\n              code\n              name_en\n              name_ch\n            }\n            last6run\n            internationalRating\n            sire\n            sexNm {\n              chinese\n              english\n            }\n            age\n            barrierDrawNumber\n            gearInfo\n            margin\n            marginNm {\n              chinese\n              english\n            }\n            lbwNm {\n              chinese\n              english\n            }\n            winOdds\n            finalPosition\n            deadHeat\n            status\n          }\n          judgeSigns {\n            value_en\n          }\n          raceName_en\n          raceName_ch\n          postTime\n          country_en\n          country_ch\n          distance\n          go_en\n          go_ch\n          raceTrack {\n            description_en\n            description_ch\n          }\n          raceCourse {\n            description_en\n            description_ch\n            displayCode\n          }\n          raceClass_en\n          raceClass_ch\n          raceResults {\n            status\n            raceTime\n            mgnInd\n          }\n        }\n        date\n        venueCode\n        pmPools {\n          leg {\n            number\n            races\n          }\n          status\n          comingleStatus\n          oddsType\n          name_en\n          name_ch\n          lastUpdateTime\n          dividends(officialOnly: true) {\n            winComb\n            type\n            div\n            seq\n            status\n            guarantee\n            partial\n            partialUnit\n          }\n        }\n        status\n      }\n    }\n    ",
                    },
                )
                response.raise_for_status()
                data = response.json()
                for race_meeting_profile in data["data"]["raceMeetingProfile"]:
                    for race in race_meeting_profile["races"]:
                        if race["status"] == "ABANDONED":
                            continue
                        yield create_hkjc_hkjc_game_model(
                            self.session, race, self.league, venue_code=venue_code
                        )
            
            def games_from_html(html: str, venue_code: str, url: str) -> Iterator[GameModel]:
                o = urlparse(url)
                query = urllib.parse.parse_qs(o.query)
                handle = io.StringIO()
                handle.write(html)
                handle.seek(0)
                dfs = pd.read_html(handle)
                race = {
                    POST_TIME_KEY: dt.isoformat(),
                    RACE_RESULTS_KEY: [{
                        RACE_TIME_KEY: ""
                    }],
                    RACE_NUMBER_KEY: int(query["RaceNo"][0]),
                    COUNTRY_KEY: "China",
                    RACE_COURSE_KEY: {
                        DESCRIPTION_KEY: "Sha Tin" if venue_code == _SHA_TIN_VENUE_CODE else "Happy Valley"
                    },
                    RACE_TRACK_KEY: {},
                    RUNNERS_KEY: []
                }
                for count, df in enumerate(dfs):
                    print(df)
                    if "Finish Time" in df.columns.values.tolist():
                        race[RACE_RESULTS_KEY] = [{RACE_TIME_KEY: df["Finish Time"].tolist()[0]}]
                    if count == 1:
                        race[DISTANCE_KEY] = int(df.iat[1, 0].split("-")[-1].replace("M", "").strip())
                        race[RACE_TRACK_KEY][DESCRIPTION_KEY] = df.iat[2, 2].split()[0].strip()
                
                yield create_hkjc_hkjc_game_model(self.session, race, self.league, venue_code=venue_code)

            response = self.session.post(
                _HKJC_GRAPHQL_BASE_URL,
                json={
                    "variables": {"date": dt_str, "oddsTypes": ["WIN", "PLA", "QIN", "QPL", "FCT", "TCE", "TRI", "FF", "QTT"]},
                    "query": "\nquery MeetingStatus($date: String, $venueCode: String, $oddsTypes: [OddsType]) {\n  raceMeetingProfile(date: $date, venueCode: $venueCode) {\n    totalNumberOfRace\n    currentNumberOfRace\n    date\n    venueCode\n    status\n    races {\n      no\n      postTime\n      status\n      raceResults {\n        status\n      }\n    }\n    pmPools(oddsTypes: $oddsTypes) {\n      oddsType\n      status\n      leg {\n        races\n      }\n    }\n  }\n}\n",
                },
            )
            response.raise_for_status()
            data = response.json()
            for race_meeting_profile in data["data"]["raceMeetingProfile"]:
                yield from games_for_venue(race_meeting_profile["venueCode"])
            
            dt_str = dt.strftime("%Y/%m/%d")
            for course in [_SHA_TIN_VENUE_CODE, _HAPPY_VALLEY_VENUE_CODE]:
                response = self.session.get(f"https://racing.hkjc.com/racing/information/English/Racing/LocalResults.aspx?RaceDate={dt_str}&Racecourse={course}&RaceNo=1")
                response.raise_for_status()
                yield from games_from_html(response.text, course, response.url)
                soup = BeautifulSoup(response.text, "lxml")
                seen_urls = {response.url}
                for a in soup.find_all("a", href=True):
                    url = urllib.parse.urljoin(response.url, a.get("href"))
                    if url in seen_urls:
                        continue
                    o = urlparse(url)
                    if not o.path.endswith("/LocalResults.aspx"):
                        continue
                    query = urllib.parse.parse_qs(o.query)
                    if "RaceNo" not in query:
                        continue
                    response = self.session.get(url)
                    response.raise_for_status()
                    yield from games_from_html(response.text, course, response.url)


        today_date = datetime.datetime.today().date()
        last_scraped_date: datetime.date | None = None
        current_date = today_date
        
        with tqdm.tqdm(position=self.position) as pbar:
            while (
                last_scraped_date is None or (last_scraped_date - current_date).days < 360
            ):
                if current_date == today_date:
                    with self.session.cache_disabled():
                        for game_model in games_for_date(current_date):
                            last_scraped_date = current_date
                            pbar.update(1)
                            yield game_model
                else:
                    for game_model in games_for_date(current_date):
                        last_scraped_date = current_date
                        pbar.update(1)
                        yield game_model
                pbar.set_description(
                    f"HKJC {current_date}"
                )
                current_date -= datetime.timedelta(days=1)
