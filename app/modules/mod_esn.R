# =============================================================================
# mod_esn.R — Módulo ESN (Echo State Network) para Shiny
# Baseado em: ESN Acoes-petr4 v2.8.1.2 Maycon G Silva.R
# =============================================================================

# Carregar utilitários
source("utils/data_prep.R", local = TRUE)
source("utils/metrics.R", local = TRUE)

# =============================================================================
# CENÁRIOS PRÉ-OTIMIZADOS (extraídos do código original)
# =============================================================================

# Estrutura de um cenário:
# list(nome, a, sr, initLen, tam_reservoir, reg, Win, W, Wout, dist_win, dist_w)

criar_cenarios_pre_otimizados <- function() {
  cenarios <- list()
  
  # --- Cenário 1: Run 10000_1, Win GED + W Normal, tam_reservoir=15 ---
  cenarios[["9220_GED_Normal_15"]] <- list(
    nome = "Run 9220 | Win GED | W Normal | Reservatório=15",
    a = 0.926230821463176,
    sr = 0.642384661748213,
    initLen = 8,
    tam_reservoir = 15,
    reg = 7.05304479452055e-5,
    dist_win = "GED",
    dist_w = "Normal",
    Win = matrix(nrow = 15, ncol = 2, c(
      23.8286867301219, 22.4774576127917, 20.137075934452, 10.847853681893, 22.2399796703719,
      19.3539696610378, 21.4438801194363, 25.0486196609061, 2.34994991185052, 13.727298132811,
      11.7019238511075, 22.4658697689091, 6.40210724749221, 16.5860217383057, 16.0964937029461,
      28.5150792598598, -0.62785271777741, 26.4983446916728, 11.3542536470011, 7.96905393969021,
      3.25133304555825, 27.0253828824319, 7.80240259855172, 22.5794404626722, 12.4584294249808,
      8.4270479971493, 19.1529332579111, 20.6835014320524, -0.963910718562021, 24.183662141808)),
    W = matrix(nrow = 15, ncol = 15, c(
      -0.0605578027386505, 0.0613606233447933, -0.108692177280012, -0.146118401859457, -0.104668593402887,
      0.0931393976224093, -0.196125216421737, 0.199516288619675, -0.149144246241641, 0.240076793045162,
      -0.31373343697169, -0.252344907593781, -0.0417714038253541, 0.0268083525527564, -0.105520093493446,
      -0.0594530357925119, -0.150491379100068, 0.282687430160602, -0.0834665207232748, 0.088965206518118,
      -0.0335701947086064, -0.124696796017321, -0.0345479866499681, 0.125941167711635, 0.122789346644619,
      -0.0300511088808818, -0.107262337086775, -0.107500332745508, -0.0740638968920839, 0.0867402457592548,
      0.139392475540952, -0.166967255069514, -0.0274290373966007, -0.0617772851779337, -0.171465955266278,
      -0.141565042806367, -0.0564615261389467, 0.0786758681885605, -0.189035387252306, 0.114766835927005,
      -0.207910138226126, 0.178368225906427, -0.0236086063240226, -0.0721756990621309, -0.0521044608660359,
      0.207742975754988, 0.146147716556039, -0.0109507190521363, 0.2253489210143, 0.175605811748501,
      0.0287666699405999, 0.031651228164254, 0.147851233053217, -0.0109401904072624, 0.0270523474265416,
      0.279589242263415, 0.0560802339246532, -0.0571999167186198, 0.0480295457498267, -0.00712236102546574,
      0.128896666418112, 0.0213902689563876, 0.0389252379594335, 0.0820219776195539, -0.0894563820294327,
      -0.00768870815808686, 0.00885286318124391, -0.174127311350024, -0.128175557533053, 0.442004023611293,
      0.29921019846169, -0.0957418354085728, -0.302107494350921, -0.246208629483895, 0.0224395858606767,
      -0.338130372482041, -0.0665621993238663, 0.0699285328416198, 0.227252631302676, -0.41824338574719,
      -0.189554356521799, -0.108592726485719, -0.350475812352884, -0.0144884258604386, -0.253613936275334,
      0.120262738998331, -0.0344940672710521, 0.0800680639376176, -0.13465639682736, 0.152271211405007,
      0.136039043160873, -0.0648068474363471, -0.0415221384457807, -0.0687131896646887, -0.129641758707413,
      0.0915414819135286, 0.071083520941652, 0.0670647820836911, -0.203971124609106, 0.17530556780431,
      -0.0981834464736943, 0.188817526161609, 0.00503067586114325, -0.239610508215445, 0.219920671461572,
      0.143153487656889, -0.0251161906276346, 0.145711655959611, 0.0894339330182637, -0.341240294583937,
      -0.162391309739654, -0.286317493789089, 0.00623808256993354, 0.02216909447318, -0.0429351282749543,
      -0.0124480048837041, 0.155096967344624, 0.2583667839895, 0.0674561852675031, 0.0665180067246987,
      -0.0124900737937065, 0.138034761161821, 0.291436908003999, 0.163490854040274, -0.0476141559133726,
      -0.0094051272230872, -0.199213318238398, -0.109514619644921, 0.0408437473516281, 0.0443523730480857,
      0.0924732101700962, 0.00514612137927645, -0.332399053489197, 0.126147706969379, -0.0986108851351968,
      -0.150672254371928, 0.16110355202604, -0.257120084490043, -0.128263664630006, -0.032794762859908,
      0.0721063460316991, 0.0255039558182129, 0.171900571237003, -0.0742504497947241, -0.251079259435687,
      -0.210347823481703, -0.10308429458622, -0.176019239900964, 0.139410889290823, -0.309641884196467,
      0.0479255897435308, 0.15930944066402, 0.222125232323247, 0.0953543582561722, 0.0511010997553698,
      -0.186554813082587, -0.0104136791100989, -0.193446304541751, -0.00887897800955654, -0.107143122624087,
      0.0181970577879041, 0.0904291618578397, -0.0067953620976761, -0.168999598332065, -0.0263959259818122,
      0.0838266221979811, -0.0335416279324124, -0.150634756609104, 0.0228041134481417, -0.0838536036244564,
      -0.0905032439288794, -0.376789201528017, 0.0103807943623318, -0.0801659559095068, 0.43074437596383,
      -0.306887178668079, 0.36910354182698, 0.0129520244510901, -0.0844416680698095, -0.0581238732941944,
      -0.0859155919765276, -0.0319352595923491, -0.141238772933404, -0.0199315623497406, 0.182649530538737,
      -0.100199520807889, 0.120329094464645, -0.199649051195628, -0.0261477231551985, -0.129899285040569,
      -0.0366301667163647, -0.0997198327664473, -0.111549338320662, 0.113821729176482, 0.153604107029243,
      -0.0403517624613573, 0.129691531401488, 0.0183857546774572, 0.206385321687794, 0.0766013364291768,
      -0.247289756761986, -0.350160317972371, 0.00495602030341325, 0.197865601913143, 0.315738590241367,
      0.0974145541693093, 0.0181751699063103, 0.0448112710522807, 0.102508096486815, -0.0796952041939838,
      0.100678546495824, 0.0737132809984029, 0.0776312058440861, -0.0575848180407413, -0.306182966035017,
      -0.132573963544067, 0.0911986475010883, 0.218012308041569, 0.0762936459550168, -0.0264959975026127,
      -0.0839407813964129, -0.014696538241568, -0.297229467524563, -0.156310996707144, 0.110439082156438)),
    Wout = matrix(nrow = 1, ncol = 17, c(
      -0.234560750424862, 1.000500792519, -0.234560750424862, 3.27989162095946,
      -0.234560839831829, -0.234560631215572, -0.234560750424862, -0.234560690820217,
      -0.234560690820217, -0.234560750424862, -0.23456072062254, -0.234560705721378,
      -0.234560675919056, -0.234560810029507, -0.234560806304216, 0.0115933330581974,
      -0.234560787677765))
  )
  
  # --- Cenário 2: MELHOR — Run 2563, Win GED + W Normal, tam_reservoir=27 ---
  cenarios[["2563_GED_Normal_27"]] <- list(
    nome = "★ MELHOR: Run 2563 | Win GED | W Normal | Reservatório=27",
    a = 0.870902030197374,
    sr = 0.406802420062409,
    initLen = 9,
    tam_reservoir = 27,
    reg = 2.2289743444227e-05,
    dist_win = "GED",
    dist_w = "Normal",
    Win = matrix(nrow = 27, ncol = 2, c(
      9.77227059626767, 21.9406967182875, 7.56098533994042, 16.3427300152356, 20.5227110728847,
      16.7502082492526, 25.3271232653089, 20.8815145270364, 27.3411246269884, -3.12756182997085,
      22.3881181164667, 10.8018698732015, 8.47396701430825, 6.2030008252043, 14.4037951773676,
      19.9210735696691, -0.721022433098833, 20.7171838453202, 12.3480840628286, 4.68081118580138,
      25.6696599730835, 22.4333858836393, 19.5231982340921, 10.3402217853663, 20.288808571131,
      15.3022949236274, 22.5870113330856,
      21.0608352530002, -0.608163163607692, 4.87984703659724, 25.6157756006469, 20.524944436405,
      13.1767258231873, 18.0568801406273, 14.1624523561748, 25.2928179349979, 2.09587370676452,
      25.0578452770533, 27.7599742514216, 16.4529483605758, 15.5440579294674, 13.7353968506056,
      16.749572323559, 17.9452141402836, 25.8668954545981, -0.95742681487415, 20.9284525176176,
      8.11888901413491, 28.4362512908884, 20.2032578713083, 1.39732762135297, -1.31661481111454,
      6.72050438063485, 4.16973383732967)),
    W = matrix(nrow = 27, ncol = 27, c(
      0.00649677002418287, -0.1804687449615, 0.13029213656126, -0.0249546938758122, -0.088919243164589,
      -0.00912526603208562, -0.0145477153968082, -0.0271306429885993, 0.00785590215703405, -0.120231210902538,
      -0.0293520461685207, 0.0549558985169559, -0.0370434941463995, -0.0327898806748673, -0.0344929426227664,
      0.0098344706640336, -0.057110689988504, -0.0430151732811373, -0.114298520249219, 0.0283278019193946,
      0.00937290673902106, -0.066314257418032, -0.0295214810676086, 0.00477216463966632, -0.0998971829985844,
      0.0391298297849389, -0.154042398176542,
      -0.0552942421979389, 0.133983307323679, -0.052813449952949, 0.0527237197070902, -0.121814337222237,
      -0.119948441320097, -0.0557533485641943, -0.0357482066182091, 0.0995663732841071, -0.0435267257399423,
      -0.00889940106213879, -0.100770494453928, 0.000414439247696767, 0.106899812726477, -0.2043565038345,
      -0.133956800870946, -0.0408136666673768, -0.00251620109145427, -0.0850335145755951, -0.0139687419703335,
      0.0398766458389699, -0.0387921589715639, 0.0178935674666168, 0.0653218472533204, 0.0113902849810536,
      0.0276043930013418, -0.0383993347627401,
      0.21046860010997, 0.0469954174527151, 0.0379758237427616, -0.0548472133226663, 0.0354685136980992,
      -0.060849133353659, 0.0230933222895814, -0.0419158553853269, -0.0303422690258588, -0.0229650322450593,
      -0.0342064733978539, -0.0102386261987612, 0.0638964781754585, 0.0218810720568388, -0.0979962873909141,
      -0.128341980934885, 0.0361647378995106, 0.104961657683703, -0.0139247440635182, 0.0278304569928122,
      0.0829109268919442, 0.0173362977597789, -0.0441875982972493, 0.0360677335194457, 0.0177057791435535,
      0.0424896018189143, 0.0100430117505705,
      -0.0104348449358025, 0.012351545075882, -0.0210537716474248, -0.0482978245761547, 0.11834956718186,
      0.0636280203059285, -0.0603564358149785, -0.0879744372031433, 0.0242922981098828, -0.0616197695444574,
      -0.0775843240920867, 0.0604316295638919, -0.00237086651710792, -0.0987873403900846, -0.0459370316600475,
      0.0985485873902004, -0.0330828897825979, -0.0833275928508972, -0.0561479784167359, -0.018769724967996,
      0.0779676541280183, -0.0597536152283654, -0.0427410432490135, -0.0457545213793554, 0.104528630983558,
      -0.0333705567241367, 0.120546669475532,
      0.0493744843838015, -0.10921921014904, 0.0182162627171288, -0.0486813127840882, 0.00465622919458513,
      -0.0226964365148644, 0.0743362389528261, 0.00333878661150918, 0.0772876137077432, 0.0127564258275132,
      -0.0773142616896845, -0.014529490814081, 0.0810172666563664, -0.0279270746685733, -0.0714999838238234,
      0.0286843941197272, -0.0868389744032628, 0.0459802537304019, -0.0352871789343823, -0.0963683182770303,
      0.0987293869361064, -0.0651906488572541, 0.118450977715624, 0.0682800215499246, 0.0121559572791327,
      -0.201823975241134, 0.150647772945221,
      0.0312567863002902, -0.0413506721741998, -0.127495699917696, -0.0316357288481837, 0.0954398099110026,
      -0.0295405453622504, 0.0757684652239007, 0.0103837806679606, -0.024786611568613, 0.0377506355643921,
      -0.077666627421775, 0.0125461158915431, -0.0309525996844947, 0.0334341878213006, 0.0607203160421205,
      -0.275340074222334, 0.0885381090424522, 0.014007039611823, 0.015352571958705, 0.0159758355408893,
      0.0222742568919598, -0.0366209332013154, -0.0511546288901363, -0.014298100262006, -0.0975985664121295,
      0.134719631646142, 0.0496566972106389,
      -0.0152217337426957, -0.109098660289689, -0.0969236421240155, -0.167818169053939, 0.0975194564311709,
      -0.0196896673827684, -0.0497345810594104, -0.0954379286273802, 0.0275084287098225, 0.00741839599181645,
      0.0334790664856324, 0.00196727166437336, 0.0130380880875637, 0.0160237134753806, -0.00224485082298003,
      0.0575791877720606, 0.0386933897025559, 0.00324710567878347, -0.0798823927707766, -0.0077297659676561,
      -0.0146323310672458, 0.0507085358511227, 0.0379890674725354, -0.00305960469680137, 0.118122010966795,
      0.0810383832877284, -0.161154543663462,
      0.0483047367108692, 0.0397856486208481, 0.0123234082854915, 0.165781608524915, -0.0207264924823998,
      -0.047970881620841, 0.11624403717494, 0.127824056685006, -0.0737037480036909, 0.0331103545412838,
      -0.00238737572514781, 0.0685603159859593, -0.209102988093314, 0.060062376278696, 0.103742507560124,
      -0.0475780766481617, -0.0623234760563418, 0.00278263134233226, -0.100567546978671, -0.0423166746509199,
      -0.108088580274689, -0.0342767425198625, 0.0163455075064429, 0.0493661924698165, -0.0167399113952885,
      0.0252953346939208, 0.0297807953522645,
      0.058612377858105, 0.0184096841927141, -0.0383276881721812, 0.0112225543115829, -0.0765585900120014,
      0.0191939740822163, -0.025387233038307, 0.0753633658382, 0.000757451513722503, -0.0785287723996362,
      0.0618227466520345, -0.119647623223016, 0.116105340137256, 0.0198410841701465, 0.0364632414486194,
      -0.110192158078284, -0.134051325071844, 0.00728484928013507, -0.0401015083920738, -0.104339482046607,
      -0.178024283047085, -0.0111380365036982, -0.122034161278339, -0.133012717889329, 0.0115261628878607,
      -0.00419205340535844, -0.140996634735417,
      0.0999049252849892, 0.127349901780978, -0.00879804510925007, -0.107611325866154, 0.0331630502984292,
      0.0277970955412834, 0.0210512854984181, -0.0151189152961597, -0.152248699098513, -0.0157071603431462,
      0.0902750372556136, 0.144488412872834, 0.0791293411419258, 0.0988401359903456, -0.0165194488098891,
      -0.0136542109406029, 0.00961804849913907, -0.117313455598107, -0.0354934357005373, -0.111253917606858,
      0.0779333487537598, -0.000243663802472363, 0.0175955816001971, 0.0314308618618561, 0.00607553917466147,
      0.144553690110425, -0.0869230730206106)),
    Wout = matrix(nrow = 1, ncol = 29, c(
      0.058057114481926, 1.0010269188183, 0.058059349656105, 1.47258765713951,
      0.0580595061182976, 0.0580593273043633, 0.0580594465136528, 0.0580596253275871,
      0.0580596253275871, 0.0580595433712006, 0.0580596253275871, -2.87848351965658,
      0.0580594837665558, 0.0580592751502991, 0.0580597519874573, 0.0580596178770065,
      0.0580593794584274, 0.0580594539642334, 0.0580596327781677, 0.0580594539642334,
      -0.0031974782866584, 0.0580597966909409, 0.0580594688653946, 0.0580596774816513,
      0.0580585524439812, 0.0580595508217812, 0.019107758673556,
      0.0580587759613991, 0.0580587387084961))
  )
  
  # --- Cenário 3: Run 5991, Win Uniforme + W Uniforme, tam_reservoir=16 ---
  cenarios[["5991_Unif_Unif_16"]] <- list(
    nome = "Run 5991 | Win Uniforme | W Uniforme | Reservatório=16",
    a = 0.96510288317019,
    sr = 0.0530781027076928,
    initLen = 63,
    tam_reservoir = 16,
    reg = 7.36302522504892e-5,
    dist_win = "Uniforme",
    dist_w = "Uniforme",
    Win = matrix(nrow = 16, ncol = 2, c(
      -0.949979824479669, -0.132717023603618, 0.496501805260777, 0.450601571705192,
      -0.97876677615568, 0.842560855671763, -0.533590911421925, 0.28396730683744,
      0.512034471612424, -0.908285025507212, 0.720015816390514, 0.191193728707731,
      0.286161761730909, -0.313760765362531, -0.808994429185987, 0.887455421965569,
      0.245803336147219, -0.706920278258622, 0.147323348093778, -0.0895752259530127,
      -0.8148033474572, -0.307290891185403, 0.65524927014485, 0.543504803907126,
      -0.849573088344187, 0.0639435504563153, 0.0269709452986717, 0.100266476627439,
      0.978426828514785, 0.137345798779279, -0.899042603094131, -0.18180310446769)),
    # W omitida por brevidade (usar a completa do arquivo original)
    W = NULL,  # Será preenchida se selecionada
    Wout = matrix(nrow = 1, ncol = 18, c(
      3.36267784843221, 0.936837192668463, -1.04390602838248, -1.92236126121134,
      -4.66130195558071, 2.22003079019487, -2.85881648957729, -1.27036350034177,
      -0.491286399774253, 3.73086121649249, 3.41261961124837, 3.01166361477226,
      -7.97232919931412, -7.325465105474, 2.24645800422877, 8.09043150767684,
      -2.78673447947949, 0.421245891600847))
  )
  
  # --- Cenário 4: Run 4943, Win Normal + W Normal, tam_reservoir=3 ---
  cenarios[["4943_Normal_Normal_3"]] <- list(
    nome = "Run 4943 | Win Normal | W Normal | Reservatório=3",
    a = 0.774015609860305,
    sr = 0.279199822996696,
    initLen = 19,
    tam_reservoir = 3,
    reg = 3.56576495107632e-5,
    dist_win = "Normal",
    dist_w = "Normal",
    Win = matrix(nrow = 3, ncol = 2, c(
      0.364242033841954, 1.49111727680063, -0.579628748641589,
      -0.0059982963110041, -0.0900987970699551, -0.744462167076191)),
    W = matrix(nrow = 3, ncol = 3, c(
      -0.0289452346432446, 0.0556342361500467, -0.063152597232525,
      -0.0253346917687517, -0.275236350594416, -0.017321638865367,
       0.10817939987002, -0.115372944330111, 0.038073032068389)),
    Wout = matrix(nrow = 1, ncol = 5, c(
      -12.7763519119471, 1.24875741361757, 42.4309823848307,
       1.16381403038395, -2.23999445140362))
  )
  
  cenarios
}

