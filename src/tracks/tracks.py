#
# DeepRacer Guru
#
# Version 3.0 onwards
#
# Copyright (c) 2021 dmh23
#

from src.tracks.aws_summit_raceway_track import AwsSummitRacewayTrack
from src.tracks.reinvent_2018_track import Reinvent2018Track
from src.tracks.sola_speedway_track import SolaSpeedwayTrack
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
from src.tracks.cosmic_circuit_track_cw import CosmicCircuitClockwiseTrack
from src.tracks.baja_turnpike_track import BajaTurnpikeTrack
from src.tracks.baja_highway_track import BajaHighwayTrack
from src.tracks.hot_rod_speedway_track import HotRodSpeedwayTrack
from src.tracks.hot_rod_super_speedway_track import HotRodSuperSpeedwayTrack
from src.tracks.a_to_z_speedway_track import AtoZSpeedwayTrack
from src.tracks.playa_raceway_track import PlayaRacewayTrack
from src.tracks.playa_super_raceway_track import PlayaSuperRacewayTrack
from src.tracks.expedition_super_loop_track import ExpeditionSuperLoopTrack
from src.tracks.expedition_loop_track import ExpeditionLoopTrack
from src.tracks.vivalas_loop_track import VivalasLoooTrack
from src.tracks.vivalas_speedway_track import VivalasSpeedwayTrack
from src.tracks.rl_speedway_track import RLSpeedwayTrack
from src.tracks.rogue_raceway_track import RogueRacewayTrack
from src.tracks.rogue_raceway_cw_track import RogueRacewayClockwiseTrack
from src.tracks.rogue_raceway_ccw_track import RogueRacewayCounterClockwiseTrack
from src.tracks.rogue_circuit_track import RogueCircuitTrack
from src.tracks.ace_speedway_track import AceSpeedwayTrack
from src.tracks.ace_super_speedway_track import AceSuperSpeedwayTrack
from src.tracks.ace_super_speedway_cw_track import AceSuperSpeedwayClockwiseTrack
from src.tracks.ace_super_speedway_ccw_track import AceSuperSpeedwayCounterClockwiseTrack
from src.tracks.ross_raceway_track import RossRacewayTrack
from src.tracks.ross_super_speedway_track import RossSuperSpeedwayTrack
from src.tracks.oval_track import OvalTrack
from src.tracks.breadcentric_loop_track import BreadCentricLoopTrack
from src.tracks.breadcentric_speedway_track import BreadCentricSpeedwayTrack
from src.tracks.dbro_raceway_track import DBroRacewayTrack
from src.tracks.dbro_super_raceway_track import DBroSuperRacewayTrack
from src.tracks.dbro_super_raceway_cw_track import DBroSuperRacewayClockwiseTrack
from src.tracks.dbro_super_raceway_ccw_track import DBroSuperRacewayCounterClockwiseTrack
from src.tracks.jochem_turnpike_track import JochemTurnpikeTrack
from src.tracks.jochem_highway_track import JochemHighwayTrack
from src.tracks.roger_super_raceway_track import RogerSuperRacewayTrack
from src.tracks.roger_super_raceway_cw_track import RogerSuperRacewayClockwiseTrack
from src.tracks.roger_super_raceway_ccw_track import RogerSuperRacewayCounterClockwiseTrack
from src.tracks.roger_ring_track import RogerRingTrack
from src.tracks.jennens_family_speedway_track import JennensFamilySpeedwayTrack
from src.tracks.jennens_super_speedway_track import JennensSuperSpeedwayTrack
from src.tracks.reinvent_2022_track import Reinvent2022Track
from src.tracks.hot_rod_super_speedway_cw_track import HotRodSuperSpeedwayClockwiseTrack
from src.tracks.hot_rod_super_speedway_ccw_track import HotRodSuperSpeedwayCounterClockwiseTrack
from src.tracks.smile_speedway_ccw import SmileSpeedwayCounterClockwiseTrack
from src.tracks.smile_speedway_cw import SmileSpeedwayClockwiseTrack
from src.tracks.po_chun_speedway_cw_track import PoChunSpeedwayClockwiseTrack
from src.tracks.po_chun_speedway_ccw_track import PoChunSpeedwayCounterClockwiseTrack
from src.tracks.lars_circuit_ccw_track import LarsCircuitCounterClockwiseTrack
from src.tracks.lars_circuit_cw_track import LarsCircuitClockwiseTrack
from src.tracks.a_to_z_speedway_cw_track import AtoZSpeedwayClockwiseTrack
from src.tracks.a_to_z_speedway_ccw_track import AtoZSpeedwayCounterClockwiseTrack
from src.tracks.ace_speedway_cw_track import AceSpeedwayClockwiseTrack
from src.tracks.ace_speedway_ccw_track import AceSpeedwayCounterClockwiseTrack
from src.tracks.breadcentric_speedway_ccw_track import BreadCentricSpeedwayCounterClockwiseTrack
from src.tracks.breadcentric_speedway_cw_track import BreadCentricSpeedwayClockwiseTrack


