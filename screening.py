"""
?E??????????E???E????????E?Efinance ????E
Step1: JPX XLS ????????????E???????????E?????E????E?????????E  ?JPX ? .xls ???E????E pip install xlrd ?????????????E??E???????????????????EStep2: ???????E?Eicker.info ? PER??????EStep3: ???????? balance_sheet?financials ???????E?????????
Step4: ??????
Step5: screening_result.json ???E"""
import os
from dotenv import load_dotenv
load_dotenv()

import pandas as pd
import json
import time
import math
from datetime import datetime, timezone, timedelta
import logging
from io import BytesIO
import requests
import yfinance as yf

try:
    import anthropic
except ImportError:
    anthropic = None

# ?E???E????E???????E????????????E CRITICAL ????E?E# for _name in ("urllib3", "urllib3.connectionpool", "yfinance"):
#     logging.getLogger(_name).setLevel(logging.CRITICAL)

# =============================
# ??E# =============================
JPX_LIST_URL = "https://www.jpx.co.jp/markets/statistics-equities/misc/tvdivq0000001vg2-att/data_j.xls"

MIN_MARKET_CAP = 3_000_000_000   # 30?E?E
MAX_MARKET_CAP = 50_000_000_000  # 500?E?E
MAX_PER = 10.0
MIN_NET_CASH_RATIO = 1.0

# Tab2 finance / real estate (JPX 33-sector names, same strings as EXCLUDE_SECTORS)
MAX_MARKET_CAP_FINANCE = 100_000_000_000  # 1000\u5104\u5186
MAX_PER_FINANCE = 30.0

EXCLUDE_SECTORS = [
    "\u9280\u884C\u696D", "\u4FDD\u967A\u696D",
    "\u8A3C\u5238\u3001\u5546\u54C1\u5148\u7269\u53D6\u5F15\u696D", "\u305D\u306E\u4ED6\u91D1\u878D\u696D", "\u4E0D\u52D5\u7523\u696D",
]

MIN_AVG_TRADING_VALUE_20D = 50_000_000
ONE_TIME_PROFIT_RATIO_THRESHOLD = 0.25
MIN_EQUITY_RATIO = 0.30
MAX_LT_DEBT_TO_NP = 5.0

# \u5927\u5316\u3051\u671f\u5f85\u2606: \u6642\u4fa1\u7dcf\u984d\u4e0a\u9650\uff08300\u5104\u672a\u6e80\uff09
TENBAGGER_MAX_MARKET_CAP = 30_000_000_000

SLEEP_SEC = 0.5
TEST_LIMIT = 0  # 0 = \u5168\u9298\u67C4\u300250 = \u30C6\u30B9\u30C8\u5B9F\u884C
ENABLE_AI = True  # True \u3067\u4E0A\u4F4D\u9298\u67C4\u304B\u3089 AI \u5206\u6790\u3092\u5B9F\u884C

# JSON\u51fa\u529b\u30fb\u91d1\u878d\u30bf\u30d6AI\u5bfe\u8c61\u306e\u4e0a\u4f4d\u4ef6\u6570
MAX_JSON_STOCKS = 50

# JPX XLS ?????? code -> ??????????Step1????
JPX_NAME_MAP = {}

# =============================
# Step1: JPX ??????????
# =============================
# JPX ????????????????????????
FALLBACK_CODES = [
    "1301", "1332", "1333", "1376", "1377", "1414", "1417", "1434", "1435", "1444",
    "1605", "1711", "1720", "1721", "1766", "1768", "1780", "1789", "1801", "1802",
    "1803", "1808", "1810", "1811", "1812", "1820", "1822", "1824", "1860", "1861",
    "1878", "1881", "1893", "1897", "1898", "1925", "1928", "1941", "1942", "1951",
    "1952", "1963", "1973", "2002", "2121", "2127", "2146", "2175", "2181", "2201",
    "2220", "2229", "2264", "2267", "2269", "2281", "2282", "2286", "2317", "2327",
    "2331", "2337", "2371", "2379", "2413", "2432", "2433", "2501", "2502", "2503",
    "2531", "2587", "2593", "2651", "2659", "2670", "2702", "2768", "2782", "2784",
    "2788", "2789", "2790", "2791", "2792", "2801", "2802", "2871", "2875", "2897",
    "2914", "3002", "3086", "3092", "3099", "3101", "3103", "3105", "3289", "3382",
    "3402", "3405", "3407", "3436", "3659", "3861", "3863", "4063", "4151", "4188",
    "4202", "4208", "4307", "4324", "4452", "4502", "4503", "4506", "4507", "4519",
    "4523", "4543", "4568", "4578", "4612", "4631", "4661", "4689", "4704", "4755",
    "4901", "4902", "4911", "5019", "5020", "5108", "5201", "5214", "5232", "5233",
    "5301", "5332", "5333", "5401", "5406", "5411", "5541", "5631", "5706", "5711",
    "5713", "5801", "5802", "5803", "6098", "6100", "6178", "6273", "6301", "6302",
    "6305", "6326", "6367", "6479", "6501", "6502", "6503", "6506", "6645", "6674",
    "6701", "6702", "6703", "6723", "6752", "6758", "6861", "6902", "6952", "6954",
    "6971", "6988", "7201", "7202", "7203", "7205", "7211", "7261", "7267", "7270",
    "7272", "7282", "7313", "7453", "7518", "7532", "7581", "7649", "7701", "7729",
    "7751", "7752", "7832", "7911", "7912", "7951", "8001", "8002", "8015", "8028",
    "8031", "8053", "8058", "8233", "8252", "8267", "8306", "8308", "8316", "8331",
    "8411", "8591", "8604", "8628", "8697", "8725", "8750", "8766", "8795", "8801",
    "8802", "8830", "9001", "9005", "9007", "9009", "9020", "9022", "9064", "9101",
    "9104", "9107", "9201", "9202", "9301", "9412", "9432", "9433", "9501", "9502",
    "9503", "9531", "9532", "9602", "9613", "9681", "9735", "9766", "9983", "9984",
]


def step1_get_list_from_jpx():
    print("Step1: JPX ??????????E..")
    try:
        r = requests.get(JPX_LIST_URL, timeout=30)
        r.raise_for_status()
    except Exception as e:
        print(f"  JPX ?????: {e}????????????")
        n = TEST_LIMIT if TEST_LIMIT > 0 else len(FALLBACK_CODES)
        df = pd.DataFrame({"code": FALLBACK_CODES[:n], "name": [""] * min(n, len(FALLBACK_CODES))})
        print(f"  ???: {len(df)}")
        return df
    content = BytesIO(r.content)
    df = None
    # .xls ? xlrd?Exlsx ? openpyxl ?????
    for engine in ["xlrd", "openpyxl"]:
        try:
            df = pd.read_excel(content, engine=engine)
            break
        except Exception as e:
            content.seek(0)
            continue
    if df is None or df.empty:
        print("  XLS/XLSX ?????xlrd/openpyxl ???????????????")
        n = TEST_LIMIT if TEST_LIMIT > 0 else len(FALLBACK_CODES)
        df = pd.DataFrame({"code": FALLBACK_CODES[:n], "name": [""] * min(n, len(FALLBACK_CODES))})
        print(f"  ???: {len(df)}")
        return df
    # ?: 1=???, 2=??, 3=??, 5=33??
    if df.shape[1] < 6:
        print("  JPX ????????????????")
        n = TEST_LIMIT if TEST_LIMIT > 0 else len(FALLBACK_CODES)
        df = pd.DataFrame({"code": FALLBACK_CODES[:n], "name": [""] * min(n, len(FALLBACK_CODES))})
        print(f"  ???: {len(df)}")
        return df
    df = pd.DataFrame({
        "code": df.iloc[:, 1],
        "name": df.iloc[:, 2],
        "market": df.iloc[:, 3],
        "sector": df.iloc[:, 5],
    })
    # ?????4???: 301 -> "1301"?
    def to_code(x):
        try:
            n = int(float(x))
            return str(n).zfill(4)
        except Exception:
            s = str(x).strip()
            return "".join(c for c in s if c.isdigit()).zfill(4)[:4]
    df["code"] = df["code"].apply(to_code)
    df = df[df["code"].str.len() >= 4]
    # ?????: 1000?9999 ?4??1301???
    df = df[df["code"].str.match(r"^[1-9]\d{3}$")]
    df = df.drop_duplicates(subset=["code"], keep="first")
    df = df.sort_values("code", ascending=False).reset_index(drop=True)

    print(f"  JPX??????E???: {len(df)}")
    # ??: ???????????????????ETF/ETN???
    m = df["market"].astype(str)
    m_prime = m.str.contains("\u30D7\u30E9\u30A4\u30E0", na=False, regex=False)
    m_std = m.str.contains("\u30B9\u30BF\u30F3\u30C0\u30FC\u30C9", na=False, regex=False)
    m_growth = m.str.contains("\u30B0\u30ED\u30FC\u30B9", na=False, regex=False)
    df = df[(m_prime | m_std | m_growth)].copy()
    print(f"  ?????????E??: {len(df)}")
    # ??: EXCLUDE_SECTORS ???
    s = df["sector"].astype(str)
    exclude_mask = s.str.contains(EXCLUDE_SECTORS[0], na=False, regex=False)
    for exc in EXCLUDE_SECTORS[1:]:
        exclude_mask = exclude_mask | s.str.contains(exc, na=False, regex=False)
    df = df.loc[~exclude_mask].copy()
    print(f"  ?????????E??: {len(df)}")
    if len(df) > 0:
        print("  ??5???E?????E????E??????E?E")
        for _, row in df.head(5).iterrows():
            print(f"    {row['code']} | {row['name']} | {row['market']} | {row['sector']}")

    if len(df) == 0:
        print("  ????????0????????????????????????")
        n = TEST_LIMIT if TEST_LIMIT > 0 else len(FALLBACK_CODES)
        df = pd.DataFrame({"code": FALLBACK_CODES[:n], "name": [""] * min(n, len(FALLBACK_CODES))})
    # code -> ????????????
    global JPX_NAME_MAP
    JPX_NAME_MAP = {}
    for _, row in df.iterrows():
        c = str(row["code"]).strip()
        nm = str(row.get("name", "") or "").strip()
        if c and nm:
            JPX_NAME_MAP[c] = nm
    print(f"  ???????: {len(df)} ??")
    return df


def step1_get_finance_list_from_jpx():
    """JPX XLS: 33-sector column; keep only bank/insurance/securities/real estate/other finance."""
    print("Step1 (finance): JPX list (finance sectors)...")
    global JPX_NAME_MAP
    try:
        r = requests.get(JPX_LIST_URL, timeout=30)
        r.raise_for_status()
    except Exception as e:
        print(f"  JPX download failed: {e}")
        return pd.DataFrame(columns=["code", "name", "market", "sector"])
    content = BytesIO(r.content)
    df = None
    for engine in ["xlrd", "openpyxl"]:
        try:
            df = pd.read_excel(content, engine=engine)
            break
        except Exception:
            content.seek(0)
            continue
    if df is None or df.empty or df.shape[1] < 6:
        print("  JPX XLS invalid for finance list")
        return pd.DataFrame(columns=["code", "name", "market", "sector"])
    df = pd.DataFrame({
        "code": df.iloc[:, 1],
        "name": df.iloc[:, 2],
        "market": df.iloc[:, 3],
        "sector": df.iloc[:, 5],
    })

    def to_code(x):
        try:
            n = int(float(x))
            return str(n).zfill(4)
        except Exception:
            s = str(x).strip()
            return "".join(c for c in s if c.isdigit()).zfill(4)[:4]

    df["code"] = df["code"].apply(to_code)
    df = df[df["code"].str.len() >= 4]
    df = df[df["code"].str.match(r"^[1-9]\d{3}$")]
    df = df.drop_duplicates(subset=["code"], keep="first")
    df = df.sort_values("code", ascending=False).reset_index(drop=True)
    m = df["market"].astype(str)
    m_prime = m.str.contains("\u30D7\u30E9\u30A4\u30E0", na=False, regex=False)
    m_std = m.str.contains("\u30B9\u30BF\u30F3\u30C0\u30FC\u30C9", na=False, regex=False)
    m_growth = m.str.contains("\u30B0\u30ED\u30FC\u30B9", na=False, regex=False)
    df = df[(m_prime | m_std | m_growth)].copy()
    s = df["sector"].astype(str)
    include_mask = s.str.contains(EXCLUDE_SECTORS[0], na=False, regex=False)
    for exc in EXCLUDE_SECTORS[1:]:
        include_mask = include_mask | s.str.contains(exc, na=False, regex=False)
    df = df.loc[include_mask].copy()
    print(f"  finance sector rows: {len(df)}")
    for _, row in df.iterrows():
        c = str(row["code"]).strip()
        nm = str(row.get("name", "") or "").strip()
        if c and nm:
            JPX_NAME_MAP[c] = nm
    return df


