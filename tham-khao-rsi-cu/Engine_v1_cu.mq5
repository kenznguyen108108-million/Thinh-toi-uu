<code id="src">//+------------------------------------------------------------------+
//|  ThinhTrading_Engine_v1.mq5                                      |
//|  GIAI DOAN 1 - ENGINE NHAN DIEN THI TRUONG (CHUA DAT LENH)       |
//|                                                                  |
//|  Muc dich: chi phat hien & ghi log cac tin hieu theo dung        |
//|  "00-DAC-TA-CHINH-THUC.md":                                      |
//|   - RSI(14) + EMA9(RSI) + WMA45(RSI) tren tung khung             |
//|   - Cau truc dinh/day (swing, fractal)                          |
//|   - 5 loai mo hinh (muc 6) + dong thuan da khung cho MH1/MH2    |
//|   - May trang thai quan tinh CO NHO + co canh bao "dang suy yeu" |
//|   - ADX(14) cheo kiem                                           |
//|   - Cung pha / nguoc pha giua khung giua va khung lon            |
//|                                                                  |
//|  KHONG dat lenh, KHONG tinh SL/TP/runner/lot - de danh gia rieng |
//|  xem engine "doc" thi truong dung chua truoc khi dong tien vao.  |
//|                                                                  |
//|  CACH DUNG:                                                      |
//|   1. Copy vao MQL5\Experts\ThinhTrading_Engine_v1.mq5            |
//|   2. Compile (F7) trong MetaEditor. Neu loi, gui em bao loi.     |
//|   3. Mo Strategy Tester (Ctrl+R) -> chon EA nay -> symbol BTC    |
//|      cua broker -> gan len chart M5 -> Model "1 minute OHLC"     |
//|      -> bat "Visual mode" de xem truc tiep tren chart.           |
//|   4. Thong so danh dau [CAN-BACKTEST] la CHUA CO SO CHOT - em dat     |
//|      khoi diem hop ly, dung tinh nang Optimization cua MT5 de     |
//|      tu tim so tot hon tren chinh data cua anh sau nay.           |
//|   5. Log CSV nam trong Common\Files (khong phai MQL5\Files) khi  |
//|      InpLogToCommonFolder = true.                                |
//+------------------------------------------------------------------+
#property copyright "System Thinhtrading - Engine v1 (nhan dien, chua giao dich)"
#property version   "1.00"
#property strict

//====================================================================
// INPUTS
//====================================================================
input string InpSymbol           = "";    // de trong = symbol cua chart dang gan EA

input bool   InpRunA = true;   // Setup A: M5/M15/H1
input bool   InpRunB = true;   // Setup B: M15/H1/H4
input bool   InpRunC = true;   // Setup C: H1/H4/1D
input bool   InpRunD = true;   // Setup D: H4/1D/1W

input int    InpRSIPeriod        = 14;    // DA CHOT
input int    InpEMAFastPeriod    = 9;     // DA CHOT (DTB nhanh tren RSI)
input int    InpWMASlowPeriod    = 45;    // DA CHOT (DTB cham tren RSI)

input int    InpADXPeriod        = 14;    // DA CHOT (period)
input double InpADXStrong        = 25.0;  // [CAN-BACKTEST] nguong ADX manh - CAN OPTIMIZE.
                                          // Do tren 46 ngay M15: muc 25 cho ra 56.7% so nen la "trend manh"
                                          // -> gan nhu khong loc duoc gi. Nhieu kha nang phai nang len 30-35
                                          // cho BTC. Hien chi GHI LOG, chua dung de chan tin hieu.
input double InpADXWeak          = 20.0;  // [CAN-BACKTEST] nguong ADX yeu/khong trend - CAN OPTIMIZE

input int    InpFractalWing      = 2;     // so nen 2 ben de xac nhan 1 swing (fractal N)
input int    InpMinBarsInZone    = 2;     // [DO TU LOG] so nen toi thieu RSI o vung 70/30 de bat quan tinh.
                                          // Do tren 46 ngay M15: 129 lan vao vung, do dai trung vi = 2 nen,
                                          // chi 36% keo dai >=3 nen. De 3 thi bo mat 64% so lan co quan tinh.
input double InpDTBFarThreshold  = 9.0;   // [DO TU LOG] khoang cach EMA9(RSI)-WMA45(RSI) duoc tinh la "xa".
                                          // Do tren 46 ngay M15: trung vi 4.1, p75=6.8, p90=9.9, max=19.6.
                                          // Muc 15.0 cu la qua cao (chi ~2% so nen dat duoc).

input int    InpATRPeriod            = 14;   // ATR chi con dung cho runner sau nay + ghi log

//--- VUNG KC/HT: NEO THEO CON SONG (thay hoan toan cach quet lich su cu) ---
// Anh chot: khong di tim vung trong qua khu. Lay CHINH con song dang chay,
// bat dau tu luc "RSI cam dau xuong" (hoac cam dau len), roi suy ra cac muc
// phia truoc theo thu tu. Cach nay KHONG can mot con so tuy tien nao.
//   Muc 1 = dinh/day trung gian gan nhat (diem dau tien gia phai vuot)
//   Muc 2 = Fibo 0.5 cua con song
//   Muc 3 = diem bat dau con song (Fibo 1.0)
// Hai cach xac dinh "cam dau xuong" deu duoc GHI LOG song song de data tu chon:
//   V1 = RSI cat xuong duoi CA HAI duong trung binh
//   V2 = EMA9(RSI) cat xuong WMA45(RSI)
input double InpFiboLevel        = 0.5;   // muc Fibo giua (anh neu 0.5)
input bool   InpLogWaveLevels    = true;  // ghi cac muc cua ca 2 cach neo

input int    InpMultiTFLookbackBars  = 30;   // khung lon: cross cung chieu trong bao nhieu nen gan day thi tinh la "dong thuan"

//--- BO DO PHAN BO R (de quyet dinh TP bang thong ke thuc te) ---
// Muc dich: tra loi cau hoi "bao nhieu % tin hieu di toi 1.5R / 2R / 3R / 6R"
// TRUOC khi cham SL. Con so nay KHONG phu thuoc TP dang dat la bao nhieu,
// nen khong bi vong tron voi bo loc vao lenh R>=2.
// LUU Y QUAN TRONG: day la lenh GIAY, khong dat lenh that. Entry lay tai
// dong nen KHUNG GIUA (chua co logic tim entry o khung nho), nen R o day
// la UOC LUONG THAP HON thuc te - entry khung nho se cho SL sat hon.
input bool   InpPaperTrade       = true;  // bat/tat bo do (tat neu nghi no gay loi)
input int    InpPaperMaxBars     = 100000; // theo doi toi khi cham SL moi thoi.
                                          // SUA: truoc de 300 nen -> cat cut dung cac lenh chay xa nhat.
                                          // Do lai: 18% lenh bi cat khi dang o 5.46R va van con chay.
input int    InpRetestMaxBars    = 30;    // BO 5: cho toi da bao nhieu nen KHUNG NHO de gia hoi ve.
                                          // Qua han thi bo lenh va ghi "KHONG_RETEST" de dem ty le bo lo.
input double InpBufferA          = 50;    // buffer SL setup A (USD gia BTC)
input double InpBufferB          = 100;   // buffer SL setup B
input double InpBufferC          = 200;   // buffer SL setup C
input double InpBufferD          = 300;   // buffer SL setup D

input bool   InpWriteCSVLog      = true;
input bool   InpLogToCommonFolder= true;  // QUAN TRONG khi chay Strategy Tester: true = ghi vao Common\Files
                                          // (neu false, file log bi ket trong thu muc rieng cua tester agent, rat kho tim)
input string InpLogSuffix        = "";    // them nhan vao ten file de khong ghi de log lan chay truoc (vd "2024_2025")
input bool   InpShowComment      = true;
input int    InpMaxSwingsStored  = 20;    // so swing gan nhat luu lai moi khung
                                          // (nang tu 8 len 20: song dai co nhieu swing,
                                          //  de 8 thi mat dinh trung gian can cho Muc 1)
input int    InpBufferBars       = 500;   // so nen lay ve moi khung de tinh toan

//====================================================================
// ENUM
//====================================================================
//--------------------------------------------------------------------
// TRANG THAI QUAN TINH - day la TRANG THAI CO NHO (latched).
// Mot khi quan tinh da bat, no GIU NGUYEN ke ca khi RSI da roi khoi
// vung 70/30 - dung y anh: "doan tau dang chay khong dung mot phat
// duoc". No chi tat khi co su kien lam no het quan tinh.
//
// LUU Y: "song rui ro" va "quan tinh can kiet" KHONG nam trong enum
// nay. Chung la 1 CO CANH BAO chay song song ben trong quan tinh
// (xem bien dangSuyYeu), khong phai trang thai tranh cho.
//--------------------------------------------------------------------
enum ENUM_MOMENTUM_STATE
  {
   MOM_NONE,       // chua xac dinh
   MOM_TANG,       // quan tinh tang dang con hieu luc
   MOM_GIAM,       // quan tinh giam dang con hieu luc
   MOM_HET_TANG,   // gia van tao DINH MOI nhung RSI khong con vao lai vung >70
   MOM_HET_GIAM    // gia van tao DAY MOI nhung RSI khong con vao lai vung <30
  };

