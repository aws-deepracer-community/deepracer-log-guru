from src.tracks.summit_raceway_track import SummitRacewayTrack
from src.tracks.reinvent_2018_track import Reinvent2018Track
from src.tracks.sola_2020_track import Sola2020Track
from src.tracks.baadal_2020_track import Baadal2020Track
from src.tracks.barcelona_2020_track import Barcelona2020Track
from src.tracks.champ_cup_2019_track import ChampionshipCup2019Track
from src.tracks.fumiaki_loop_2020_track import FumiakiLoop2020Track
from src.tracks.roger_raceway_track import RogerRacewayTrack
from src.tracks.yun_speedway_track import YunSpeedwayTrack
from src.tracks.cumulo_turnpike_track import CumuloTurnpikeTrack
from src.tracks.stratus_loop_2020_track import StratusLoop2020Track



def get_all_tracks():
    tracks = {}

    for t in [ Reinvent2018Track(), ChampionshipCup2019Track(), StratusLoop2020Track(),
               CumuloTurnpikeTrack(), YunSpeedwayTrack(),
               RogerRacewayTrack(), FumiakiLoop2020Track(), SummitRacewayTrack(),
               Sola2020Track(), Baadal2020Track(), Barcelona2020Track() ]:
        t.prepare()
        tracks[t.world_name] = t

    return tracks