def _market_label_for_code(stocks_df, code):
    """JPX XLS market column joined by stock code (\u5e02\u5834\u30fb\u5546\u54c1\u533a\u5206)."""
    if stocks_df is None or "market" not in stocks_df.columns:
        return ""
    sub = stocks_df.loc[stocks_df["code"] == code, "market"]
    if sub.empty:
        return ""
    v = sub.iloc[0]
    if pd.isna(v):
        return ""
    s = str(v).strip()
    if not s or s.lower() == "nan":
        return ""
    return s


# =============================
# Step2: ???????E?Eicker.info?E?E# =============================
def step2_first_filter(stocks_df):
    print("Step2: ???????E?EER??????E..")
    codes = stocks_df["code"].tolist()
    if TEST_LIMIT > 0:
        codes = codes[:TEST_LIMIT]
    first_pass = []
    total = len(codes)
    for i, code in enumerate(codes):
        progress_interval = 10 if TEST_LIMIT > 0 else 100
        if (i + 1) % progress_interval == 0 or (i + 1) == total:
            print(f"  ??E {i+1}/{total} ??????? {len(first_pass)} ??", flush=True)
        if (i + 1) % 100 == 0 and first_pass:
            tmp = [{"code": r["code"], "name": (r.get("name") or r["code"] or "").strip() or r["code"], "per": round(r["per"], 2), "market_cap_oku": round(r["market_cap"] / 1e8, 1)} for r in first_pass]
            with open("screening_result_tmp.json", "w", encoding="utf-8") as f:
                json.dump(tmp, f, ensure_ascii=False, indent=2)
            print(f"  ????E screening_result_tmp.json ({len(first_pass)} ??)", flush=True)
        time.sleep(SLEEP_SEC)
        try:
            ticker = yf.Ticker(f"{code}.T")
            info = ticker.info or {}
            price = info.get("currentPrice") or info.get("regularMarketPrice")
            if price is None or (isinstance(price, float) and math.isnan(price)) or float(price) <= 0:
                continue
            price = float(price)
            market_cap = info.get("marketCap")
            if market_cap is None or (isinstance(market_cap, float) and math.isnan(market_cap)):
                continue
            market_cap = float(market_cap)
            if market_cap < MIN_MARKET_CAP or market_cap > MAX_MARKET_CAP:
                continue
            pe = info.get("trailingPE")
            if pe is None or (isinstance(pe, float) and math.isnan(pe)):
                continue
            per = float(pe)
            if not per or per <= 0 or per > MAX_PER:
                continue
            eps = info.get("trailingEps")
            if eps is None: eps = price / per if per else 0
            # \u9ED2\u5B57\u5224\u5B9A: financials \u306E Net Income \u76F4\u6700\u671F\u786E\u5B9A\u5024\u3092\u4F7F\u3046
            try:
                fin = ticker.financials
                if fin is not None and not fin.empty and "Net Income" in fin.index:
                    net_income = fin.loc["Net Income"].iloc[0]
                    if net_income is not None and not (isinstance(net_income, float) and math.isnan(net_income)):
                        if float(net_income) <= 0:
                            continue  # \u8D64\u5B57\u9664\u5916
            except Exception:
                pass  # \u53D6\u5F97\u3067\u304D\u306A\u3044\u5834\u5408\u306F\u30B9\u30AD\u30C3\u30D7\u3057\u306A\u3044
            sector = (info.get("sector") or info.get("industry") or "") or ""
            if any(exc in sector for exc in EXCLUDE_SECTORS):
                continue
            nm = info.get("shortName") or ""
            if not nm and "name" in stocks_df.columns:
                rows = stocks_df[stocks_df["code"] == code]
                nm = rows["name"].values[0] if len(rows) else ""
            if not nm:
                nm = code
            # dividend_yield: yfinance info["dividendYield"] is already % (e.g. 3.45); do not *100
            raw_div = info.get("dividendYield", 0)
            try:
                raw_div = float(raw_div)
                if math.isnan(raw_div):
                    raw_div = 0.0
            except Exception:
                raw_div = 0.0
            div_yield = round(raw_div, 2)

            # chart_signals: 1y/week で簡易トレンド判定
            chart_signals = {
                "volume_surge": False,
                "above_ma": False,
                "near_high": False,
            }
            try:
                hist = ticker.history(period="1y", interval="1wk")
                if hist is not None and not hist.empty and "Volume" in hist.columns and "Close" in hist.columns:
                    vol = hist["Volume"].dropna()
                    close = hist["Close"].dropna()
                    if len(vol) >= 21:
                        latest_vol = float(vol.iloc[-1])
                        avg20 = float(vol.iloc[-21:-1].mean())
                        if avg20 > 0 and latest_vol >= 2 * avg20:
                            chart_signals["volume_surge"] = True
                    if len(close) >= 13:
                        latest_close = float(close.iloc[-1])
                        ma13 = float(close.rolling(window=13).mean().iloc[-1])
                        if ma13 > 0 and latest_close > ma13:
                            chart_signals["above_ma"] = True
                    if len(close) >= 52:
                        latest_close = float(close.iloc[-1])
                        high52 = float(close.iloc[-52:].max())
                        if high52 > 0 and latest_close >= 0.9 * high52:
                            chart_signals["near_high"] = True
            except Exception:
                pass

            website = info.get("website", "") or ""
            jpx_market = _market_label_for_code(stocks_df, code)
            first_pass.append({
                "code": code,
                "name": nm,
                "price": price,
                "market_cap": market_cap,
                "per": per,
                "eps": eps,
                "info": info,
                "dividend_yield": div_yield,
                "website": website,
                "market": jpx_market,
                "chart_signals": chart_signals,
            })
            if TEST_LIMIT > 0:
                print(f"    ????: {code} {nm} (PER={per:.2f}, ????E{market_cap/1e8:.1f}?E", flush=True)
        except Exception as e:
            if TEST_LIMIT > 0:
                print(f"    ??? {code}: {e}", flush=True)
            continue
    print(f"  ????: {len(first_pass)} ??")
    return first_pass


def step2_first_filter_finance(stocks_df):
    print("Step2 (finance): first filter (PBR focus tab)...")
    codes = stocks_df["code"].tolist()
    if TEST_LIMIT > 0:
        codes = codes[:TEST_LIMIT]
    first_pass = []
    total = len(codes)
    for i, code in enumerate(codes):
        progress_interval = 10 if TEST_LIMIT > 0 else 100
        if (i + 1) % progress_interval == 0 or (i + 1) == total:
            print(f"  progress {i+1}/{total} passed {len(first_pass)}", flush=True)
        time.sleep(SLEEP_SEC)
        try:
            ticker = yf.Ticker(f"{code}.T")
            info = ticker.info or {}
            price = info.get("currentPrice") or info.get("regularMarketPrice")
            if price is None or (isinstance(price, float) and math.isnan(price)) or float(price) <= 0:
                continue
            price = float(price)
            market_cap = info.get("marketCap")
            if market_cap is None or (isinstance(market_cap, float) and math.isnan(market_cap)):
                continue
            market_cap = float(market_cap)
            if market_cap < MIN_MARKET_CAP or market_cap > MAX_MARKET_CAP_FINANCE:
                continue
            pe = info.get("trailingPE")
            if pe is None or (isinstance(pe, float) and math.isnan(pe)):
                continue
            per = float(pe)
            if not per or per <= 0 or per > MAX_PER_FINANCE:
                continue
            eps = info.get("trailingEps")
            if eps is None:
                eps = price / per if per else 0
            try:
                fin = ticker.financials
                if fin is not None and not fin.empty and "Net Income" in fin.index:
                    net_income = fin.loc["Net Income"].iloc[0]
                    if net_income is not None and not (isinstance(net_income, float) and math.isnan(net_income)):
                        if float(net_income) <= 0:
                            continue
            except Exception:
                pass
            nm = info.get("shortName") or ""
            if not nm and "name" in stocks_df.columns:
                rows = stocks_df[stocks_df["code"] == code]
                nm = rows["name"].values[0] if len(rows) else ""
            if not nm:
                nm = code
            raw_div = info.get("dividendYield", 0)
            try:
                raw_div = float(raw_div)
                if math.isnan(raw_div):
                    raw_div = 0.0
            except Exception:
                raw_div = 0.0
            div_yield = round(raw_div, 2)
            chart_signals = {
                "volume_surge": False,
                "above_ma": False,
                "near_high": False,
            }
            try:
                hist = ticker.history(period="1y", interval="1wk")
                if hist is not None and not hist.empty and "Volume" in hist.columns and "Close" in hist.columns:
                    vol = hist["Volume"].dropna()
                    close = hist["Close"].dropna()
                    if len(vol) >= 21:
                        latest_vol = float(vol.iloc[-1])
                        avg20 = float(vol.iloc[-21:-1].mean())
                        if avg20 > 0 and latest_vol >= 2 * avg20:
                            chart_signals["volume_surge"] = True
                    if len(close) >= 13:
                        latest_close = float(close.iloc[-1])
                        ma13 = float(close.rolling(window=13).mean().iloc[-1])
                        if ma13 > 0 and latest_close > ma13:
                            chart_signals["above_ma"] = True
                    if len(close) >= 52:
                        latest_close = float(close.iloc[-1])
                        high52 = float(close.iloc[-52:].max())
                        if high52 > 0 and latest_close >= 0.9 * high52:
                            chart_signals["near_high"] = True
            except Exception:
                pass
            website = info.get("website", "") or ""
            jpx_market = _market_label_for_code(stocks_df, code)
            first_pass.append({
                "code": code,
                "name": nm,
                "price": price,
                "market_cap": market_cap,
                "per": per,
                "eps": eps,
                "info": info,
                "dividend_yield": div_yield,
                "website": website,
                "market": jpx_market,
                "chart_signals": chart_signals,
                "screening_tab": "finance",
            })
        except Exception:
            continue
    print(f"  Step2 finance pass: {len(first_pass)}")
    return first_pass


# =============================
# Step3: ???E?E????????E???????
# =============================
def _num(x):
    if x is None or (isinstance(x, float) and math.isnan(x)): return 0.0
    return float(x)


def get_balance_sheet(ticker):
    try:
        bs = ticker.balance_sheet
        if bs is None or bs.empty: return None
        ca = _num(bs.loc["Current Assets"].iloc[0]) if "Current Assets" in bs.index else 0.0
        tl = _num(bs.loc["Total Liabilities Net Minority Interest"].iloc[0]) if "Total Liabilities Net Minority Interest" in bs.index else 0.0
        inv = _num(bs.loc["Available For Sale Securities"].iloc[0]) if "Available For Sale Securities" in bs.index else 0.0
        cash = _num(bs.loc["Cash And Cash Equivalents"].iloc[0]) if "Cash And Cash Equivalents" in bs.index else 0.0
        ltd = 0.0
        for k in ["Long Term Debt", "Long Term Debt And Capital Lease Obligation"]:
            if k in bs.index: ltd = _num(bs.loc[k].iloc[0]); break
        eq = 0.0
        for k in ["Stockholders Equity", "Total Equity Gross Minority Interest", "Common Stock Equity"]:
            if k in bs.index: eq = _num(bs.loc[k].iloc[0]); break
        ta = _num(bs.loc["Total Assets"].iloc[0]) if "Total Assets" in bs.index else 0.0
        return {"current_assets": ca, "total_liabilities": tl, "inv_securities": inv, "cash": cash, "long_term_debt": ltd, "eq": eq, "ta": ta}
    except Exception:
        return None


def get_valuation_score(net_cash_ratio, per):
    """\u5272\u5B89\u5EA6\u30B9\u30B3\u30A2 \u6700\u592727\u70B9"""
    score = 0
    if net_cash_ratio:
        if net_cash_ratio >= 2.0: score += 18
        elif net_cash_ratio >= 1.5: score += 14
        elif net_cash_ratio >= 1.2: score += 9
        elif net_cash_ratio >= 1.0: score += 5
    if per:
        if per < 5: score += 9
        elif per < 8: score += 5
    return score


