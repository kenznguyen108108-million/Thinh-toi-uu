<code>//+------------------------------------------------------------------+
//|  ThinhTrading_EA_v2_6.mq5                                        |
//|  Bot giao dich - cau hinh da toi uu bang backtest Python         |
//|  (2018-2026, kiem dinh tach doi 2018-2021 / 2022-2026)           |
//|                                                                  |
//|  MOI O v2.6: VIET LAI TOAN BO KHOI BAN. Chieu mua KHONG DOI 1 DONG.
//|   Ba thay doi cot loi so voi v2.5:
//|
//|   1. TIN HIEU BAN DEN TU KHUNG LON, khong phai khung giua nua.
//|      Setup B: H4 cat xuong -> vao o nen H1 dau tien sau do.
//|      Setup C: D1 cat xuong -> vao o nen H4 dau tien sau do.
//|      (v2.5 bat cat xuong o khung giua, khung lon chi lam bo loc.)
//|
//|   2. BAT BUOC CHE DO GIAM DA XAC NHAN - ca hai dieu kien:
//|        a) D1 dong cua DUOI SMA50 cua chinh D1
//|        b) W1: EMA9(RSI) < WMA45(RSI)
//|      Day la thu lam chieu ban tu AM thanh DUONG.
//|
//|   3. MAGIC RIENG + RUI RO RIENG cho chieu ban.
//|      v2.5 dung chung magic voi chieu mua -> lenh ban chiem cho
//|      trong han muc 3 lenh va CHAN lenh mua. Loi nghiem trong.
//|      v2.6 tach han: chieu ban co magic rieng, han muc rieng,
//|      % rui ro rieng (mac dinh 0.5%, bang nua chieu mua).
//|
//|   SO LIEU (tru spread 28 USD):
//|     Ban ngau nhien (placebo)              -0.324 R/lenh
//|     Tin hieu khung lon, chua loc che do   -0.072 R/lenh
//|     + loc che do giam, toan ky            +0.091 R/lenh (0.4 SE)
//|     + loc che do giam, walk-forward MU    +0.181 R/lenh (0.7 SE)
//|   Ghep vao chieu mua (mua 1% / ban 0.5%, 2018-2026):
//|     Chi mua   : von x8.30  CAGR +28.2%  sut sau nhat -40.01%
//|     Mua + ban : von x8.80  CAGR +29.1%  sut sau nhat -40.01%
//|
//|   NOI THAT: chieu ban CHUA duoc chung minh (0.7 SE; muon du 2 SE
//|   can ~990 lenh, tuc khoang 50 nam du lieu). No KHONG phai cai phao:
//|   tuong quan thang voi chieu mua la +0.166 - thang nao mua lo thi
//|   ban cung lo. Ly do bat no la no KHONG lam hong chieu mua (sut von
//|   gan nhu khong doi) va chay that la cach duy nhat con lai de lay
//|   them bang chung. -> CHAY DEMO TRUOC. Giu rui ro ban 0.5%.
//|
//|  MOI O v2.4: CAT BO phan dau hong cua mang chi bao.
//|   Log v2.3 chi ra: setup C doc duoc 515 nen D1 (khong phai 800),
//|   va bo loc khung lon D1 KHONG BAO GIO tu choi - trong khi setup B
//|   tu choi 40 lan. Ly do: nhung o dau mang chua duoc tinh mang gia
//|   tri rac (EMPTY_VALUE = so cuc lon). EMA seed tu 9 o dau do nen
//|   keo theo ca duong EMA thanh so khong lo -> luon > WMA -> luon
//|   dong thuan. v2.4 do lai: chi tinh tu o hop le cuoi cung tro di
//|   (RSI phai nam trong 0..100).
//|
//|  MOI O v2.3: doc chi bao KHUNG LON chac chan hon.
//|   Trieu chung o v2.2: setup C (khung lon D1) khong bao gio ra
//|   MH2, chi ra MH3a - dung y nhu khi ham doc khung lon that bai
//|   (MH2 can khung lon dong thuan, MH3a thi khong). Setup B (khung
//|   lon H4) khop 21/21 lenh voi Python nen loi nam o cach doc D1.
//|   v2.3: xin dung so nen dang co, kiem tra chi bao da tinh xong
//|   chua, va GHI LOG khi doc that bai de biet chinh xac ly do.
//|
//|  MOI O v2.2: chi vao lenh khi SL nam trong 0.5% - 1.5% gia BTC.
//|   Do tu 2018-2026: SL <0.5% gia -> -0.56R/lenh (bi quet).
//|   SL 0.5-1.5% gia -> +0.60R/lenh (3.4 SE), duong 8/9 nam.
//|   SL >1.5% gia -> +0.09R, gan nhu het loi the.
//|   Loc nay vua tang loi the vua lam SL tinh bang USD nho lai,
//|   nen tai khoan nho moi chiu duoc.
//|
//|  SUA SO VOI v2.0:                                                |
//|   Ban v2.0 dung may trang thai quan tinh kieu CONG DON qua tung  |
//|   nen. Neu chi mot nen bi bo lo (tester tra du lieu cham, tick   |
//|   dau nen den muon...) thi bo dem lech vinh vien -> MH3a vao     |
//|   tre dung 1 nen so voi Python.                                  |
//|   v2.1 DUNG LAI TOAN BO trang thai tu lich su moi nen (swing +   |
//|   quan tinh), nen khong the lech nua. Da kiem chung tren Python: |
//|   dung lai tu 300 nen gan nhat cho ket qua GIONG HET chay tu     |
//|   dau lich su.                                                   |
//|                                                                  |
//|  CAU HINH:                                                       |
//|   - Setup B: khung giua H1, khung lon H4                         |
//|   - Setup C: khung giua H4, khung lon D1                         |
//|   - MH2 (EMA9(RSI) cat LEN WMA45(RSI) + khung lon dong thuan)    |
//|     va MH3a (quan tinh tang VUA BAT)                             |
//|   - CHI LENH MUA                                                 |
//|   - SL dat DUNG tai day swing gan nhat khung giua, KHONG DEM     |
//|   - Thoat 100% bang trailing doi theo day swing moi              |
//|   - Toi da 3 lenh mo cung luc moi setup                          |
//|                                                                  |
//|  KHONG dung #include.                                            |
//+------------------------------------------------------------------+
#property copyright "ThinhTrading"
#property version   "2.60"
#property strict

//====================== THAM SO ====================================
input group "--- Quan ly von ---"
input double InpRiskPercent   = 2.0;     // Rui ro moi lenh (% so du)
input int    InpMaxPositions  = 3;       // Toi da lenh mo cung luc (moi setup)
input double InpSLMinPct      = 0.5;     // SL toi thieu (% gia BTC) - duoi nguong nay bo qua
input double InpSLMaxPct      = 1.5;     // SL toi da  (% gia BTC) - tren nguong nay bo qua
input double InpTranRuiRoPct  = 3.0;     // Neu 0.01 lot rui ro hon % nay so du -> bo qua lenh

