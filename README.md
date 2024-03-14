# sportsball

<a href="https://pypi.org/project/sportsball/">
    <img alt="PyPi" src="https://img.shields.io/pypi/v/sportsball">
</a>

A library for pulling in and normalising sports stats.

![sportsball](sportsball.png "sportsball")

## Dependencies :globe_with_meridians:

Python 3.11.6:

- [pandas](https://pandas.pydata.org/)
- [requests](https://requests.readthedocs.io/en/latest/)
- [requests-cache](https://requests-cache.readthedocs.io/en/stable/)
- [python-dateutil](https://github.com/dateutil/dateutil)
- [tqdm](https://github.com/tqdm/tqdm)

## Raison D'être :thought_balloon:

`sportsball` aims to be a library for pulling in historical information about previous sporting games in a standardised fashion for easy data processing.
The models it uses are designed to be used for many different types of sports.

The supported leagues are:

* 🏈 [NFL](https://www.nfl.com/)

## Architecture :triangular_ruler:

`sportsball` is an object orientated library. The entities are organised like so:

* **League**: The entry point to accessing data about a league.
    * **Season**: A season within a league.
        * **Game**: A game within a season.
            * **Team**: The team within the game. Note that in games with individual players a team exists as a wrapper.
                * **Player**: A player within the team.
                * **Odds**: The odds for the team to win the game.
                    * **Bookie**: The bookie publishing the odds.
            * **Venue**: The venue the game was played in.
                * **Address**: The address information of a venue.

## Caching

This library uses very aggressive caching due to the large data requirements.
The initial data load will take some time however after that it will cache the old data for up to 1 year.

## Installation :inbox_tray:

This is a python package hosted on pypi, so to install simply run the following command:

`pip install sportsball`

## Usage example :eyes:

To pull a dataframe containing all the information for a particular league, the following example can be used:

```python
import logging
import sportsball as spb

logging.basicConfig(level='DEBUG')
ball = spb.SportsBall()
league = ball.league(spb.League.NFL)
df = league.to_frame()
```

This results in a dataframe where each game is represented by all its features.

## License :memo:

The project is available under the [MIT License](LICENSE).