def calc_shareholder_score(ticker, info, bs_df):
    """\u682A\u4E3B\u9084\u5143\u4F59\u5730\u30B9\u30B3\u30A2 \u6700\u592718\u70B9\u3002bs_df\u306Fbalance_sheet\u306EDataFrame\u3002"""
    score = 0
    # \u914D\u5F53\u6027\u5411 (0-5)
    pr = info.get("payoutRatio")
    if pr is not None and not (isinstance(pr, float) and math.isnan(pr)):
        pr = float(pr)
        if pr < 0.30: score += 5
        elif pr < 0.50: score += 2
    # \u30AD\u30E3\u30C3\u30B7\u30E5\u7A4D\u307F\u4E0A\u304C\u308A (0-5)
    if bs_df is not None and not bs_df.empty and "Cash And Cash Equivalents" in bs_df.index and bs_df.shape[1] >= 2:
        c0 = _num(bs_df.loc["Cash And Cash Equivalents"].iloc[0])
        c1 = _num(bs_df.loc["Cash And Cash Equivalents"].iloc[1])
        if c1 > 0:
            chg = (c0 - c1) / c1
            if chg > 0.05: score += 5
            elif abs(chg) <= 0.05: score += 2
    # \u9084\u5143\u65B9\u91DD\u5909\u5316 \u5143\u306F\u5897\u914D (0-4) \u53D6\u5F97\u3067\u304D\u306A\u3044\u5834\u5408\u306F0
    try:
        div_rate = info.get("dividendRate") or info.get("dividendsPerShare")
        if div_rate is not None and not (isinstance(div_rate, float) and math.isnan(div_rate)):
            divs = getattr(ticker, "dividends", None)
            if divs is not None and hasattr(divs, "values") and len(divs) >= 2:
                last_2y = divs.tail(8)
                if len(last_2y) >= 2:
                    recent = last_2y.iloc[-2:].sum()
                    older = last_2y.iloc[:-2].tail(4).sum() if len(last_2y) > 2 else last_2y.iloc[0]
                    if older and recent and float(recent) > float(older) * 1.01:
                        score += 4
    except Exception:
        pass
    # \u6771\u8A3CPBR\u5BFE\u5FDC (0-4)
    pbr = info.get("priceToBook")
    if pbr is not None and not (isinstance(pbr, float) and math.isnan(pbr)):
        pbr = float(pbr)
        if pbr < 1.0: score += 4
        elif pbr < 1.5: score += 2
    return score


def calc_risk_penalty(ticker, info, fin, bs_dict):
    """\u30EA\u30B9\u30AF\u51CF\u70B9 \u6700\u5927-18\u70B9\u3002bs_dict\u306Fget_balance_sheet\u306E\u8FD4\u308A\u5024\u3002"""
    penalty = 0
    # \u51FA\u6765\u91CF\u30EA\u30B9\u30AF (-5) 20\u65E5\u5E73\u5747\u58F2\u8CB7\u4EE3\u91D1 (\u5186)
    vol = info.get("averageVolume")
    price = info.get("currentPrice") or info.get("regularMarketPrice")
    if vol is not None and price is not None:
        vol = float(vol) if not (isinstance(vol, float) and math.isnan(vol)) else None
        price = float(price) if not (isinstance(price, float) and math.isnan(price)) else None
        if vol is not None and price is not None and vol > 0 and price > 0:
            trading_value = vol * price
            if trading_value < 50_000_000:
                penalty -= 5
    # \u4E00\u904E\u6027\u5229\u76CA\u30EA\u30B9\u30AF (-5)
    if fin is not None and not fin.empty and "Net Income" in fin.index and "Operating Income" in fin.index:
        ni = _num(fin.loc["Net Income"].iloc[0])
        oi = _num(fin.loc["Operating Income"].iloc[0])
        if ni != 0 and abs(ni) > 1e-6:
            diff_ratio = abs(ni - oi) / abs(ni)
            if diff_ratio > 0.3:
                penalty -= 5
    # \u8CA1\u52D9\u5065\u5168\u6027 (-3) \u81EA\u5DF1\u8CC7\u672C\u6BD4\u7387 < 30%
    if bs_dict is not None and bs_dict.get("ta") and bs_dict.get("eq") is not None:
        ta, eq = bs_dict["ta"], bs_dict["eq"]
        if ta and ta > 0 and eq is not None:
            if (eq / ta) < 0.30:
                penalty -= 3
    return penalty


def get_roe_roic(fin, bs):
    """ROE\u3001ROIC\u3092\u8A08\u7B97\u3002ROE=NI/Equity, ROIC=OP/(Equity+LTD-Cash)"""
    roe_pct = None
    roic_pct = None
    if fin is None or fin.empty or bs is None:
        return roe_pct, roic_pct
    ni = _num(fin.loc["Net Income"].iloc[0]) if "Net Income" in fin.index else 0
    op = _num(fin.loc["Operating Income"].iloc[0]) if "Operating Income" in fin.index else 0
    eq = bs.get("eq") or 0
    ltd = bs.get("long_term_debt") or 0
    cash = bs.get("cash") or 0
    if eq and eq > 0:
        roe_pct = round((ni / eq) * 100, 2)
    ic = eq + ltd - cash
    if ic and ic > 0 and op:
        roic_pct = round((op / ic) * 100, 2)
    return roe_pct, roic_pct


def get_financials_3periods(ticker):
    """??3???????"""
    try:
        fin = ticker.financials
        if fin is None or fin.empty or fin.shape[1] < 3: return []
        rev = fin.loc["Total Revenue"].iloc[:3].tolist() if "Total Revenue" in fin.index else []
        op = fin.loc["Operating Income"].iloc[:3].tolist() if "Operating Income" in fin.index else []
        ni = fin.loc["Net Income"].iloc[:3].tolist() if "Net Income" in fin.index else []
        n = min(3, len(rev) or 3, len(op) or 3, len(ni) or 3)
        if n == 0: return []
        out = []
        for i in range(n):
            out.append({
                "Sales": _num(rev[i]) if i < len(rev) else 0,
                "OP": _num(op[i]) if i < len(op) else 0,
                "NP": _num(ni[i]) if i < len(ni) else 0,
            })
        return out
    except Exception:
        return []


def calc_net_cash_ratio(bs, market_cap):
    if not bs or not market_cap or market_cap <= 0: return None
    ca = bs["current_assets"]
    tl = bs["total_liabilities"]
    inv = bs["inv_securities"]
    if ca == 0 and tl == 0 and inv == 0: return None
    net_cash = ca + (inv * 0.7) - tl
    return net_cash / market_cap


def calc_theoretical_price(row, info):
    """theoretical_price = asset_value + business_value (yfinance info + row roe/equity_ratio %)."""
    info = info or {}
    try:
        bps = float(info.get("bookValue") or 0)
    except (TypeError, ValueError):
        bps = 0.0
    if isinstance(bps, float) and math.isnan(bps):
        bps = 0.0
    try:
        eps = float(info.get("trailingEps") or 0)
    except (TypeError, ValueError):
        eps = 0.0
    if isinstance(eps, float) and math.isnan(eps):
        eps = 0.0
    sp_raw = info.get("currentPrice")
    if sp_raw is None:
        sp_raw = info.get("regularMarketPrice", 0)
    try:
        stock_price = float(sp_raw or 0)
    except (TypeError, ValueError):
        stock_price = 0.0
    if isinstance(stock_price, float) and math.isnan(stock_price):
        stock_price = 0.0

    try:
        er = float(row.get("equity_ratio") or 0)
    except (TypeError, ValueError):
        er = 0.0
    if isinstance(er, float) and math.isnan(er):
        er = 0.0
    if er >= 70:
        discount_rate = 1.0
    elif er >= 50:
        discount_rate = 0.8
    elif er >= 30:
        discount_rate = 0.6
    else:
        discount_rate = 0.4

    if bps < 0:
        asset_value = 0.0
    else:
        asset_value = bps * discount_rate

    try:
        roe = float(row.get("roe") or 0)
    except (TypeError, ValueError):
        roe = 0.0
    if isinstance(roe, float) and math.isnan(roe):
        roe = 0.0
    if roe >= 20:
        roe_correction = 1.2
    elif roe >= 15:
        roe_correction = 1.1
    elif roe >= 10:
        roe_correction = 1.0
    elif roe >= 8:
        roe_correction = 0.8
    else:
        roe_correction = 0.6

    base_per = 12.0
    if eps < 0:
        business_value = 0.0
    else:
        business_value = eps * base_per * roe_correction

    theoretical_price = asset_value + business_value
    row["theoretical_price"] = round(theoretical_price, 0)

    if stock_price <= 0:
        upside = 0.0
    else:
        upside = round((theoretical_price - stock_price) / stock_price * 100, 1)
    row["upside_percent"] = upside


def step3_detail_and_net_cash(first_pass):
    print("Step3: ???????????E?E????E??????E???????...")
    second = []
    total = len(first_pass)
    for i, row in enumerate(first_pass):
        progress_interval = 10 if TEST_LIMIT > 0 else 100
        if (i + 1) % progress_interval == 0 or (i + 1) == total:
            print(f"  ??E {i+1}/{total} ??????? {len(second)} ??", flush=True)
        time.sleep(SLEEP_SEC)
        try:
            code = row["code"]
            ticker = yf.Ticker(f"{code}.T")
            bs = get_balance_sheet(ticker)
            if bs is None:
                continue
            nc = calc_net_cash_ratio(bs, row["market_cap"])
            if nc is None or nc < MIN_NET_CASH_RATIO:
                continue
            annual_list = get_financials_3periods(ticker)
            if not annual_list:
                continue
            np_latest = annual_list[0]["NP"]
            np_val = float(np_latest) if np_latest is not None else 0
            if np_val <= 0:
                continue
            fin = ticker.financials
            info = row.get("info") or {}
            bs_raw = ticker.balance_sheet
            shareholder_score = calc_shareholder_score(ticker, info, bs_raw)
            risk_penalty = calc_risk_penalty(ticker, info, fin, bs)
            roe_pct, roic_pct = get_roe_roic(fin, bs)
            # payout_ratio: 配当性向（%）= info["payoutRatio"] * 100
            raw_pr = info.get("payoutRatio", 0)
            try:
                v = float(raw_pr)
                if math.isnan(v):
                    v = 0
            except Exception:
                v = 0
            payout_ratio = round(v * 100, 2)
            pbr = info.get("priceToBook")
            if pbr is not None and not (isinstance(pbr, float) and math.isnan(pbr)):
                pbr = round(float(pbr), 2)
            else:
                pbr = None
            # Inputs for the new shareholder/bonus scoring.
            cash_score = 0
            policy_change_score = 1
            bonus_operating_cf_3y = False
            bonus_dividend_3y_increasing = False
            try:
                # Cash trend (cash equivalents)
                if bs_raw is not None and not bs_raw.empty and "Cash And Cash Equivalents" in bs_raw.index and bs_raw.shape[1] >= 2:
                    c0 = _num(bs_raw.loc["Cash And Cash Equivalents"].iloc[0])
                    c1 = _num(bs_raw.loc["Cash And Cash Equivalents"].iloc[1])
                    if c1 and c1 != 0:
                        if c0 > c1:
                            cash_score = 3
                        elif abs(c0 - c1) / abs(c1) <= 0.05:
                            cash_score = 1

                # Operating Cash Flow (3 periods positive)
                cashflow = getattr(ticker, "cashflow", None)
                if cashflow is not None and not cashflow.empty:
                    for key in (
                        "Operating Cash Flow",
                        "Net Cash Provided By Operating Activities",
                        "NetCashProvidedByOperatingActivities",
                    ):
                        if key in cashflow.index:
                            vals = cashflow.loc[key].iloc[:3].tolist()
                            if len(vals) >= 3:
                                ok = True
                                for vv in vals:
                                    try:
                                        fvv = float(vv)
                                        if math.isnan(fvv) or fvv <= 0:
                                            ok = False
                                            break
                                    except Exception:
                                        ok = False
                                        break
                                bonus_operating_cf_3y = ok
                            break

                # Dividend increase (3 annual periods strictly increasing)
                divs = getattr(ticker, "dividends", None)
                if divs is not None and hasattr(divs, "resample") and len(divs) >= 10:
                    annual = divs.resample("Y").sum()
                    if annual is not None and len(annual) >= 3:
                        last3 = annual.iloc[-3:].tolist()
                        try:
                            a0 = float(last3[0])
                            a1 = float(last3[1])
                            a2 = float(last3[2])
                            if a0 > 0 and a1 > 0 and a2 > 0 and a0 < a1 and a1 < a2:
                                bonus_dividend_3y_increasing = True
                        except Exception:
                            pass

                    # Dividend up/maintenance/down for policy change score
                    if len(annual) >= 2:
                        prev = float(annual.iloc[-2])
                        last = float(annual.iloc[-1])
                        if prev > 0:
                            chg = (last - prev) / abs(prev)
                            if chg >= 0.01:
                                div_inc = True
                            elif abs(chg) <= 0.01:
                                div_maintain = True
                        else:
                            div_inc = last > 0
                    else:
                        div_inc = False
                        div_maintain = False

                    div_inc = locals().get("div_inc", False)
                    div_maintain = locals().get("div_maintain", False)

                    # Buyback detection
                    buyback = False
                    try:
                        cashflow2 = getattr(ticker, "cashflow", None)
                        if cashflow2 is not None and not cashflow2.empty:
                            for key in (
                                "Repurchase Of Stock",
                                "RepurchaseOfStock",
                                "PaymentsForRepurchaseOfStock",
                                "Stock BuyBack",
                                "Repurchase Of Common Stock",
                                "Repurchase Of Equity",
                            ):
                                if key in cashflow2.index:
                                    vrep = cashflow2.loc[key].iloc[0]
                                    fvp = float(vrep)
                                    if not math.isnan(fvp) and fvp < 0:
                                        buyback = True
                                        break
                    except Exception:
                        pass

                    if div_inc or buyback:
                        policy_change_score = 2
                    elif div_maintain and not buyback:
                        policy_change_score = 1
                    else:
                        policy_change_score = 0
            except Exception:
                pass

            try:
                ta_val = float(bs.get("ta") or 0)
                eq_val = float(bs.get("eq") or 0)
                equity_ratio_pct = round(eq_val / ta_val * 100, 2) if ta_val > 0 else 0.0
            except (TypeError, ValueError):
                equity_ratio_pct = 0.0

            r = dict(row)
            r["yf_bs"] = bs
            r["net_cash_ratio"] = nc
            r["annual_list"] = annual_list
            r["sales"] = annual_list[0]["Sales"]
            r["op"] = annual_list[0]["OP"]
            r["np"] = np_latest
            r["eq"] = bs["eq"]
            r["ta"] = bs["ta"]
            r["odp"] = r["np"]
            r["shareholder_score"] = shareholder_score
            r["risk_penalty"] = risk_penalty
            r["roe"] = roe_pct
            r["roic"] = roic_pct
            r["payout_ratio"] = payout_ratio
            r["pbr"] = pbr
            r["equity_ratio"] = equity_ratio_pct
            # New scoring inputs
            r["cash_score"] = cash_score
            r["policy_change_score"] = policy_change_score
            r["bonus_operating_cf_3y"] = bonus_operating_cf_3y
            r["bonus_dividend_3y_increasing"] = bonus_dividend_3y_increasing
            r["upward_revision"] = False
            info_latest = ticker.info or {}
            calc_theoretical_price(r, info_latest)
            second.append(r)
        except Exception as e:
            import traceback
            print(f"    ERROR {row['code']}: {e}", flush=True)
            if TEST_LIMIT > 0:
                traceback.print_exc()
            continue
    print(f"  \u901A\u904B: {len(second)} \u4EF6")
    return second


