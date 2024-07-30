#
# DeepRacer Guru
#
# Version 3.0 onwards
#
# Copyright (c) 2021 dmh23
#

from src.tracks.track import Track
import src.personalize.configuration.personal_track_annotations as config


class RossRacewayTrack(Track):
    def __init__(self):
        super().__init__()

        self._ui_name = "Ross Raceway (Original)"
        self._ui_description = "The Ross Raceway was named in honor of the 2021 AWS DeepRacer 3rd place Champion, Ross Williams. Expect to see racers put the pedal to the metal on the 3x dragstrips featured on the Ross Raceway, but there will be no shortage of off tracks as they navigate the various sweeping turns."
        self._ui_length_in_m = 99.99  # metres  NOT SPECIFIED
        self._ui_width_in_cm = 107  # centimetres   NOT SPECIFIED
        self._world_name = "2022_may_open"
        self._track_sector_dividers = [27, 58, 86, 110, 128]
        self._annotations = config.ross_raceway_annotations
        self._track_width = 1.066

        self._track_waypoints = [(5.05151104927063, 0.8635410368442535), (5.051487922668457, 1.1652929782867432),
                                 (5.051440954208374, 1.4670439958572388), (5.051444053649902, 1.7687965035438538),
                                 (5.051599025726318, 2.070554494857788), (5.051395893096924, 2.3723000288009644),
                                 (5.0503363609313965, 2.674015998840332), (5.0518200397491455, 2.9758189916610718),
                                 (5.058016538619995, 3.2777814865112305), (5.047324895858765, 3.57916259765625),
                                 (4.988653659820557, 3.8742620944976807), (4.8676605224609375, 4.150005459785461),
                                 (4.696577072143555, 4.397716522216797), (4.487322092056274, 4.614569664001465),
                                 (4.249698996543884, 4.799951076507568), (3.9902760982513428, 4.953553915023804),
                                 (3.7165430784225464, 5.0800065994262695), (3.431645393371582, 5.178957462310791),
                                 (3.1383464336395264, 5.249284982681274), (2.8402515649795532, 5.294960975646973),
                                 (2.539469003677368, 5.316683053970337), (2.237810969352722, 5.322011947631836),
                                 (1.9360340237617493, 5.320683479309082), (1.6342874765396118, 5.321023941040039),
                                 (1.3325344920158386, 5.321022033691406), (1.0307824611663818, 5.3210790157318115),
                                 (0.7290307283401489, 5.321120977401733), (0.42727886140346527, 5.321163177490234),
                                 (0.12552685290575027, 5.3212080001831055), (-0.17622459679841995, 5.32124400138855),
                                 (-0.4779783934354782, 5.321331024169922), (-0.779723197221756, 5.321250915527344),
                                 (-1.081496000289917, 5.321721076965332), (-1.3832324743270874, 5.321502923965454),
                                 (-1.3832324743270874, 5.321502923965454), (-1.6822450160980225, 5.283059597015381),
                                 (-1.9764400720596313, 5.216461658477783), (-2.2615424394607544, 5.117757558822632),
                                 (-2.5388784408569336, 4.999503135681152), (-2.8076934814453125, 4.862544059753418),
                                 (-3.0641084909439087, 4.703683137893677), (-3.3063565492630005, 4.523935556411743),
                                 (-3.5315524339675903, 4.323431968688965), (-3.7344250679016113, 4.100539445877075),
                                 (-3.908614158630371, 3.8546475172042842), (-4.042842864990234, 3.584898591041565),
                                 (-4.123146057128906, 3.294624447822571), (-4.147691011428833, 2.9941509962081905),
                                 (-4.130027890205383, 2.693168520927429), (-4.074256062507629, 2.3972585201263428),
                                 (-3.9614880084991455, 2.1181549429893494), (-3.785645008087158, 1.8740904927253723),
                                 (-3.557160496711731, 1.6781390309333801), (-3.2926095724105835, 1.5338324904441833),
                                 (-3.0095235109329215, 1.429819196462631), (-2.716428518295288, 1.3582335710525513),
                                 (-2.4179689884185804, 1.3136492371559145), (-2.1181920766830444, 1.2827846705913544),
                                 (-1.8168085217475891, 1.2680464386940002), (-1.5154070258140564, 1.2534971833229065),
                                 (-1.2140135169029236, 1.2386945486068726), (-0.9123319983482361, 1.2360387444496155),
                                 (-0.6105800867080688, 1.2362182140350342), (-0.30883659422397614, 1.2362462878227234),
                                 (-0.007869549095630646, 1.2188115417957306), (0.28562935441732407, 1.150725781917572),
                                 (0.5636615604162216, 1.0352135300636292), (0.8147738724946976, 0.8687145709991455),
                                 (1.0285892188549042, 0.6565247029066086), (1.2009552717208862, 0.40962475538253784),
                                 (1.3303884863853455, 0.13762212358415127), (1.4167506694793701, -0.1511495988816023),
                                 (1.4517148435115814, -0.45026665925979614), (1.39376962184906, -0.746226966381073),
                                 (1.2917408049106602, -1.029869973659514), (1.1444857716560364, -1.292592853307724),
                                 (0.9522843956947327, -1.5242300033569336), (0.718870654702185, -1.7142369747161874),
                                 (0.45231299102306194, -1.8546310067176823), (0.16254803910851479, -1.9371169805526733),
                                 (-0.1365537978708744, -1.9741739630699158),
                                 (-0.43844684958457947, -1.9732614755630493), (-0.7401604056358317, -1.975717008113861),
                                 (-1.0419135093688965, -1.9774324893951416), (-1.3436585068702716, -1.9792969822883606),
                                 (-1.6454049944877625, -1.9811339974403381), (-1.947151482105254, -1.9829760193824768),
                                 (-2.2488975524902344, -1.9848149418830872), (-2.5506434440612793, -1.98666650056839),
                                 (-2.8523919582366943, -1.988437533378601), (-3.1541240215301514, -1.9907370209693909),
                                 (-3.455960988998413, -1.9897119998931885), (-3.75676691532135, -2.0094494819641113),
                                 (-4.045078873634338, -2.095644533634186), (-4.307120442390442, -2.243748426437378),
                                 (-4.5325188636779785, -2.443784475326538), (-4.718019485473633, -2.681376576423645),
                                 (-4.864444017410278, -2.9447399377822876), (-4.971361398696899, -3.226241111755371),
                                 (-5.037429332733154, -3.5202900171279907), (-5.039270877838135, -3.8203794956207275),
                                 (-4.983691453933716, -4.116943001747131), (-4.889368057250977, -4.403225898742676),
                                 (-4.7508299350738525, -4.6704795360565186), (-4.562358379364014, -4.905071020126343),
                                 (-4.326965093612671, -5.09250807762146), (-4.056070446968079, -5.223686456680298),
                                 (-3.7642170190811157, -5.297856569290161), (-3.4637705087661743, -5.322885036468506),
                                 (-3.162044048309326, -5.323251962661743), (-2.8601925373077393, -5.31890606880188),
                                 (-2.558448076248169, -5.318608999252319), (-2.256711006164551, -5.318568468093872),
                                 (-1.9549565315246582, -5.317893981933594), (-1.6532039642334029, -5.31725001335144),
                                 (-1.3514524698257446, -5.3167009353637695), (-1.0497019886970484, -5.316137075424194),
                                 (-0.7479503154754639, -5.3155601024627686), (-0.44619889557361603, -5.314986944198608),
                                 (-0.14444755017757416, -5.3144145011901855), (0.1573037952184677, -5.313841104507446),
                                 (0.45905520021915436, -5.313270092010498), (0.7608067691326177, -5.312701940536499),
                                 (1.0625574588775635, -5.312118053436279), (1.364308476448059, -5.311525344848633),
                                 (1.6660625338554382, -5.311041355133057), (1.9678159952163696, -5.3105340003967285),
                                 (2.269547462463379, -5.309326410293579), (2.5713000297546356, -5.3087921142578125),
                                 (2.873189091682431, -5.312604904174805), (3.174834966659546, -5.30867600440979),
                                 (3.474912405014038, -5.2803521156311035), (3.767619013786316, -5.209180593490601),
                                 (4.044913053512573, -5.0910725593566895), (4.299377918243408, -4.9298553466796875),
                                 (4.5263295173645, -4.7317569255828875), (4.718136548995969, -4.499257087707522),
                                 (4.869032859802246, -4.238522529602051), (4.977253198623657, -3.9574304819107056),
                                 (5.037458419799805, -3.662133574485779), (5.0549163818359375, -3.3610655069351196),
                                 (5.054198503494263, -3.0592960119247437), (5.051084995269775, -2.7574654817581177),
                                 (5.051368474960327, -2.4557210206985474), (5.051839828491211, -2.15398108959198),
                                 (5.05174994468689, -1.852227509021759), (5.0516581535339355, -1.5504735112190247),
                                 (5.051655054092407, -1.248722493648529), (5.051645994186401, -0.9469707012176514),
                                 (5.051620960235596, -0.645218700170517), (5.0515971183776855, -0.34346674382686615),
                                 (5.051574945449829, -0.04171484149992466), (5.051552057266235, 0.26003704965114594),
                                 (5.0515289306640625, 0.561788946390152), (5.05151104927063, 0.8635410368442535)]