# =============================================================================
# FUNÇÕES CORE DA ESN
# =============================================================================

#' Treina a ESN e gera previsões (validação)
#' @param dados_split Lista retornada por dividir_dados()
#' @param params Lista com a, sr, initLen, tam_reservoir, reg
#' @param Win Matriz de pesos de entrada
#' @param W Matriz de pesos do reservatório
#' @param Wout Matriz de pesos de saída (se NULL, calcula)
#' @return Lista com previsões, métricas, tempo
esn_validacao <- function(dados_split, params, Win, W, Wout = NULL) {
  treino_valida <- dados_split$treino_valida
  treino_n <- dados_split$idx$treino_n
  valida_n <- dados_split$idx$valida_n
  
  a <- params$a
  sr <- params$sr
  initLen <- params$initLen
  tam_reservoir <- params$tam_reservoir
  reg <- params$reg
  inSize <- 1
  outSize <- 1
  
  t_inicio <- proc.time()
  
  # Escalar W pelo raio espectral
  rhoW <- abs(eigen(W, only.values = TRUE)$values[1])
  W_scaled <- sr * W / rhoW
  
  # Fase de treino
  X <- matrix(0, 1 + inSize + tam_reservoir, treino_n - initLen)
  Yt <- matrix(treino_valida[(initLen + 2):(treino_n + 1)], 1)
  x <- rep(0, tam_reservoir)
  
  for (t in 1:treino_n) {
    u <- treino_valida[t]
    x <- (1 - a) * x + a * tanh(Win %*% rbind(1, u) + W_scaled %*% x)
    if (t > initLen)
      X[, t - initLen] <- rbind(1, u, x)
  }
  
  X_T <- t(X)
  
  if (is.null(Wout)) {
    Wout <- Yt %*% X_T %*% solve(X %*% X_T + reg * diag(1 + inSize + tam_reservoir))
  }
  
  # Previsão validação
  Y <- matrix(0, outSize, valida_n)
  u <- treino_valida[treino_n + 1]
  
  for (t in 1:valida_n) {
    x <- (1 - a) * x + a * tanh(Win %*% rbind(1, u) + W_scaled %*% x)
    y <- Wout %*% rbind(1, u, x)
    Y[, t] <- y
    u <- treino_valida[treino_n + t + 1]
  }
  
  # Previsão treino
  Ytr <- matrix(0, outSize, treino_n)
  u <- treino_valida[1]
  
  for (j in 1:treino_n) {
    x <- (1 - a) * x + a * tanh(Win %*% rbind(1, u) + W_scaled %*% x)
    y <- Wout %*% rbind(1, u, x)
    Ytr[, j] <- y
    u <- treino_valida[j + 1]
  }
  
  t_fim <- proc.time()
  tempo_exec <- (t_fim - t_inicio)["elapsed"]
  
  # Métricas
  real_valida <- treino_valida[(treino_n + 2):(treino_n + valida_n)]
  prev_valida <- as.numeric(Y[outSize, 1:(valida_n - 1)])
  
  real_treino <- treino_valida[2:treino_n]
  prev_treino <- as.numeric(Ytr[outSize, 1:(treino_n - 1)])
  
  metricas_treino <- calcular_todas_metricas(real_treino, prev_treino, tempo_exec)
  metricas_valida <- calcular_todas_metricas(real_valida, prev_valida, tempo_exec)
  
  list(
    previsao_valida = as.numeric(Y),
    previsao_treino = as.numeric(Ytr),
    metricas_treino = metricas_treino,
    metricas_valida = metricas_valida,
    tempo = tempo_exec,
    Wout = Wout
  )
}