def step3_detail_finance(first_pass):
    print("Step3 (finance): detail (no NC ratio gate)...")
    second = []
    total = len(first_pass)
    for i, row in enumerate(first_pass):
        progress_interval = 10 if TEST_LIMIT > 0 else 100
        if (i + 1) % progress_interval == 0 or (i + 1) == total:
            print(f"  progress {i+1}/{total} passed {len(second)}", flush=True)
        time.sleep(SLEEP_SEC)
        try:
            code = row["code"]
            ticker = yf.Ticker(f"{code}.T")
            bs = get_balance_sheet(ticker)
            if bs is None:
                continue
            nc = calc_net_cash_ratio(bs, row["market_cap"])
            if nc is None:
                nc = 0.0
            annual_list = get_financials_3periods(ticker)
            if not annual_list:
                continue
            np_latest = annual_list[0]["NP"]
            np_val = float(np_latest) if np_latest is not None else 0
            if np_val <= 0:
                continue
            fin = ticker.financials
            info = row.get("info") or {}
            bs_raw = ticker.balance_sheet
            shareholder_score = calc_shareholder_score(ticker, info, bs_raw)
            risk_penalty = calc_risk_penalty(ticker, info, fin, bs)
            roe_pct, roic_pct = get_roe_roic(fin, bs)
            raw_pr = info.get("payoutRatio", 0)
            try:
                v = float(raw_pr)
                if math.isnan(v):
                    v = 0
            except Exception:
                v = 0
            payout_ratio = round(v * 100, 2)
            pbr = info.get("priceToBook")
            if pbr is not None and not (isinstance(pbr, float) and math.isnan(pbr)):
                pbr = round(float(pbr), 2)
            else:
                pbr = None
            cash_score = 0
            policy_change_score = 1
            bonus_operating_cf_3y = False
            bonus_dividend_3y_increasing = False
            finance_dividend_quality_score = 3
            finance_recent_div_increase = False
            try:
                if bs_raw is not None and not bs_raw.empty and "Cash And Cash Equivalents" in bs_raw.index and bs_raw.shape[1] >= 2:
                    c0 = _num(bs_raw.loc["Cash And Cash Equivalents"].iloc[0])
                    c1 = _num(bs_raw.loc["Cash And Cash Equivalents"].iloc[1])
                    if c1 and c1 != 0:
                        if c0 > c1:
                            cash_score = 3
                        elif abs(c0 - c1) / abs(c1) <= 0.05:
                            cash_score = 1
                cashflow = getattr(ticker, "cashflow", None)
                if cashflow is not None and not cashflow.empty:
                    for key in (
                        "Operating Cash Flow",
                        "Net Cash Provided By Operating Activities",
                        "NetCashProvidedByOperatingActivities",
                    ):
                        if key in cashflow.index:
                            vals = cashflow.loc[key].iloc[:3].tolist()
                            if len(vals) >= 3:
                                ok = True
                                for vv in vals:
                                    try:
                                        fvv = float(vv)
                                        if math.isnan(fvv) or fvv <= 0:
                                            ok = False
                                            break
                                    except Exception:
                                        ok = False
                                        break
                                bonus_operating_cf_3y = ok
                            break
                divs = getattr(ticker, "dividends", None)
                if divs is not None and hasattr(divs, "resample") and len(divs) >= 10:
                    annual = divs.resample("Y").sum()
                    if annual is not None and len(annual) >= 3:
                        last3 = annual.iloc[-3:].tolist()
                        try:
                            a0 = float(last3[0])
                            a1 = float(last3[1])
                            a2 = float(last3[2])
                            if a0 > 0 and a1 > 0 and a2 > 0 and a0 < a1 and a1 < a2:
                                bonus_dividend_3y_increasing = True
                        except Exception:
                            pass
                    div_inc = False
                    div_maintain = False
                    if annual is not None and len(annual) >= 2:
                        prev = float(annual.iloc[-2])
                        last = float(annual.iloc[-1])
                        if prev > 0:
                            chg = (last - prev) / abs(prev)
                            if chg >= 0.01:
                                div_inc = True
                            elif abs(chg) <= 0.01:
                                div_maintain = True
                        else:
                            div_inc = last > 0
                    buyback = False
                    try:
                        cashflow2 = getattr(ticker, "cashflow", None)
                        if cashflow2 is not None and not cashflow2.empty:
                            for key in (
                                "Repurchase Of Stock",
                                "RepurchaseOfStock",
                                "PaymentsForRepurchaseOfStock",
                                "Stock BuyBack",
                                "Repurchase Of Common Stock",
                                "Repurchase Of Equity",
                            ):
                                if key in cashflow2.index:
                                    vrep = cashflow2.loc[key].iloc[0]
                                    fvp = float(vrep)
                                    if not math.isnan(fvp) and fvp < 0:
                                        buyback = True
                                        break
                    except Exception:
                        pass
                    if div_inc or buyback:
                        policy_change_score = 2
                    elif div_maintain and not buyback:
                        policy_change_score = 1
                    else:
                        policy_change_score = 0
                    finance_dividend_quality_score = 3
                    if bonus_dividend_3y_increasing:
                        finance_dividend_quality_score = 5
                    elif annual is not None and len(annual) >= 2:
                        try:
                            _dlast = float(annual.iloc[-1])
                            _dprev = float(annual.iloc[-2])
                            if _dlast < _dprev:
                                finance_dividend_quality_score = 0
                        except Exception:
                            pass
                    finance_recent_div_increase = bool(div_inc)
            except Exception:
                pass
            try:
                ta_val = float(bs.get("ta") or 0)
                eq_val = float(bs.get("eq") or 0)
                equity_ratio_pct = round(eq_val / ta_val * 100, 2) if ta_val > 0 else 0.0
            except (TypeError, ValueError):
                equity_ratio_pct = 0.0
            r = dict(row)
            r["yf_bs"] = bs
            r["net_cash_ratio"] = nc
            r["equity_ratio"] = equity_ratio_pct
            r["annual_list"] = annual_list
            r["sales"] = annual_list[0]["Sales"]
            r["op"] = annual_list[0]["OP"]
            r["np"] = np_latest
            r["eq"] = bs["eq"]
            r["ta"] = bs["ta"]
            r["odp"] = r["np"]
            r["shareholder_score"] = shareholder_score
            r["risk_penalty"] = risk_penalty
            r["roe"] = roe_pct
            r["roic"] = roic_pct
            r["payout_ratio"] = payout_ratio
            r["pbr"] = pbr
            r["cash_score"] = cash_score
            r["policy_change_score"] = policy_change_score
            r["bonus_operating_cf_3y"] = bonus_operating_cf_3y
            r["bonus_dividend_3y_increasing"] = bonus_dividend_3y_increasing
            r["finance_dividend_quality_score"] = finance_dividend_quality_score
            r["finance_recent_div_increase"] = finance_recent_div_increase
            r["upward_revision"] = False
            info_latest = ticker.info or {}
            calc_theoretical_price(r, info_latest)
            second.append(r)
        except Exception as e:
            print(f"    ERROR finance {row.get('code')}: {e}", flush=True)
            continue
    print(f"  Step3 finance pass: {len(second)}")
    return second