input group "--- Chieu BAN (tin hieu tu KHUNG LON + che do giam) ---"
input bool   InpDungChieuBan   = true;    // Bat chieu ban
input double InpBanRiskPercent = 0.5;     // Rui ro moi lenh BAN (% so du) - giu 0.5
input int    InpBanMaxPositions= 2;       // Toi da lenh BAN mo cung luc (moi setup)
input double InpBanSLMinPct    = 0.5;     // SL toi thieu cho lenh ban (% gia)
input double InpBanSLMaxPct    = 1.5;     // SL toi da  cho lenh ban (% gia)
input double InpBanBatTrailR   = 1.5;     // Lai du bao nhieu R thi bat trailing
input bool   InpBanCanW1Xuong  = true;    // Bat buoc W1: EMA9(RSI) < WMA45(RSI)
input bool   InpBanCanD1DuoiMA = true;    // Bat buoc D1 dong cua duoi SMA50 cua D1
input int    InpBanD1MAPeriod  = 50;      // Chu ky SMA tren D1

input group "--- Setup ---"
input bool   InpDungSetupB    = true;    // Setup B (H1 / H4)
input bool   InpDungSetupC    = true;    // Setup C (H4 / D1)

input group "--- Chi bao ---"
input int    InpRSIPeriod     = 14;
input int    InpEMAPeriod     = 9;       // EMA tren RSI
input int    InpWMAPeriod     = 45;      // WMA tren RSI
input int    InpWing          = 2;       // so nen 2 ben de xac nhan swing
input int    InpMinBarsInZone = 2;       // so nen lien tiep trong vung 70/30

input group "--- Khac ---"
input long   InpMagicB        = 20260901;
input long   InpMagicC        = 20260902;
input long   InpMagicBanB     = 20260911;   // magic RIENG cho lenh ban setup B
input long   InpMagicBanC     = 20260912;   // magic RIENG cho lenh ban setup C
input int    InpSlippage      = 50;
input bool   InpGhiLog        = true;    // ghi CSV de doi chieu voi Python
input string InpLogSuffix     = "v25";

#define LOOKBACK   800
#define MAX_SWING  20     // giong het ban Python da kiem chung
#define MAX_POS    64

//====================== CAU TRUC ===================================
struct SwingPt
  {
   datetime time;
   double   price;
   double   rsi;
  };

struct PosState
  {
   ulong    ticket;
   datetime tVao;
   double   entry;
   double   slGoc;
   int      st;          // 0 cho Dinh1, 1 cho Day1, 2 cho pha Dinh1, 3 dang trail
   double   dinh1;
   datetime tDinh1;
   double   day1;
   double   trail;
   string   mohinh;
   int      huong;       // +1 mua, -1 ban
  };

struct SetupState
  {
   bool            dung;
   string          ten;
   ENUM_TIMEFRAMES tfMid;
   ENUM_TIMEFRAMES tfLarge;
   long            magic;
   long            magicBan;
   int             hRsiMid;
   int             hRsiLarge;
   datetime        lastBar;
   datetime        tLonBan;      // nen khung lon cuoi cung da xet cho chieu ban
   SwingPt         sH[MAX_SWING];
   int             nH;
   SwingPt         sL[MAX_SWING];
   int             nL;
   PosState        pos[MAX_POS];
   int             nPos;
   bool            daBaoThieuDL;
   bool            daBaoKhungLon;
   bool            daBaoKhungLonOK;
  };

//--- khai bao truoc
void  DonDepLenh(const int k, const bool ghiLog);
void  CapNhatTrailTheoNen(const int k, const double nenHigh, const double nenClose);
void  CapNhatTrailBan(const int k, const double nenHigh, const double nenLow, const double nenClose);
bool  KhungTuanXuong(void);
bool  D1DuoiTrungBinh(void);
bool  CheDoGiam(void);
bool  KhungLonCatXuong(const int k);
void  XuLyChieuBan(const int k, const datetime tNen);
void  VaoLenhBan(const int k, const datetime tNen);
void  DatSLBan(const ulong ticket, const double slMoi);
double TinhLotVoiRuiRo(const double slDistance, const double riskPct);
void  DatSL(const ulong ticket, const double slMoi);
void  XuLySetup(const int k);
bool  DocKhungLon(const int k, double &eLon, double &wLon);
int   CatDauHong(const double &src[], const int n);
void  XayDungTrangThai(const int k, const MqlRates &rt[], const double &rsi[],
                       const int n, int &momNow, int &momTruoc);
ENUM_ORDER_TYPE_FILLING LayKieuKhop(void);

SetupState g_su[2];
int    g_log = INVALID_HANDLE;
double g_tickSize = 0, g_tickValue = 0, g_lotMin = 0, g_lotMax = 0, g_lotStep = 0;
int    g_stopLevel = 0;
int    g_hRsiW1   = INVALID_HANDLE;

//====================== TRUNG BINH DONG TU VIET ====================
// src[] xep theo thu tu TANG dan thoi gian. out[] cung kich thuoc.
void ComputeEMA(const double &src[], const int n, const int period, double &out[])
  {
   ArrayResize(out, n);
   ArrayInitialize(out, EMPTY_VALUE);
   if(n < period || period < 1) return;
   double sum = 0;
   for(int i = 0; i < period; i++) sum += src[i];
   out[period-1] = sum / period;
   double k = 2.0 / (period + 1.0);
   for(int i = period; i < n; i++)
      out[i] = src[i] * k + out[i-1] * (1.0 - k);
  }

void ComputeWMA(const double &src[], const int n, const int period, double &out[])
  {
   ArrayResize(out, n);
   ArrayInitialize(out, EMPTY_VALUE);
   if(n < period || period < 1) return;
   double denom = period * (period + 1) / 2.0;
   for(int i = period-1; i < n; i++)
     {
      double s = 0;
      for(int j = 0; j < period; j++)
         s += src[i-j] * (period - j);     // nen moi nhat trong so lon nhat
      out[i] = s / denom;
     }
  }

//====================== TIEN ICH ===================================
bool LaGiaTriTot(const double v) { return(v != EMPTY_VALUE && v == v); }

// Tra ve vi tri bat dau cua doan DUOI CUNG toan gia tri hop le.
// RSI luon nam trong 0..100; bat cu o nao ngoai khoang do la chua
// duoc tinh (MT5 dien EMPTY_VALUE) -> phai bo, neu khong EMA seed
// se hong va keo lech ca duong.
int CatDauHong(const double &src[], const int n)
  {
   int bd = 0;
   for(int i = 0; i < n; i++)
      if(!LaGiaTriTot(src[i]) || src[i] < 0.0 || src[i] > 100.0) bd = i + 1;
   return(bd);
  }

void ThemSwing(SwingPt &arr[], int &n, const datetime t, const double p, const double r)
  {
   if(n >= MAX_SWING)
     {
      for(int i = 1; i < MAX_SWING; i++) arr[i-1] = arr[i];
      n = MAX_SWING - 1;
     }
   arr[n].time = t; arr[n].price = p; arr[n].rsi = r;
   n++;
  }