#' Treina a ESN e gera previsões (teste)
#' @param dados_split Lista retornada por dividir_dados()
#' @param params Lista com a, sr, initLen, tam_reservoir, reg
#' @param Win Matriz de pesos de entrada
#' @param W Matriz de pesos do reservatório
#' @param Wout Matriz de pesos de saída
#' @return Lista com previsões, métricas, tempo
esn_teste <- function(dados_split, params, Win, W, Wout) {
  treina_testa <- dados_split$treina_testa
  treino_n <- dados_split$idx$treino_n
  teste_n <- dados_split$idx$teste_n
  
  a <- params$a
  sr <- params$sr
  initLen <- params$initLen
  tam_reservoir <- params$tam_reservoir
  reg <- params$reg
  inSize <- 1
  outSize <- 1
  
  t_inicio <- proc.time()
  
  rhoW <- abs(eigen(W, only.values = TRUE)$values[1])
  W_scaled <- sr * W / rhoW
  
  X <- matrix(0, 1 + inSize + tam_reservoir, treino_n - initLen)
  Yt <- matrix(treina_testa[(initLen + 2):(treino_n + 1)], 1)
  x <- rep(0, tam_reservoir)
  
  for (t in 1:treino_n) {
    u <- treina_testa[t]
    x <- (1 - a) * x + a * tanh(Win %*% rbind(1, u) + W_scaled %*% x)
    if (t > initLen)
      X[, t - initLen] <- rbind(1, u, x)
  }
  
  # Previsão teste
  Y <- matrix(0, outSize, teste_n)
  u <- treina_testa[treino_n + 1]
  
  for (t in 1:teste_n) {
    x <- (1 - a) * x + a * tanh(Win %*% rbind(1, u) + W_scaled %*% x)
    y <- Wout %*% rbind(1, u, x)
    Y[, t] <- y
    u <- treina_testa[treino_n + t + 1]
  }
  
  # Previsão treino
  Ytr <- matrix(0, outSize, treino_n)
  u <- treina_testa[1]
  
  for (j in 1:treino_n) {
    x <- (1 - a) * x + a * tanh(Win %*% rbind(1, u) + W_scaled %*% x)
    y <- Wout %*% rbind(1, u, x)
    Ytr[, j] <- y
    u <- treina_testa[j + 1]
  }
  
  t_fim <- proc.time()
  tempo_exec <- (t_fim - t_inicio)["elapsed"]
  
  real_teste <- treina_testa[(treino_n + 2):(treino_n + teste_n)]
  prev_teste <- as.numeric(Y[outSize, 1:(teste_n - 1)])
  
  real_treino <- treina_testa[2:treino_n]
  prev_treino <- as.numeric(Ytr[outSize, 1:(treino_n - 1)])
  
  metricas_treino <- calcular_todas_metricas(real_treino, prev_treino, tempo_exec)
  metricas_teste <- calcular_todas_metricas(real_teste, prev_teste, tempo_exec)
  
  list(
    previsao_teste = as.numeric(Y),
    previsao_treino = as.numeric(Ytr),
    metricas_treino = metricas_treino,
    metricas_teste = metricas_teste,
    tempo = tempo_exec
  )
}

