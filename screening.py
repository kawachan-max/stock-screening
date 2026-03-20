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

EXCLUDE_SECTORS = [
    "\u9280\u884C\u696D", "\u4FDD\u967A\u696D",
    "\u8A3C\u5238\u3001\u5546\u54C1\u5148\u7269\u53D6\u5F15\u696D", "\u305D\u306E\u4ED6\u91D1\u878D\u696D", "\u4E0D\u52D5\u7523\u696D",
]

MIN_AVG_TRADING_VALUE_20D = 50_000_000
ONE_TIME_PROFIT_RATIO_THRESHOLD = 0.25
MIN_EQUITY_RATIO = 0.30
MAX_LT_DEBT_TO_NP = 5.0

SLEEP_SEC = 0.5
TEST_LIMIT = 0  # 0 = \u5168\u9298\u67C4\u300250 = \u30C6\u30B9\u30C8\u5B9F\u884C
ENABLE_AI = True  # True \u3067\u4E0A\u4F4D\u9298\u67C4\u304B\u3089 AI \u5206\u6790\u3092\u5B9F\u884C

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
            # ?????: yfinance ? dividendYield ???(0.035)?????100 ?1????1???????????
            div_yield = info.get("yield") or info.get("dividendYield")
            if div_yield is not None and not (isinstance(div_yield, float) and math.isnan(div_yield)):
                try:
                    v = float(div_yield)
                    if v < 1:
                        div_yield = round(v * 100, 2)  # 0.0351 -> 3.51%
                    else:
                        div_yield = round(v, 2)  # ??%????????
                except (TypeError, ValueError):
                    div_yield = None
            else:
                div_yield = None
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
            })
            if TEST_LIMIT > 0:
                print(f"    ????: {code} {nm} (PER={per:.2f}, ????E{market_cap/1e8:.1f}?E", flush=True)
        except Exception as e:
            if TEST_LIMIT > 0:
                print(f"    ??? {code}: {e}", flush=True)
            continue
    print(f"  ????: {len(first_pass)} ??")
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
            payout_ratio = info.get("payoutRatio")
            if payout_ratio is not None and not (isinstance(payout_ratio, float) and math.isnan(payout_ratio)):
                payout_ratio = round(float(payout_ratio) * 100, 2)
            else:
                payout_ratio = None
            pbr = info.get("priceToBook")
            if pbr is not None and not (isinstance(pbr, float) and math.isnan(pbr)):
                pbr = round(float(pbr), 2)
            else:
                pbr = None
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
            second.append(r)
        except Exception as e:
            import traceback
            print(f"    ERROR {row['code']}: {e}", flush=True)
            if TEST_LIMIT > 0:
                traceback.print_exc()
            continue
    print(f"  \u901A\u904B: {len(second)} \u4EF6")
    return second


# =============================
# Step4: \u30B9\u30B3\u30A2\u30EA\u30F3\u30B0
# =============================
def calc_score(row):
    nc = row["net_cash_ratio"]
    per = row["per"]
    valuation_score = get_valuation_score(nc, per)
    growth_score = 0
    np_val = row["np"]
    eq = row["eq"]
    op = row["op"]
    sales = row["sales"]
    ta = row["ta"]
    if sales > 0: growth_score += 2
    if op > 0: growth_score += 2
    if np_val and float(np_val) > 0: growth_score += 2
    roe = row.get("roe")
    if roe is not None and roe >= 15: growth_score += 5
    roic = row.get("roic")
    if roic is not None and roic >= 8: growth_score += 5
    yf_bs = row.get("yf_bs")
    if yf_bs:
        lt = yf_bs.get("long_term_debt", 0) or 0
        cash = yf_bs.get("cash", 0) or 0
        ic = eq + lt - cash
        if ic and ic > 0 and op and (op / ic) >= 0.08: growth_score += 5
    elif eq and op and (op / eq) >= 0.08: growth_score += 5
    annual_list = row.get("annual_list", [])
    if len(annual_list) >= 3:
        o0, o1, o2 = annual_list[0]["OP"], annual_list[1]["OP"], annual_list[2]["OP"]
        if o0 > o1 > o2: growth_score += 9
    if ta and ta > 0 and (eq / ta) >= 0.5: growth_score += 5
    shareholder_score = row.get("shareholder_score", 0)
    risk_penalty = row.get("risk_penalty", 0)
    trend_score = row.get("trend_score", 0)
    quality_score = row.get("quality_score", 0)
    row["valuation_score"] = valuation_score
    row["growth_score"] = growth_score
    total = valuation_score + growth_score + shareholder_score + risk_penalty
    total += trend_score  # \u6700\u592710\u70B9
    total += quality_score  # \u6700\u592710\u70B9
    return max(0, total)