enum ENUM_MOHINH
  {
   MH_NONE,
   MH1_RESET_TANG_CAT_XUONG,   // het quan tinh tang, RSI cat XUONG 2 DTB -> dao chieu giam
   MH2_RESET_GIAM_CAT_LEN,     // het quan tinh giam, RSI cat LEN 2 DTB -> dao chieu tang
   MH3_TIEP_DIEN_CHO_RESET,    // con quan tinh, dang cho reset de vao lai (tiep dien)
   MH4_DINH_DAY_THAP_DAN,
   MH5_DINH_DAY_CAO_DAN
  };

//====================================================================
// CAU TRUC DU LIEU
//====================================================================
#define N_TF 6
ENUM_TIMEFRAMES g_tfEnum[N_TF] = {PERIOD_M5, PERIOD_M15, PERIOD_H1, PERIOD_H4, PERIOD_D1, PERIOD_W1};
string          g_tfName[N_TF] = {"M5","M15","H1","H4","D1","W1"};

int g_hRSI[N_TF];
int g_hADX[N_TF];
int g_hATR[N_TF];

struct SwingPoint
  {
   datetime time;
   double   price;
   double   rsiAtSwing;
   bool     isHigh;
  };

// Trang thai luu lai cho moi khung thoi gian
struct TFState
  {
   datetime lastClosedBarTime;
   double   rsi;         // RSI cua nen vua dong (shift=1)
   double   rsiPrev;      // RSI cua nen dong truoc do (shift=2)
   double   emaFast;      // EMA9(RSI) tai shift=1
   double   emaFastPrev;
   double   wmaSlow;      // WMA45(RSI) tai shift=1
   double   wmaSlowPrev;
   double   adx;
   double   atr;
   int      barsInZone70;    // so nen lien tiep RSI>=70 (tinh den nen vua dong)
   int      barsInZone30;    // so nen lien tiep RSI<=30
   ENUM_MOMENTUM_STATE momState;   // trang thai CO NHO, chi doi khi co su kien
   bool     dangSuyYeu;      // co canh bao chay SONG SONG trong quan tinh:
                             //  - trong quan tinh TANG  = "song rui ro" (dinh gia cao dan, dinh RSI thap dan)
                             //  - trong quan tinh GIAM  = "can kiet"    (day gia thap dan, day RSI cao dan)
                             // Day la 2 ten anh dat cho cung 1 co che, soi guong qua nhau.
   int      lastCrossDir;    // +1 = EMA9 vua cat len WMA45 tai nen vua dong, -1 = cat xuong, 0 = khong cat
   int      crossDirRecent;  // huong cat gan nhat trong InpMultiTFLookbackBars nen (de xet dong thuan)
   SwingPoint swingHighs[];  // luu tu cu->moi, phan tu cuoi la moi nhat
   SwingPoint swingLows[];
   bool     initialized;

   // --- NEO SONG cho vung KC/HT (mo ta cua anh: bat dau tu luc RSI cam dau) ---
   // V1 = RSI cat xuong/len CA HAI duong trung binh
   int      waveDirV1;      // -1 song giam, +1 song tang, 0 chua co
   double   waveOrgV1;      // gia tai diem bat dau song
   double   waveExtV1;      // day thap nhat (song giam) / dinh cao nhat (song tang) ke tu do
   datetime waveTimeV1;
   // V2 = EMA9(RSI) cat WMA45(RSI)
   int      waveDirV2;
   double   waveOrgV2;
   double   waveExtV2;
   datetime waveTimeV2;

   // --- CON SONG VUA HOAN THANH (day moi la cai dung de tinh muc TP) ---
   // SUA LOI: ban truoc lay muc TP tu con song MOI vua mo ra ngay tai
   // khoanh khac co tin hieu -> cac muc roi het sang phia SAU lung gia
   // (100% lech huong). Dung y anh: sau 1 con song giam dai, khi day 2
   // quay len thi cac KHANG CU phia truoc lay tu chinh CON SONG GIAM DO.
   int      prevDirV1; double prevOrgV1; double prevExtV1; datetime prevT0V1; datetime prevT1V1;
   int      prevDirV2; double prevOrgV2; double prevExtV2; datetime prevT0V2; datetime prevT1V2;
  };

TFState g_st[N_TF];

struct SetupDef
  {
   string name;
   int    idxSmall;
   int    idxMid;
   int    idxLarge;
   bool   enabled;
  };

SetupDef g_setup[4];

//--- LENH GIAY - KHONG dat lenh that, chi de DO ---
// Moi tin hieu sinh ra 2 lenh giay de so truc tiep:
//   "NGAY"   = vao ngay tai gia dong nen khung giua (cach cu, de doi chieu)
//   "RETEST" = cho gia hoi ve tao cau truc o KHUNG NHO roi moi vao -> SL hep hon
// Tren moi lenh, do SONG SONG nhieu cach thoat khac nhau. Cung 1 lenh,
// cung entry, cung SL - chi khac cach thoat - nen so sanh moi sach.
struct PaperTrade
  {
   bool     active;
   int      setupIdx;
   int      dir;            // +1 buy, -1 sell
   string   loaiVao;        // "NGAY" hoac "RETEST"
   datetime timeIn;
   double   entry;
   double   sl;
   double   rUnit;          // |entry - sl|, don vi USD gia BTC
   int      bars;
   string   mohinh;

   // BO 3 - chay toi cung, khong gioi han thoi gian (tran tham chieu)
   double   mfeR;

   // BO 4 - cac muc KC/HT neo theo song, khoang cach tinh bang R
   double   lvl1R, lvl2R, lvl3R;

   // BO 1 - day swing dau tien (luat cua anh).
   // Day1 chi duoc TINH khi gia tao dinh moi pha qua Dinh1.
   // Do 4 bien the cung luc, khong ep chon truoc:
   //   A = giu nguyen Day1 , quet bang RAU nen
   //   B = giu nguyen Day1 , quet bang DONG nen
   //   C = doi theo day moi, quet bang RAU nen
   //   D = doi theo day moi, quet bang DONG nen
   int      s1State;        // 0 chua co Dinh1 | 1 co Dinh1 | 2 co Day1 | 3 Day1 hop le
   double   s1Dinh1;
   double   s1Day1;         // day co dinh (bien the A,B)
   double   s1DayTrail;     // day doi dan  (bien the C,D)
   datetime s1TimeDinh1;
   double   s1RA, s1RB, s1RC, s1RD;
   bool     s1XongA, s1XongB, s1XongC, s1XongD;
  };
PaperTrade g_paper[];

// Hang cho vao lenh theo RETEST: tin hieu da co, dang doi khung nho hoi ve.
struct ChoRetest
  {
   bool     active;
   int      setupIdx;
   int      dir;
   datetime timeTinHieu;
   string   mohinh;
   int      soNenCho;
   double   lvl1R, lvl2R, lvl3R;   // chot tai thoi diem co tin hieu
  };
ChoRetest g_cho[];

string   g_symbol;
int      g_csvHandle   = INVALID_HANDLE;
int      g_paperHandle = INVALID_HANDLE;