# =============================
# Step4: \u30B9\u30B3\u30A2\u30EA\u30F3\u30B0
# =============================
def calc_score(row):
    # Valuation (max 30)
    nc = row.get("net_cash_ratio", 0) or 0
    per = row.get("per", 0) or 0

    nc_score = 0
    if nc >= 3.0:
        nc_score = 20
    elif nc >= 2.0:
        nc_score = 16
    elif nc >= 1.5:
        nc_score = 13
    elif nc >= 1.0:
        nc_score = 10
    elif nc >= 0.7:
        nc_score = 6
    elif nc >= 0.5:
        nc_score = 3
    else:
        nc_score = 0

    per_score = 0
    if per <= 3:
        per_score = 10
    elif per <= 5:
        per_score = 8
    elif per <= 8:
        per_score = 6
    elif per <= 10:
        per_score = 4
    elif per <= 15:
        per_score = 2
    else:
        per_score = 0

    valuation_score = nc_score + per_score
    valuation_score = min(30, max(0, valuation_score))

    # Growth (max 20)
    annual_list = row.get("annual_list") or []
    sales0 = sales1 = sales2 = 0.0
    np0 = np1 = np2 = 0.0
    if len(annual_list) >= 3:
        sales0 = float(annual_list[0].get("Sales", 0) or 0)
        sales1 = float(annual_list[1].get("Sales", 0) or 0)
        sales2 = float(annual_list[2].get("Sales", 0) or 0)
        np0 = float(annual_list[0].get("NP", 0) or 0)
        np1 = float(annual_list[1].get("NP", 0) or 0)
        np2 = float(annual_list[2].get("NP", 0) or 0)

    revenue_consecutive = 5 if (sales0 > sales1 > sales2) else 0
    profit_consecutive = 5 if (np0 > np1 > np2) else 0

    revenue_growth_score = 0
    if sales1 != 0:
        try:
            revenue_growth_pct = (sales0 - sales1) / abs(sales1) * 100
            if revenue_growth_pct >= 20:
                revenue_growth_score = 5
            elif revenue_growth_pct >= 10:
                revenue_growth_score = 4
            elif revenue_growth_pct >= 5:
                revenue_growth_score = 3
            elif revenue_growth_pct >= 0:
                revenue_growth_score = 1
            else:
                revenue_growth_score = 0
        except Exception:
            revenue_growth_score = 0

    profit_growth_score = 0
    if np1 != 0:
        try:
            profit_growth_pct = (np0 - np1) / abs(np1) * 100
            if profit_growth_pct >= 20:
                profit_growth_score = 5
            elif profit_growth_pct >= 10:
                profit_growth_score = 4
            elif profit_growth_pct >= 5:
                profit_growth_score = 3
            elif profit_growth_pct >= 0:
                profit_growth_score = 1
            else:
                profit_growth_score = 0
        except Exception:
            profit_growth_score = 0

    growth_score = revenue_consecutive + revenue_growth_score + profit_consecutive + profit_growth_score
    growth_score = min(20, max(0, growth_score))

    # Business quality / profitability (max 15)
    roe = row.get("roe") or 0
    roic = row.get("roic") or 0
    roe_score = 0
    if roe >= 15:
        roe_score = 5
    elif roe >= 10:
        roe_score = 4
    elif roe >= 8:
        roe_score = 3
    elif roe >= 5:
        roe_score = 1
    else:
        roe_score = 0

    roic_score = 0
    if roic >= 15:
        roic_score = 5
    elif roic >= 10:
        roic_score = 4
    elif roic >= 8:
        roic_score = 3
    elif roic >= 5:
        roic_score = 1
    else:
        roic_score = 0

    stability_count = 0
    for j in range(3):
        if len(annual_list) < 3:
            break
        sj = float(annual_list[j].get("Sales", 0) or 0)
        oj = float(annual_list[j].get("OP", 0) or 0)
        if sj > 0:
            margin = oj / sj * 100
            if margin >= 5:
                stability_count += 1

    stability_score = 0
    if stability_count == 3:
        stability_score = 5
    elif stability_count == 2:
        stability_score = 3
    elif stability_count == 1:
        stability_score = 1
    else:
        stability_score = 0

    quality_score_detail = roe_score + roic_score + stability_score
    quality_score_detail = min(15, max(0, quality_score_detail))

    # Shareholder return capacity (max 10)
    payout_ratio = row.get("payout_ratio")
    try:
        payout_ratio = float(payout_ratio) if payout_ratio is not None else 0.0
    except Exception:
        payout_ratio = 0.0

    dividend_yield = row.get("dividend_yield")
    try:
        dividend_yield = float(dividend_yield) if dividend_yield is not None else 0.0
    except Exception:
        dividend_yield = 0.0

    payout_score = 0
    if payout_ratio > 0 and dividend_yield > 0:
        if payout_ratio < 30:
            payout_score = 3
        elif payout_ratio < 50:
            payout_score = 2
        else:
            payout_score = 1

    cash_score = row.get("cash_score") or 0
    try:
        cash_score = int(cash_score)
    except Exception:
        cash_score = 0
    cash_score = min(3, max(0, cash_score))

    policy_change_score = row.get("policy_change_score") or 0
    try:
        policy_change_score = int(policy_change_score)
    except Exception:
        policy_change_score = 1
    policy_change_score = min(2, max(0, policy_change_score))

    pbr = row.get("pbr")
    pbr_score = 0
    try:
        if pbr is not None:
            pbr = float(pbr)
            if pbr < 1.0:
                pbr_score = 2
            elif pbr < 2.0:
                pbr_score = 1
            else:
                pbr_score = 0
    except Exception:
        pbr_score = 0

    shareholder_score = payout_score + cash_score + policy_change_score + pbr_score
    shareholder_score = min(10, max(0, shareholder_score))

    # Bonus (max 5)
    bonus_operating_cf_3y = bool(row.get("bonus_operating_cf_3y"))
    bonus_dividend_3y_increasing = bool(row.get("bonus_dividend_3y_increasing"))
    upward_revision = bool(row.get("upward_revision"))

    bonus_combo1 = bool(dividend_yield >= 3.0 and pbr is not None and pbr < 1.0)
    bonus_combo2 = bool(nc >= 2.0 and per <= 5)

    bonus_score = 0
    if bonus_operating_cf_3y:
        bonus_score += 1
    if bonus_dividend_3y_increasing:
        bonus_score += 1
    if upward_revision:
        bonus_score += 1
    if bonus_combo1:
        bonus_score += 1
    if bonus_combo2:
        bonus_score += 1
    bonus_score = min(5, max(0, bonus_score))

    # Risk penalty (negative, approx -30)
    risk_checks = row.get("risk_checks") or {}

    def is_bad(key, inverted):
        val = risk_checks.get(key)
        if val is None:
            return False
        if inverted:
            return bool(val) is True
        return bool(val) is False

    bad_roe = is_bad("roe_15_percent", inverted=False)
    bad_equity = is_bad("equity_ratio_50_percent", inverted=False)
    bad_debt = is_bad("debt_to_profit_5x", inverted=False)
    bad_fcf = is_bad("fcf_stability", inverted=False)
    bad_liquidity = is_bad("liquidity_risk", inverted=True)
    bad_one_time = is_bad("one_time_profit_risk", inverted=True)

    individual = 0
    if bad_roe:
        individual -= 2
    if bad_equity:
        individual -= 3
    if bad_debt:
        individual -= 4
    if bad_fcf:
        individual -= 4
    if bad_liquidity:
        individual -= 3
    if bad_one_time:
        individual -= 4

    xcount = sum([bad_roe, bad_equity, bad_debt, bad_fcf, bad_liquidity, bad_one_time])
    additional = 0
    if xcount <= 2:
        additional = 0
    elif xcount == 3:
        additional = -3
    elif xcount == 4:
        additional = -6
    else:
        additional = -10

    risk_penalty = individual + additional
    risk_penalty = min(0, max(-30, risk_penalty))

    # AI components (0-10 each)
    try:
        trend_score = max(0, min(10, int(row.get("trend_score", 0) or 0)))
    except (TypeError, ValueError):
        trend_score = 0
    try:
        quality_score = max(0, min(10, int(row.get("quality_score", 0) or 0)))
    except (TypeError, ValueError):
        quality_score = 0

    total_score = (
        valuation_score
        + growth_score
        + quality_score_detail
        + shareholder_score
        + trend_score
        + quality_score
        + bonus_score
        + risk_penalty
    )

    total_score = max(0, total_score)

    tenbagger_stars = 0
    try:
        _mc = float(row.get("market_cap") or 0)
        if _mc > 0 and _mc < TENBAGGER_MAX_MARKET_CAP:
            tenbagger_stars += 1
    except (TypeError, ValueError):
        pass
    if len(annual_list) >= 3:
        if sales0 > sales1 > sales2 and sales1 != 0:
            try:
                if (sales0 - sales1) / abs(sales1) * 100 >= 10.0:
                    tenbagger_stars += 1
            except Exception:
                pass
        if np0 > np1 > np2:
            try:
                _op0 = float(annual_list[0].get("OP", 0) or 0)
                _op1 = float(annual_list[1].get("OP", 0) or 0)
                if _op1 != 0 and (_op0 - _op1) / abs(_op1) * 100 >= 10.0:
                    tenbagger_stars += 1
            except Exception:
                pass
    try:
        if float(row.get("roe") or 0) >= 15.0:
            tenbagger_stars += 1
    except (TypeError, ValueError):
        pass
    if nc >= 0.7 and per > 0 and per <= 12:
        tenbagger_stars += 1
    tenbagger_stars = min(5, max(0, int(tenbagger_stars)))

    row["trend_score"] = trend_score
    row["quality_score"] = quality_score
    row["valuation_score"] = valuation_score
    row["growth_score"] = growth_score
    row["quality_score_detail"] = quality_score_detail
    row["shareholder_score"] = shareholder_score
    row["bonus_score"] = bonus_score
    row["risk_penalty"] = risk_penalty
    row["score"] = total_score
    row["tenbagger_stars"] = tenbagger_stars

    return total_score


def calc_score_finance(row):
    """\u91d1\u878d\u30bf\u30d6: \u5272\u5b8935+\u8cea20+AI20+\u682a\u4e3b10+\u30dc\u30fc\u30ca\u30b95\u3001\u30ea\u30b9\u30af\u6700\u5927-30\u3001\u5408\u8a08100\u3002"""
    try:
        per = float(row.get("per") or 0)
    except (TypeError, ValueError):
        per = 0.0
    pbr = row.get("pbr")
    pbr_score = 0
    try:
        if pbr is not None:
            pb = float(pbr)
            if pb < 0.5:
                pbr_score = 30
            elif pb < 0.8:
                pbr_score = 24
            elif pb < 1.0:
                pbr_score = 18
            elif pb < 1.2:
                pbr_score = 8
            elif pb < 1.5:
                pbr_score = 3
            else:
                pbr_score = 0
    except Exception:
        pbr_score = 0

    per_score_fin = 0
    if per > 0:
        if per < 8:
            per_score_fin = 5
        elif per < 12:
            per_score_fin = 3
        elif per < 20:
            per_score_fin = 1

    valuation_score = min(35, max(0, pbr_score + per_score_fin))

    try:
        roe = float(row.get("roe") or 0)
    except (TypeError, ValueError):
        roe = 0.0
    if roe >= 15:
        roe_q = 5
    elif roe >= 10:
        roe_q = 4
    elif roe >= 8:
        roe_q = 3
    elif roe >= 5:
        roe_q = 1
    else:
        roe_q = 0

    annual_list = row.get("annual_list") or []
    op_streak = 0
    for j in range(3):
        if len(annual_list) <= j:
            break
        try:
            op_j = float(annual_list[j].get("OP") or 0)
        except (TypeError, ValueError):
            op_j = 0.0
        if op_j > 0:
            op_streak += 1
        else:
            break
    if op_streak >= 3:
        profit_stab_score = 5
    elif op_streak == 2:
        profit_stab_score = 3
    elif op_streak == 1:
        profit_stab_score = 1
    else:
        profit_stab_score = 0

    try:
        div_stab_score = int(row.get("finance_dividend_quality_score", 3) or 0)
    except (TypeError, ValueError):
        div_stab_score = 3
    div_stab_score = min(5, max(0, div_stab_score))

    try:
        erf = float(row.get("equity_ratio") or 0)
    except (TypeError, ValueError):
        erf = 0.0
    if erf >= 20:
        eq_score = 5
    elif erf >= 10:
        eq_score = 3
    elif erf >= 5:
        eq_score = 1
    else:
        eq_score = 0

    quality_score_detail = min(20, max(0, roe_q + profit_stab_score + div_stab_score + eq_score))

    dividend_yield = row.get("dividend_yield")
    try:
        dividend_yield = float(dividend_yield) if dividend_yield is not None else 0.0
    except Exception:
        dividend_yield = 0.0

    payout_ratio = row.get("payout_ratio")
    try:
        payout_ratio = float(payout_ratio) if payout_ratio is not None else 0.0
    except Exception:
        payout_ratio = 0.0

    if dividend_yield >= 4:
        dy_score = 4
    elif dividend_yield >= 3:
        dy_score = 3
    elif dividend_yield >= 2:
        dy_score = 2
    elif dividend_yield >= 1:
        dy_score = 1
    else:
        dy_score = 0

    if dividend_yield < 0.01:
        payout_pts = 0
    elif payout_ratio < 30:
        payout_pts = 3
    elif payout_ratio < 50:
        payout_pts = 2
    else:
        payout_pts = 1

    policy_change_score = row.get("policy_change_score") or 0
    try:
        policy_change_score = int(policy_change_score)
    except Exception:
        policy_change_score = 1
    if policy_change_score >= 2:
        policy_pts = 3
    elif policy_change_score == 1:
        policy_pts = 1
    else:
        policy_pts = 0

    shareholder_score = min(10, max(0, dy_score + payout_pts + policy_pts))

    trend_score = row.get("trend_score", 0) or 0
    try:
        trend_score = max(0, min(10, int(trend_score)))
    except Exception:
        trend_score = 0
    quality_score = row.get("quality_score", 0) or 0
    try:
        quality_score = max(0, min(10, int(quality_score)))
    except Exception:
        quality_score = 0

    risk_checks = row.get("risk_checks") or {}

    def is_bad(key, inverted):
        val = risk_checks.get(key)
        if val is None:
            return False
        if inverted:
            return bool(val) is True
        return bool(val) is False

    bad_roe = is_bad("roe_15_percent", inverted=False)
    bad_profit_stab = is_bad("profit_stability", inverted=False)
    bad_dividend = is_bad("dividend_stability", inverted=False)
    bad_one_time = is_bad("one_time_profit_risk", inverted=True)
    bad_liquidity = is_bad("liquidity_risk", inverted=True)
    bad_financial = is_bad("financial_health", inverted=False)

    individual = 0
    if bad_roe:
        individual -= 2
    if bad_profit_stab:
        individual -= 4
    if bad_dividend:
        individual -= 3
    if bad_one_time:
        individual -= 4
    if bad_liquidity:
        individual -= 3
    if bad_financial:
        individual -= 4
    individual = max(-20, individual)

    xcount = sum(
        [bad_roe, bad_profit_stab, bad_dividend, bad_one_time, bad_liquidity, bad_financial]
    )
    if xcount <= 2:
        additional = 0
    elif xcount == 3:
        additional = -3
    elif xcount == 4:
        additional = -6
    else:
        additional = -10

    risk_penalty = min(0, max(-30, individual + additional))

    pbr_for_bonus = None
    try:
        if row.get("pbr") is not None:
            pbr_for_bonus = float(row.get("pbr"))
    except Exception:
        pbr_for_bonus = None

    bonus_high_div_no_cut = bool(
        dividend_yield >= 3.0 and risk_checks.get("dividend_stability") is True
    )
    bonus_recent_div_up = bool(row.get("finance_recent_div_increase"))
    bonus_pbr_roe = bool(pbr_for_bonus is not None and pbr_for_bonus < 0.5 and roe >= 10)
    bonus_operating_cf_3y = bool(row.get("bonus_operating_cf_3y"))
    upward_revision = bool(row.get("upward_revision"))

    bonus_score = 0
    if bonus_high_div_no_cut:
        bonus_score += 1
    if bonus_recent_div_up:
        bonus_score += 1
    if bonus_pbr_roe:
        bonus_score += 1
    if bonus_operating_cf_3y:
        bonus_score += 1
    if upward_revision:
        bonus_score += 1
    bonus_score = min(5, max(0, bonus_score))

    growth_score = 0
    total_score = (
        valuation_score
        + quality_score_detail
        + trend_score
        + quality_score
        + shareholder_score
        + bonus_score
        + risk_penalty
    )
    total_score = max(0, total_score)

    row["valuation_score"] = valuation_score
    row["growth_score"] = growth_score
    row["quality_score_detail"] = quality_score_detail
    row["shareholder_score"] = shareholder_score
    row["bonus_score"] = bonus_score
    row["risk_penalty"] = risk_penalty
    row["trend_score"] = trend_score
    row["quality_score"] = quality_score
    row["score"] = total_score
    return total_score


