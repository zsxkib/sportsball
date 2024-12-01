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
- [beautifulsoup](https://www.crummy.com/software/BeautifulSoup/)
- [openpyxl](https://openpyxl.readthedocs.io/en/stable/)
- [feature-engine](https://feature-engine.trainindata.com/en/latest/)
- [catboost](https://catboost.ai/)
- [venn-abers](https://github.com/ip200/venn-abers)
- [joblib](https://joblib.readthedocs.io/en/stable/)
- [optuna](https://optuna.readthedocs.io/en/stable/)
- [pyarrow](https://arrow.apache.org/docs/python/index.html)
- [scikit-learn](https://scikit-learn.org/)
- [skfolio](https://skfolio.org/)
- [fullmonte](https://github.com/8W9aG/fullmonte)
- [ipython](https://ipython.org/)
- [scipy](https://scipy.org/)
- [openskill](https://openskill.me/en/latest/index.html)
- [pytorch](https://pytorch.org/)
- [pandarallel](https://nalepae.github.io/pandarallel/)
- [pyfolio-reloaded](https://github.com/stefan-jansen/pyfolio-reloaded)
- [matplotlib](https://matplotlib.org/)
- [empyrical](https://github.com/quantopian/empyrical)
- [pytz](https://pythonhosted.org/pytz/)
- [python-dotenv](https://github.com/theskumar/python-dotenv)
- [geocoder](https://geocoder.readthedocs.io/)

## Raison D'être :thought_balloon:

`sportsball` aims to be a library for pulling in historical information about previous sporting games in a standardised fashion for easy data processing.
The models it uses are designed to be used for many different types of sports.

The supported leagues are:

* 🏉 [AFL](https://www.afl.com.au/)
* 🏀 [NBA](https://www.nba.com/)
* 🏈 [NCAAF](https://www.ncaa.com/sports/football/fbs)
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
import sportsball as spb

ball = spb.SportsBall()
league = ball.league(spb.League.AFL)
df = league.to_frame()
strategy = ball.create_strategy(league, "test_strategy")
strategy.fit()
portfolio = ball.create_portfolio([strategy], "test_portfolio")
returns = portfolio.fit()
portfolio.render(returns)
```

This results in a dataframe where each game is represented by all its features.

## License :memo:

The project is available under the [MIT License](LICENSE).