int DemLenhMo(const long magic)
  {
   int c = 0;
   for(int i = PositionsTotal()-1; i >= 0; i--)
     {
      ulong tk = PositionGetTicket(i);
      if(tk == 0) continue;
      if(PositionGetString(POSITION_SYMBOL) != _Symbol) continue;
      if(PositionGetInteger(POSITION_MAGIC) != magic) continue;
      c++;
     }
   return(c);
  }

bool LenhConSong(const ulong ticket)
  {
   for(int i = PositionsTotal()-1; i >= 0; i--)
      if(PositionGetTicket(i) == ticket) return(true);
   return(false);
  }

double TinhLotVoiRuiRo(const double slDistance, const double riskPct)
  {
   if(slDistance <= 0 || g_tickSize <= 0 || g_tickValue <= 0) return(0);
   if(riskPct <= 0) return(0);
   double tien = AccountInfoDouble(ACCOUNT_BALANCE) * riskPct / 100.0;
   double loMotLot = (slDistance / g_tickSize) * g_tickValue;
   if(loMotLot <= 0) return(0);
   double lot = tien / loMotLot;
   lot = MathFloor(lot / g_lotStep) * g_lotStep;
   if(lot < g_lotMin) return(0);
   if(lot > g_lotMax) lot = g_lotMax;
   return(NormalizeDouble(lot, 2));
  }

// Chieu mua giu nguyen hanh vi cu: van la InpRiskPercent.
double TinhLot(const double slDistance)
  {
   return(TinhLotVoiRuiRo(slDistance, InpRiskPercent));
  }

ENUM_ORDER_TYPE_FILLING LayKieuKhop(void)
  {
   long mode = SymbolInfoInteger(_Symbol, SYMBOL_FILLING_MODE);
   if((mode & SYMBOL_FILLING_FOK) != 0) return(ORDER_FILLING_FOK);
   if((mode & SYMBOL_FILLING_IOC) != 0) return(ORDER_FILLING_IOC);
   return(ORDER_FILLING_RETURN);
  }

//====================== GHI LOG ====================================
void MoLog(void)
  {
   if(!InpGhiLog) return;
   string ten = "ThinhTrading_EA_" + InpLogSuffix + "_" + _Symbol + ".csv";
   g_log = FileOpen(ten, FILE_WRITE|FILE_CSV|FILE_ANSI|FILE_COMMON, ',');
   if(g_log == INVALID_HANDLE) { Print("Khong mo duoc file log: ", GetLastError()); return; }
   FileWrite(g_log, "thoi_gian", "nen_tin_hieu", "setup", "mo_hinh", "huong",
             "gia_vao", "sl", "r_usd", "lot", "ket_qua");
   FileFlush(g_log);
  }

void GhiLog(const string setup, const datetime tNen, const string mh, const string huong,
            const double entry, const double sl, const double r,
            const double lot, const string kq)
  {
   if(g_log == INVALID_HANDLE) return;
   FileWrite(g_log, TimeToString(TimeCurrent(), TIME_DATE|TIME_MINUTES),
             TimeToString(tNen, TIME_DATE|TIME_MINUTES),
             setup, mh, huong,
             DoubleToString(entry, _Digits), DoubleToString(sl, _Digits),
             DoubleToString(r, 2), DoubleToString(lot, 2), kq);
   FileFlush(g_log);
  }

//====================== KHOI TAO ===================================
int OnInit()
  {
   g_tickSize  = SymbolInfoDouble(_Symbol, SYMBOL_TRADE_TICK_SIZE);
   g_tickValue = SymbolInfoDouble(_Symbol, SYMBOL_TRADE_TICK_VALUE);
   g_lotMin    = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MIN);
   g_lotMax    = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MAX);
   g_lotStep   = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_STEP);
   g_stopLevel = (int)SymbolInfoInteger(_Symbol, SYMBOL_TRADE_STOPS_LEVEL);

   if(g_tickSize <= 0 || g_tickValue <= 0 || g_lotStep <= 0)
     { Print("Khong doc duoc thong so symbol"); return(INIT_FAILED); }

   g_su[0].dung = InpDungSetupB; g_su[0].ten = "B";
   g_su[0].tfMid = PERIOD_H1;    g_su[0].tfLarge = PERIOD_H4;
   g_su[0].magic = InpMagicB;    g_su[0].magicBan = InpMagicBanB;

   g_su[1].dung = InpDungSetupC; g_su[1].ten = "C";
   g_su[1].tfMid = PERIOD_H4;    g_su[1].tfLarge = PERIOD_D1;
   g_su[1].magic = InpMagicC;    g_su[1].magicBan = InpMagicBanC;

   for(int i = 0; i < 2; i++)
     {
      g_su[i].hRsiMid = INVALID_HANDLE; g_su[i].hRsiLarge = INVALID_HANDLE;
      g_su[i].nH = 0; g_su[i].nL = 0;
      g_su[i].lastBar = 0; g_su[i].tLonBan = 0;
      g_su[i].nPos = 0; g_su[i].daBaoThieuDL = false;
      g_su[i].daBaoKhungLon = false; g_su[i].daBaoKhungLonOK = false;
      if(!g_su[i].dung) continue;
      g_su[i].hRsiMid   = iRSI(_Symbol, g_su[i].tfMid,   InpRSIPeriod, PRICE_CLOSE);
      g_su[i].hRsiLarge = iRSI(_Symbol, g_su[i].tfLarge, InpRSIPeriod, PRICE_CLOSE);
      if(g_su[i].hRsiMid == INVALID_HANDLE || g_su[i].hRsiLarge == INVALID_HANDLE)
        { Print("Khong tao duoc handle RSI cho setup ", g_su[i].ten); return(INIT_FAILED); }
     }

   if(InpDungChieuBan)
     {
      g_hRsiW1 = iRSI(_Symbol, PERIOD_W1, InpRSIPeriod, PRICE_CLOSE);
      if(g_hRsiW1 == INVALID_HANDLE) { Print("Khong tao duoc RSI khung tuan"); return(INIT_FAILED); }
     }

   MoLog();
   Print("ThinhTrading EA v2.6 khoi dong. MUA: rui ro ", InpRiskPercent,
         "%/lenh, toi da ", InpMaxPositions, " lenh moi setup.");
   if(InpDungChieuBan)
      Print("  BAN: BAT - rui ro ", InpBanRiskPercent, "%/lenh, toi da ",
            InpBanMaxPositions, " lenh moi setup, chi vao khi che do giam.");
   else
      Print("  BAN: TAT.");
   return(INIT_SUCCEEDED);
  }

void OnDeinit(const int reason)
  {
   if(g_log != INVALID_HANDLE) { FileClose(g_log); g_log = INVALID_HANDLE; }
   if(g_hRsiW1 != INVALID_HANDLE) IndicatorRelease(g_hRsiW1);
   for(int i = 0; i < 2; i++)
     {
      if(g_su[i].hRsiMid   != INVALID_HANDLE) IndicatorRelease(g_su[i].hRsiMid);
      if(g_su[i].hRsiLarge != INVALID_HANDLE) IndicatorRelease(g_su[i].hRsiLarge);
     }
  }