def step4_scoring(second_pass):
    print("Step4: ????????????...")
    for r in second_pass:
        r["score"] = calc_score(r)
    return sorted(second_pass, key=lambda x: -x["score"])


def step4_scoring_finance(second_pass):
    print("Step4 (finance): scoring...")
    for r in second_pass:
        r["score"] = calc_score_finance(r)
    return sorted(second_pass, key=lambda x: -x["score"])


# =============================
# AI \u5206\u6790 (Claude API)
# =============================
AI_RISK_KEYS = [
    "roe_15_percent",
    "equity_ratio_50_percent",
    "debt_to_profit_5x",
    "fcf_stability",
    "liquidity_risk",
    "one_time_profit_risk",
]

FINANCE_AI_RISK_KEYS = [
    "roe_15_percent",
    "profit_stability",
    "dividend_stability",
    "one_time_profit_risk",
    "liquidity_risk",
    "financial_health",
]


def _ai_cache_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "ai_cache.json")


def load_ai_cache():
    path = _ai_cache_path()
    if not os.path.isfile(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def save_ai_cache(cache_data):
    path = _ai_cache_path()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(cache_data, f, ensure_ascii=False, indent=2)


def get_cached_ai(cache, code, mode="general"):
    if not cache or not isinstance(cache, dict):
        return None
    sect = cache.get(mode)
    if not isinstance(sect, dict):
        return None
    return sect.get(str(code))


def _default_risk_checks():
    return {k: None for k in AI_RISK_KEYS}


def _default_finance_risk_checks():
    return {k: None for k in FINANCE_AI_RISK_KEYS}


def _finance_dividend_stability_ok(ticker):
    """\u914d\u5f53\u306e\u5b89\u5b9a\u6027: \u76f4\u8fd1\u5e74\u9593\u914d\u5f53\u304c\u524d\u5e74\u4ee5\u4e0b\u306b\u6e1b\u3063\u3066\u3044\u306a\u3044\u3002\u53d6\u5f97\u4e0d\u53ef\u306fTrue\u3002"""
    try:
        divs = getattr(ticker, "dividends", None)
        if divs is None or not hasattr(divs, "resample") or len(divs) < 2:
            return True
        try:
            annual = divs.resample("YE").sum()
        except Exception:
            annual = divs.resample("Y").sum()
        if annual is None or len(annual) < 2:
            return True
        try:
            last = float(annual.iloc[-1])
            prev = float(annual.iloc[-2])
        except (TypeError, ValueError, IndexError):
            return True
        if math.isnan(last) or math.isnan(prev):
            return True
        return last >= prev
    except Exception:
        return True


def compute_finance_programmatic_risk_checks(row, ticker):
    """\u91d1\u878d\u30bf\u30d6\u7528\u30ea\u30b9\u30af\uff084\u9805\u76ee\uff09\u3092\u30d7\u30ed\u30b0\u30e9\u30e0\u8a08\u7b97\u3002"""
    out = {}
    er = row.get("equity_ratio")
    try:
        if er is not None:
            out["financial_health"] = float(er) >= 5.0
    except (TypeError, ValueError):
        out["financial_health"] = None

    out["dividend_stability"] = _finance_dividend_stability_ok(ticker)

    al = row.get("annual_list") or []
    if len(al) >= 3:
        ok = True
        for j in range(3):
            try:
                op_j = float(al[j].get("OP") or 0)
            except (TypeError, ValueError):
                op_j = 0.0
            if op_j <= 0:
                ok = False
                break
        out["profit_stability"] = ok
    else:
        out["profit_stability"] = True

    if al:
        try:
            op0 = float(al[0].get("OP") or 0)
            np0 = float(al[0].get("NP") or 0)
            denom = max(abs(op0), abs(np0), 1e-9)
            gap = abs(op0 - np0) / denom
            out["one_time_profit_risk"] = gap >= 0.5
        except (TypeError, ValueError):
            out["one_time_profit_risk"] = False
    else:
        out["one_time_profit_risk"] = False

    return out


def finalize_finance_risk_checks(row, ticker):
    """AI\uff082\u9805\u76ee\uff09\u3068\u30d7\u30ed\u30b0\u30e9\u30e0\uff084\u9805\u76ee\uff09\u3092\u7d50\u5408\u3057\u30666\u9805\u76ee\u306erisk_checks\u3092\u5b8c\u6210\u3002"""
    prog = compute_finance_programmatic_risk_checks(row, ticker)
    ai_rc = row.get("risk_checks") or {}
    out = _default_finance_risk_checks()
    for k, v in prog.items():
        if v is not None:
            out[k] = bool(v)
    if ai_rc.get("roe_15_percent") is not None:
        out["roe_15_percent"] = bool(ai_rc["roe_15_percent"])
    else:
        try:
            roe_v = float(row.get("roe") or 0)
            out["roe_15_percent"] = roe_v >= 15.0
        except (TypeError, ValueError):
            out["roe_15_percent"] = None
    if ai_rc.get("liquidity_risk") is not None:
        out["liquidity_risk"] = bool(ai_rc["liquidity_risk"])
    else:
        out["liquidity_risk"] = False
    row["risk_checks"] = out


def _sales_growth_pct(row):
    al = row.get("annual_list") or []
    if len(al) < 2:
        return None
    s0 = al[0].get("Sales") if al[0] else None
    s1 = al[1].get("Sales") if al[1] else None
    if s0 is None or s1 is None or not s1:
        return None
    try:
        return round((float(s0) - float(s1)) / float(s1) * 100, 2)
    except (TypeError, ValueError):
        return None


def _format_3y(values):
    """\u904E\u53BB3\u671F\u306E\u6570\u5024\u3092\u6587\u5B57\u5217\u306B\u30D5\u30A9\u30FC\u30DE\u30C3\u30C8\u3002"""
    if not values:
        return "N/A"
    try:
        return ", ".join(str(int(v)) for v in values[:3])
    except (TypeError, ValueError):
        return "N/A"


def generate_ai_analysis(row, finance_mode=False):
    try:
        if not os.environ.get("ANTHROPIC_API_KEY"):
            return "", ({} if finance_mode else _default_risk_checks()), 0, 0, False

        import anthropic
        client = anthropic.Anthropic()

        name_jp = row.get("name_jp") or row.get("name") or row.get("code")
        code = row.get("code")

        # yfinance ?? IR????????3?????????
        sector = "N/A"
        fin = None
        try:
            ticker = yf.Ticker(f"{code}.T")
            info = ticker.info or {}
            sector = info.get("sector") or info.get("industry") or "N/A"
            fin = ticker.financials
        except Exception:
            fin = None

        revenue_3y = fin.loc["Total Revenue"].iloc[:3].tolist() if fin is not None and not fin.empty and "Total Revenue" in fin.index else []
        op_income_3y = fin.loc["Operating Income"].iloc[:3].tolist() if fin is not None and not fin.empty and "Operating Income" in fin.index else []
        net_income_3y = fin.loc["Net Income"].iloc[:3].tolist() if fin is not None and not fin.empty and "Net Income" in fin.index else []

        def calc_yoy(values):
            if len(values) >= 2:
                try:
                    v0 = float(values[0])
                    v1 = float(values[1])
                    if v1 != 0:
                        return round((v0 - v1) / abs(v1) * 100, 1)
                except Exception:
                    return None
            return None

        revenue_yoy = calc_yoy(revenue_3y)
        op_income_yoy = calc_yoy(op_income_3y)

        def fmt_oku(v):
            try:
                return f"{float(v) / 1e8:.1f}"
            except Exception:
                return "N/A"

        revenue_latest_oku = fmt_oku(revenue_3y[0]) if len(revenue_3y) >= 1 else "N/A"
        revenue_yoy_str = f"{revenue_yoy}" if revenue_yoy is not None else "N/A"
        op_latest_oku = fmt_oku(op_income_3y[0]) if len(op_income_3y) >= 1 else "N/A"
        op_income_yoy_str = f"{op_income_yoy}" if op_income_yoy is not None else "N/A"
        net_latest_oku = fmt_oku(net_income_3y[0]) if len(net_income_3y) >= 1 else "N/A"

        if len(revenue_3y) >= 3:
            revenue_trend = f"{fmt_oku(revenue_3y[2])} -> {fmt_oku(revenue_3y[1])} -> {fmt_oku(revenue_3y[0])}"
        else:
            revenue_trend = "N/A"

        pbr_s = row.get("pbr", "N/A")
        ai_cap = 10

        if finance_mode:
            rubric_trend = f"""trend_score (AI\u696d\u7e3e\u5206\u6790\u3001\u6700\u5927{ai_cap}\u70b9):
\u30fb\u5229\u76ca\u306e\u5b89\u5b9a\u6027\u30fb\u4e00\u904e\u6027\u5229\u76ca\u4f9d\u5b58\u306e\u6709\u7121\u3092\u91cd\u8996
\u30fb\u91d1\u5229\u5909\u52d5\u306e\u5f71\u97ff\u306e\u5927\u304d\u3055
\u30fb3\u671f\u9023\u7d9a\u5897\u6536\u5897\u76ca\u306a\u3089\u9ad8\u70b9\u3001\u6e1b\u53ce\u6e1b\u76ca\u7d99\u7d9a\u306f\u4f4e\u70b9
\u30fb0\u301c{ai_cap}\u306e\u6574\u6570\u3067\u8a55\u4fa1"""

            rubric_quality = f"""quality_score (AI\u4e8b\u696d\u8a55\u4fa1\u3001\u6700\u5927{ai_cap}\u70b9):
\u30fb\u53ce\u76ca\u6e90\u306e\u8cea\uff08\u624b\u6570\u6599\u53ce\u5165vs\u58f2\u5374\u76ca\u7b49\uff09
\u30fb\u8cc7\u672c\u653f\u7b56\u30fb\u9084\u5143\u59ff\u52e2
\u30fb\u666f\u6c17\u611f\u6027\u30fb\u4e8b\u696d\u306e\u7d99\u7d9a\u6027
\u30fb0\u301c{ai_cap}\u306e\u6574\u6570\u3067\u8a55\u4fa1"""

            finance_axes = """
\u3010\u91d1\u878d\u30fb\u4e0d\u52d5\u7523\u5411\u3051\u89b3\u70b9\u3011
\u30fb\u5229\u76ca\u306e\u5b89\u5b9a\u6027\uff08\u4e00\u904e\u6027\u5229\u76ca\u4f9d\u5b58\u306e\u6709\u7121\uff09
\u30fb\u91d1\u5229\u5909\u52d5\u306e\u5f71\u97ff
\u30fb\u53ce\u76ca\u6e90\u306e\u8cea\uff08\u624b\u6570\u6599\u53ce\u5165vs\u58f2\u5374\u76ca\u7b49\uff09
\u30fb\u8cc7\u672c\u653f\u7b56\u30fb\u9084\u5143\u59ff\u52e2
\u30fb\u666f\u6c17\u611f\u6027
"""
        else:
            rubric_trend = """trend_score (\u696d\u7e3e\u30c8\u30ec\u30f3\u30c9\u3001\u6700\u592710\u70b9):
\u30fb3\u671f\u9023\u7d9a\u5897\u6536\u5897\u76ca \u2192 10\u70b9
\u30fb\u5897\u6536 or \u5897\u76ca(\u76f4\u8fd1) \u2192 7\u70b9
\u30fb\u6a2a\u3070\u3044(\u00b15%\u4ee5\u5185) \u2192 4\u70b9
\u30fb\u6e1b\u6536 or \u6e1b\u76ca(\u76f4\u8fd1) \u2192 2\u70b9
\u30fb\u6e1b\u6536\u6e1b\u76ca\u304c\u7d9a\u304f \u2192 0\u70b9"""

            rubric_quality = """quality_score (\u4e8b\u696d\u306e\u8cea\u3001\u6700\u592710\u70b9):
\u30fb\u5f37\u56fa\u306a\u7af6\u4e89\u512a\u4f4d\u6027\u30fb\u53c2\u5165\u969c\u58c1 \u2192 10\u70b9
\u30fb\u4e00\u5b9a\u306e\u7af6\u4e89\u512a\u4f4d \u2192 7\u70b9
\u30fb\u5e73\u5747\u7684 \u2192 4\u70b9
\u30fb\u7af6\u4e89\u6fc0\u5316\u30fb\u53ce\u76ca\u4e0d\u5b89\u5b9a \u2192 2\u70b9
\u30fb\u7d9a\u304d\u61f8\u5ff5 \u2192 0\u70b9"""

            finance_axes = ""

        if finance_mode:
            metrics_line = (
                f"\u81ea\u5df1\u8cc7\u672c\u6bd4: {row.get('equity_ratio', 'N/A')}% / NC\u6bd4: {row.get('net_cash_ratio', 'N/A')} / "
                f"PER: {row.get('per', 'N/A')} / PBR: {pbr_s} / ROE: {row.get('roe', 'N/A')}%"
            )
            fin_risk_note = (
                "\n\uff08\u6ce8\uff09JSON\u5185 risk_checks \u306f"
                " roe_15_percent \u3068 liquidity_risk \u306e2\u30ad\u30fc\u306e\u307f\u8a18\u8f09"
                "\u3059\u308b\u4e8b\u3002\u4ed6\u9805\u76ee\u306f\u30b5\u30fc\u30d0\u5074\u3067\u8a08\u7b97\u3059\u308b\u3002"
            )
            risk_sample_inner = """    "roe_15_percent": true,
    "liquidity_risk": false"""
        else:
            metrics_line = (
                f"NC\u6bd4: {row.get('net_cash_ratio', 'N/A')} / PER: {row.get('per', 'N/A')} / PBR: {pbr_s} / ROE: {row.get('roe', 'N/A')}%"
            )
            fin_risk_note = ""
            risk_sample_inner = """    "roe_15_percent": true,
    "equity_ratio_50_percent": true,
    "debt_to_profit_5x": true,
    "fcf_stability": true,
    "liquidity_risk": false,
    "one_time_profit_risk": false"""

        prompt = f"""
\u9298\u67c4: {name_jp}
\u30bb\u30af\u30bf\u30fc: {sector}

\u6700\u65b0\u696d\u7e3e\u6982\u8981
\u58f2\u4e0a: {revenue_latest_oku}\u5104\u5186
\u58f2\u4e0a\u540c\u6bd4: {revenue_yoy_str}%
\u55b6\u696d\u5229\u76ca: {op_latest_oku}\u5104\u5186
\u55b6\u696d\u5229\u76ca\u540c\u6bd4: {op_income_yoy_str}%
\u7d20\u5229\u76ca: {net_latest_oku}\u5104\u5186

\u904e\u53bb3\u671f\u58f2\u4e0a\u63a8\u79fb: {revenue_trend}

\u6307\u6a19
{metrics_line}
{finance_axes}{fin_risk_note}

\u4ee5\u4e0b\u306eJSON\u306e\u307f\u3067\u56de\u7b54\uff08markdown\u7981\u6b62\uff09\u3002

{rubric_trend}

{rubric_quality}

JSON\u30b5\u30f3\u30d7\u30eb:
{{"ai_comment": "\u696d\u7e3e\u30c8\u30ec\u30f3\u30c9\u30fb\u4e8b\u696d\u8cea\u30fb\u5c06\u6765\u6027\u3092300\u5b57\u7a0b\u5ea6",
  "trend_score": 7,
  "quality_score": 4,
  "risk_checks": {{
{risk_sample_inner}
  }},
  "upward_revision": false
}}
"""

        message = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1200 if finance_mode else 1000,
            system="You are a Japanese stock analyst. Respond ONLY in valid JSON format with no markdown.",
            messages=[{"role": "user", "content": prompt}]
        )

        text = message.content[0].text.strip()
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        text = text.strip()

        try:
            data = json.loads(text)
        except json.JSONDecodeError as e:
            print(f"[AI] JSON parse error: {e}")
            return "", ({} if finance_mode else _default_risk_checks()), 0, 0, False

        ai_comment = (data.get("ai_comment") or "").strip()
        trend_score = data.get("trend_score")
        try:
            trend_score = max(0, min(ai_cap, int(trend_score))) if trend_score is not None else 0
        except (TypeError, ValueError):
            trend_score = 0

        quality_score = data.get("quality_score")
        try:
            quality_score = max(0, min(ai_cap, int(quality_score))) if quality_score is not None else 0
        except (TypeError, ValueError):
            quality_score = 0

        raw_rc = data.get("risk_checks") or {}
        if finance_mode:
            risk_checks = {}
            for k in ("roe_15_percent", "liquidity_risk"):
                v = raw_rc.get(k)
                risk_checks[k] = bool(v) if v is not None else None
        else:
            risk_checks = dict(raw_rc)
            for k in AI_RISK_KEYS:
                if k not in risk_checks:
                    risk_checks[k] = None
                elif risk_checks[k] is not None:
                    risk_checks[k] = bool(risk_checks[k])

        upward_revision = bool(data.get("upward_revision", False))
        return ai_comment, risk_checks, trend_score, quality_score, upward_revision

    except Exception as e:
        print(f"[AI] \u30A8\u30E9\u30FC: {e}")
        import traceback
        traceback.print_exc()
        return "", ({} if finance_mode else _default_risk_checks()), 0, 0, False