//====================================================================
// OnInit
//====================================================================
int OnInit()
  {
   g_symbol = (InpSymbol == "" ? _Symbol : InpSymbol);
   if(!SymbolSelect(g_symbol, true))
     {
      PrintFormat("Khong tim thay symbol '%s'.", g_symbol);
      return(INIT_FAILED);
     }

   for(int i = 0; i < N_TF; i++)
     {
      g_hRSI[i] = iRSI(g_symbol, g_tfEnum[i], InpRSIPeriod, PRICE_CLOSE);
      g_hADX[i] = iADX(g_symbol, g_tfEnum[i], InpADXPeriod);
      g_hATR[i] = iATR(g_symbol, g_tfEnum[i], InpATRPeriod);
      if(g_hRSI[i] == INVALID_HANDLE || g_hADX[i] == INVALID_HANDLE || g_hATR[i] == INVALID_HANDLE)
        {
         PrintFormat("Khong tao duoc indicator handle cho khung %s.", g_tfName[i]);
         return(INIT_FAILED);
        }
      g_st[i].lastClosedBarTime = 0;
      g_st[i].initialized = false;
      g_st[i].barsInZone70 = 0;
      g_st[i].barsInZone30 = 0;
      g_st[i].crossDirRecent = 0;
      g_st[i].momState     = MOM_NONE;
      g_st[i].dangSuyYeu   = false;
      g_st[i].lastCrossDir = 0;
      g_st[i].waveDirV1 = 0; g_st[i].waveOrgV1 = 0; g_st[i].waveExtV1 = 0; g_st[i].waveTimeV1 = 0;
      g_st[i].waveDirV2 = 0; g_st[i].waveOrgV2 = 0; g_st[i].waveExtV2 = 0; g_st[i].waveTimeV2 = 0;
      g_st[i].prevDirV1 = 0; g_st[i].prevOrgV1 = 0; g_st[i].prevExtV1 = 0; g_st[i].prevT0V1 = 0; g_st[i].prevT1V1 = 0;
      g_st[i].prevDirV2 = 0; g_st[i].prevOrgV2 = 0; g_st[i].prevExtV2 = 0; g_st[i].prevT0V2 = 0; g_st[i].prevT1V2 = 0;
      ArrayResize(g_st[i].swingHighs, 0);
      ArrayResize(g_st[i].swingLows, 0);
     }

   // Index trong g_tfEnum: 0=M5 1=M15 2=H1 3=H4 4=D1 5=W1
   g_setup[0].name = "A"; g_setup[0].idxSmall = 0; g_setup[0].idxMid = 1; g_setup[0].idxLarge = 2; g_setup[0].enabled = InpRunA;
   g_setup[1].name = "B"; g_setup[1].idxSmall = 1; g_setup[1].idxMid = 2; g_setup[1].idxLarge = 3; g_setup[1].enabled = InpRunB;
   g_setup[2].name = "C"; g_setup[2].idxSmall = 2; g_setup[2].idxMid = 3; g_setup[2].idxLarge = 4; g_setup[2].enabled = InpRunC;
   g_setup[3].name = "D"; g_setup[3].idxSmall = 3; g_setup[3].idxMid = 4; g_setup[3].idxLarge = 5; g_setup[3].enabled = InpRunD;

   if(InpWriteCSVLog)
     {
      string clean = g_symbol;
      StringReplace(clean, ".", "_");
      StringReplace(clean, "#", "_");
      string suffix = (InpLogSuffix == "" ? "" : "_" + InpLogSuffix);
      string fname = StringFormat("ThinhTrading_EngineLog_%s%s.csv", clean, suffix);

      int logFlags = FILE_WRITE | FILE_CSV | FILE_ANSI;
      if(InpLogToCommonFolder) logFlags |= FILE_COMMON;

      g_csvHandle = FileOpen(fname, logFlags, ",");
      if(g_csvHandle == INVALID_HANDLE)
         PrintFormat("Khong mo duoc file log %s. Loi=%d", fname, GetLastError());
      else
        {
         FileWrite(g_csvHandle, "time_mid_tf_closed", "setup", "tf_small", "tf_mid", "tf_large",
                   "mohinh", "cat_khung_giua", "dong_thuan_khung_lon", "phase_mid_vs_large",
                   "mom_small", "mom_mid", "mom_large",
                   "suy_yeu_mid", "suy_yeu_large",
                   "rsi_mid", "ema9_mid", "wma45_mid", "dtb_distance_mid",
                   "adx_small", "adx_mid", "adx_large", "atr_mid",
                   "v1_huong_song", "v1_muc1_trung_gian", "v1_muc2_fibo", "v1_muc3_goc",
                   "v2_huong_song", "v2_muc1_trung_gian", "v2_muc2_fibo", "v2_muc3_goc");
         PrintFormat("Log CSV: %s  ->  %s", fname,
                     (InpLogToCommonFolder
                      ? TerminalInfoString(TERMINAL_COMMONDATA_PATH) + "\\Files"
                      : TerminalInfoString(TERMINAL_DATA_PATH) + "\\MQL5\\Files"));
        }
     }

   ArrayResize(g_paper, 0);
   ArrayResize(g_cho, 0);
   if(InpPaperTrade)
     {
      string clean2 = g_symbol;
      StringReplace(clean2, ".", "_");
      StringReplace(clean2, "#", "_");
      string suffix2 = (InpLogSuffix == "" ? "" : "_" + InpLogSuffix);
      string fname2 = StringFormat("ThinhTrading_PhanBoR_%s%s.csv", clean2, suffix2);
      int flags2 = FILE_WRITE | FILE_CSV | FILE_ANSI;
      if(InpLogToCommonFolder) flags2 |= FILE_COMMON;
      g_paperHandle = FileOpen(fname2, flags2, ",");
      if(g_paperHandle == INVALID_HANDLE)
         PrintFormat("Khong mo duoc file phan bo R %s. Loi=%d", fname2, GetLastError());
      else
        {
         FileWrite(g_paperHandle, "time_vao", "time_ra", "setup", "tf_mid", "loai_vao", "huong", "mohinh",
                   "entry", "sl", "r_unit_usd", "mfe_R", "ket_thuc", "so_nen_giu",
                   "muc1_cach_R", "muc2_cach_R", "muc3_cach_R",
                   "bo1_A_day1_rau", "bo1_B_day1_dongnen", "bo1_C_doiday_rau", "bo1_D_doiday_dongnen",
                   "bo1_trangthai");
         PrintFormat("File phan bo R: %s", fname2);
        }
     }

   PrintFormat("ThinhTrading Engine v1 khoi dong cho symbol %s. Chi nhan dien & log, KHONG dat lenh that.", g_symbol);
   return(INIT_SUCCEEDED);
  }

void OnDeinit(const int reason)
  {
   // dong not cac lenh giay con dang mo de khong mat du lieu
   for(int p = 0; p < ArraySize(g_paper); p++)
      if(g_paper[p].active)
         ClosePaperTrade(p, "CON_DANG_MO");

   if(g_csvHandle != INVALID_HANDLE)   FileClose(g_csvHandle);
   if(g_paperHandle != INVALID_HANDLE) FileClose(g_paperHandle);
  }

//====================================================================
// HELPER: tu tinh EMA va WMA tren 1 mang bat ky
// (KHONG dung <MovingAverages.mqh> - file thu vien do bi loi tren
//  mot so ban cai MT5, nen tu viet cho chac an)
// Mang src[] sap xep TANG DAN theo thoi gian: index 0 = cu nhat.
//====================================================================
void ComputeEMA(const double &src[], const int total, const int period, double &out[])
  {
   ArrayResize(out, total);
   if(total <= 0 || period <= 1) return;
   if(total < period)
     {
      for(int i = 0; i < total; i++) out[i] = src[i];
      return;
     }
   double k = 2.0 / (period + 1.0);
   double sum = 0;
   for(int i = 0; i < period; i++)
     {
      sum += src[i];
      out[i] = src[i];          // vung chua du du lieu: tam gan bang chinh gia tri goc
     }
   out[period - 1] = sum / period;   // hat giong = SMA cua `period` gia tri dau
   for(int i = period; i < total; i++)
      out[i] = src[i] * k + out[i - 1] * (1.0 - k);
  }

void ComputeWMA(const double &src[], const int total, const int period, double &out[])
  {
   ArrayResize(out, total);
   if(total <= 0 || period <= 1) return;
   double wsum = period * (period + 1) / 2.0;
   for(int i = 0; i < total; i++)
     {
      if(i < period - 1) { out[i] = src[i]; continue; }
      double acc = 0;
      for(int j = 0; j < period; j++)
         acc += src[i - j] * (double)(period - j);  // nen moi nhat co trong so lon nhat
      out[i] = acc / wsum;
     }
  }

//====================================================================
// HELPER: fractal swing detection
//====================================================================
bool IsFractalHigh(const double &arr[], const int idx, const int wing, const int total)
  {
   if(idx - wing < 0 || idx + wing >= total) return(false);
   double center = arr[idx];
   for(int k = idx - wing; k <= idx + wing; k++)
     {
      if(k == idx) continue;
      if(arr[k] >= center) return(false);
     }
   return(true);
  }

bool IsFractalLow(const double &arr[], const int idx, const int wing, const int total)
  {
   if(idx - wing < 0 || idx + wing >= total) return(false);
   double center = arr[idx];
   for(int k = idx - wing; k <= idx + wing; k++)
     {
      if(k == idx) continue;
      if(arr[k] <= center) return(false);
     }
   return(true);
  }

// them 1 swing moi vao mang (ring buffer don gian, giu toi da InpMaxSwingsStored)
void PushSwing(SwingPoint &arr[], datetime t, double price, double rsiVal, bool isHigh)
  {
   int n = ArraySize(arr);
   ArrayResize(arr, n + 1);
   arr[n].time = t;
   arr[n].price = price;
   arr[n].rsiAtSwing = rsiVal;
   arr[n].isHigh = isHigh;
   if(ArraySize(arr) > InpMaxSwingsStored)
     {
      for(int k = 0; k < ArraySize(arr) - 1; k++)
         arr[k] = arr[k + 1];
      ArrayResize(arr, InpMaxSwingsStored);
     }
  }

//====================================================================
// Chot lai con song vua ket thuc, TRUOC khi mo con song moi.
// Day chinh la con song dung de tinh cac muc TP.
//====================================================================
void LuuSongVuaXong(const int i, const int variant, const datetime tKetThuc)
  {
   if(variant == 1)
     {
      if(g_st[i].waveDirV1 == 0) return;
      g_st[i].prevDirV1 = g_st[i].waveDirV1;
      g_st[i].prevOrgV1 = g_st[i].waveOrgV1;
      g_st[i].prevExtV1 = g_st[i].waveExtV1;
      g_st[i].prevT0V1  = g_st[i].waveTimeV1;
      g_st[i].prevT1V1  = tKetThuc;
     }
   else
     {
      if(g_st[i].waveDirV2 == 0) return;
      g_st[i].prevDirV2 = g_st[i].waveDirV2;
      g_st[i].prevOrgV2 = g_st[i].waveOrgV2;
      g_st[i].prevExtV2 = g_st[i].waveExtV2;
      g_st[i].prevT0V2  = g_st[i].waveTimeV2;
      g_st[i].prevT1V2  = tKetThuc;
     }
  }