//====================== DOC CHI BAO KHUNG LON ======================
bool DocKhungLon(const int k, double &eLon, double &wLon)
  {
   //--- so nen khung lon dang thuc su co
   int coNen = Bars(_Symbol, g_su[k].tfLarge);
   int daTinh = BarsCalculated(g_su[k].hRsiLarge);
   int muon = LOOKBACK;
   if(coNen > 1 && coNen - 1 < muon) muon = coNen - 1;
   if(daTinh > 1 && daTinh - 1 < muon) muon = daTinh - 1;
   if(muon < InpWMAPeriod + 5)
     {
      if(!g_su[k].daBaoKhungLon)
        {
         g_su[k].daBaoKhungLon = true;
         GhiLog(g_su[k].ten, 0, "-", "-", 0, 0, 0, 0,
                "KHUNG LON chua du: Bars=" + IntegerToString(coNen) +
                " BarsCalculated=" + IntegerToString(daTinh));
        }
      return(false);
     }

   double rsi[];
   ArraySetAsSeries(rsi, false);
   int got = CopyBuffer(g_su[k].hRsiLarge, 0, 1, muon, rsi);
   if(got < InpWMAPeriod + 5)
     {
      if(!g_su[k].daBaoKhungLon)
        {
         g_su[k].daBaoKhungLon = true;
         GhiLog(g_su[k].ten, 0, "-", "-", 0, 0, 0, 0,
                "KHUNG LON CopyBuffer=" + IntegerToString(got) +
                " (xin " + IntegerToString(muon) + ", Bars=" + IntegerToString(coNen) + ")");
        }
      return(false);
     }

   int bd = CatDauHong(rsi, got);
   int m  = got - bd;
   if(m < InpWMAPeriod + 5)
     {
      if(!g_su[k].daBaoKhungLon)
        {
         g_su[k].daBaoKhungLon = true;
         GhiLog(g_su[k].ten, 0, "-", "-", 0, 0, 0, 0,
                "KHUNG LON sau khi cat dau hong chi con " + IntegerToString(m) + " nen");
        }
      return(false);
     }
   double sach[];
   ArrayResize(sach, m);
   for(int i = 0; i < m; i++) sach[i] = rsi[bd + i];
   got = m;

   double e[], w[];
   ComputeEMA(sach, got, InpEMAPeriod, e);
   ComputeWMA(sach, got, InpWMAPeriod, w);
   if(!LaGiaTriTot(e[got-1]) || !LaGiaTriTot(w[got-1]))
     {
      if(!g_su[k].daBaoKhungLon)
        {
         g_su[k].daBaoKhungLon = true;
         GhiLog(g_su[k].ten, 0, "-", "-", 0, 0, 0, 0,
                "KHUNG LON gia tri hong, got=" + IntegerToString(got));
        }
      return(false);
     }

   if(!g_su[k].daBaoKhungLonOK)
     {
      g_su[k].daBaoKhungLonOK = true;
      GhiLog(g_su[k].ten, 0, "-", "-", 0, 0, 0, 0,
             "khung lon OK: dung " + IntegerToString(got) + " nen (bo " +
             IntegerToString(bd) + " nen dau hong)");
     }
   eLon = e[got-1]; wLon = w[got-1];
   return(true);
  }

//====================== DUNG LAI TRANG THAI TU LICH SU =============
// Day la cho sua chinh cua v2.1.
// Moi lan co nen khung giua dong cua, ta KHONG cong don tiep vao
// trang thai cu, ma dung lai toan bo tu dau cua so du lieu:
//   - danh sach swing (fractal InpWing nen hai ben)
//   - may trang thai quan tinh (vung 70/30 + co suy yeu)
// Nho vay bo lo mot nen cung khong lam lech trang thai vinh vien.
// Da kiem chung tren Python: dung lai tu 300 nen gan nhat cho ket
// qua giong het chay tu dau lich su (11/11 lan bat quan tinh).
void XayDungTrangThai(const int k, const MqlRates &rt[], const double &rsi[],
                      const int n, int &momNow, int &momTruoc)
  {
   int wing = InpWing;
   g_su[k].nH = 0; g_su[k].nL = 0;
   int  mom = 0, z70 = 0, z30 = 0;
   bool suy = false;
   momNow = 0; momTruoc = 0;

   for(int i = 2*wing; i < n; i++)
     {
      if(!LaGiaTriTot(rsi[i])) continue;

      //--- swing xac nhan tai nen i-wing
      bool coDinhMoi = false, coDayMoi = false;
      int c = i - wing;
      bool laDinh = true, laDay = true;
      int demH = 0, demL = 0;
      for(int q = c - wing; q <= c + wing; q++)
        {
         if(rt[q].high > rt[c].high) laDinh = false;
         if(rt[q].low  < rt[c].low ) laDay  = false;
         if(rt[q].high == rt[c].high) demH++;
         if(rt[q].low  == rt[c].low ) demL++;
        }
      if(laDinh && demH == 1)
         if(g_su[k].nH == 0 || g_su[k].sH[g_su[k].nH-1].time != rt[c].time)
           { ThemSwing(g_su[k].sH, g_su[k].nH, rt[c].time, rt[c].high, rsi[c]); coDinhMoi = true; }
      if(laDay && demL == 1)
         if(g_su[k].nL == 0 || g_su[k].sL[g_su[k].nL-1].time != rt[c].time)
           { ThemSwing(g_su[k].sL, g_su[k].nL, rt[c].time, rt[c].low, rsi[c]); coDayMoi = true; }

      //--- may trang thai quan tinh
      momTruoc = mom;
      z70 = (rsi[i] >= 70.0) ? z70 + 1 : 0;
      z30 = (rsi[i] <= 30.0) ? z30 + 1 : 0;

      if(z70 >= InpMinBarsInZone)
        {
         if(mom != 1) { mom = 1; suy = false; }
        }
      else if(z30 >= InpMinBarsInZone)
        {
         if(mom != -1) { mom = -1; suy = false; }
        }
      else
        {
         if(mom == 1 && coDinhMoi && g_su[k].nH >= 2)
           {
            double gm = g_su[k].sH[g_su[k].nH-1].price, gc = g_su[k].sH[g_su[k].nH-2].price;
            double rm = g_su[k].sH[g_su[k].nH-1].rsi,   rc = g_su[k].sH[g_su[k].nH-2].rsi;
            if(gm > gc)
              {
               if(rm < 70.0)    { mom = 2;  suy = false; }
               else if(rm < rc) { suy = true; }
              }
           }
         if(mom == -1 && coDayMoi && g_su[k].nL >= 2)
           {
            double gm = g_su[k].sL[g_su[k].nL-1].price, gc = g_su[k].sL[g_su[k].nL-2].price;
            double rm = g_su[k].sL[g_su[k].nL-1].rsi,   rc = g_su[k].sL[g_su[k].nL-2].rsi;
            if(gm < gc)
              {
               if(rm > 30.0)    { mom = -2; suy = false; }
               else if(rm > rc) { suy = true; }
              }
           }
        }
     }
   momNow = mom;
  }

