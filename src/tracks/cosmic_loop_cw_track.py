#
# DeepRacer Guru
#
# Version 3.0 onwards
#
# Copyright (c) 2021 dmh23
#

from src.tracks.track import Track
import src.personalize.configuration.personal_track_annotations as config


class CosmicLoopClockwiseTrack(Track):
    def __init__(self):
        super().__init__()

        self._ui_name = "Cosmic Loop (Clockwise)"
        self._ui_description = "Cosmic Loop is a short track (46.18m) that features a single sprint straightaway and a challenging technical section with multiple 90 degree turns and and two hairpins. A successful run will require skillful command of time (steps) and (action) space."
        self._ui_length_in_m = 46.18  # metres
        self._ui_width_in_cm = 107  # centimetres   # TODO
        self._world_name = "jyllandsringen_open_cw"
        self._track_sector_dividers = [53, 82, 118]
        self._annotations = config.cosmic_loop_cw_annotations
        self._track_width = 1.066

        self._track_waypoints = [(2.0657709884643554, -3.9498729705810547), (1.9357709884643555, -3.9498729705810547),
                                 (1.805770988464353, -3.9498729705810547), (1.6342589855194092, -3.9498729705810547),
                                 (1.332746982574463, -3.9498729705810547), (1.0312345027923566, -3.9498729705810547),
                                 (0.729722350835802, -3.9498729705810547), (0.4282101541757566, -3.9498724937438965),
                                 (0.1266980022191979, -3.9498724937438965), (-0.17481420189142227, -3.9498729705810547),
                                 (-0.4763264060020429, -3.9498740434646606), (-0.7778385579586029, -3.9498759508132935),
                                 (-1.0793509483337402, -3.949877381324768), (-1.3808630108833313, -3.9498759508132935),
                                 (-1.6823749542236328, -3.9498705863952637), (-1.983887493610382, -3.949861526489258),
                                 (-2.2853994369506836, -3.9498519897460938), (-2.5869115591049194, -3.949862480163574),
                                 (-2.888423442840576, -3.949895977973938), (-3.18993604183197, -3.949951171875),
                                 (-3.4914485216140747, -3.949932098388672), (-3.792960524559021, -3.949761986732483),
                                 (-4.094473123550415, -3.94962215423584), (-4.395984411239624, -3.950270891189575),
                                 (-4.697269916534424, -3.9403334856033325), (-4.995997190475464, -3.9002315998077393),
                                 (-5.288575649261474, -3.827882409095764), (-5.571247100830078, -3.7233424186706543),
                                 (-5.84053134918213, -3.587991476058959), (-6.093607902526856, -3.4242990016937247),
                                 (-6.328837633132935, -3.2358360290527344), (-6.545417070388794, -3.026189923286438),
                                 (-6.743067026138306, -2.798588514328003), (-6.921900033950806, -2.5559134483337402),
                                 (-7.082149505615234, -2.3005789518356323), (-7.223817825317383, -2.0344755053520203),
                                 (-7.347121000289917, -1.7593824863433838), (-7.451476097106934, -1.4765569567680363),
                                 (-7.53636908531189, -1.1872949600219727), (-7.600237131118774, -0.8927040994167328),
                                 (-7.63802433013916, -0.593673050403595), (-7.64171576499939, -0.29239899665117264),
                                 (-7.589874744415283, 0.0038803964853286743), (-7.532837390899658, 0.2994953468441963),
                                 (-7.53211522102356, 0.600574404001236), (-7.577288866043091, 0.8985081613063812),
                                 (-7.638094663619995, 1.19381445646286), (-7.663690567016602, 1.4935710430145264),
                                 (-7.5895867347717285, 1.7836995720863342), (-7.41456937789917, 2.0278015732765198),
                                 (-7.20467209815979, 2.2442524433135986), (-6.990350961685181, 2.4563241004943848),
                                 (-6.771106481552124, 2.663299083709717), (-6.54634952545166, 2.864269495010376),
                                 (-6.315372467041016, 3.0580559968948364), (-6.07731294631958, 3.243062973022461),
                                 (-5.831128120422363, 3.4170950651168823), (-5.575864553451538, 3.57749605178833),
                                 (-5.310406446456909, 3.7203385829925537), (-5.033526182174683, 3.83941113948822),
                                 (-4.744671821594238, 3.9250824451446533), (-4.446020603179932, 3.9632744789123535),
                                 (-4.147039175033569, 3.9323296546936035), (-3.875293493270874, 3.8060801029205322),
                                 (-3.7045198678970337, 3.5643515586853027), (-3.6579984426498413, 3.267261028289795),
                                 (-3.664011001586914, 2.9659860134124756), (-3.698385000228882, 2.66650652885437),
                                 (-3.7514395713806152, 2.3697350025177), (-3.820055842399597, 2.0761664509773254),
                                 (-3.902363896369934, 1.786134958267212), (-4.001382112503052, 1.5013940334320068),
                                 (-4.111952066421509, 1.2208974957466125), (-4.1918785572052, 0.9304228723049164),
                                 (-4.215919613838196, 0.6304240524768829), (-4.158581614494324, 0.33555375039577484),
                                 (-4.0074074268341064, 0.07624335587024689), (-3.783052444458008, -0.12391561269760132),
                                 (-3.518569588661194, -0.2678430452942848), (-3.2346209287643433, -0.3686901330947876),
                                 (-2.941232442855835, -0.43779056519269943), (-2.64319908618927, -0.4831073395907879),
                                 (-2.3429185152053833, -0.5099777057766914), (-2.0416669845581055, -0.5219571115449071),
                                 (-1.7401710152626038, -0.5214773002080619), (-1.4388709664344788, -0.510493797250092),
                                 (-1.1379565000534058, -0.491584662348032), (-0.8399493396282196, -0.4555088598281145),
                                 (-0.5847757384181023, -0.2994813770055771),
                                 (-0.42420710250735283, -0.04712459444999695),
                                 (-0.3827516958117485, 0.2502535507082939), (-0.3656531050801277, 0.5512774288654327),
                                 (-0.34443483501672745, 0.8520409166812897), (-0.319631852209568, 1.1525269746780396),
                                 (-0.2898005396127701, 1.4525570273399353), (-0.2550387680530548, 1.7520555257797241),
                                 (-0.19711154699325562, 2.0474640130996704), (-0.06505225598812103, 2.316981077194214),
                                 (0.16741552390158176, 2.5037354230880737), (0.46180105209350586, 2.5578805208206177),
                                 (0.7594241499900818, 2.5142800211906433), (1.0439418256282806, 2.415271520614624),
                                 (1.314161479473114, 2.2818239331245422), (1.56997948884964, 2.1224344968795776),
                                 (1.8062774538993807, 1.9355470538139365), (2.0328494906425476, 1.7366464734077454),
                                 (2.24965900182724, 1.5271530151367188), (2.4549754858016968, 1.3064051270484924),
                                 (2.648969531059265, 1.075618863105774), (2.8367810249328613, 0.8397464603185654),
                                 (3.0341739654540993, 0.6120025888085392), (3.270347476005554, 0.42607799638062716),
                                 (3.5376545190811157, 0.2960719019174576), (3.835137486457821, 0.24790149927139338),
                                 (4.132393360137942, 0.2006543576717375), (4.433423042297363, 0.18359950184822083),
                                 (4.734144449234005, 0.16180901229381586), (5.034510850906372, 0.1355804055929184),
                                 (5.334433317184452, 0.10469438135623893), (5.63374400138855, 0.06836314499378204),
                                 (5.932160139083862, 0.02531611919403076), (6.229271650314333, -0.025947690010071252),
                                 (6.524434089660647, -0.08740416169166645), (6.816042184829712, -0.16383711993694305),
                                 (7.098291873931885, -0.26907750219106674), (7.36332106590271, -0.4117639921605587),
                                 (7.566271543502808, -0.6312690824270248), (7.646334409713745, -0.9199740588665009),
                                 (7.652164697647095, -1.221239984035492), (7.659568548202515, -1.5226605534553528),
                                 (7.664599895477295, -1.8241299986839294), (7.666955232620239, -2.1256314516067505),
                                 (7.666102409362793, -2.4271414279937744), (7.662091016769409, -2.72862446308136),
                                 (7.653779029846191, -3.030019521713257), (7.629644393920898, -3.330287456512451),
                                 (7.535741329193115, -3.6154900789260864), (7.338901996612549, -3.8399914503097534),
                                 (7.060518980026245, -3.949346899986267), (6.759964942932129, -3.949944019317627),
                                 (6.458454132080078, -3.9498729705810547), (6.156941890716553, -3.9498729705810547),
                                 (5.855429172515869, -3.9498729705810547), (5.553916931152344, -3.9498729705810547),
                                 (5.252405166625977, -3.9498729705810547), (4.950892925262451, -3.9498729705810547),
                                 (4.649381160736084, -3.9498729705810547), (4.347867965698242, -3.9498729705810547),
                                 (4.046356201171875, -3.9498729705810547), (3.7448439598083496, -3.9498729705810547),
                                 (3.4433319568634033, -3.9498729705810547), (3.141819953918457, -3.9498729705810547),
                                 (2.8403079509735107, -3.9498729705810547), (2.538794994354248, -3.9498729705810547),
                                 (2.2372829914093018, -3.9498729705810547), (2.0657709884643554, -3.9498729705810547)]