def get_all_tracks():
    tracks = {}

    for t in [AmericanHillsSpeedwayTrack(), AsiaPacificBayLoopTrack(), EuropeanSeasideCircuitTrack(),
              Reinvent2018Track(), AtoZSpeedwayTrack(), AtoZSpeedwayClockwiseTrack(),
              AtoZSpeedwayCounterClockwiseTrack(), ChampionshipCup2019Track(),
              SmileSpeedwayClockwiseTrack(), SmileSpeedwayCounterClockwiseTrack(),
              StratusLoop2020Track(), HotRodSpeedwayTrack(), HotRodSuperSpeedwayTrack(),
              HotRodSuperSpeedwayClockwiseTrack(), HotRodSuperSpeedwayCounterClockwiseTrack(),
              CumuloTurnpikeTrack(), YunSpeedwayTrack(),
              RogerRacewayTrack(), FumiakiLoop2020Track(), AwsSummitRacewayTrack(),
              SolaSpeedwayTrack(), Baadal2020Track(), Barcelona2020Track(), BowtieTrack(),
              PoChunSuperSpeedwayTrack(), PoChunSpeedwayTrack(), LarsCircuitTrack(), LarsLoopTrack(),
              KueiRacewayTrack(), KueiSuperRacewayTrack(), CosmicLoopTrack(),
              CosmicCircuitTrack(), CosmicCircuitClockwiseTrack(), BajaTurnpikeTrack(), BajaHighwayTrack(),
              PlayaRacewayTrack(), PlayaSuperRacewayTrack(), ExpeditionSuperLoopTrack(), ExpeditionLoopTrack(),
              VivalasLoooTrack(), VivalasSpeedwayTrack(), RLSpeedwayTrack(),
              RogueCircuitTrack(), AceSpeedwayTrack(), AceSpeedwayClockwiseTrack(), AceSpeedwayCounterClockwiseTrack(),
              AceSuperSpeedwayTrack(), AceSuperSpeedwayClockwiseTrack(), AceSuperSpeedwayCounterClockwiseTrack(),
              RossRacewayTrack(), DBroSuperRacewayClockwiseTrack(), DBroSuperRacewayCounterClockwiseTrack(),
              RossSuperSpeedwayTrack(), OvalTrack(), BreadCentricLoopTrack(), BreadCentricSpeedwayTrack(),
              BreadCentricSpeedwayClockwiseTrack(), BreadCentricSpeedwayCounterClockwiseTrack(),
              DBroRacewayTrack(), DBroSuperRacewayTrack(), JochemTurnpikeTrack(), JochemHighwayTrack(),
              RogerRingTrack(), JennensSuperSpeedwayTrack(), JennensFamilySpeedwayTrack(),
              Reinvent2022Track(), PoChunSpeedwayClockwiseTrack(), PoChunSpeedwayCounterClockwiseTrack(),
              LarsCircuitClockwiseTrack(), LarsCircuitCounterClockwiseTrack(),
              RogueRacewayTrack(), RogueRacewayClockwiseTrack(), RogueRacewayCounterClockwiseTrack(),
              RogerSuperRacewayTrack(), RogerSuperRacewayClockwiseTrack(), RogerSuperRacewayCounterClockwiseTrack()
              ]:
        t.prepare(tracks)

    return tracks