//====================== CHE DO THI TRUONG (chi dung cho chieu ban) =
// Hai dieu kien, deu tinh bang nen DA DONG (shift 1 tro di).
// Day la bo loc lam chieu ban tu AM (-0.072R) thanh DUONG (+0.091R).
// Quan trong: phan lon loi the den tu CHE DO, khong phai tu tin hieu
// RSI - nen KHONG duoc bo bo loc nay de "cho no vao nhieu lenh hon".
bool KhungTuanXuong(void)
  {
   if(g_hRsiW1 == INVALID_HANDLE) return(false);
   int coNen = Bars(_Symbol, PERIOD_W1);
   int daTinh = BarsCalculated(g_hRsiW1);
   int muon = LOOKBACK;
   if(coNen  > 1 && coNen  - 1 < muon) muon = coNen  - 1;
   if(daTinh > 1 && daTinh - 1 < muon) muon = daTinh - 1;
   if(muon < InpWMAPeriod + 5) return(false);
   double r[];
   ArraySetAsSeries(r, false);
   int got = CopyBuffer(g_hRsiW1, 0, 1, muon, r);
   if(got < InpWMAPeriod + 5) return(false);
   int bd = CatDauHong(r, got);
   int m = got - bd;
   if(m < InpWMAPeriod + 5) return(false);
   double sach[];
   ArrayResize(sach, m);
   for(int i = 0; i < m; i++) sach[i] = r[bd + i];
   double e[], w[];
   ComputeEMA(sach, m, InpEMAPeriod, e);
   ComputeWMA(sach, m, InpWMAPeriod, w);
   if(!LaGiaTriTot(e[m-1]) || !LaGiaTriTot(w[m-1])) return(false);
   return(e[m-1] < w[m-1]);
  }

// D1 dong cua duoi SMA50 cua chinh D1 (nen D1 da dong).
bool D1DuoiTrungBinh(void)
  {
   int per = InpBanD1MAPeriod;
   if(per < 2) return(false);
   MqlRates r[];
   ArraySetAsSeries(r, false);
   int got = CopyRates(_Symbol, PERIOD_D1, 1, per, r);
   if(got < per) return(false);
   double s = 0;
   for(int i = 0; i < got; i++)
     {
      if(r[i].close <= 0) return(false);
      s += r[i].close;
     }
   double ma = s / got;
   return(r[got-1].close < ma);
  }

bool CheDoGiam(void)
  {
   if(InpBanCanD1DuoiMA && !D1DuoiTrungBinh()) return(false);
   if(InpBanCanW1Xuong  && !KhungTuanXuong())  return(false);
   return(true);
  }

//====================== TIN HIEU BAN TU KHUNG LON ==================
// Khac han v2.5: v2.5 bat EMA/WMA cat xuong o KHUNG GIUA roi hoi
// khung lon co dong y khong. v2.6 bat cat xuong NGAY TREN KHUNG LON,
// khung giua chi con nhiem vu dat SL.
// Doc hai gia tri cuoi cua duong EMA/WMA khung lon (nen da dong) va
// tra ve true neu nen khung lon VUA DONG la nen cat xuong.
bool KhungLonCatXuong(const int k)
  {
   int coNen  = Bars(_Symbol, g_su[k].tfLarge);
   int daTinh = BarsCalculated(g_su[k].hRsiLarge);
   int muon = LOOKBACK;
   if(coNen  > 1 && coNen  - 1 < muon) muon = coNen  - 1;
   if(daTinh > 1 && daTinh - 1 < muon) muon = daTinh - 1;
   if(muon < InpWMAPeriod + 5) return(false);

   double rsi[];
   ArraySetAsSeries(rsi, false);
   int got = CopyBuffer(g_su[k].hRsiLarge, 0, 1, muon, rsi);
   if(got < InpWMAPeriod + 5) return(false);

   int bd = CatDauHong(rsi, got);
   int m  = got - bd;
   if(m < InpWMAPeriod + 5) return(false);
   double sach[];
   ArrayResize(sach, m);
   for(int i = 0; i < m; i++) sach[i] = rsi[bd + i];

   double e[], w[];
   ComputeEMA(sach, m, InpEMAPeriod, e);
   ComputeWMA(sach, m, InpWMAPeriod, w);
   if(!LaGiaTriTot(e[m-1]) || !LaGiaTriTot(w[m-1]) ||
      !LaGiaTriTot(e[m-2]) || !LaGiaTriTot(w[m-2])) return(false);

   return(e[m-2] >= w[m-2] && e[m-1] < w[m-1]);
  }

//====================== DIEU PHOI CHIEU BAN ========================
// Goi moi khi co nen KHUNG GIUA dong cua. Chi vao lenh o nen khung
// giua DAU TIEN sau khi nen khung lon dong cua - giong het ban Python
// (sim8.py): tim vi tri bang searchsorted tren thoi diem dong cua.
// Co tLonBan dam bao mot nen khung lon chi sinh ra toi da MOT lenh.
void XuLyChieuBan(const int k, const datetime tNen)
  {
   datetime tLon = iTime(_Symbol, g_su[k].tfLarge, 1);   // nen khung lon da dong
   if(tLon == 0) return;
   if(tLon == g_su[k].tLonBan) return;                   // nen nay da xet roi
   bool lanDau = (g_su[k].tLonBan == 0);
   g_su[k].tLonBan = tLon;
   if(lanDau) return;        // vua nap EA: khong vao lenh theo tin hieu cu

   //--- chi vao o nen khung giua DAU TIEN sau khi nen khung lon dong.
   //    Neu EA bo lo nen do (mat ket noi, tester nhay nen) thi bo qua
   //    luon, khong vao tre - vao tre la khop o gia khac han backtest.
   datetime tLonDong = tLon  + PeriodSeconds(g_su[k].tfLarge);
   datetime tMidDong = tNen  + PeriodSeconds(g_su[k].tfMid);
   if(tMidDong < tLonDong) return;
   if(tMidDong - tLonDong >= PeriodSeconds(g_su[k].tfMid))
     {
      GhiLog(g_su[k].ten, tNen, "BAN_LON", "SELL", 0, 0, 0, 0,
             "bo qua - lo nen khung lon, khong vao tre");
      return;
     }

   if(!KhungLonCatXuong(k)) return;

   if(!CheDoGiam())
     {
      GhiLog(g_su[k].ten, tNen, "BAN_LON", "SELL", 0, 0, 0, 0,
             "bo qua - chua du che do giam (D1 duoi SMA" +
             IntegerToString(InpBanD1MAPeriod) + " + W1 xuong)");
      return;
     }
   if(g_su[k].nH < 1) return;
   VaoLenhBan(k, tNen);
  }