//====================================================================
// Cap nhat 1 khung thoi gian khi co nen moi dong
//====================================================================
void UpdateTF(int i)
  {
   datetime curBarTime = iTime(g_symbol, g_tfEnum[i], 0);
   if(curBarTime == g_st[i].lastClosedBarTime) return; // nen hien tai chua dong (chua co nen moi)
   // Nen o shift=1 vua dong xong

   int need = InpBufferBars;
   double  rsiBuf[], adxBuf[], atrBuf[];
   double  highBuf[], lowBuf[];
   datetime timeBuf[];

   ArraySetAsSeries(rsiBuf, true);
   ArraySetAsSeries(adxBuf, true);
   ArraySetAsSeries(atrBuf, true);
   ArraySetAsSeries(highBuf, true);
   ArraySetAsSeries(lowBuf, true);
   ArraySetAsSeries(timeBuf, true);

   int gotRSI = CopyBuffer(g_hRSI[i], 0, 0, need, rsiBuf);
   int gotADX = CopyBuffer(g_hADX[i], 0, 0, need, adxBuf);
   int gotATR = CopyBuffer(g_hATR[i], 0, 0, need, atrBuf);
   int gotHigh = CopyHigh(g_symbol, g_tfEnum[i], 0, need, highBuf);
   int gotLow  = CopyLow(g_symbol, g_tfEnum[i], 0, need, lowBuf);
   int gotTime = CopyTime(g_symbol, g_tfEnum[i], 0, need, timeBuf);

   int gotMin = gotRSI;
   if(gotADX  < gotMin) gotMin = gotADX;
   if(gotATR  < gotMin) gotMin = gotATR;
   if(gotHigh < gotMin) gotMin = gotHigh;
   if(gotLow  < gotMin) gotMin = gotLow;
   if(gotTime < gotMin) gotMin = gotTime;
   if(gotMin < InpWMASlowPeriod + InpFractalWing + 5) return; // chua du du lieu

   // EMA9(RSI) va WMA45(RSI): can mang KHONG phai series (tang dan theo thoi gian) de dua vao ham co san
   double rsiAsc[];
   ArrayResize(rsiAsc, gotMin);
   for(int k = 0; k < gotMin; k++)
      rsiAsc[k] = rsiBuf[gotMin - 1 - k]; // dao nguoc: index 0 = cu nhat

   double emaAsc[], wmaAsc[];
   ComputeEMA(rsiAsc, gotMin, InpEMAFastPeriod, emaAsc);
   ComputeWMA(rsiAsc, gotMin, InpWMASlowPeriod, wmaAsc);

   // Lay lai gia tri tai nen vua dong (shift=1 trong he series) va nen truoc do (shift=2)
   // Trong mang Asc, "shift=1" (series) tuong ung index (gotMin-1-1)=gotMin-2 ; "shift=2" tuong ung gotMin-3
   int ascIdxShift1 = gotMin - 2;
   int ascIdxShift2 = gotMin - 3;
   if(ascIdxShift2 < 0) return;

   g_st[i].rsiPrev     = g_st[i].rsi;
   g_st[i].emaFastPrev = g_st[i].emaFast;
   g_st[i].wmaSlowPrev = g_st[i].wmaSlow;

   g_st[i].rsi     = rsiAsc[ascIdxShift1];
   g_st[i].emaFast = emaAsc[ascIdxShift1];
   g_st[i].wmaSlow = wmaAsc[ascIdxShift1];
   g_st[i].adx     = adxBuf[1];
   g_st[i].atr     = atrBuf[1];

   double rsiShift2   = rsiAsc[ascIdxShift2];
   double emaShift2   = emaAsc[ascIdxShift2];
   double wmaShift2   = wmaAsc[ascIdxShift2];

   // --- cross detection tren DTB cua RSI ---
   g_st[i].lastCrossDir = 0;
   if(g_st[i].initialized)
     {
      bool wasBelow = (emaShift2 <= wmaShift2);
      bool nowAbove = (g_st[i].emaFast > g_st[i].wmaSlow);
      bool wasAbove = (emaShift2 >= wmaShift2);
      bool nowBelow = (g_st[i].emaFast < g_st[i].wmaSlow);
      if(wasBelow && nowAbove) g_st[i].lastCrossDir = +1;
      if(wasAbove && nowBelow) g_st[i].lastCrossDir = -1;
     }
   if(g_st[i].lastCrossDir != 0)
      g_st[i].crossDirRecent = g_st[i].lastCrossDir; // ghi nho huong cat gan nhat (dung cho dong thuan da khung)

   // --- dem so nen lien tiep RSI trong vung 70 / 30 (dung cho "quan tinh") ---
   if(g_st[i].rsi >= 70.0) g_st[i].barsInZone70++; else g_st[i].barsInZone70 = 0;
   if(g_st[i].rsi <= 30.0) g_st[i].barsInZone30++; else g_st[i].barsInZone30 = 0;

   // --- swing detection (fractal) tren mang High/Low series ---
   int wing = InpFractalWing;
   int candIdx = 1 + wing; // ung vien fractal moi co the xac nhan (can wing nen moi hon da dong het)
   bool coSwingHighMoi = false;
   bool coSwingLowMoi  = false;
   if(candIdx + wing < gotMin)
     {
      if(IsFractalHigh(highBuf, candIdx, wing, gotMin))
        {
         // rsi tai vi tri swing (chuyen ve mang Asc): shift candIdx -> ascIdx = gotMin-1-candIdx
         int ascIdx = gotMin - 1 - candIdx;
         double rsiAtSwing = (ascIdx >= 0 && ascIdx < gotMin) ? rsiAsc[ascIdx] : g_st[i].rsi;
         datetime tSwing = timeBuf[candIdx];
         int n = ArraySize(g_st[i].swingHighs);
         bool already = (n > 0 && g_st[i].swingHighs[n-1].time == tSwing);
         if(!already)
           {
            PushSwing(g_st[i].swingHighs, tSwing, highBuf[candIdx], rsiAtSwing, true);
            coSwingHighMoi = true;
           }
        }
      if(IsFractalLow(lowBuf, candIdx, wing, gotMin))
        {
         int ascIdx = gotMin - 1 - candIdx;
         double rsiAtSwing = (ascIdx >= 0 && ascIdx < gotMin) ? rsiAsc[ascIdx] : g_st[i].rsi;
         datetime tSwing = timeBuf[candIdx];
         int n = ArraySize(g_st[i].swingLows);
         bool already = (n > 0 && g_st[i].swingLows[n-1].time == tSwing);
         if(!already)
           {
            PushSwing(g_st[i].swingLows, tSwing, lowBuf[candIdx], rsiAtSwing, false);
            coSwingLowMoi = true;
           }
        }
     }

   // ============ NEO SONG cho vung KC/HT (mo ta cua anh) ============
   // Su kien "RSI cam dau xuong/len" mo ra 1 con song moi. Ghi log SONG SONG
   // ca 2 cach xac dinh, de thong ke tu chi ra cach nao dung - khong ep chon truoc.
   double rsiNow = g_st[i].rsi, emaNow = g_st[i].emaFast, wmaNow = g_st[i].wmaSlow;
   bool belowBothNow  = (rsiNow    < emaNow    && rsiNow    < wmaNow);
   bool belowBothPrev = (rsiShift2 < emaShift2 && rsiShift2 < wmaShift2);
   bool aboveBothNow  = (rsiNow    > emaNow    && rsiNow    > wmaNow);
   bool aboveBothPrev = (rsiShift2 > emaShift2 && rsiShift2 > wmaShift2);

   int nHh = ArraySize(g_st[i].swingHighs);
   int nLl = ArraySize(g_st[i].swingLows);
   double dinhGanNhat = (nHh > 0 ? g_st[i].swingHighs[nHh-1].price : highBuf[1]);
   double dayGanNhat  = (nLl > 0 ? g_st[i].swingLows[nLl-1].price  : lowBuf[1]);

   // --- V1: RSI cat xuong/len CA HAI duong trung binh ---
   if(!belowBothPrev && belowBothNow)
     {
      LuuSongVuaXong(i, 1, timeBuf[1]);
      g_st[i].waveDirV1 = -1; g_st[i].waveOrgV1 = dinhGanNhat;
      g_st[i].waveExtV1 = lowBuf[1];  g_st[i].waveTimeV1 = timeBuf[1];
     }
   else if(!aboveBothPrev && aboveBothNow)
     {
      LuuSongVuaXong(i, 1, timeBuf[1]);
      g_st[i].waveDirV1 = +1; g_st[i].waveOrgV1 = dayGanNhat;
      g_st[i].waveExtV1 = highBuf[1]; g_st[i].waveTimeV1 = timeBuf[1];
     }
   else
     {
      if(g_st[i].waveDirV1 == -1 && lowBuf[1]  < g_st[i].waveExtV1) g_st[i].waveExtV1 = lowBuf[1];
      if(g_st[i].waveDirV1 == +1 && highBuf[1] > g_st[i].waveExtV1) g_st[i].waveExtV1 = highBuf[1];
     }

   // --- V2: EMA9(RSI) cat WMA45(RSI) ---
   if(g_st[i].lastCrossDir == -1)
     {
      LuuSongVuaXong(i, 2, timeBuf[1]);
      g_st[i].waveDirV2 = -1; g_st[i].waveOrgV2 = dinhGanNhat;
      g_st[i].waveExtV2 = lowBuf[1];  g_st[i].waveTimeV2 = timeBuf[1];
     }
   else if(g_st[i].lastCrossDir == +1)
     {
      LuuSongVuaXong(i, 2, timeBuf[1]);
      g_st[i].waveDirV2 = +1; g_st[i].waveOrgV2 = dayGanNhat;
      g_st[i].waveExtV2 = highBuf[1]; g_st[i].waveTimeV2 = timeBuf[1];
     }
   else
     {
      if(g_st[i].waveDirV2 == -1 && lowBuf[1]  < g_st[i].waveExtV2) g_st[i].waveExtV2 = lowBuf[1];
      if(g_st[i].waveDirV2 == +1 && highBuf[1] > g_st[i].waveExtV2) g_st[i].waveExtV2 = highBuf[1];
     }

   // --- cap nhat trang thai quan tinh (muc 7) ---
   UpdateMomentum(i, coSwingHighMoi, coSwingLowMoi);

   g_st[i].initialized = true;
   g_st[i].lastClosedBarTime = curBarTime;
  }