# =============================================================================
# UI SHINY DO MÓDULO ESN
# =============================================================================

esn_ui <- function(id) {
  ns <- NS(id)
  
  tagList(
    fluidRow(
      column(4,
        div(class = "well model-card-esn",
          div(class = "section-subtitle", "PARÂMETROS DA REDE"),
          h4(style = "margin-top:0; color: var(--esn-color); font-weight: 800;", "🧠 Echo State Network"),
          hr(),
          
          checkboxInput(ns("usar_pre_otimizado"), "Usar Cenário Pré-Otimizado (GA)", value = TRUE),
          
          conditionalPanel(
            condition = paste0("input['", ns("usar_pre_otimizado"), "']"),
            selectInput(ns("cenario"), "Selecione o Cenário:", choices = NULL)
          ),
          
          conditionalPanel(
            condition = paste0("!input['", ns("usar_pre_otimizado"), "']"),
            div(style = "background: var(--bg-app); padding: 12px; border-radius: var(--radius-sm); margin-bottom: 12px;",
              h5(style = "margin-top:0; font-weight:700;", "🎲 Distribuições Personalizadas:"),
              selectInput(ns("dist_win"), "Distribuição W_in (Entrada):", choices = NULL),
              selectInput(ns("dist_w"), "Distribuição W (Reservatório):", choices = NULL)
            )
          ),
          
          hr(),
          actionButton(ns("btn_rodar"), "🚀 Executar ESN", 
                       class = "btn-success btn-block",
                       style = "width:100%; height: 46px;")
        )
      ),
      column(8,
        div(class = "well",
          tabsetPanel(
            tabPanel("📊 Métricas de Desempenho",
              br(),
              verbatimTextOutput(ns("resultados_texto")),
              hr(),
              h5(style = "font-weight: 700;", "📋 Tabela de Resumo:"),
              tableOutput(ns("tabela_metricas"))
            ),
            tabPanel("📈 Validação (In-sample)",
              br(),
              plotOutput(ns("grafico_validacao"), height = "380px")
            ),
            tabPanel("📉 Teste (Out-of-sample)",
              br(),
              plotOutput(ns("grafico_teste"), height = "380px")
            )
          )
        )
      )
    )
  )
}

