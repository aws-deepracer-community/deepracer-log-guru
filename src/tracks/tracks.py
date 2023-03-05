#
# DeepRacer Guru
#
# Version 3.0 onwards
#
# Copyright (c) 2021 dmh23
#

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
from src.tracks.bowtie_track import BowtieTrack
from src.tracks.american_hills_speedway_track import AmericanHillsSpeedwayTrack
from src.tracks.asia_pacific_bay_loop_track import AsiaPacificBayLoopTrack
from src.tracks.european_seaside_circuit_track import EuropeanSeasideCircuitTrack
from src.tracks.po_chun_super_speedway_track import PoChunSuperSpeedwayTrack
from src.tracks.po_chun_speedway_track import PoChunSpeedwayTrack
from src.tracks.lars_loop_track import LarsLoopTrack
from src.tracks.lars_circuit_track import LarsCircuitTrack
from src.tracks.kuei_raceway_track import KueiRacewayTrack
from src.tracks.kuei_super_raceway_track import KueiSuperRacewayTrack
from src.tracks.cosmic_loop_track import CosmicLoopTrack
from src.tracks.cosmic_circuit_track import CosmicCircuitTrack
from src.tracks.baja_turnpike_track import BajaTurnpikeTrack
from src.tracks.baja_highway_track import BajaHighwayTrack
from src.tracks.hot_rod_speedway_track import HotRodSpeedwayTrack
from src.tracks.hot_rod_super_speedway_track import HotRodSuperSpeedwayTrack
from src.tracks.reinvent_2018_wide_track import Reinvent2018WideTrack
from src.tracks.playa_raceway_track import PlayaRacewayTrack
from src.tracks.playa_super_raceway_track import PlayaSuperRacewayTrack
from src.tracks.expedition_super_loop_track import ExpeditionSuperLoopTrack
from src.tracks.expedition_loop_track import ExpeditionLoopTrack
from src.tracks.vivalas_loop_track import VivalasLoooTrack
from src.tracks.vivalas_speedway_track import VivalasSpeedwayTrack
from src.tracks.summit_speedway_track import SummitSpeedwayTrack
from src.tracks.rogue_raceway_track import RogueRacewayTrack
from src.tracks.rogue_circuit_track import RogueCircuitTrack
from src.tracks.ace_speedway_track import AceSpeedwayTrack
from src.tracks.ace_super_speedway_track import AceSuperSpeedwayTrack
from src.tracks.ross_raceway_track import RossRacewayTrack
from src.tracks.ross_super_speedway_track import RossSuperSpeedwayTrack
from src.tracks.oval_track import OvalTrack
from src.tracks.breadcentric_loop_track import BreadCentricLoopTrack
from src.tracks.breadcentric_speedway_track import BreadCentricSpeedwayTrack
from src.tracks.dbro_raceway_track import DBroRacewayTrack
from src.tracks.dbro_super_raceway_track import DBroSuperRacewayTrack
from src.tracks.jochem_turnpike_track import JochemTurnpikeTrack
from src.tracks.jochem_highway_track import JochemHighwayTrack
from src.tracks.roger_super_raceway_track import RogerSuperRacewayTrack
from src.tracks.roger_ring_track import RogerRingTrack
from src.tracks.jennens_family_speedway_track import JennensFamilySpeedwayTrack
from src.tracks.jennens_super_speedway_track import JennensSuperSpeedwayTrack
from src.tracks.reinvent_2022_track import Reinvent2022Track
from src.tracks.hot_rod_super_speedway_cw_track import HotRodSuperSpeedwayClockwiseTrack
from src.tracks.hot_rod_super_speedway_ccw_track import HotRodSuperSpeedwayCounterClockwiseTrack


def get_all_tracks():
    tracks = {}

    for t in [AmericanHillsSpeedwayTrack(), AsiaPacificBayLoopTrack(), EuropeanSeasideCircuitTrack(),
              Reinvent2018Track(), Reinvent2018WideTrack(), ChampionshipCup2019Track(), StratusLoop2020Track(),
              CumuloTurnpikeTrack(), YunSpeedwayTrack(),
              RogerRacewayTrack(), FumiakiLoop2020Track(), SummitRacewayTrack(),
              Sola2020Track(), Baadal2020Track(), Barcelona2020Track(), BowtieTrack(),
              PoChunSuperSpeedwayTrack(), PoChunSpeedwayTrack(), LarsCircuitTrack(), LarsLoopTrack(),
              KueiRacewayTrack(), KueiSuperRacewayTrack(), CosmicLoopTrack(), CosmicCircuitTrack(),
              BajaTurnpikeTrack(), BajaHighwayTrack(), HotRodSpeedwayTrack(), HotRodSuperSpeedwayTrack(),
              PlayaRacewayTrack(), PlayaSuperRacewayTrack(), ExpeditionSuperLoopTrack(), ExpeditionLoopTrack(),
              VivalasLoooTrack(), VivalasSpeedwayTrack(), SummitSpeedwayTrack(), RogueRacewayTrack(),
              RogueCircuitTrack(), AceSpeedwayTrack(), AceSuperSpeedwayTrack(), RossRacewayTrack(),
              RossSuperSpeedwayTrack(), OvalTrack(), BreadCentricLoopTrack(), BreadCentricSpeedwayTrack(),
              DBroRacewayTrack(), DBroSuperRacewayTrack(), JochemTurnpikeTrack(), JochemHighwayTrack(),
              RogerSuperRacewayTrack(), RogerRingTrack(), JennensSuperSpeedwayTrack(), JennensFamilySpeedwayTrack(),
              Reinvent2022Track(), HotRodSuperSpeedwayClockwiseTrack(), HotRodSuperSpeedwayCounterClockwiseTrack()
              ]:
        t.prepare(tracks)

    return tracks