//====================================================================
// CAP NHAT TRANG THAI QUAN TINH (muc 7 dac ta) - VIET LAI TRON KHOI
//
// Day la MAY TRANG THAI CO NHO, khong phai phan loai lai tu dau moi
// nen. Quy tac chuyen trang thai bam sat dung cau chu trong dac ta:
//
//  (1) BAT quan tinh: RSI nam trong vung >=70 (hoac <=30) du
//      InpMinBarsInZone nen lien tiep -> MOM_TANG (hoac MOM_GIAM).
//
//  (2) GIU quan tinh: RSI roi khoi vung thi trang thai VAN GIU NGUYEN.
//      Day la cho sua quan trong nhat so voi ban truoc - dung y anh
//      "doan tau dang chay khong the dung mot phat duoc".
//
//  (3) CO CANH BAO "dang suy yeu" - chay SONG SONG, KHONG tat quan tinh:
//      - trong MOM_TANG: swing high moi CAO HON swing high truoc nhung
//        dinh RSI tai do THAP HON     -> anh goi la "song rui ro"
//      - trong MOM_GIAM: swing low moi THAP HON swing low truoc nhung
//        day RSI tai do CAO HON       -> anh goi la "can kiet"
//      Hai cai nay la cung mot co che soi guong, nen dung chung 1 co.
//
//  (4) TAT quan tinh -> HET quan tinh: gia tao DINH MOI (cao hon dinh
//      truoc) nhung RSI tai dinh do KHONG con vao lai vung >=70.
//      Doi xung cho phe giam voi vung <=30.
//      CA HAI ve deu bat buoc. Ban truoc em bo sot ve "dinh moi" nen
//      trang thai nay nuot mat 75% so nen.
//
// Cac buoc (3) va (4) chi duoc xet KHI CO SWING MOI duoc xac nhan.
// Khong co swing moi = khong co thong tin moi = giu nguyen trang thai.
//====================================================================
void UpdateMomentum(const int i, const bool coSwingHighMoi, const bool coSwingLowMoi)
  {
   int nH = ArraySize(g_st[i].swingHighs);
   int nL = ArraySize(g_st[i].swingLows);

   // --- (1) BAT quan tinh khi RSI o trong vung du lau ---
   if(g_st[i].barsInZone70 >= InpMinBarsInZone)
     {
      if(g_st[i].momState != MOM_TANG)
        {
         g_st[i].momState   = MOM_TANG;
         g_st[i].dangSuyYeu = false;   // quan tinh moi -> xoa canh bao cu
        }
      return;
     }
   if(g_st[i].barsInZone30 >= InpMinBarsInZone)
     {
      if(g_st[i].momState != MOM_GIAM)
        {
         g_st[i].momState   = MOM_GIAM;
         g_st[i].dangSuyYeu = false;
        }
      return;
     }

   // --- Phe TANG: chi xet khi dang trong quan tinh tang + co dinh moi ---
   if(coSwingHighMoi && nH >= 2 && g_st[i].momState == MOM_TANG)
     {
      double giaMoi = g_st[i].swingHighs[nH-1].price;
      double giaCu  = g_st[i].swingHighs[nH-2].price;
      double rsiMoi = g_st[i].swingHighs[nH-1].rsiAtSwing;
      double rsiCu  = g_st[i].swingHighs[nH-2].rsiAtSwing;

      if(giaMoi > giaCu)                       // gia VAN tao dinh moi
        {
         if(rsiMoi < 70.0)                     // (4) nhung RSI khong con vao lai vung
           {
            g_st[i].momState   = MOM_HET_TANG;
            g_st[i].dangSuyYeu = false;
            return;
           }
         if(rsiMoi < rsiCu)                    // (3) van vao vung nhung yeu hon lan truoc
            g_st[i].dangSuyYeu = true;
        }
     }

   // --- Phe GIAM: doi xung hoan toan ---
   if(coSwingLowMoi && nL >= 2 && g_st[i].momState == MOM_GIAM)
     {
      double giaMoi = g_st[i].swingLows[nL-1].price;
      double giaCu  = g_st[i].swingLows[nL-2].price;
      double rsiMoi = g_st[i].swingLows[nL-1].rsiAtSwing;
      double rsiCu  = g_st[i].swingLows[nL-2].rsiAtSwing;

      if(giaMoi < giaCu)                       // gia VAN tao day moi
        {
         if(rsiMoi > 30.0)                     // (4)
           {
            g_st[i].momState   = MOM_HET_GIAM;
            g_st[i].dangSuyYeu = false;
            return;
           }
         if(rsiMoi > rsiCu)                    // (3)
            g_st[i].dangSuyYeu = true;
        }
     }
  }

//====================================================================
// Nhan dien mo hinh (muc 6) tai khung GIUA cua 1 setup, kem dong thuan
// voi khung LON cho MH1/MH2
//====================================================================
ENUM_MOHINH DetectMoHinh(const int idxMid, const int idxLarge,
                         bool &dongThuanKhungLon, int &huongCatKhungGiua)
  {
   dongThuanKhungLon = false;
   // BO SUNG DO DEM: ban truoc cot "dong_thuan" vo dung vi no luon bang
   // so lan ra MH1/MH2. Gio ghi rieng huong cat cua khung giua, de dem
   // duoc bao nhieu lan khung giua CAT nhung bi khung lon TU CHOI.
   huongCatKhungGiua = g_st[idxMid].lastCrossDir;
   // Truy cap truc tiep g_st[idxMid], KHONG copy ca struct (struct co mang dong,
   // copy de sinh loi/ton bo nho).

   // MH1: EMA9(RSI) vua cat XUONG WMA45(RSI) tai khung giua, sau khi da co quan tinh tang truoc do
   if(g_st[idxMid].lastCrossDir == -1)
     {
      bool dongThuan = (g_st[idxLarge].crossDirRecent == -1) || (g_st[idxLarge].emaFast < g_st[idxLarge].wmaSlow);
      dongThuanKhungLon = dongThuan;
      if(dongThuan) return(MH1_RESET_TANG_CAT_XUONG);
     }
   // MH2: doi xung, cat LEN
   if(g_st[idxMid].lastCrossDir == +1)
     {
      bool dongThuan = (g_st[idxLarge].crossDirRecent == +1) || (g_st[idxLarge].emaFast > g_st[idxLarge].wmaSlow);
      dongThuanKhungLon = dongThuan;
      if(dongThuan) return(MH2_RESET_GIAM_CAT_LEN);
     }

   // MH3: con quan tinh (chua reset), dang cho de vao lai
   if(g_st[idxMid].momState == MOM_TANG || g_st[idxMid].momState == MOM_GIAM)
      return(MH3_TIEP_DIEN_CHO_RESET);

   // MH4 / MH5: cau truc dinh day (dua tren 2 swing gan nhat cua khung giua)
   int nH = ArraySize(g_st[idxMid].swingHighs);
   int nL = ArraySize(g_st[idxMid].swingLows);
   if(nH >= 2 && nL >= 2)
     {
      bool higherHigh = g_st[idxMid].swingHighs[nH-1].price > g_st[idxMid].swingHighs[nH-2].price;
      bool higherLow  = g_st[idxMid].swingLows[nL-1].price  > g_st[idxMid].swingLows[nL-2].price;
      bool lowerHigh  = g_st[idxMid].swingHighs[nH-1].price < g_st[idxMid].swingHighs[nH-2].price;
      bool lowerLow   = g_st[idxMid].swingLows[nL-1].price  < g_st[idxMid].swingLows[nL-2].price;
      if(higherHigh && higherLow) return(MH5_DINH_DAY_CAO_DAN);
      if(lowerHigh && lowerLow)   return(MH4_DINH_DAY_THAP_DAN);
     }

   return(MH_NONE);
  }