def step4_scoring(second_pass):
    print("Step4: ????????????...")
    for r in second_pass:
        r["score"] = calc_score(r)
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


def _default_risk_checks():
    return {k: None for k in AI_RISK_KEYS}


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


def generate_ai_analysis(row):
    try:
        if not os.environ.get("ANTHROPIC_API_KEY"):
            return "", _default_risk_checks(), 0, 0

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
            revenue_trend = f"{fmt_oku(revenue_3y[2])}? ? {fmt_oku(revenue_3y[1])}? ? {fmt_oku(revenue_3y[0])}?"
        else:
            revenue_trend = "N/A"

        prompt = f"""
???: {name_jp}
??: {sector}

?????????
???????: {revenue_latest_oku}??
??????: {revenue_yoy_str}%
????????: {op_latest_oku}??
???????: {op_income_yoy_str}%
???????: {net_latest_oku}??

???3???????
{revenue_trend}

??????
NC??: {row.get('net_cash_ratio', 'N/A')} / PER: {row.get('per', 'N/A')}? / ROE: {row.get('roe', 'N/A')}%

\u4EE5\u4E0B\u306EJSON\u5F62\u5F0F\u3067\u306F\u306A\u304F\u56DE\u7B54\u3057\u3066\u304F\u3060\u3055\u3044\u3002

trend_score (\u696D\u7E8C\u30C8\u30EC\u30F3\u30C9\u3001\u6700\u592710\u70B9):
\u30FB3\u671F\u9023\u7D9A\u5897\u6536\u5897\u76CA \u2192 10\u70B9
\u30FB\u5897\u6536 or \u5897\u76CA(\u76F4\u8FD1) \u2192 7\u70B9
\u30FB\u6A2A\u3070\u3044(\u00B15%\u4EE5\u5185) \u2192 4\u70B9
\u30FB\u6E1B\u6536 or \u6E1B\u76CA(\u76F4\u8FD1) \u2192 2\u70B9
\u30FB\u6E1B\u6536\u6E1B\u76CA\u304C\u7D9A\u3044\u3066\u3044\u308B \u2192 0\u70B9

quality_score (\u4E8B\u696D\u306E\u8CEA\u3001\u6700\u592710\u70B9):
\u30FB\u5F37\u56FA\u306A\u7AF6\u4E89\u512A\u4F4D\u6027\u30FB\u9AD8\u3044\u53C2\u5165\u969C\u58C1\u30FB\u5B89\u5B9A\u3057\u305F\u6536\u76CA\u57FA\u76E4 \u2192 10\u70B9
\u30FB\u4E00\u5B9A\u306E\u7AF6\u4E89\u512A\u4F4D\u6027\u3042\u308A \u2192 7\u70B9
\u30FB\u5E73\u5747\u7684\u306A\u4E8B\u696D\u54C1\u8CEA \u2192 4\u70B9
\u30FB\u7AF6\u4E89\u6FC0\u5316\u30FB\u6536\u76CA\u4E0D\u5B89\u5B9A \u2192 2\u70B9
\u30FB\u4E8B\u696D\u306E\u7D9A\u7D9A\u6027\u306B\u61F8\u5FFD \u2192 0\u70B9

JSON\u30B5\u30F3\u30D7\u30EB:
{{"ai_comment": "\u696D\u7E8C\u30C8\u30EC\u30F3\u30C9\u30FB\u4E8B\u696D\u306E\u8CEA\u30FB\u5C06\u6765\u6027\u3092150\u5B57\u7A0B\u5EA6\u3067",
  "trend_score": 7,
  "quality_score": 4,
  "risk_checks": {{
    "roe_15_percent": true,
    "equity_ratio_50_percent": true,
    "debt_to_profit_5x": true,
    "fcf_stability": true,
    "liquidity_risk": false,
    "one_time_profit_risk": false
  }}
}}
"""

        message = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1000,
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
            return "", _default_risk_checks(), 0, 0

        ai_comment = (data.get("ai_comment") or "").strip()
        trend_score = data.get("trend_score")
        if trend_score is not None:
            try:
                trend_score = max(0, min(10, int(trend_score)))
            except (TypeError, ValueError):
                trend_score = 0
        else:
            trend_score = 0
        quality_score = data.get("quality_score")
        if quality_score is not None:
            try:
                quality_score = max(0, min(10, int(quality_score)))
            except (TypeError, ValueError):
                quality_score = 0
        else:
            quality_score = 0

        risk_checks = data.get("risk_checks") or {}
        for k in AI_RISK_KEYS:
            if k not in risk_checks:
                risk_checks[k] = None
            elif risk_checks[k] is not None:
                risk_checks[k] = bool(risk_checks[k])

        return ai_comment, risk_checks, trend_score, quality_score

    except Exception as e:
        print(f"[AI] \u30A8\u30E9\u30FC: {e}")
        import traceback
        traceback.print_exc()
        return "", _default_risk_checks(), 0, 0
    base_name = (row.get("name") or row.get("code") or "").strip() or row.get("code", "")
    name_jp = JPX_NAME_MAP.get(row["code"], base_name)
    code = row.get("code", "")
    net_cash_ratio = row.get("net_cash_ratio")
    per = row.get("per")
    market_cap_oku = round(row["market_cap"] / 1e8, 1) if row.get("market_cap") else None
    roe = row.get("roe")
    roic = row.get("roic")
    payout_ratio = row.get("payout_ratio")
    pbr = row.get("pbr")
    net_cash_str = str(net_cash_ratio) if net_cash_ratio is not None else "N/A"
    per_str = f"{per}\u500D" if per is not None else "N/A"
    market_str = f"{market_cap_oku}\u5104\u5186" if market_cap_oku is not None else "N/A"
    roe_str = f"{roe}%" if roe is not None else "N/A"
    roic_str = f"{roic}%" if roic is not None else "N/A"
    payout_str = f"{payout_ratio}%" if payout_ratio is not None else "N/A"
    pbr_str = f"{pbr}\u500D" if pbr is not None else "N/A"

    # \u904E\u53BB3\u671F\u306E\u58F2\u4E0A\u30FB\u55B6\u696D\u5229\u76CA\u30FB\u7D20\u5229\u76CA
    annual_list = row.get("annual_list") or []
    if not annual_list:
        try:
            ticker = yf.Ticker(f"{code}.T")
            annual_list = get_financials_3periods(ticker)
        except Exception:
            pass
    revenue_3y = _format_3y([a.get("Sales") for a in annual_list[:3]])
    op_income_3y = _format_3y([a.get("OP") for a in annual_list[:3]])
    net_income_3y = _format_3y([a.get("NP") for a in annual_list[:3]])

    # \u4F1A\u793E\u4E88\u60F3\u30FB\u30A2\u30CA\u30EA\u30B9\u30C8\u8A55\u4FA1
    revenue_estimate = "N/A"
    earnings_estimate = "N/A"
    recommendation_mean = "N/A"
    try:
        ticker = yf.Ticker(f"{code}.T")
        info = ticker.info or {}
        revenue_estimate = info.get("revenueEstimate") or info.get("targetRevenueMean") or "N/A"
        if isinstance(revenue_estimate, (int, float)) and not math.isnan(revenue_estimate):
            revenue_estimate = str(int(revenue_estimate))
        earnings_estimate = info.get("earningsEstimate") or info.get("targetEarningsMean") or "N/A"
        if isinstance(earnings_estimate, (int, float)) and not math.isnan(earnings_estimate):
            earnings_estimate = str(earnings_estimate)
        rec = info.get("recommendationMean")
        if rec is not None and not (isinstance(rec, float) and math.isnan(rec)):
            recommendation_mean = str(round(rec, 2))
    except Exception:
        pass

    system_prompt = """You are a Japanese stock analyst specializing in value investing.
Analyze the TREND and BUSINESS QUALITY, not just the numbers.
Respond ONLY in valid JSON format."""

    user_prompt = f"""\u9298\u67C4\u540D: {name_jp}
\u6642\u4FA1\u7D4C\u984D: {market_str}

?\u8CA1\u52D9\u6307\u6807?
NC\u6BD4\u7387: {net_cash_str} / PER: {per_str} / PBR: {pbr_str}
ROE: {roe_str} / ROIC: {roic_str} / \u914D\u5F53\u6027\u5411: {payout_str}%

?\u904E\u53BB3\u671F\u306E\u696D\u7E8C\u63A8\u79FB?
\u58F2\u4E0A\u9AD8: {revenue_3y}\uFF08\u5358\u4F4D\uff1A\u767E\u8429\u5186\uff09
\u55B6\u696D\u5229\u76CA: {op_income_3y}
\u7D20\u5229\u76CA: {net_income_3y}

?\u4F1A\u793E\u4E88\u60F3\u30FB\u30A2\u30CA\u30EA\u30B9\u30C8\u8A55\u4FA1?
\u901A\u671F\u58F2\u4E0A\u4E88\u60F3: {revenue_estimate}
\u901A\u671F\u5229\u76CA\u4E88\u60F3: {earnings_estimate}
\u30A2\u30CA\u30EA\u30B9\u30C8\u8A55\u4FA1(recommendationMean): {recommendation_mean}

\u4EE5\u4E0B\u306EJSON\u5F62\u5F0F\u306E\u307F\u3067\u56DE\u7B54\u3057\u3066\u304F\u3060\u3055\u3044\u3002
\u30FBai_comment: \u696D\u7E8C\u30C8\u30EC\u30F3\u30C9\u30FB\u4E8B\u696D\u306E\u8CEA\u30FB\u5C06\u6765\u6027\u30FB\u6295\u8CC7\u5224\u65AD\u3092150\u5B57\u7A0B\u5EA6\u3067\u8A18\u8FF0\u3002\u6570\u5024\u306E\u8AAC\u660E\u3067\u306F\u306A\u304F\u89B3\u5BDF\u3092\u66F8\u304F\u3002
\u30FBrisk_checks: \u5404\u9805\u76EE\u3092true/false\u3067\u8A55\u4FA1\u3002

{{"ai_comment": "...",
  "risk_checks": {{
    "roe_15_percent": true or false,
    "equity_ratio_50_percent": true or false,
    "debt_to_profit_5x": true or false,
    "fcf_stability": true or false,
    "liquidity_risk": true or false,
    "one_time_profit_risk": true or false
  }}
}}"""

    try:
        print(f"  [AI] Calling Claude API for {name_jp} ({row.get('code', '')})...", flush=True)
        client = anthropic.Anthropic(api_key=api_key)
        message = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1000,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )
        text = (message.content[0].text if message.content else "") or ""
        print(f"  [AI] \u30EC\u30B9\u30DD\u30F3\u30B9\u5168\u4F53: {text!r}", flush=True)
        if not text.strip():
            print(f"  [AI] WARNING: Empty response for {name_jp}", flush=True)
            return "", _default_risk_checks()
        try:
            data = json.loads(text)
            print(f"  [AI] JSON\u30D1\u30FC\u30B9\u7D50\u679C: {data}", flush=True)
        except json.JSONDecodeError as e:
            print(f"  [AI] JSON parse error for {name_jp}: {e}", flush=True)
            print(f"  [AI] Raw response (first 500 chars): {text[:500]!r}", flush=True)
            return "", _default_risk_checks()
        ai_comment = (data.get("ai_comment") or "").strip()
        risk_checks = data.get("risk_checks") or {}
        for k in AI_RISK_KEYS:
            if k not in risk_checks:
                risk_checks[k] = None
        return ai_comment, risk_checks
    except Exception as e:
        import traceback
        print(f"  [AI] ERROR for {name_jp} ({row.get('code', '')}): {e}", flush=True)
        traceback.print_exc()
        return "", _default_risk_checks()


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
        })
    JST = timezone(timedelta(hours=9))
    updated_at = datetime.now(JST).strftime("%Y-%m-%dT%H:%M:%S+09:00")
    result = {"updated_at": updated_at, "stocks": out}
    with open("screening_result.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print("Step5: screening_result.json ???????")
    return out


# =============================
# ???
# =============================
def run_screening():
    start_time = time.perf_counter()
    print("=" * 60)
    print("??????????JPX + yfinance?")
    print("=" * 60)
    print(f"[DEBUG] ENABLE_AI={ENABLE_AI}")
    print(f"[DEBUG] API\u30AD\u30FC\u8A2D\u5B9A\u6E08\u307F={bool(os.environ.get('ANTHROPIC_API_KEY'))}")
    stocks = step1_get_list_from_jpx()
    if stocks is None or len(stocks) == 0:
        print("???????????????")
        step5_save([])
        return
    if TEST_LIMIT > 0:
        print(f"??????: ?? {TEST_LIMIT} ????")
    first = step2_first_filter(stocks)
    if not first:
        print("Step2 ?? 0 ????????")
        step5_save([])
        return
    second = step3_detail_and_net_cash(first)
    if not second:
        print("Step3 \u901A\u904B 0 \u4EF6\u306E\u305F\u3081\u7D42\u4E86\u3057\u307E\u3059\u3002")
        step5_save([])
        return
    if ENABLE_AI and anthropic and os.environ.get("ANTHROPIC_API_KEY"):
        print("AI \u5206\u6790\u3092\u5B9F\u884C\u3057\u307E\u3059 (\u4E8C\u6B21\u901A\u904B\u9298\u67C4\u306E\u307F)...")
        for i, r in enumerate(second):
            print(f"[AI] \u51E6\u7406\u958B\u59CB: {r.get('name_jp', r.get('code'))}")
            time.sleep(3)
            ai_comment, risk_checks, trend_score, quality_score = generate_ai_analysis(r)
            r["ai_comment"] = ai_comment
            r["risk_checks"] = risk_checks
            r["trend_score"] = trend_score
            r["quality_score"] = quality_score
            if (i + 1) % 5 == 0 or (i + 1) == len(second):
                print(f"  AI \u5206\u6790 {i+1}/{len(second)} \u5B8C\u4E86", flush=True)
    else:
        for r in second:
            r["trend_score"] = 0
            r["quality_score"] = 0
    results = step4_scoring(second)
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


if __name__ == "__main__":
    run_screening()