# =============================
# Step5: ??E# =============================
def step5_save(results):
    out = []
    for r in results:
        per_val = round(float(r.get("per") or 0), 2)
        if per_val == 0:
            try:
                ticker = yf.Ticker(f"{r['code']}.T")
                info = ticker.info or {}
                pe = info.get("trailingPE")
                if pe is not None and not (isinstance(pe, float) and math.isnan(pe)):
                    pe_f = float(pe)
                    if pe_f >= 0.01:
                        per_val = round(pe_f, 2)
                    else:
                        price = info.get("currentPrice") or info.get("regularMarketPrice")
                        ni = info.get("netIncomeToCommon") or info.get("netIncome")
                        sh = info.get("sharesOutstanding")
                        if price and ni and sh and float(sh) > 0:
                            eps = float(ni) / float(sh)
                            per_val = round(float(price) / eps, 2)
            except Exception:
                pass
        if per_val > MAX_PER:
            continue
        base_name = (r.get("name") or r["code"] or "").strip() or r["code"]
        name_jp = JPX_NAME_MAP.get(r["code"], base_name)
        div_yield = r.get("dividend_yield")
        if div_yield is not None and not (isinstance(div_yield, float) and math.isnan(div_yield)):
            div_yield = round(float(div_yield), 2)
        else:
            div_yield = None
        out.append({
            "code": r["code"],
            "name": base_name,
            "name_jp": name_jp,
            "website": r.get("website", ""),
            "market": r.get("market", ""),
            "score": r["score"],
            "valuation_score": r.get("valuation_score", 0),
            "growth_score": r.get("growth_score", 0),
            "shareholder_score": r.get("shareholder_score", 0),
            "quality_score_detail": r.get("quality_score_detail", 0),
            "bonus_score": r.get("bonus_score", 0),
            "risk_penalty": r.get("risk_penalty", 0),
            "net_cash_ratio": round(r["net_cash_ratio"], 2),
            "per": per_val,
            "market_cap_oku": round(r["market_cap"] / 1e8, 1),
            "dividend_yield": div_yield,
            "payout_ratio": r.get("payout_ratio"),
            "roe": r.get("roe"),
            "roic": r.get("roic"),
            "pbr": r.get("pbr"),
            "ai_comment": r.get("ai_comment", ""),
            "risk_checks": r.get("risk_checks"),
            "trend_score": r.get("trend_score", 0),
            "quality_score": r.get("quality_score", 0),
            "chart_signals": r.get("chart_signals", {}),
            "tenbagger_stars": int(r.get("tenbagger_stars", 0) or 0),
            "tab": "general",
            "theoretical_price": r.get("theoretical_price", 0),
            "upside_percent": r.get("upside_percent", 0),
        })
    out = sorted(out, key=lambda x: x["score"], reverse=True)[:MAX_JSON_STOCKS]
    JST = timezone(timedelta(hours=9))
    updated_at = datetime.now(JST).strftime("%Y-%m-%dT%H:%M:%S+09:00")
    result = {"updated_at": updated_at, "stocks": out}
    with open("screening_result.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print("Step5: screening_result.json ???????")
    return out


def step5_save_finance(results):
    """Write screening_result_finance.json and copy to public/."""
    out = []
    for r in results:
        per_val = round(float(r.get("per") or 0), 2)
        if per_val == 0:
            try:
                ticker = yf.Ticker(f"{r['code']}.T")
                info = ticker.info or {}
                pe = info.get("trailingPE")
                if pe is not None and not (isinstance(pe, float) and math.isnan(pe)):
                    pe_f = float(pe)
                    if pe_f >= 0.01:
                        per_val = round(pe_f, 2)
                    else:
                        price = info.get("currentPrice") or info.get("regularMarketPrice")
                        ni = info.get("netIncomeToCommon") or info.get("netIncome")
                        sh = info.get("sharesOutstanding")
                        if price and ni and sh and float(sh) > 0:
                            eps = float(ni) / float(sh)
                            per_val = round(float(price) / eps, 2)
            except Exception:
                pass
        if per_val > MAX_PER_FINANCE:
            continue
        base_name = (r.get("name") or r["code"] or "").strip() or r["code"]
        name_jp = JPX_NAME_MAP.get(r["code"], base_name)
        div_yield = r.get("dividend_yield")
        if div_yield is not None and not (isinstance(div_yield, float) and math.isnan(div_yield)):
            div_yield = round(float(div_yield), 2)
        else:
            div_yield = None
        nc_raw = r.get("net_cash_ratio", 0) or 0
        try:
            nc_rounded = round(float(nc_raw), 2)
        except (TypeError, ValueError):
            nc_rounded = 0.0
        rc_src = r.get("risk_checks") or {}
        risk_checks_out = {k: rc_src.get(k) for k in FINANCE_AI_RISK_KEYS}
        out.append({
            "code": r["code"],
            "name": base_name,
            "name_jp": name_jp,
            "website": r.get("website", ""),
            "market": r.get("market", ""),
            "score": r["score"],
            "valuation_score": r.get("valuation_score", 0),
            "growth_score": 0,
            "shareholder_score": r.get("shareholder_score", 0),
            "quality_score_detail": r.get("quality_score_detail", 0),
            "bonus_score": r.get("bonus_score", 0),
            "risk_penalty": r.get("risk_penalty", 0),
            "net_cash_ratio": nc_rounded,
            "per": per_val,
            "market_cap_oku": round(r["market_cap"] / 1e8, 1),
            "dividend_yield": div_yield,
            "payout_ratio": r.get("payout_ratio"),
            "roe": r.get("roe"),
            "roic": r.get("roic"),
            "pbr": r.get("pbr"),
            "equity_ratio": round(float(r.get("equity_ratio") or 0), 2),
            "ai_comment": r.get("ai_comment", ""),
            "risk_checks": risk_checks_out,
            "trend_score": r.get("trend_score", 0),
            "quality_score": r.get("quality_score", 0),
            "chart_signals": r.get("chart_signals", {}),
            "tab": "finance",
            "theoretical_price": r.get("theoretical_price", 0),
            "upside_percent": r.get("upside_percent", 0),
        })
    out = sorted(out, key=lambda x: x["score"], reverse=True)[:MAX_JSON_STOCKS]
    JST = timezone(timedelta(hours=9))
    updated_at = datetime.now(JST).strftime("%Y-%m-%dT%H:%M:%S+09:00")
    result = {"updated_at": updated_at, "stocks": out}
    with open("screening_result_finance.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    pub_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public")
    os.makedirs(pub_dir, exist_ok=True)
    pub_path = os.path.join(pub_dir, "screening_result_finance.json")
    with open(pub_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print("Step5 (finance): screening_result_finance.json + public/")
    return out


# =============================
# Tab2 finance pipeline (always run after general)
# =============================
def run_screening_finance_tab():
    print("\n" + "=" * 60)
    print("Tab2: finance / real estate screening")
    print("=" * 60)
    stocks_f = step1_get_finance_list_from_jpx()
    if stocks_f is None or len(stocks_f) == 0:
        print("Step1 (finance): 0 rows")
        step5_save_finance([])
        return
    if TEST_LIMIT > 0:
        stocks_f = stocks_f.iloc[:TEST_LIMIT].copy()
        print(f"TEST_LIMIT: finance first {TEST_LIMIT} codes")
    first_f = step2_first_filter_finance(stocks_f)
    if not first_f:
        print("Step2 (finance): 0 pass")
        step5_save_finance([])
        return
    second_f = step3_detail_finance(first_f)
    if not second_f:
        print("Step3 (finance): 0 pass")
        step5_save_finance([])
        return

    for r in second_f:
        r["ai_comment"] = ""
        r["risk_checks"] = {}
        r["trend_score"] = 0
        r["quality_score"] = 0
        r["upward_revision"] = False
    for r in second_f:
        try:
            finalize_finance_risk_checks(r, yf.Ticker(f"{r['code']}.T"))
        except Exception as ex:
            print(f"  finalize_finance_risk_checks {r.get('code')}: {ex}", flush=True)
    scored_all = step4_scoring_finance(second_f)
    top_f = scored_all[:MAX_JSON_STOCKS]

    skip_ai = os.getenv("SKIP_AI", "true").lower() == "true"
    ai_cache = load_ai_cache()

    if not skip_ai and ENABLE_AI and anthropic and os.environ.get("ANTHROPIC_API_KEY"):
        print(
            "AI\u5206\u6790\u3092\u5b9f\u884c\u3057\u307e\u3059\uff08\u91d1\u878d\u30bf\u30d6\u3001API\u4f7f\u7528\u3001\u4e0a\u4f4d"
            f"{MAX_JSON_STOCKS}\u4ef6\u306e\u307f\uff09..."
        )
        if "finance" not in ai_cache:
            ai_cache["finance"] = {}
        for i, r in enumerate(top_f):
            time.sleep(3)
            ai_comment, risk_checks, trend_score, quality_score, upward_revision = generate_ai_analysis(
                r, finance_mode=True
            )
            r["ai_comment"] = ai_comment
            r["risk_checks"] = risk_checks
            r["trend_score"] = trend_score
            r["quality_score"] = quality_score
            r["upward_revision"] = upward_revision
            code = str(r.get("code", ""))
            ai_cache["finance"][code] = {
                "ai_comment": ai_comment,
                "risk_checks": risk_checks,
                "trend_score": trend_score,
                "quality_score": quality_score,
                "upward_revision": upward_revision,
            }
            if (i + 1) % 5 == 0 or (i + 1) == len(top_f):
                print(
                    f"  AI\u5206\u6790\uff08\u91d1\u878d\uff09 {i+1}/{len(top_f)} \u5b8c\u4e86",
                    flush=True,
                )
        _jst_ai = timezone(timedelta(hours=9))
        ai_cache["generated_at"] = datetime.now(_jst_ai).strftime("%Y-%m-%dT%H:%M:%S+09:00")
        save_ai_cache(ai_cache)
    else:
        print(
            "AI\u30ad\u30e3\u30c3\u30b7\u30e5\u304b\u3089\u8aad\u307f\u8fbc\u307f\uff08\u91d1\u878d\u30bf\u30d6\u3001API\u30b9\u30ad\u30c3\u30d7\u3001\u4e0a\u4f4d"
            f"{MAX_JSON_STOCKS}\u4ef6\u306e\u307f\uff09..."
        )
        for r in top_f:
            code = str(r.get("code", ""))
            cached = get_cached_ai(ai_cache, code, "finance")
            if cached:
                r["ai_comment"] = cached.get("ai_comment", "")
                r["risk_checks"] = cached.get("risk_checks", {})
                r["trend_score"] = cached.get("trend_score", 0)
                r["quality_score"] = cached.get("quality_score", 0)
                r["upward_revision"] = cached.get("upward_revision", False)
            else:
                r["ai_comment"] = ""
                r["risk_checks"] = {}
                r["trend_score"] = 0
                r["quality_score"] = 0
                r["upward_revision"] = False
    for r in top_f:
        try:
            finalize_finance_risk_checks(r, yf.Ticker(f"{r['code']}.T"))
        except Exception as ex:
            print(f"  finalize_finance_risk_checks {r.get('code')}: {ex}", flush=True)
    results_f = step4_scoring_finance(top_f)
    out_f = step5_save_finance(results_f)
    print(f"Tab2 done: {len(out_f)} stocks")


# =============================
# ???
# =============================
def run_screening():
    start_time = time.perf_counter()
    out = []
    try:
        print("=" * 60)
        print("??????????JPX + yfinance?")
        print("=" * 60)
        print(f"[DEBUG] ENABLE_AI={ENABLE_AI}")
        print(f"[DEBUG] API\u30AD\u30FC\u8A2D\u5B9A\u6E08\u307F={bool(os.environ.get('ANTHROPIC_API_KEY'))}")
        print(
            f"[DEBUG] SKIP_AI={os.getenv('SKIP_AI', 'true')!r} "
            f"-> skip={os.getenv('SKIP_AI', 'true').lower() == 'true'}"
        )
        stocks = step1_get_list_from_jpx()
        if stocks is None or len(stocks) == 0:
            print("???????????????")
            out = step5_save([])
        else:
            if TEST_LIMIT > 0:
                print(f"??????: ?? {TEST_LIMIT} ????")
            first = step2_first_filter(stocks)
            if not first:
                print("Step2 ?? 0 ????????")
                out = step5_save([])
            else:
                second = step3_detail_and_net_cash(first)
                if not second:
                    print("Step3 \u901A\u904B 0 \u4EF6\u306E\u305F\u3081\u7D42\u4E86\u3057\u307E\u3059\u3002")
                    out = step5_save([])
                else:
                    for r in second:
                        r["ai_comment"] = ""
                        r["risk_checks"] = {}
                        r["trend_score"] = 0
                        r["quality_score"] = 0
                        r["upward_revision"] = False
                    scored_all = step4_scoring(second)
                    top_second = scored_all[:MAX_JSON_STOCKS]

                    skip_ai = os.getenv("SKIP_AI", "true").lower() == "true"
                    ai_cache = load_ai_cache()

                    if not skip_ai and ENABLE_AI and anthropic and os.environ.get("ANTHROPIC_API_KEY"):
                        print(
                            "AI\u5206\u6790\u3092\u5b9f\u884c\u3057\u307e\u3059\uff08API\u4f7f\u7528\u3001\u4e0a\u4f4d"
                            f"{MAX_JSON_STOCKS}\u4ef6\u306e\u307f\uff09..."
                        )
                        if "general" not in ai_cache:
                            ai_cache["general"] = {}
                        for i, r in enumerate(top_second):
                            time.sleep(3)
                            ai_comment, risk_checks, trend_score, quality_score, upward_revision = (
                                generate_ai_analysis(r, finance_mode=False)
                            )
                            r["ai_comment"] = ai_comment
                            r["risk_checks"] = risk_checks
                            r["trend_score"] = trend_score
                            r["quality_score"] = quality_score
                            r["upward_revision"] = upward_revision
                            code = str(r.get("code", ""))
                            ai_cache["general"][code] = {
                                "ai_comment": ai_comment,
                                "risk_checks": risk_checks,
                                "trend_score": trend_score,
                                "quality_score": quality_score,
                                "upward_revision": upward_revision,
                            }
                            if (i + 1) % 5 == 0 or (i + 1) == len(top_second):
                                print(
                                    f"  AI\u5206\u6790 {i+1}/{len(top_second)} \u5b8c\u4e86",
                                    flush=True,
                                )
                        _jst_ai = timezone(timedelta(hours=9))
                        ai_cache["generated_at"] = datetime.now(_jst_ai).strftime(
                            "%Y-%m-%dT%H:%M:%S+09:00"
                        )
                        save_ai_cache(ai_cache)
                    else:
                        print(
                            "AI\u30ad\u30e3\u30c3\u30b7\u30e5\u304b\u3089\u8aad\u307f\u8fbc\u307f\uff08API\u30b9\u30ad\u30c3\u30d7\u3001\u4e0a\u4f4d"
                            f"{MAX_JSON_STOCKS}\u4ef6\u306e\u307f\uff09..."
                        )
                        for r in top_second:
                            code = str(r.get("code", ""))
                            cached = get_cached_ai(ai_cache, code, "general")
                            if cached:
                                r["ai_comment"] = cached.get("ai_comment", "")
                                r["risk_checks"] = cached.get("risk_checks", {})
                                r["trend_score"] = cached.get("trend_score", 0)
                                r["quality_score"] = cached.get("quality_score", 0)
                                r["upward_revision"] = cached.get("upward_revision", False)
                            else:
                                r["ai_comment"] = ""
                                r["risk_checks"] = {}
                                r["trend_score"] = 0
                                r["quality_score"] = 0
                                r["upward_revision"] = False
                    results = step4_scoring(top_second)
                    out = step5_save(results)
        elapsed = time.perf_counter() - start_time
        print("\n" + "=" * 60)
        print(f"?????????: {len(out)} ????")
        print(f"??E???E {elapsed:.1f} ?E({elapsed/60:.1f} ?E")
        print("=" * 60)
        if out:
            print(pd.DataFrame(out).head(30).to_string(index=False))
        if TEST_LIMIT > 0 and out:
            print("\n--- \u30B9\u30B3\u30A2\u5185\u8A33 (\u5148\u982D10\u4ED6) ---")
            for r in out[:10]:
                print(f"  {r['code']} {r.get('name_jp', r.get('name', ''))}: "
                      f"\u5272\u5B89\u5EA6={r.get('valuation_score', 0)}, "
                      f"\u6210\u9577\u6027={r.get('growth_score', 0)}, "
                      f"\u682A\u4E3B\u9084\u5143={r.get('shareholder_score', 0)}, "
                      f"\u30EA\u30B9\u30AF={r.get('risk_penalty', 0)}, "
                      f"\u5408\u8A08={r['score']} | "
                      f"ROE={r.get('roe')}, ROIC={r.get('roic')}, PBR={r.get('pbr')}, \u914D\u5F53\u6027\u5411={r.get('payout_ratio')}%")
    finally:
        run_screening_finance_tab()


if __name__ == "__main__":
    run_screening()