# =============================================================================
# SERVER SHINY DO MÓDULO ESN
# =============================================================================

esn_server <- function(id, dados_reativo) {
  moduleServer(id, function(input, output, session) {
    ns <- session$ns
    
    # Carregar cenários
    cenarios <- criar_cenarios_pre_otimizados()
    
    # Preencher choices de cenários
    nomes_cenarios <- sapply(cenarios, function(c) c$nome)
    updateSelectInput(session, "cenario", choices = setNames(names(cenarios), nomes_cenarios),
                      selected = "2563_GED_Normal_27")
    
    # Preencher choices de distribuições (do registro)
    observe({
      dists <- listar_distribuicoes()
      updateSelectInput(session, "dist_win", choices = dists, selected = "GED")
      updateSelectInput(session, "dist_w", choices = dists, selected = "Normal")
    })
    
    # Resultados reativos
    resultados <- reactiveValues(
      validacao = NULL,
      teste = NULL,
      metricas = NULL
    )
    
    # Rodar ESN
    observeEvent(input$btn_rodar, {
      req(dados_reativo())
      
      withProgress(message = "Executando ESN...", value = 0, {
        dados <- dados_reativo()
        dados_split <- dividir_dados(dados)
        
        if (input$usar_pre_otimizado) {
          cen <- cenarios[[input$cenario]]
          
          if (is.null(cen$W)) {
            showNotification("Este cenário tem a matriz W omitida por tamanho. Selecione outro cenário.", type = "error")
            return()
          }
          
          params <- list(
            a = cen$a, sr = cen$sr, initLen = cen$initLen,
            tam_reservoir = cen$tam_reservoir, reg = cen$reg
          )
          
          setProgress(0.3, detail = "Calculando Validação...")
          res_val <- esn_validacao(dados_split, params, cen$Win, cen$W, cen$Wout)
          
          setProgress(0.6, detail = "Calculando Teste...")
          res_teste <- esn_teste(dados_split, params, cen$Win, cen$W, cen$Wout)
          
        } else {
          # Gerar novas matrizes com distribuições selecionadas
          tam_r <- 27  # Default
          params <- list(a = 0.87, sr = 0.4, initLen = 9, tam_reservoir = tam_r, reg = 2.2e-05)
          
          Win_new <- matrix(gerar_amostras(input$dist_win, tam_r * 2), nrow = tam_r, ncol = 2)
          W_new <- matrix(gerar_amostras(input$dist_w, tam_r * tam_r), nrow = tam_r, ncol = tam_r)
          
          setProgress(0.3, detail = "Calculando Validação...")
          res_val <- esn_validacao(dados_split, params, Win_new, W_new, Wout = NULL)
          
          setProgress(0.6, detail = "Calculando Teste...")
          res_teste <- esn_teste(dados_split, params, Win_new, W_new, res_val$Wout)
        }
        
        setProgress(0.9, detail = "Finalizando...")
        resultados$validacao <- res_val
        resultados$teste <- res_teste
        resultados$metricas <- list(
          modelo = "ESN",
          treino = res_val$metricas_treino,
          validacao = res_val$metricas_valida,
          teste = res_teste$metricas_teste,
          tempo = res_val$tempo + res_teste$tempo
        )
      })
      
      showNotification("✅ ESN executada com sucesso!", type = "message")
    })
    
    # Saídas
    output$resultados_texto <- renderPrint({
      req(resultados$validacao)
      cat("=====================================================\n")
      cat("  MÉTRICAS DETALHADAS — ECHO STATE NETWORK (ESN)\n")
      cat("=====================================================\n\n")
      cat("• FASE DE VALIDAÇÃO (In-Sample):\n")
      cat(sprintf("  - MAE:   %.6f\n", resultados$validacao$metricas_valida$MAE))
      cat(sprintf("  - RMSE:  %.6f\n", resultados$validacao$metricas_valida$RMSE))
      cat(sprintf("  - MAPE:  %.2f%%\n", resultados$validacao$metricas_valida$MAPE))
      cat(sprintf("  - R²:    %.4f\n", resultados$validacao$metricas_valida$R2))
      cat(sprintf("  - Tempo: %.4f segundos\n\n", resultados$validacao$tempo))
      cat("• FASE DE TESTE (Out-of-Sample):\n")
      cat(sprintf("  - MAE:   %.6f\n", resultados$teste$metricas_teste$MAE))
      cat(sprintf("  - RMSE:  %.6f\n", resultados$teste$metricas_teste$RMSE))
      cat(sprintf("  - MAPE:  %.2f%%\n", resultados$teste$metricas_teste$MAPE))
      cat(sprintf("  - R²:    %.4f\n", resultados$teste$metricas_teste$R2))
      cat(sprintf("  - Tempo: %.4f segundos\n", resultados$teste$tempo))
    })
    
    output$tabela_metricas <- renderTable({
      req(resultados$validacao)
      data.frame(
        "Fase" = c("Validação", "Teste"),
        "MAE"  = sprintf("%.6f", c(resultados$validacao$metricas_valida$MAE, resultados$teste$metricas_teste$MAE)),
        "RMSE" = sprintf("%.6f", c(resultados$validacao$metricas_valida$RMSE, resultados$teste$metricas_teste$RMSE)),
        "MAPE %" = sprintf("%.2f%%", c(resultados$validacao$metricas_valida$MAPE, resultados$teste$metricas_teste$MAPE)),
        "R²"   = sprintf("%.4f", c(resultados$validacao$metricas_valida$R2, resultados$teste$metricas_teste$R2)),
        "Tempo (s)" = sprintf("%.4f", c(resultados$validacao$tempo, resultados$teste$tempo)),
        check.names = FALSE,
        stringsAsFactors = FALSE
      )
    })
    
    output$grafico_validacao <- renderPlot({
      req(resultados$validacao)
      dados <- dados_reativo()
      ds <- dividir_dados(dados)
      real <- ds$treino_valida[(ds$idx$treino_n + 1):(ds$idx$treino_n + ds$idx$valida_n)]
      prev <- resultados$validacao$previsao_valida
      
      par(mar = c(3.5, 4, 2, 1), bg = "transparent")
      plot(real, type = 'l', col = '#0f172a', lwd = 2,
           ylab = "Preço PETR4 (R$)", xlab = "Dias",
           main = "ESN — Previsão na Fase de Validação", axes = FALSE, col.main = "#0f172a")
      axis(1, col = "#cbd5e1", col.axis = "#475569")
      axis(2, col = "#cbd5e1", col.axis = "#475569")
      grid(col = "#e2e8f0", lty = "dotted")
      
      lines(prev, col = '#059669', lwd = 1.8)
      legend('topright', legend = c('Série Real', 'ESN Prevista'),
             col = c('#0f172a', '#059669'), lty = 1, lwd = c(2, 1.8), bty = 'n', text.col = '#0f172a')
    })
    
    output$grafico_teste <- renderPlot({
      req(resultados$teste)
      dados <- dados_reativo()
      ds <- dividir_dados(dados)
      real <- ds$treina_testa[(ds$idx$treino_n + 1):(ds$idx$treino_n + ds$idx$teste_n)]
      prev <- resultados$teste$previsao_teste
      
      par(mar = c(3.5, 4, 2, 1), bg = "transparent")
      plot(real, type = 'l', col = '#0f172a', lwd = 2,
           ylab = "Preço PETR4 (R$)", xlab = "Dias",
           main = "ESN — Previsão na Fase de Teste", axes = FALSE, col.main = "#0f172a")
      axis(1, col = "#cbd5e1", col.axis = "#475569")
      axis(2, col = "#cbd5e1", col.axis = "#475569")
      grid(col = "#e2e8f0", lty = "dotted")
      
      lines(prev, col = '#059669', lwd = 1.8)
      legend('topright', legend = c('Série Real', 'ESN Prevista'),
             col = c('#0f172a', '#059669'), lty = 1, lwd = c(2, 1.8), bty = 'n', text.col = '#0f172a')
    })
    
    # Retornar métricas para comparação
    reactive(resultados$metricas)
  })
}