// VUNG KC/HT - NEO THEO CON SONG DANG CHAY (thay hoan toan cach quet cu)
//
// Mo ta cua anh: khong di tim vung trong qua khu. Lay chinh con song dang
// chay - bat dau tu luc RSI cam dau xuong (hoac len) - roi suy ra cac muc
// phia truoc theo dung thu tu gia se gap:
//   L1 = dinh/day TRUNG GIAN gan nhat  (diem dau tien gia phai vuot)
//   L2 = Fibo InpFiboLevel cua con song
//   L3 = diem BAT DAU con song          (Fibo 1.0)
//
// Uu diem: KHONG can mot con so tuy tien nao - khong nguong ATR, khong
// "quet lai bao nhieu swing", khong "% gia". Ba muc suy ra 100% tu hinh
// dang con song.
//
// variant = 1 (RSI cat ca 2 DTB) hoac 2 (EMA9 cat WMA45). Ca hai deu duoc
// ghi log song song de thong ke tu chi ra cach neo nao dung.
// Tra ve huong song: -1 song giam (3 muc la KHANG CU phia tren),
//                    +1 song tang (3 muc la HO TRO phia duoi), 0 = chua co.
//====================================================================
int ComputeWaveLevels(const int idx, const int variant, double &L1, double &L2, double &L3)
  {
   L1 = 0; L2 = 0; L3 = 0;
   // SUA LOI: doc CON SONG VUA HOAN THANH, khong phai con song moi vua mo.
   // Sau 1 con song giam, khi gia quay len thi cac KHANG CU phia truoc lay
   // tu chinh con song giam do (dung mo ta cua anh).
   int      dir = (variant == 1 ? g_st[idx].prevDirV1 : g_st[idx].prevDirV2);
   double   org = (variant == 1 ? g_st[idx].prevOrgV1 : g_st[idx].prevOrgV2);
   double   ext = (variant == 1 ? g_st[idx].prevExtV1 : g_st[idx].prevExtV2);
   datetime t0  = (variant == 1 ? g_st[idx].prevT0V1  : g_st[idx].prevT0V2);
   datetime t1  = (variant == 1 ? g_st[idx].prevT1V1  : g_st[idx].prevT1V2);
   if(dir == 0) return(0);

   L3 = org;
   L2 = ext + (org - ext) * InpFiboLevel;   // dung cho ca 2 huong song

   double best = 0;
   if(dir == -1)
     {
      // song giam: L1 = dinh THAP NHAT hinh thanh sau khi neo, nam giua day va diem bat dau
      int n = ArraySize(g_st[idx].swingHighs);
      for(int k = 0; k < n; k++)
        {
         if(g_st[idx].swingHighs[k].time <= t0) continue;
         if(g_st[idx].swingHighs[k].time >  t1) continue;   // chi lay swing TRONG con song do
         double pr = g_st[idx].swingHighs[k].price;
         if(pr <= ext || pr >= org) continue;
         if(best == 0 || pr < best) best = pr;
        }
     }
   else
     {
      // song tang: L1 = day CAO NHAT hinh thanh sau khi neo, nam giua dinh va diem bat dau
      int n = ArraySize(g_st[idx].swingLows);
      for(int k = 0; k < n; k++)
        {
         if(g_st[idx].swingLows[k].time <= t0) continue;
         if(g_st[idx].swingLows[k].time >  t1) continue;
         double pr = g_st[idx].swingLows[k].price;
         if(pr >= ext || pr <= org) continue;
         if(best == 0 || pr > best) best = pr;
        }
     }
   L1 = best;   // = 0 neu chua co muc trung gian nao
   return(dir);
  }

//====================================================================
// Chuoi mo ta ngan cho log/comment
//====================================================================
string MomToStr(ENUM_MOMENTUM_STATE s)
  {
   switch(s)
     {
      case MOM_TANG:               return("Quan_tinh_TANG");
      case MOM_GIAM:               return("Quan_tinh_GIAM");
      case MOM_HET_TANG:           return("Het_quan_tinh_TANG");
      case MOM_HET_GIAM:           return("Het_quan_tinh_GIAM");
      default:                     return("None");
     }
  }

string MoHinhToStr(ENUM_MOHINH m)
  {
   switch(m)
     {
      case MH1_RESET_TANG_CAT_XUONG: return("MH1_dao_chieu_GIAM");
      case MH2_RESET_GIAM_CAT_LEN:   return("MH2_dao_chieu_TANG");
      case MH3_TIEP_DIEN_CHO_RESET:  return("MH3_tiep_dien_cho_reset");
      case MH4_DINH_DAY_THAP_DAN:    return("MH4_dinh_day_thap_dan");
      case MH5_DINH_DAY_CAO_DAN:     return("MH5_dinh_day_cao_dan");
      default:                       return("Khong_co_mo_hinh");
     }
  }

//====================================================================
// Xu ly 1 setup khi khung GIUA cua no vua co nen dong moi
//====================================================================
// LENH GIAY - do phan bo R (KHONG dat lenh that)
//
// Tra loi: "bao nhieu % tin hieu di toi 1.5R / 2R / 3R / 6R truoc khi
// cham SL". Con so nay khong phu thuoc TP dang dat, nen khong bi vong
// tron voi bo loc vao lenh R>=2 - dat TP the nao no cung dung yen.
//
// CANH BAO KHI DOC KET QUA:
//  - Entry lay tai dong nen KHUNG GIUA (chua co logic tim entry o khung
//    nho), nen R o day la UOC LUONG THAP HON thuc te.
//  - Do tren MOI tin hieu, ke ca tin hieu thua ngay - khong loc song sot.
//====================================================================
// LENH GIAY - do nhieu cach thoat song song tren cung mot tin hieu
//
// CANH BAO KHI DOC KET QUA:
//  - Day la lenh GIAY, khong dat lenh that.
//  - Loai "NGAY" vao tai gia dong nen khung giua -> SL rong -> R thap hon
//    thuc te. Loai "RETEST" moi gan voi cach anh trade tay.
//  - Do tren MOI tin hieu, ke ca tin hieu thua ngay - khong loc song sot.
//====================================================================
double BufferCuaSetup(const int setupIdx)
  {
   if(setupIdx == 0) return(InpBufferA);
   if(setupIdx == 1) return(InpBufferB);
   if(setupIdx == 2) return(InpBufferC);
   return(InpBufferD);
  }

void ClosePaperTrade(const int p, const string lyDo)
  {
   if(!g_paper[p].active) return;
   g_paper[p].active = false;
   if(g_paperHandle == INVALID_HANDLE) return;
   int dg = (int)SymbolInfoInteger(g_symbol, SYMBOL_DIGITS);
   FileWrite(g_paperHandle,
             TimeToString(g_paper[p].timeIn, TIME_DATE | TIME_MINUTES),
             TimeToString(TimeCurrent(),     TIME_DATE | TIME_MINUTES),
             g_setup[g_paper[p].setupIdx].name,
             g_tfName[g_setup[g_paper[p].setupIdx].idxMid],
             g_paper[p].loaiVao,
             (g_paper[p].dir > 0 ? "BUY" : "SELL"),
             g_paper[p].mohinh,
             DoubleToString(g_paper[p].entry, dg),
             DoubleToString(g_paper[p].sl,    dg),
             DoubleToString(g_paper[p].rUnit, 2),
             DoubleToString(g_paper[p].mfeR,  3),
             lyDo,
             IntegerToString(g_paper[p].bars),
             DoubleToString(g_paper[p].lvl1R, 3),
             DoubleToString(g_paper[p].lvl2R, 3),
             DoubleToString(g_paper[p].lvl3R, 3),
             DoubleToString(g_paper[p].s1RA, 3),
             DoubleToString(g_paper[p].s1RB, 3),
             DoubleToString(g_paper[p].s1RC, 3),
             DoubleToString(g_paper[p].s1RD, 3),
             IntegerToString(g_paper[p].s1State));
  }

//--- mo 1 lenh giay. Tra ve true neu mo duoc. -----------------------
bool MoLenhGiay(const int setupIdx, const int dir, const string mhName,
                const string loaiVao, const double entry, const double sl,
                const double L1R, const double L2R, const double L3R)
  {
   if(entry <= 0) return(false);
   if(dir > 0 && sl >= entry) return(false);
   if(dir < 0 && sl <= entry) return(false);
   double rUnit = MathAbs(entry - sl);
   if(rUnit <= 0) return(false);

   int slot = -1;
   for(int k = 0; k < ArraySize(g_paper); k++)
      if(!g_paper[k].active) { slot = k; break; }
   if(slot < 0) { slot = ArraySize(g_paper); ArrayResize(g_paper, slot + 1); }

   g_paper[slot].active      = true;
   g_paper[slot].setupIdx    = setupIdx;
   g_paper[slot].dir         = dir;
   g_paper[slot].loaiVao     = loaiVao;
   g_paper[slot].timeIn      = iTime(g_symbol, g_tfEnum[g_setup[setupIdx].idxMid], 1);
   g_paper[slot].entry       = entry;
   g_paper[slot].sl          = sl;
   g_paper[slot].rUnit       = rUnit;
   g_paper[slot].bars        = 0;
   g_paper[slot].mohinh      = mhName;
   g_paper[slot].mfeR        = 0;
   g_paper[slot].lvl1R       = L1R;
   g_paper[slot].lvl2R       = L2R;
   g_paper[slot].lvl3R       = L3R;
   g_paper[slot].s1State     = 0;
   g_paper[slot].s1Dinh1     = 0;
   g_paper[slot].s1Day1      = 0;
   g_paper[slot].s1DayTrail  = 0;
   g_paper[slot].s1TimeDinh1 = 0;
   g_paper[slot].s1RA = 0;  g_paper[slot].s1RB = 0;
   g_paper[slot].s1RC = 0;  g_paper[slot].s1RD = 0;
   g_paper[slot].s1XongA = false; g_paper[slot].s1XongB = false;
   g_paper[slot].s1XongC = false; g_paper[slot].s1XongD = false;
   return(true);
  }

