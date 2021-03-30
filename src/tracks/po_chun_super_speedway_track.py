from src.tracks.track import Track
import src.configuration.personal_track_annotations as config


class PoChunSuperSpeedwayTrack(Track):
    def __init__(self):
        super().__init__()

        self._ui_name = "Po-Chun Super Speedway"
        self._ui_description = "Po-Chun Super Speedway is a long track (89.24m) which adds back-to-back hairpins and a high speed right angle turn its short track counterpart. It is named in honor of the 2020 AWS DeepRacer League Champion from NCTU CGI Taiwan."
        self._ui_length_in_m = 89.24  # metres
        self._ui_width_in_cm = 107  # centimetres
        self._world_name = "penbay_pro"
        self._track_sector_dividers = [70, 103, 130, 176, 233]
        self._annotations = config.po_chun_super_speedway_annotations
        self._track_width = 1.066

        self._track_waypoints = [(-2.430124044418335, -4.6310834884643555), (-2.130122423171997, -4.616528511047363),
                                 (-1.830029010772705, -4.604029178619385), (-1.5298445224761963, -4.5935845375061035),
                                 (-1.2295674681663513, -4.585195541381836), (-0.9291991591453552, -4.578861951828003),
                                 (-0.6287389993667603, -4.574584007263184), (-0.3281870484352112, -4.57236123085022),
                                 (-0.027543379925191402, -4.572193384170532), (0.27319204807281494, -4.574082136154175),
                                 (0.574019193649292, -4.5780251026153564), (0.8749381005764008, -4.584023475646973),
                                 (1.175948977470398, -4.5920774936676025), (1.4770514965057373, -4.602187395095825),
                                 (1.7782435417175293, -4.614315032958984), (2.0794479846954346, -4.626747131347656),
                                 (2.380623459815979, -4.638553142547607), (2.68176805973053, -4.64973258972168),
                                 (2.9828829765319824, -4.660285949707031), (3.283967971801758, -4.670212984085083),
                                 (3.5850229263305664, -4.679513454437256), (3.8860480785369873, -4.688188076019287),
                                 (4.1870434284210205, -4.69623589515686), (4.488008975982666, -4.703657865524292),
                                 (4.7889440059661865, -4.710453987121582), (5.089849472045898, -4.716622829437256),
                                 (5.3907248973846436, -4.722166538238525), (5.691570997238159, -4.727083444595337),
                                 (5.992386341094971, -4.731374025344849), (6.293172121047974, -4.7350380420684814),
                                 (6.593928098678589, -4.7380759716033936), (6.894653558731079, -4.740488052368164),
                                 (7.195349931716919, -4.742273569107056), (7.195349931716919, -4.742273569107056),
                                 (7.496015548706055, -4.743432998657227), (7.796566486358643, -4.737317323684692),
                                 (8.096156597137451, -4.712990999221802), (8.392126560211182, -4.661058664321899),
                                 (8.67834186553955, -4.570133924484253), (8.939287662506104, -4.422395586967468),
                                 (9.14907169342041, -4.2085829973220825), (9.290607929229736, -3.9441665410995483),
                                 (9.374144554138184, -3.6557085514068604), (9.420714378356934, -3.358809471130371),
                                 (9.445830821990967, -3.0592504739761353), (9.459988594055176, -2.758949518203735),
                                 (9.469439029693604, -2.458457469940186), (9.478309631347656, -2.157946467399597),
                                 (9.489231586456299, -1.8575045466423035), (9.504131317138672, -1.5572359561920166),
                                 (9.524545669555664, -1.2572925090789795), (9.551346778869629, -0.9578520655632019),
                                 (9.587671279907227, -0.659421294927597), (9.62569284439087, -0.3611939549446106),
                                 (9.664241790771484, -0.06303377007134259), (9.702705383300781, 0.23513704538345337),
                                 (9.740477085113525, 0.5333961397409439), (9.777248859405518, 0.8317808508872986),
                                 (9.812594413757324, 1.1303365230560312), (9.846135139465332, 1.4291009902954102),
                                 (9.87756872177124, 1.7280945181846619), (9.906436920166016, 2.0273460149765015),
                                 (9.932222843170166, 2.3268784284591675), (9.954477787017822, 2.6266934871673584),
                                 (9.972814083099365, 2.9267730712890625), (9.986804008483887, 3.2270859479904175),
                                 (9.995913028717041, 3.527586579322815), (9.999640941619873, 3.8282010555267334),
                                 (9.997497081756592, 4.128830671310425), (9.988949298858643, 4.429344177246094),
                                 (9.973399639129639, 4.7295753955841064), (9.949857234954834, 5.029285192489626),
                                 (9.918274879455566, 5.328254461288452), (9.877529621124268, 5.6261088848114),
                                 (9.826738834381104, 5.922415494918823), (9.758614540100098, 6.214697360992432),
                                 (9.636386394500732, 6.489189386367798), (9.480982303619385, 6.746299028396606),
                                 (9.288434982299805, 6.976783990859985), (9.058995246887207, 7.170398473739624),
                                 (8.799074649810793, 7.320734500885009), (8.51647663116455, 7.422268390655518),
                                 (8.221739768981935, 7.480210304260254), (7.921878814697266, 7.5000388622283936),
                                 (7.6215283870697, 7.489731550216675), (7.3229146003723145, 7.455408573150635),
                                 (7.0270469188690186, 7.402256011962891), (6.734105110168457, 7.334752082824707),
                                 (6.443860054016113, 7.256415128707886), (6.156522989273071, 7.168391942977905),
                                 (5.884455919265747, 7.040875434875488), (5.627530574798584, 6.885026454925537),
                                 (5.3853349685668945, 6.707059144973755), (5.157548666000366, 6.51094651222229),
                                 (4.943450450897217, 6.299946069717407), (4.742493391036987, 6.076385021209717),
                                 (4.552919149398804, 5.843064546585083), (4.376629114151001, 5.599672794342041),
                                 (4.223207592964172, 5.341230392456055), (4.0917768478393555, 5.07092547416687),
                                 (3.9822139739990234, 4.791034936904907), (3.8938815593719482, 4.50372838973999),
                                 (3.8278305530548096, 4.210512161254883), (3.7850064039230347, 3.913007974624634),
                                 (3.7659590244293213, 3.613065481185913), (3.7755849361419678, 3.3126925230026245),
                                 (3.815258026123047, 3.0148249864578247), (3.8935909271240234, 2.724830985069275),
                                 (4.016179919242861, 2.4507409334182713), (4.191602468490601, 2.207356572151184),
                                 (4.4219770431518555, 2.015594959259033), (4.695976972579956, 1.8941834568977356),
                                 (4.992300510406491, 1.8476459383964545), (5.292114496231079, 1.8636009693145752),
                                 (5.579845666885376, 1.9417184591293335), (5.801500558853151, 2.1427034735679653),
                                 (5.97893500328064, 2.3851314783096313), (6.137029886245725, 2.6408215761184657),
                                 (6.292307138442993, 2.8982549905776978), (6.460271120071411, 3.1474565267562866),
                                 (6.631062030792236, 3.3561785221099854), (6.94663500785828, 3.451653480529784),
                                 (7.244168043136597, 3.3208584785461426), (7.4054441452026385, 3.0864959955215423),
                                 (7.5610740184783936, 2.8296334743499756), (7.676098346710205, 2.552169442176819),
                                 (7.749621868133545, 2.260894536972046), (7.78407621383667, 1.9624285101890564),
                                 (7.784628629684448, 1.661926507949829), (7.753325462341309, 1.3630459904670715),
                                 (7.695392608642578, 1.068128913640976), (7.612145900726318, 0.7793349623680115),
                                 (7.506695508956911, 0.49786868691444786), (7.3794496059417725, 0.2255704291164875),
                                 (7.2311930656433105, -0.03588584065437317), (7.061892032623288, -0.284218596294525),
                                 (6.870421648025513, -0.5158436447381973), (6.655433893203735, -0.7257693856954575),
                                 (6.413336992263794, -0.9034991711378098), (6.143733501434326, -1.0351834893226624),
                                 (5.850797891616821, -1.1002704799175262), (5.550658941268921, -1.1137186586856842),
                                 (5.250178575515747, -1.1042318940162659), (4.94961142539978, -1.1010663211345673),
                                 (4.649264097213745, -1.0977000892162323), (4.348665952682495, -1.1013858616352081),
                                 (4.048200607299805, -1.1116590201854706), (3.747630000114441, -1.1175246834754944),
                                 (3.447206974029541, -1.1078741550445557), (3.1490849256515503, -1.070337325334549),
                                 (2.8593244552612305, -0.9914660155773163), (2.5928150415420532, -0.8539344817399979),
                                 (2.356622040271759, -0.6684979796409607), (2.1545180082321167, -0.4463408850133419),
                                 (1.9868130087852478, -0.19707608595490456), (1.8498889803886414, 0.07040854543447495),
                                 (1.7377354502677917, 0.3492656424641609), (1.6460335850715637, 0.6355338841676712),
                                 (1.5690045356750488, 0.9261116683483124), (1.5028469264507294, 1.2193740010261536),
                                 (1.4440574645996094, 1.5142065286636353), (1.3895851075649261, 1.8098710179328918),
                                 (1.336341381072998, 2.1057599782943726), (1.2813157737255096, 2.4013224840164185),
                                 (1.2190353870391846, 2.695385456085205), (1.129233479499817, 2.982155442237854),
                                 (1.0045355260372162, 3.2553720474243164), (0.8315969705581665, 3.5005855560302734),
                                 (0.5962213575839996, 3.6850509643554688), (0.305494099855423, 3.7460179328918457),
                                 (0.024867892265319824, 3.647498846054077), (-0.19345930963754654, 3.4428365230560303),
                                 (-0.3510669991374016, 3.187432050704956), (-0.46061595156788826, 2.907734990119934),
                                 (-0.5338581795804203, 2.6163305044174194), (-0.587820615619421, 2.320572018623352),
                                 (-0.6405379176139832, 2.024588465690613), (-0.6939584761857986, 1.7287319898605347),
                                 (-0.7480108961462975, 1.4329895377159119), (-0.8028516322374344, 1.1373934745788574),
                                 (-0.8613181561231613, 0.8424929082393646), (-0.9235265254974365, 0.5483614504337311),
                                 (-0.9907737225294091, 0.25533980131150263),
                                 (-1.0642608106136322, -0.03617264702916145),
                                 (-1.1368589997291545, -0.32791440188883914),
                                 (-1.2154776751995107, -0.6180874854326316), (-1.3021363019943237, -0.9059553146362305),
                                 (-1.4004294574260712, -1.1900448203086853), (-1.5178849697113037, -1.4666975140571594),
                                 (-1.6681599617004395, -1.7266314625740051), (-1.8815330266952583, -1.935601532459261),
                                 (-2.167093038558967, -2.0184000730514526), (-2.467566967010505, -2.0137939453125004),
                                 (-2.7679264545440674, -2.026146948337555), (-3.0681475400924683, -2.0419684648513794),
                                 (-3.3687245845794678, -2.044815421104431), (-3.668005585670471, -2.0182260274887085),
                                 (-3.958536982536316, -1.9431445002555847), (-4.220651388168335, -1.7984524369239807),
                                 (-4.424093961715698, -1.5790520310401917), (-4.5528340339660645, -1.3083374500274658),
                                 (-4.619600057601929, -1.015651524066925), (-4.627529859542847, -0.715287446975708),
                                 (-4.607590913772583, -0.41537633538246155), (-4.568633556365968, -0.1172997225076049),
                                 (-4.518140077590942, 0.17906633019447327), (-4.466545939445496, 0.47524674236774445),
                                 (-4.421532511711121, 0.7724817097187042), (-4.3914880752563485, 1.0715615153312634),
                                 (-4.3853970766067505, 1.3720359802246094), (-4.406944632530212, 1.6718485355377197),
                                 (-4.4319764375686646, 1.9714464545249897), (-4.458406567573547, 2.270921468734741),
                                 (-4.489547610282897, 2.569943070411677), (-4.5271360874176025, 2.868216037750244),
                                 (-4.574212074279784, 3.165132403373712), (-4.633819818496702, 3.4597765207290556),
                                 (-4.709562540054321, 3.7506635189056396), (-4.805798530578613, 4.035404086112976),
                                 (-4.928437471389774, 4.309750795364386), (-5.083076477050786, 4.5672941207885795),
                                 (-5.274833440780645, 4.798391103744511), (-5.499994993209839, 4.997262001037598),
                                 (-5.746784925460815, 5.167815923690796), (-6.028879404067993, 5.268628358840942),
                                 (-6.328155040740967, 5.280660629272461), (-6.618443489074699, 5.206075429916384),
                                 (-6.883103132247925, 5.064640522003174), (-7.11795043945312, 4.8774580955505416),
                                 (-7.32399964332581, 4.658805608749384), (-7.502840995788574, 4.417321443557739),
                                 (-7.656172037124634, 4.158854007720947), (-7.784522533416748, 3.8871010541915894),
                                 (-7.8748714923858625, 3.6009069681167656), (-7.950711488723755, 3.309988498687744),
                                 (-8.02601218223572, 3.018929481506341), (-8.101375579833986, 2.7278873920440607),
                                 (-8.176248550415039, 2.4367189407348633), (-8.252087354660034, 2.145799994468689),
                                 (-8.328953266143799, 1.8551515340805054), (-8.404784202575684, 1.564230501651764),
                                 (-8.480850696563719, 1.2733709812164384), (-8.556511878967287, 0.9824056029319694),
                                 (-8.632545471191408, 0.6915374100208214), (-8.708434581756592, 0.4006316512823105),
                                 (-8.783548355102539, 0.10952449310570955), (-8.859080314636229, -0.18147392012178315),
                                 (-8.93493366241455, -0.47238920629024506), (-9.010858058929443, -0.763285905122757),
                                 (-9.086645126342773, -1.054218202829361), (-9.162533283233643, -1.3451244831085205),
                                 (-9.238336563110352, -1.6360524892807007), (-9.31397008895874, -1.9270249605178833),
                                 (-9.389853477478027, -2.2179324626922607), (-9.465883255004883, -2.508802056312561),
                                 (-9.541830062866211, -2.799692988395691), (-9.619751930236816, -3.090052008628845),
                                 (-9.698315620422363, -3.3802454471588135), (-9.772529125213623, -3.6715790033340454),
                                 (-9.840312004089355, -3.9644711017608643), (-9.899288177490234, -4.259257078170776),
                                 (-9.947181701660156, -4.556037425994873), (-9.981398582458496, -4.854693412780762),
                                 (-9.998600006103516, -5.154799461364746), (-9.996078491210938, -5.45535945892334),
                                 (-9.969909191131592, -5.754769325256348), (-9.915900230407715, -6.050400495529175),
                                 (-9.830880641937256, -6.33860445022583), (-9.707103252410889, -6.612091064453125),
                                 (-9.536486625671387, -6.859166860580444), (-9.32621717453003, -7.073501348495483),
                                 (-9.082514762878418, -7.2489354610443115), (-8.812891960144043, -7.381120443344116),
                                 (-8.524944305419922, -7.466286897659302), (-8.226527690887451, -7.499348163604736),
                                 (-7.927458047866821, -7.474273443222046), (-7.644726514816284, -7.377177953720093),
                                 (-7.417553424835205, -7.181813478469849), (-7.2401769161224365, -6.939528942108154),
                                 (-7.096879959106445, -6.675363063812256), (-6.971076965332031, -6.402328014373779),
                                 (-6.850262880325317, -6.127029895782471), (-6.722007513046265, -5.85515284538269),
                                 (-6.5831334590911865, -5.5885865688323975), (-6.421311140060425, -5.335346937179565),
                                 (-6.227766036987305, -5.105727434158325), (-5.995217561721802, -4.916128873825073),
                                 (-5.723948001861572, -4.7884743213653564), (-5.42985200881958, -4.729269981384277),
                                 (-5.129565000534058, -4.719938516616821), (-4.829322338104248, -4.734981060028076),
                                 (-4.5291688442230225, -4.751984119415283), (-4.228614330291748, -4.755470514297485),
                                 (-3.928755044937134, -4.734689950942993), (-3.6292120218276978, -4.709857940673828),
                                 (-3.329577922821045, -4.6870808601379395), (-3.0298514366149902, -4.666360139846802),
                                 (-2.73003351688385, -4.647693872451782), (-2.430124044418335, -4.6310834884643555)]