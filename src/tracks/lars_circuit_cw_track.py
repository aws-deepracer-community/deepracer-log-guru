#
# DeepRacer Guru
#
# Version 3.0 onwards
#
# Copyright (c) 2021 dmh23
#

from src.tracks.track import Track
import src.personalize.configuration.personal_track_annotations as config


class LarsCircuitClockwiseTrack(Track):
    def __init__(self):
        super().__init__()

        self._ui_name = "Lars Circuit Clockwise"
        self._ui_description = "Lars Circuit is a pro difficulty track that adds an increasing to decreasing double apex and multiple high speed straightaways to its shorter cohort Lars Loop. It is named in honor of 2020 AWS DeepRacer League silver medalist Lars Ludvigson (Duckworth)"
        self._ui_length_in_m = 59.23  # metres
        self._ui_width_in_cm = 107  # centimetres
        self._world_name = "thunder_hill_pro_cw"
        self._track_sector_dividers = [39, 78, 113, 161]
        self._annotations = config.lars_circuit_cw_annotations
        self._track_width = 1.066

        self._track_waypoints = [(2.452657327873855930e+00, 3.716859206432351903e-01),
                                (2.322673082351684570e+00, 3.696620836853981018e-01),
                                (2.192688589985234415e+00, 3.676541633091131578e-01),
                                (2.021908044815063477e+00, 3.650160506367683411e-01),
                                (1.721143007278441939e+00, 3.603529557585716248e-01),
                                (1.420378029346466064e+00, 3.556938022375106812e-01),
                                (1.119612991809844971e+00, 3.510354608297348022e-01),
                                (8.188480436801910400e-01, 3.463771864771842957e-01),
                                (5.180829763412475586e-01, 3.417172133922576904e-01),
                                (2.173180058598518372e-01, 3.370580524206161499e-01),
                                (-8.344700187444686890e-02, 3.323995918035507202e-01),
                                (-3.842120021581649780e-01, 3.277401849627494812e-01),
                                (-6.849769949913024902e-01, 3.230808898806571960e-01),
                                (-9.857420027256011963e-01, 3.184231072664260864e-01),
                                (-1.286506950855255127e+00, 3.137547075748443604e-01),
                                (-1.587272524833679199e+00, 3.091280013322830200e-01),
                                (-1.888036549091339111e+00, 3.043801486492156982e-01),
                                (-2.188802003860473633e+00, 2.997841909527778625e-01),
                                (-2.488536477088928223e+00, 2.781310155987739563e-01),
                                (-2.779304504394531250e+00, 2.036561071872711182e-01),
                                (-3.025648474693298340e+00, 3.731741011142730713e-02),
                                (-3.121860027313232422e+00, -2.470885179936885834e-01),
                                (-3.230623006820678711e+00, -5.275231003761291504e-01),
                                (-3.346309423446655273e+00, -8.051840066909790039e-01),
                                (-3.466438055038452148e+00, -1.080954283475875854e+00),
                                (-3.590103983879089355e+00, -1.355157017707824707e+00),
                                (-3.632608532905578613e+00, -1.650329530239105225e+00),
                                (-3.523424029350280762e+00, -1.925336539745330811e+00),
                                (-3.278442502021789551e+00, -2.094487965106964111e+00),
                                (-2.984074473381042480e+00, -2.139160037040710449e+00),
                                (-2.683272480964660645e+00, -2.139138460159301758e+00),
                                (-2.382858991622924805e+00, -2.124479532241821289e+00),
                                (-2.082351565361022949e+00, -2.111197531223297119e+00),
                                (-1.781760990619659424e+00, -2.099951565265655518e+00),
                                (-1.481117486953735352e+00, -2.090227007865905762e+00),
                                (-1.180428504943847656e+00, -2.082027435302734375e+00),
                                (-8.797017335891723633e-01, -2.075363457202911377e+00),
                                (-5.789597630500793457e-01, -2.069401502609252930e+00),
                                (-2.782032042741775513e-01, -2.064271032810211182e+00),
                                (2.258953917771577835e-02, -2.062324464321136475e+00),
                                (3.233157992362976074e-01, -2.068417549133300781e+00),
                                (6.233294606208801270e-01, -2.089503943920135498e+00),
                                (9.202745556831359863e-01, -2.136389493942260742e+00),
                                (1.204966425895690918e+00, -2.231584966182708740e+00),
                                (1.450966954231262207e+00, -2.402922511100769043e+00),
                                (1.722369015216827393e+00, -2.526587605476379395e+00),
                                (2.021925985813140869e+00, -2.534471035003662109e+00),
                                (2.320029497146606445e+00, -2.494590580463409424e+00),
                                (2.619286537170410156e+00, -2.465692460536956787e+00),
                                (2.914102554321289062e+00, -2.510718464851379395e+00),
                                (3.166846036911010742e+00, -2.671159505844116211e+00),
                                (3.363971471786499023e+00, -2.897334933280944824e+00),
                                (3.499363422393798828e+00, -3.165050983428955078e+00),
                                (3.564290523529052734e+00, -3.457974433898925781e+00),
                                (3.578886032104492188e+00, -3.758398532867431641e+00),
                                (3.586687445640563965e+00, -4.059091091156005859e+00),
                                (3.587734103202819824e+00, -4.359879970550537109e+00),
                                (3.576985001564025879e+00, -4.660458564758300781e+00),
                                (3.545305013656616211e+00, -4.959451675415039062e+00),
                                (3.456297039985656738e+00, -5.246365070343017578e+00),
                                (3.231963992118835449e+00, -5.442764282226562500e+00),
                                (2.940503001213073730e+00, -5.481115818023681641e+00),
                                (2.642308950424194336e+00, -5.520580768585205078e+00),
                                (2.344491958618164062e+00, -5.562706947326660156e+00),
                                (2.046595036983489990e+00, -5.604280471801757812e+00),
                                (1.747492015361785889e+00, -5.636098861694335938e+00),
                                (1.447663962841033936e+00, -5.660130023956298828e+00),
                                (1.147428512573242188e+00, -5.678488969802856445e+00),
                                (8.469030559062957764e-01, -5.691282987594604492e+00),
                                (5.462153851985931396e-01, -5.699446916580200195e+00),
                                (2.454424500465393066e-01, -5.703427553176879883e+00),
                                (-5.535599961876869202e-02, -5.703270435333251953e+00),
                                (-3.556213974952697754e-01, -5.710031986236572266e+00),
                                (-6.539948880672454834e-01, -5.748088598251342773e+00),
                                (-9.512360394001007080e-01, -5.794168472290039062e+00),
                                (-1.247055470943450928e+00, -5.848622083663940430e+00),
                                (-1.540832459926605225e+00, -5.913161516189575195e+00),
                                (-1.831378519535064697e+00, -5.990900516510009766e+00),
                                (-2.116413056850433350e+00, -6.086760520935058594e+00),
                                (-2.390679955482482910e+00, -6.209963083267211914e+00),
                                (-2.671500563621520996e+00, -6.316936969757080078e+00),
                                (-2.967261910438537598e+00, -6.367522001266479492e+00),
                                (-3.263084411621093750e+00, -6.324554443359375000e+00),
                                (-3.508201479911804199e+00, -6.156256914138793945e+00),
                                (-3.682719945907592773e+00, -5.911300182342529297e+00),
                                (-3.861365556716918945e+00, -5.669299602508544922e+00),
                                (-4.044927954673767090e+00, -5.431009054183959961e+00),
                                (-4.232613921165466309e+00, -5.195955038070678711e+00),
                                (-4.425116300582885742e+00, -4.964824438095092773e+00),
                                (-4.621956586837768555e+00, -4.737375497817993164e+00),
                                (-4.823176145553588867e+00, -4.513791561126708984e+00),
                                (-5.028560161590576172e+00, -4.294028043746948242e+00),
                                (-5.238161563873291016e+00, -4.078284382820129395e+00),
                                (-5.452080965042114258e+00, -3.866822004318237305e+00),
                                (-5.669037580490112305e+00, -3.658476591110229492e+00),
                                (-5.879651546478271484e+00, -3.443732976913452148e+00),
                                (-6.083657979965209961e+00, -3.222716569900512695e+00),
                                (-6.276221990585327148e+00, -2.991699099540710449e+00),
                                (-6.447117805480957031e+00, -2.744400024414062500e+00),
                                (-6.542968511581420898e+00, -2.464175939559936523e+00),
                                (-6.553581476211547852e+00, -2.163573980331420898e+00),
                                (-6.561298131942749023e+00, -1.862872481346130371e+00),
                                (-6.566658020019531250e+00, -1.562119960784912109e+00),
                                (-6.569708347320556641e+00, -1.261335015296936035e+00),
                                (-6.569895505905151367e+00, -9.605342447757720947e-01),
                                (-6.567871332168579102e+00, -6.597407460212707520e-01),
                                (-6.563146591186523438e+00, -3.589777499437332153e-01),
                                (-6.555159568786621094e+00, -5.828478187322616577e-02),
                                (-6.544605493545532227e+00, 2.423286437988281250e-01),
                                (-6.522720813751220703e+00, 5.422623902559300380e-01),
                                (-6.478438377380371094e+00, 8.397246003150939941e-01),
                                (-6.414607524871826172e+00, 1.133624494075775146e+00),
                                (-6.333232402801514560e+00, 1.423168480396267421e+00),
                                (-6.236847877502441406e+00, 1.708077490329742432e+00),
                                (-6.126446485519409180e+00, 1.987855970859527588e+00),
                                (-6.003616094589233398e+00, 2.262408494949340820e+00),
                                (-5.868571996688842773e+00, 2.531168937683105469e+00),
                                (-5.722400426864624023e+00, 2.794039011001586914e+00),
                                (-5.564512014389038086e+00, 3.050037503242492676e+00),
                                (-5.394480466842651367e+00, 3.298123478889465332e+00),
                                (-5.207866907119750977e+00, 3.533947587013244629e+00),
                                (-5.000058412551879883e+00, 3.751310586929321289e+00),
                                (-4.778875112533569336e+00, 3.955097436904907227e+00),
                                (-4.543109655380249023e+00, 4.141737461090087891e+00),
                                (-4.277584552764892578e+00, 4.275022387504577637e+00),
                                (-3.978692412376403809e+00, 4.302906632423400879e+00),
                                (-3.682698011398315430e+00, 4.255747556686401367e+00),
                                (-3.419662952423095703e+00, 4.113559126853942871e+00),
                                (-3.228514432907104492e+00, 3.883466482162475586e+00),
                                (-3.085964918136596680e+00, 3.618720054626464844e+00),
                                (-2.912765026092529297e+00, 3.373042464256286621e+00),
                                (-2.709118962287902832e+00, 3.151956081390380859e+00),
                                (-2.478106975555419922e+00, 2.959650039672851562e+00),
                                (-2.224163055419921875e+00, 2.798793554306030273e+00),
                                (-1.937278985977172852e+00, 2.709513902664184570e+00),
                                (-1.639684498310089111e+00, 2.669368028640747070e+00),
                                (-1.344021975994110107e+00, 2.713446497917175293e+00),
                                (-1.114599972963333130e+00, 2.899472475051879883e+00),
                                (-1.000996708869934082e+00, 3.177403926849365234e+00),
                                (-8.650614619255065918e-01, 3.421032071113586426e+00),
                                (-6.068992614746093750e-01, 3.530719399452209473e+00),
                                (-3.079966530203819275e-01, 3.517488479614257812e+00),
                                (-2.580035477876663208e-02, 3.619057536125183105e+00),
                                (2.253605127334594727e-01, 3.783665537834167480e+00),
                                (4.521942958235740662e-01, 3.981035590171813965e+00),
                                (7.154473662376403809e-01, 4.123751044273376465e+00),
                                (1.011717349290847778e+00, 4.163952112197875977e+00),
                                (1.303629517555236816e+00, 4.097178101539611816e+00),
                                (1.556224465370178223e+00, 3.940809130668640137e+00),
                                (1.725043535232543945e+00, 3.692258477210998535e+00),
                                (1.932292044162750244e+00, 3.474748969078063965e+00),
                                (2.176424980163574219e+00, 3.299950480461120605e+00),
                                (2.454056501388549805e+00, 3.186287045478820801e+00),
                                (2.751753926277160645e+00, 3.152011513710021973e+00),
                                (3.044340491294860840e+00, 3.215511441230773926e+00),
                                (3.304554939270019531e+00, 3.364567041397094727e+00),
                                (3.522794008255004883e+00, 3.570819973945617676e+00),
                                (3.698200941085815430e+00, 3.814622521400451660e+00),
                                (3.774941444396972656e+00, 4.105453014373779297e+00),
                                (3.854979515075683594e+00, 4.395410060882568359e+00),
                                (3.937350034713745117e+00, 4.684711933135986328e+00),
                                (4.022776365280150479e+00, 4.973126173019407403e+00),
                                (4.111782431602478027e+00, 5.260454416275024414e+00),
                                (4.205074548721313477e+00, 5.546418428421020508e+00),
                                (4.308547019958496094e+00, 5.828725099563598633e+00),
                                (4.470946788787841797e+00, 6.080511093139648438e+00),
                                (4.708148002624511719e+00, 6.262716531753540039e+00),
                                (4.993758916854858398e+00, 6.353126525878906250e+00),
                                (5.293702602386474609e+00, 6.363875150680541992e+00),
                                (5.590363979339599609e+00, 6.316252946853637695e+00),
                                (5.877067565917968750e+00, 6.225951433181762695e+00),
                                (6.149999618530273438e+00, 6.100139379501342773e+00),
                                (6.369915485382080078e+00, 5.897995471954345703e+00),
                                (6.501977682113647461e+00, 5.629106521606445312e+00),
                                (6.560607433319091797e+00, 5.334652900695800781e+00),
                                (6.566045999526977539e+00, 5.034187793731689453e+00),
                                (6.523860692977905273e+00, 4.736864089965820312e+00),
                                (6.455312490463256836e+00, 4.443979978561401367e+00),
                                (6.383426189422607422e+00, 4.151897668838500977e+00),
                                (6.307988405227661133e+00, 3.860711097717285156e+00),
                                (6.229055166244506836e+00, 3.570453405380249023e+00),
                                (6.145443439483642578e+00, 3.281511425971984863e+00),
                                (6.056455373764038086e+00, 2.994179487228393555e+00),
                                (5.960769414901733398e+00, 2.709013938903808594e+00),
                                (5.855376720428466797e+00, 2.427302956581115723e+00),
                                (5.734679698944091797e+00, 2.151848018169403076e+00),
                                (5.590353488922119141e+00, 1.888026535511016846e+00),
                                (5.428771018981933594e+00, 1.634358465671539307e+00),
                                (5.256325006484985352e+00, 1.387926995754241943e+00),
                                (5.074297904968262607e+00, 1.148473769426346491e+00),
                                (4.883213996887207031e+00, 9.162861704826354980e-01),
                                (4.658768892288208008e+00, 7.166556715965270996e-01),
                                (4.402160882949829102e+00, 5.605030320584774017e-01),
                                (4.121596455574035645e+00, 4.531609602272510529e-01),
                                (3.826274037361145020e+00, 3.982743397355079651e-01),
                                (3.525722980499267578e+00, 3.892398923635482788e-01),
                                (3.224965929985046387e+00, 3.837353363633155823e-01),
                                (2.924200057983398438e+00, 3.791950047016143799e-01),
                                (2.623438000679016113e+00, 3.743449524044990540e-01),
                                (2.452657327873855930e+00, 3.716859206432351903e-01)]