//--- BO 1: cap nhat may trang thai "day swing dau tien" -------------
// Dung swing da duoc dua ra boi bo do fractal cua khung giua (da kiem chung).
void CapNhatBo1(const int p, const double hi, const double lo, const double dong)
  {
   int idxMid = g_setup[g_paper[p].setupIdx].idxMid;
   int dir    = g_paper[p].dir;
   int nH = ArraySize(g_st[idxMid].swingHighs);
   int nL = ArraySize(g_st[idxMid].swingLows);

   // --- di chuyen qua cac buoc xac lap Dinh1 / Day1 ---
   if(g_paper[p].s1State == 0)
     {
      // tim dinh (buy) / day (sell) dau tien hinh thanh SAU khi vao lenh
      if(dir > 0)
        {
         for(int k = 0; k < nH; k++)
            if(g_st[idxMid].swingHighs[k].time > g_paper[p].timeIn)
              { g_paper[p].s1Dinh1 = g_st[idxMid].swingHighs[k].price;
                g_paper[p].s1TimeDinh1 = g_st[idxMid].swingHighs[k].time;
                g_paper[p].s1State = 1; break; }
        }
      else
        {
         for(int k = 0; k < nL; k++)
            if(g_st[idxMid].swingLows[k].time > g_paper[p].timeIn)
              { g_paper[p].s1Dinh1 = g_st[idxMid].swingLows[k].price;
                g_paper[p].s1TimeDinh1 = g_st[idxMid].swingLows[k].time;
                g_paper[p].s1State = 1; break; }
        }
     }
   if(g_paper[p].s1State == 1)
     {
      // tim day (buy) / dinh (sell) dau tien sau Dinh1
      if(dir > 0)
        {
         for(int k = 0; k < nL; k++)
            if(g_st[idxMid].swingLows[k].time > g_paper[p].s1TimeDinh1)
              { g_paper[p].s1Day1 = g_st[idxMid].swingLows[k].price;
                g_paper[p].s1DayTrail = g_paper[p].s1Day1;
                g_paper[p].s1State = 2; break; }
        }
      else
        {
         for(int k = 0; k < nH; k++)
            if(g_st[idxMid].swingHighs[k].time > g_paper[p].s1TimeDinh1)
              { g_paper[p].s1Day1 = g_st[idxMid].swingHighs[k].price;
                g_paper[p].s1DayTrail = g_paper[p].s1Day1;
                g_paper[p].s1State = 2; break; }
        }
     }
   if(g_paper[p].s1State == 2)
     {
      // Day1 chi duoc TINH khi gia tao dinh moi PHA QUA Dinh1 (luat cua anh)
      if(dir > 0 && hi > g_paper[p].s1Dinh1) g_paper[p].s1State = 3;
      if(dir < 0 && lo < g_paper[p].s1Dinh1) g_paper[p].s1State = 3;
     }
   if(g_paper[p].s1State < 3) return;   // chua hop le -> van dung SL goc

   // --- bien the C,D: doi day len theo day swing moi cao hon ---
   if(dir > 0)
     {
      for(int k = 0; k < nL; k++)
        {
         double pr = g_st[idxMid].swingLows[k].price;
         if(g_st[idxMid].swingLows[k].time > g_paper[p].s1TimeDinh1 &&
            pr > g_paper[p].s1DayTrail && pr < dong)
            g_paper[p].s1DayTrail = pr;
        }
     }
   else
     {
      for(int k = 0; k < nH; k++)
        {
         double pr = g_st[idxMid].swingHighs[k].price;
         if(g_st[idxMid].swingHighs[k].time > g_paper[p].s1TimeDinh1 &&
            pr < g_paper[p].s1DayTrail && pr > dong)
            g_paper[p].s1DayTrail = pr;
        }
     }

   // --- kiem tra quet, 4 bien the ---
   double e = g_paper[p].entry, r = g_paper[p].rUnit;
   if(dir > 0)
     {
      if(!g_paper[p].s1XongA && lo   <= g_paper[p].s1Day1)     { g_paper[p].s1RA=(g_paper[p].s1Day1-e)/r;     g_paper[p].s1XongA=true; }
      if(!g_paper[p].s1XongB && dong <= g_paper[p].s1Day1)     { g_paper[p].s1RB=(g_paper[p].s1Day1-e)/r;     g_paper[p].s1XongB=true; }
      if(!g_paper[p].s1XongC && lo   <= g_paper[p].s1DayTrail) { g_paper[p].s1RC=(g_paper[p].s1DayTrail-e)/r; g_paper[p].s1XongC=true; }
      if(!g_paper[p].s1XongD && dong <= g_paper[p].s1DayTrail) { g_paper[p].s1RD=(g_paper[p].s1DayTrail-e)/r; g_paper[p].s1XongD=true; }
     }
   else
     {
      if(!g_paper[p].s1XongA && hi   >= g_paper[p].s1Day1)     { g_paper[p].s1RA=(e-g_paper[p].s1Day1)/r;     g_paper[p].s1XongA=true; }
      if(!g_paper[p].s1XongB && dong >= g_paper[p].s1Day1)     { g_paper[p].s1RB=(e-g_paper[p].s1Day1)/r;     g_paper[p].s1XongB=true; }
      if(!g_paper[p].s1XongC && hi   >= g_paper[p].s1DayTrail) { g_paper[p].s1RC=(e-g_paper[p].s1DayTrail)/r; g_paper[p].s1XongC=true; }
      if(!g_paper[p].s1XongD && dong >= g_paper[p].s1DayTrail) { g_paper[p].s1RD=(e-g_paper[p].s1DayTrail)/r; g_paper[p].s1XongD=true; }
     }
  }

void UpdatePaperTrades(const int setupIdx)
  {
   int idxMid = g_setup[setupIdx].idxMid;
   double hi   = iHigh (g_symbol, g_tfEnum[idxMid], 1);
   double lo   = iLow  (g_symbol, g_tfEnum[idxMid], 1);
   double dong = iClose(g_symbol, g_tfEnum[idxMid], 1);
   if(hi <= 0 || lo <= 0 || dong <= 0) return;

   for(int k = 0; k < ArraySize(g_paper); k++)
     {
      if(!g_paper[k].active || g_paper[k].setupIdx != setupIdx) continue;
      g_paper[k].bars++;

      double fav;
      bool chamSL;
      if(g_paper[k].dir > 0) { fav = (hi - g_paper[k].entry) / g_paper[k].rUnit; chamSL = (lo <= g_paper[k].sl); }
      else                   { fav = (g_paper[k].entry - lo) / g_paper[k].rUnit; chamSL = (hi >= g_paper[k].sl); }
      if(fav > g_paper[k].mfeR) g_paper[k].mfeR = fav;

      CapNhatBo1(k, hi, lo, dong);

      if(chamSL)
        {
         // cac bien the chua thoat thi coi nhu thoat tai SL = -1R
         if(!g_paper[k].s1XongA) { g_paper[k].s1RA = -1; g_paper[k].s1XongA = true; }
         if(!g_paper[k].s1XongB) { g_paper[k].s1RB = -1; g_paper[k].s1XongB = true; }
         if(!g_paper[k].s1XongC) { g_paper[k].s1RC = -1; g_paper[k].s1XongC = true; }
         if(!g_paper[k].s1XongD) { g_paper[k].s1RD = -1; g_paper[k].s1XongD = true; }
         ClosePaperTrade(k, "CHAM_SL");
        }
      else if(g_paper[k].bars >= InpPaperMaxBars) ClosePaperTrade(k, "HET_HAN");
     }
  }

//--- BO 5: cho gia hoi ve tao cau truc o KHUNG NHO roi moi vao ------
void DangKyChoRetest(const int setupIdx, const int dir, const string mhName,
                     const double L1R, const double L2R, const double L3R)
  {
   int slot = -1;
   for(int k = 0; k < ArraySize(g_cho); k++)
      if(!g_cho[k].active) { slot = k; break; }
   if(slot < 0) { slot = ArraySize(g_cho); ArrayResize(g_cho, slot + 1); }
   g_cho[slot].active      = true;
   g_cho[slot].setupIdx    = setupIdx;
   g_cho[slot].dir         = dir;
   g_cho[slot].timeTinHieu = iTime(g_symbol, g_tfEnum[g_setup[setupIdx].idxMid], 1);
   g_cho[slot].mohinh      = mhName;
   g_cho[slot].soNenCho    = 0;
   g_cho[slot].lvl1R = L1R; g_cho[slot].lvl2R = L2R; g_cho[slot].lvl3R = L3R;
  }

// Goi moi khi KHUNG NHO cua setup do dong nen.
void KiemTraRetest(const int setupIdx)
  {
   int idxSmall = g_setup[setupIdx].idxSmall;
   double dong = iClose(g_symbol, g_tfEnum[idxSmall], 1);
   if(dong <= 0) return;

   for(int k = 0; k < ArraySize(g_cho); k++)
     {
      if(!g_cho[k].active || g_cho[k].setupIdx != setupIdx) continue;
      g_cho[k].soNenCho++;

      // qua han cho -> bo, ghi lai de dem ty le "khong retest"
      if(g_cho[k].soNenCho > InpRetestMaxBars)
        {
         g_cho[k].active = false;
         if(g_paperHandle != INVALID_HANDLE)
            FileWrite(g_paperHandle,
                      TimeToString(g_cho[k].timeTinHieu, TIME_DATE | TIME_MINUTES),
                      TimeToString(TimeCurrent(), TIME_DATE | TIME_MINUTES),
                      g_setup[setupIdx].name, g_tfName[g_setup[setupIdx].idxMid],
                      "RETEST", (g_cho[k].dir > 0 ? "BUY" : "SELL"), g_cho[k].mohinh,
                      "0","0","0","0","KHONG_RETEST",IntegerToString(g_cho[k].soNenCho),
                      "0","0","0","0","0","0","0","0");
         continue;
        }

      // co swing moi o khung nho hinh thanh SAU tin hieu -> vao lenh
      int nH = ArraySize(g_st[idxSmall].swingHighs);
      int nL = ArraySize(g_st[idxSmall].swingLows);
      double sl = 0; bool co = false;
      if(g_cho[k].dir > 0)
        {
         for(int q = nL - 1; q >= 0; q--)
            if(g_st[idxSmall].swingLows[q].time > g_cho[k].timeTinHieu &&
               g_st[idxSmall].swingLows[q].price < dong)
              { sl = g_st[idxSmall].swingLows[q].price - BufferCuaSetup(setupIdx); co = true; break; }
        }
      else
        {
         for(int q = nH - 1; q >= 0; q--)
            if(g_st[idxSmall].swingHighs[q].time > g_cho[k].timeTinHieu &&
               g_st[idxSmall].swingHighs[q].price > dong)
              { sl = g_st[idxSmall].swingHighs[q].price + BufferCuaSetup(setupIdx); co = true; break; }
        }
      if(!co) continue;

      if(MoLenhGiay(setupIdx, g_cho[k].dir, g_cho[k].mohinh, "RETEST", dong, sl,
                    g_cho[k].lvl1R, g_cho[k].lvl2R, g_cho[k].lvl3R))
         g_cho[k].active = false;
     }
  }