//====================== XU LY 1 NEN KHUNG GIUA =====================
void XuLySetup(const int k)
  {
   if(!g_su[k].dung) return;

   datetime tBar = iTime(_Symbol, g_su[k].tfMid, 0);
   if(tBar == 0 || tBar == g_su[k].lastBar) { DonDepLenh(k, false); return; }
   g_su[k].lastBar = tBar;

   //--- lay cac nen DA DONG (tu shift 1), xep TANG dan thoi gian
   //    LUU Y: CopyRates va CopyBuffer co the tra ve SO LUONG KHAC NHAU
   //    (nen co san nhieu hon gia tri chi bao da tinh). Ca hai deu ket
   //    thuc o nen shift 1, nen ta cat lay PHAN CUOI bang nhau roi moi
   //    dung. Ban v2.0 doi hai so phai bang nhau va lang le bo qua ca
   //    nen do - day la ly do setup C gan nhu khong vao lenh nao.
   MqlRates rtAll[];
   double   rsiAll[];
   ArraySetAsSeries(rtAll, false);
   ArraySetAsSeries(rsiAll, false);
   int nRate = CopyRates(_Symbol, g_su[k].tfMid, 1, LOOKBACK, rtAll);
   int nRsi  = CopyBuffer(g_su[k].hRsiMid, 0, 1, LOOKBACK, rsiAll);
   int n = MathMin(nRate, nRsi);
   int nToiThieu = InpWMAPeriod + 4*InpWing + 20;
   if(n < nToiThieu)
     {
      if(!g_su[k].daBaoThieuDL)
        {
         g_su[k].daBaoThieuDL = true;
         GhiLog(g_su[k].ten, tBar, "-", "-", 0, 0, 0, 0,
                "chua du du lieu: nen=" + IntegerToString(nRate) +
                " rsi=" + IntegerToString(nRsi));
        }
      return;
     }

   //--- cat bo phan dau hong (o chi bao chua duoc tinh)
   double tam[];
   ArrayResize(tam, n);
   for(int i = 0; i < n; i++) tam[i] = rsiAll[nRsi - n + i];
   int bdMid = CatDauHong(tam, n);
   n -= bdMid;
   if(n < nToiThieu) return;

   MqlRates rt[];
   double   rsi[];
   ArrayResize(rt, n);
   ArrayResize(rsi, n);
   for(int i = 0; i < n; i++)
     {
      rt[i]  = rtAll[nRate - n + i];
      rsi[i] = rsiAll[nRsi  - n + i];
     }

   double ema[], wma[];
   ComputeEMA(rsi, n, InpEMAPeriod, ema);
   ComputeWMA(rsi, n, InpWMAPeriod, wma);
   int j = n - 1;                       // nen vua dong cua
   if(!LaGiaTriTot(ema[j])   || !LaGiaTriTot(wma[j]) ||
      !LaGiaTriTot(ema[j-1]) || !LaGiaTriTot(wma[j-1])) return;

   //--- dung lai swing + quan tinh tu dau cua so (khong cong don)
   int momNow = 0, momTruoc = 0;
   XayDungTrangThai(k, rt, rsi, n, momNow, momTruoc);

   //--- cap nhat trailing cho cac lenh dang mo
   CapNhatTrailTheoNen(k, rt[j].high, rt[j].close);
   if(InpDungChieuBan) CapNhatTrailBan(k, rt[j].high, rt[j].low, rt[j].close);

   //--- tin hieu
   int cross = 0;
   if(ema[j-1] <= wma[j-1] && ema[j] > wma[j]) cross = +1;
   if(ema[j-1] >= wma[j-1] && ema[j] < wma[j]) cross = -1;

   double eLon = 0, wLon = 0;
   bool coLon = DocKhungLon(k, eLon, wLon);

   string mohinh = "";
   if(cross == +1 && coLon && eLon > wLon) mohinh = "MH2";
   else if(cross == +1)
      GhiLog(g_su[k].ten, rt[j].time, "MH2", "BUY", 0, 0, 0, 0,
             coLon ? "bo qua - khung lon nguoc (" + DoubleToString(eLon,2) + " vs " +
                     DoubleToString(wLon,2) + ")"
                   : "bo qua - khong doc duoc khung lon");
   if(mohinh == "" && momNow == 1 && momTruoc != 1) mohinh = "MH3a";

   //================= CHIEU BAN ====================================
   // Tin hieu lay tu KHUNG LON, khong dung bien `cross` cua khung giua.
   // Toan bo dieu kien nam trong XuLyChieuBan(). Khoi nay khong dung
   // den bat ky bien nao cua chieu mua -> khong the lam lech chieu mua.
   if(InpDungChieuBan) XuLyChieuBan(k, rt[j].time);

   if(mohinh == "") return;
   if(g_su[k].nL < 1) return;

   if(DemLenhMo(g_su[k].magic) >= InpMaxPositions)
     { GhiLog(g_su[k].ten, rt[j].time, mohinh, "BUY", 0, 0, 0, 0, "bo qua - da du lenh"); return; }

   //--- vao lenh MUA
   double sl  = g_su[k].sL[g_su[k].nL-1].price;     // day swing gan nhat, KHONG dem
   double ask = SymbolInfoDouble(_Symbol, SYMBOL_ASK);
   if(ask <= 0 || sl >= ask) return;
   double r = ask - sl;
   //--- LOC DAI SL (phat hien tu backtest 2018-2026):
   //    SL duoi 0.5% gia -> bi quet nhieu, -0.56R/lenh
   //    SL 0.5-1.5% gia  -> +0.60R/lenh (3.4 SE), duong 8/9 nam
   //    SL tren 1.5% gia -> gan nhu khong con loi the (+0.09R)
   double slPct = 100.0 * r / ask;
   if(InpSLMinPct > 0 && slPct < InpSLMinPct)
     { GhiLog(g_su[k].ten, rt[j].time, mohinh, "BUY", ask, sl, r, 0,
              "bo qua - SL qua hep " + DoubleToString(slPct,2) + "%"); return; }
   if(InpSLMaxPct > 0 && slPct > InpSLMaxPct)
     { GhiLog(g_su[k].ten, rt[j].time, mohinh, "BUY", ask, sl, r, 0,
              "bo qua - SL qua rong " + DoubleToString(slPct,2) + "%"); return; }
   double minStop = g_stopLevel * _Point;
   if(minStop > 0 && r < minStop)
     { GhiLog(g_su[k].ten, rt[j].time, mohinh, "BUY", ask, sl, r, 0, "bo qua - SL duoi muc broker"); return; }

   double lot = TinhLot(r);
   if(lot <= 0)
     {
      //--- rui ro tinh theo % muon nho hon lot toi thieu cua san.
      //    Chi nhan lenh neu lot toi thieu van nam trong tran rui ro.
      double loLotMin = (r / g_tickSize) * g_tickValue * g_lotMin;
      double tranTien = AccountInfoDouble(ACCOUNT_BALANCE) * InpTranRuiRoPct / 100.0;
      if(loLotMin > tranTien)
        {
         GhiLog(g_su[k].ten, rt[j].time, mohinh, "BUY", ask, sl, r, 0,
                "bo qua - lot toi thieu rui ro " + DoubleToString(loLotMin,2) + " USD"); return;
        }
      lot = g_lotMin;
     }

   MqlTradeRequest req; MqlTradeResult res;
   ZeroMemory(req); ZeroMemory(res);
   req.action       = TRADE_ACTION_DEAL;
   req.symbol       = _Symbol;
   req.volume       = lot;
   req.type         = ORDER_TYPE_BUY;
   req.price        = ask;
   req.sl           = NormalizeDouble(sl, _Digits);
   req.tp           = 0;
   req.deviation    = InpSlippage;
   req.magic        = g_su[k].magic;
   req.comment      = g_su[k].ten + "_" + mohinh;
   req.type_filling = LayKieuKhop();

   if(!OrderSend(req, res) ||
      (res.retcode != TRADE_RETCODE_DONE && res.retcode != TRADE_RETCODE_PLACED))
     {
      GhiLog(g_su[k].ten, rt[j].time, mohinh, "BUY", ask, sl, r, lot,
             "loi " + IntegerToString(res.retcode));
      return;
     }

   //--- tim ticket vi the vua mo
   ulong tkThat = res.order;
   if(!PositionSelectByTicket(tkThat))
     {
      tkThat = 0;
      datetime moiNhat = 0;
      for(int q = PositionsTotal()-1; q >= 0; q--)
        {
         ulong tk = PositionGetTicket(q);
         if(tk == 0) continue;
         if(PositionGetString(POSITION_SYMBOL) != _Symbol) continue;
         if(PositionGetInteger(POSITION_MAGIC) != g_su[k].magic) continue;
         datetime tt = (datetime)PositionGetInteger(POSITION_TIME);
         if(tt >= moiNhat) { moiNhat = tt; tkThat = tk; }
        }
     }

   double giaVao = (res.price > 0 ? res.price : ask);
   if(g_su[k].nPos < MAX_POS && tkThat > 0)
     {
      int p = g_su[k].nPos;
      g_su[k].pos[p].ticket = tkThat;
      g_su[k].pos[p].tVao   = rt[j].time;
      g_su[k].pos[p].entry  = giaVao;
      g_su[k].pos[p].slGoc  = sl;
      g_su[k].pos[p].st     = 0;
      g_su[k].pos[p].dinh1  = 0;
      g_su[k].pos[p].tDinh1 = 0;
      g_su[k].pos[p].day1   = 0;
      g_su[k].pos[p].trail  = 0;
      g_su[k].pos[p].mohinh = mohinh;
      g_su[k].pos[p].huong  = +1;
      g_su[k].nPos++;
     }

   GhiLog(g_su[k].ten, rt[j].time, mohinh, "BUY", giaVao, sl, r, lot, "mo");
  }

//====================== TRAILING ===================================
// May trang thai giong het ban Python da kiem chung:
//   st0 -> tim DINH swing dau tien sau khi vao lenh        -> Dinh1
//   st1 -> tim DAY swing dau tien sau Dinh1                -> Day1, trail = Day1
//   st2 -> cho gia PHA qua Dinh1                           -> bat trailing
//   st3 -> moi day swing moi cao hon trail va thap hon gia -> doi trail len
// Chi khi st = 3 moi dat SL = trail (truoc do giu SL goc).
void CapNhatTrailTheoNen(const int k, const double nenHigh, const double nenClose)
  {
   DonDepLenh(k, true);

   for(int p = 0; p < g_su[k].nPos; p++)
     {
      if(g_su[k].pos[p].huong != +1) continue;      // lenh ban co ham rieng
      if(g_su[k].pos[p].st == 0)
        {
         for(int i = 0; i < g_su[k].nH; i++)
            if(g_su[k].sH[i].time > g_su[k].pos[p].tVao)
              {
               g_su[k].pos[p].dinh1  = g_su[k].sH[i].price;
               g_su[k].pos[p].tDinh1 = g_su[k].sH[i].time;
               g_su[k].pos[p].st     = 1;
               break;
              }
        }
      if(g_su[k].pos[p].st == 1)
        {
         for(int i = 0; i < g_su[k].nL; i++)
            if(g_su[k].sL[i].time > g_su[k].pos[p].tDinh1)
              {
               g_su[k].pos[p].day1  = g_su[k].sL[i].price;
               g_su[k].pos[p].trail = g_su[k].sL[i].price;
               g_su[k].pos[p].st    = 2;
               break;
              }
        }
      if(g_su[k].pos[p].st == 2)
        {
         if(nenHigh > g_su[k].pos[p].dinh1) g_su[k].pos[p].st = 3;
        }
      if(g_su[k].pos[p].st == 3)
        {
         for(int i = 0; i < g_su[k].nL; i++)
           {
            if(g_su[k].sL[i].time <= g_su[k].pos[p].tDinh1) continue;
            double pr = g_su[k].sL[i].price;
            if(pr > g_su[k].pos[p].trail && pr < nenClose) g_su[k].pos[p].trail = pr;
           }
         DatSL(g_su[k].pos[p].ticket, g_su[k].pos[p].trail);
        }
     }
  }

// Bo cac lenh da dong ra khoi danh sach theo doi
void DonDepLenh(const int k, const bool ghiLog)
  {
   for(int p = g_su[k].nPos - 1; p >= 0; p--)
     {
      if(LenhConSong(g_su[k].pos[p].ticket)) continue;
      if(ghiLog)
         GhiLog(g_su[k].ten, g_su[k].pos[p].tVao, g_su[k].pos[p].mohinh,
                (g_su[k].pos[p].huong == -1 ? "SELL" : "BUY"),
                g_su[k].pos[p].entry, g_su[k].pos[p].slGoc, 0, 0, "dong");
      for(int q = p; q < g_su[k].nPos-1; q++) g_su[k].pos[q] = g_su[k].pos[q+1];
      g_su[k].nPos--;
     }
  }

void DatSL(const ulong ticket, const double slMoi)
  {
   if(!PositionSelectByTicket(ticket)) return;
   double slHienTai = PositionGetDouble(POSITION_SL);
   double sl = NormalizeDouble(slMoi, _Digits);
   if(sl <= slHienTai) return;                       // chi doi len
   double bid = SymbolInfoDouble(_Symbol, SYMBOL_BID);
   double minStop = g_stopLevel * _Point;
   if(bid - sl < minStop) return;                    // qua sat gia, broker tu choi

   MqlTradeRequest req; MqlTradeResult res;
   ZeroMemory(req); ZeroMemory(res);
   req.action   = TRADE_ACTION_SLTP;
   req.symbol   = _Symbol;
   req.position = ticket;
   req.sl       = sl;
   req.tp       = 0;
   OrderSend(req, res);
  }