//====================================================================
// Xu ly 1 setup khi khung GIUA cua no vua co nen dong moi
//====================================================================
// LENH GIAY - do phan bo R (KHONG dat lenh that)
//
// Tra loi: "bao nhieu % tin hieu di toi 1.5R / 2R / 3R / 6R truoc khi
// cham SL". Con so nay khong phu thuoc TP dang dat, nen khong bi vong
// tron voi bo loc vao lenh R>=2 - dat TP the nao no cung dung yen.
//
// CANH BAO KHI DOC KET QUA:
//  - Entry lay tai dong nen KHUNG GIUA (chua co logic tim entry o khung
//    nho), nen R o day la UOC LUONG THAP HON thuc te.
//  - Do tren MOI tin hieu, ke ca tin hieu thua ngay - khong loc song sot.
//====================================================================
void ProcessSetupIfMidClosed(int setupIdx, datetime midClosedTimeThisTick)
  {
   SetupDef s = g_setup[setupIdx];
   if(!s.enabled) return;
   int idxSmall = s.idxSmall, idxMid = s.idxMid, idxLarge = s.idxLarge;

   // cap nhat cac lenh giay dang mo TRUOC khi mo lenh moi
   if(InpPaperTrade) UpdatePaperTrades(setupIdx);

   bool dongThuan = false;
   int  huongCat  = 0;
   ENUM_MOHINH mh = DetectMoHinh(idxMid, idxLarge, dongThuan, huongCat);
   string catStr = (huongCat == 0 ? "-" : (huongCat > 0 ? "CAT_LEN" : "CAT_XUONG"));
   string dongThuanStr = (huongCat == 0 ? "-" : (dongThuan ? "CO" : "KHONG"));

   // Cung pha / nguoc pha giua khung giua va khung lon (muc 8)
   bool midBiasUp   = (g_st[idxMid].emaFast   > g_st[idxMid].wmaSlow);
   bool largeBiasUp = (g_st[idxLarge].emaFast > g_st[idxLarge].wmaSlow);
   string phase = (midBiasUp == largeBiasUp) ? "DONG_PHA" : "NGUOC_PHA";

   double dtbDist = MathAbs(g_st[idxMid].emaFast - g_st[idxMid].wmaSlow);

   // --- cac muc cua con song, theo CA HAI cach neo ---
   double a1 = 0, a2 = 0, a3 = 0, b1 = 0, b2 = 0, b3 = 0;
   int dirV1 = ComputeWaveLevels(idxMid, 1, a1, a2, a3);
   int dirV2 = ComputeWaveLevels(idxMid, 2, b1, b2, b3);
   int dg = (int)SymbolInfoInteger(g_symbol, SYMBOL_DIGITS);

   if(InpWriteCSVLog && g_csvHandle != INVALID_HANDLE)
     {
      FileWrite(g_csvHandle,
                // SUA: ghi thoi diem cua NEN VUA DONG (truoc day ghi nham thoi
                // diem nen MOI MO nen lech 1 nen so voi file lenh giay)
                TimeToString(iTime(g_symbol, g_tfEnum[idxMid], 1), TIME_DATE | TIME_MINUTES),
                s.name, g_tfName[idxSmall], g_tfName[idxMid], g_tfName[idxLarge],
                MoHinhToStr(mh), catStr, dongThuanStr, phase,
                MomToStr(g_st[idxSmall].momState), MomToStr(g_st[idxMid].momState), MomToStr(g_st[idxLarge].momState),
                (g_st[idxMid].dangSuyYeu ? "CO" : "-"), (g_st[idxLarge].dangSuyYeu ? "CO" : "-"),
                DoubleToString(g_st[idxMid].rsi, 2), DoubleToString(g_st[idxMid].emaFast, 2), DoubleToString(g_st[idxMid].wmaSlow, 2),
                DoubleToString(dtbDist, 2),
                DoubleToString(g_st[idxSmall].adx, 2), DoubleToString(g_st[idxMid].adx, 2), DoubleToString(g_st[idxLarge].adx, 2),
                DoubleToString(g_st[idxMid].atr, 2),
                (dirV1 == 0 ? "-" : (dirV1 < 0 ? "SONG_GIAM" : "SONG_TANG")),
                (a1 > 0 ? DoubleToString(a1, dg) : "-"), DoubleToString(a2, dg), DoubleToString(a3, dg),
                (dirV2 == 0 ? "-" : (dirV2 < 0 ? "SONG_GIAM" : "SONG_TANG")),
                (b1 > 0 ? DoubleToString(b1, dg) : "-"), DoubleToString(b2, dg), DoubleToString(b3, dg));
     }

   // --- co tin hieu that -> mo CA HAI loai lenh giay de so truc tiep ---
   if(InpPaperTrade && (mh == MH1_RESET_TANG_CAT_XUONG || mh == MH2_RESET_GIAM_CAT_LEN))
     {
      int huong = (mh == MH2_RESET_GIAM_CAT_LEN ? +1 : -1);
      string mhTen = (huong > 0 ? "MH2" : "MH1");

      // khoang cach toi 3 muc cua con song vua xong, tinh bang R (dung SL cua loai NGAY)
      double e0 = iClose(g_symbol, g_tfEnum[idxMid], 1);
      double sl0 = 0; bool co0 = false;
      int nH0 = ArraySize(g_st[idxMid].swingHighs);
      int nL0 = ArraySize(g_st[idxMid].swingLows);
      if(huong > 0 && nL0 > 0) { sl0 = g_st[idxMid].swingLows[nL0-1].price  - BufferCuaSetup(setupIdx); co0 = true; }
      if(huong < 0 && nH0 > 0) { sl0 = g_st[idxMid].swingHighs[nH0-1].price + BufferCuaSetup(setupIdx); co0 = true; }

      double W1 = 0, W2 = 0, W3 = 0;
      ComputeWaveLevels(idxMid, 2, W1, W2, W3);
      double r0 = (co0 ? MathAbs(e0 - sl0) : 0);
      double L1R = (W1 > 0 && r0 > 0 ? (W1 - e0) * huong / r0 : 0);
      double L2R = (W2 > 0 && r0 > 0 ? (W2 - e0) * huong / r0 : 0);
      double L3R = (W3 > 0 && r0 > 0 ? (W3 - e0) * huong / r0 : 0);

      if(co0) MoLenhGiay(setupIdx, huong, mhTen, "NGAY", e0, sl0, L1R, L2R, L3R);
      DangKyChoRetest(setupIdx, huong, mhTen, L1R, L2R, L3R);
     }

   if(mh == MH1_RESET_TANG_CAT_XUONG || mh == MH2_RESET_GIAM_CAT_LEN || huongCat != 0)
      PrintFormat("[Setup %s | %s dong nen] Mo hinh=%s Cat=%s DongThuan=%s Phase=%s Mom(giua)=%s%s ADX=%.1f",
                  s.name, g_tfName[idxMid], MoHinhToStr(mh), catStr, dongThuanStr, phase,
                  MomToStr(g_st[idxMid].momState),
                  (g_st[idxMid].dangSuyYeu ? "+SUY_YEU" : ""), g_st[idxMid].adx);
  }

//====================================================================
// OnTick
//====================================================================
void OnTick()
  {
   // Cap nhat tat ca khung truoc, roi moi xu ly setup, de dam bao khung lon
   // da co du lieu moi nhat khi kiem tra dong thuan.
   datetime midClosedTime[N_TF];
   bool     justClosed[N_TF];
   for(int i = 0; i < N_TF; i++)
     {
      datetime before = g_st[i].lastClosedBarTime;
      UpdateTF(i);
      justClosed[i] = (g_st[i].lastClosedBarTime != before);
      midClosedTime[i] = g_st[i].lastClosedBarTime;
     }

   for(int s = 0; s < 4; s++)
     {
      if(!g_setup[s].enabled) continue;
      // BO 5 chay truoc: khung nho dong nen thi kiem tra hang cho retest
      if(InpPaperTrade && justClosed[g_setup[s].idxSmall]) KiemTraRetest(s);

      int idxMid = g_setup[s].idxMid;
      if(justClosed[idxMid])
         ProcessSetupIfMidClosed(s, midClosedTime[idxMid]);
     }

   if(InpShowComment)
     {
      string cm = "== ThinhTrading Engine v1 (chi nhan dien, CHUA dat lenh) ==\n";
      for(int i = 0; i < N_TF; i++)
        {
         cm += StringFormat("%s: RSI=%.1f EMA9=%.1f WMA45=%.1f ADX=%.1f Mom=%s%s\n",
                             g_tfName[i], g_st[i].rsi, g_st[i].emaFast, g_st[i].wmaSlow, g_st[i].adx,
                             MomToStr(g_st[i].momState), (g_st[i].dangSuyYeu ? " [SUY YEU]" : ""));
        }
      Comment(cm);
     }
  }
//+------------------------------------------------------------------+