//====================== VAO LENH BAN ===============================
// Dieu kien tin hieu + che do da duoc XuLyChieuBan() kiem tra xong.
// Ham nay chi lo phan dat lenh: SL, dai SL, khoi luong, gui lenh.
// Dung MAGIC RIENG va HAN MUC RIENG -> khong bao gio chiem cho cua
// lenh mua (day la loi nghiem trong cua v2.5).
void VaoLenhBan(const int k, const datetime tNen)
  {
   if(DemLenhMo(g_su[k].magicBan) >= InpBanMaxPositions)
     { GhiLog(g_su[k].ten, tNen, "BAN_LON", "SELL", 0, 0, 0, 0,
              "bo qua - da du lenh ban"); return; }

   double sl  = g_su[k].sH[g_su[k].nH-1].price;    // dinh swing gan nhat khung giua
   double bid = SymbolInfoDouble(_Symbol, SYMBOL_BID);
   if(bid <= 0 || sl <= bid) return;
   double r = sl - bid;
   double slPct = 100.0 * r / bid;
   if(InpBanSLMinPct > 0 && slPct < InpBanSLMinPct)
     { GhiLog(g_su[k].ten, tNen, "BAN_LON", "SELL", bid, sl, r, 0,
              "bo qua - SL qua hep " + DoubleToString(slPct,2) + "%"); return; }
   if(InpBanSLMaxPct > 0 && slPct > InpBanSLMaxPct)
     { GhiLog(g_su[k].ten, tNen, "BAN_LON", "SELL", bid, sl, r, 0,
              "bo qua - SL qua rong " + DoubleToString(slPct,2) + "%"); return; }
   double minStop = g_stopLevel * _Point;
   if(minStop > 0 && r < minStop) return;

   double lot = TinhLotVoiRuiRo(r, InpBanRiskPercent);
   if(lot <= 0)
     {
      double loLotMin = (r / g_tickSize) * g_tickValue * g_lotMin;
      double tranTien = AccountInfoDouble(ACCOUNT_BALANCE) * InpTranRuiRoPct / 100.0;
      if(loLotMin > tranTien)
        { GhiLog(g_su[k].ten, tNen, "BAN_LON", "SELL", bid, sl, r, 0,
                 "bo qua - lot toi thieu rui ro " + DoubleToString(loLotMin,2) + " USD"); return; }
      lot = g_lotMin;
     }

   MqlTradeRequest req; MqlTradeResult res;
   ZeroMemory(req); ZeroMemory(res);
   req.action       = TRADE_ACTION_DEAL;
   req.symbol       = _Symbol;
   req.volume       = lot;
   req.type         = ORDER_TYPE_SELL;
   req.price        = bid;
   req.sl           = NormalizeDouble(sl, _Digits);
   req.tp           = 0;
   req.deviation    = InpSlippage;
   req.magic        = g_su[k].magicBan;
   req.comment      = g_su[k].ten + "_BAN_LON";
   req.type_filling = LayKieuKhop();

   if(!OrderSend(req, res) ||
      (res.retcode != TRADE_RETCODE_DONE && res.retcode != TRADE_RETCODE_PLACED))
     { GhiLog(g_su[k].ten, tNen, "BAN_LON", "SELL", bid, sl, r, lot,
              "loi " + IntegerToString(res.retcode)); return; }

   ulong tk = res.order;
   if(!PositionSelectByTicket(tk))
     {
      tk = 0; datetime moiNhat = 0;
      for(int q = PositionsTotal()-1; q >= 0; q--)
        {
         ulong t2 = PositionGetTicket(q);
         if(t2 == 0) continue;
         if(PositionGetString(POSITION_SYMBOL) != _Symbol) continue;
         if(PositionGetInteger(POSITION_MAGIC) != g_su[k].magicBan) continue;
         datetime tt = (datetime)PositionGetInteger(POSITION_TIME);
         if(tt >= moiNhat) { moiNhat = tt; tk = t2; }
        }
     }
   double giaVao = (res.price > 0 ? res.price : bid);
   if(g_su[k].nPos < MAX_POS && tk > 0)
     {
      int p = g_su[k].nPos;
      g_su[k].pos[p].ticket = tk;
      g_su[k].pos[p].tVao   = tNen;
      g_su[k].pos[p].entry  = giaVao;
      g_su[k].pos[p].slGoc  = sl;
      g_su[k].pos[p].st     = 0;
      g_su[k].pos[p].dinh1  = 0;
      g_su[k].pos[p].tDinh1 = 0;
      g_su[k].pos[p].day1   = 0;
      g_su[k].pos[p].trail  = 0;
      g_su[k].pos[p].mohinh = "BAN_LON";
      g_su[k].pos[p].huong  = -1;
      g_su[k].nPos++;
     }
   GhiLog(g_su[k].ten, tNen, "BAN_LON", "SELL", giaVao, sl, r, lot, "mo");
  }

//====================== TRAILING CHIEU BAN =========================
// Khac han chieu mua: KHONG doi chuoi Day1 -> Dinh1 -> pha Day1.
// Chi can lai du InpBanBatTrailR lan R la bat trailing ngay, lay dinh
// swing gan nhat nam TREN gia dong cua lam muc doi SL.
void CapNhatTrailBan(const int k, const double nenHigh, const double nenLow, const double nenClose)
  {
   for(int p = 0; p < g_su[k].nPos; p++)
     {
      if(g_su[k].pos[p].huong != -1) continue;
      double e = g_su[k].pos[p].entry;
      double r = g_su[k].pos[p].slGoc - e;
      if(r <= 0) continue;
      double lai = (e - nenLow) / r;                  // da lai bao nhieu R
      if(lai < InpBanBatTrailR) continue;

      for(int i = 0; i < g_su[k].nH; i++)
        {
         if(g_su[k].sH[i].time <= g_su[k].pos[p].tVao) continue;
         double pr = g_su[k].sH[i].price;
         if(pr <= nenClose) continue;
         if(g_su[k].pos[p].trail == 0 || pr < g_su[k].pos[p].trail)
            g_su[k].pos[p].trail = pr;
        }
      if(g_su[k].pos[p].trail > 0) DatSLBan(g_su[k].pos[p].ticket, g_su[k].pos[p].trail);
     }
  }

void DatSLBan(const ulong ticket, const double slMoi)
  {
   if(!PositionSelectByTicket(ticket)) return;
   double slHienTai = PositionGetDouble(POSITION_SL);
   double sl = NormalizeDouble(slMoi, _Digits);
   if(slHienTai > 0 && sl >= slHienTai) return;       // chi doi XUONG
   double ask = SymbolInfoDouble(_Symbol, SYMBOL_ASK);
   double minStop = g_stopLevel * _Point;
   if(sl - ask < minStop) return;

   MqlTradeRequest req; MqlTradeResult res;
   ZeroMemory(req); ZeroMemory(res);
   req.action   = TRADE_ACTION_SLTP;
   req.symbol   = _Symbol;
   req.position = ticket;
   req.sl       = sl;
   req.tp       = 0;
   OrderSend(req, res);
  }

//====================== VONG LAP ===================================
void OnTick()
  {
   for(int k = 0; k < 2; k++) XuLySetup(k);
  }
//+------------------------------------------------------------------+
