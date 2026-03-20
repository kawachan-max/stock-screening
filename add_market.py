import json
import urllib.request
import pandas as pd
from datetime import datetime, timezone, timedelta

# JPX上場銘柄一覧をダウンロード
url = "https://www.jpx.co.jp/markets/statistics-equities/misc/tvdivq0000001vg2-att/data_j.xls"
print("Downloading JPX data...")
urllib.request.urlretrieve(url, "data_j.xls")
print("Downloaded.")

# XLS読み込み
df = pd.read_excel("data_j.xls")
print("Columns:", df.columns.tolist())
print("Sample:\n", df.head(2))

# コード列と市場区分列を特定
# 通常: コード=1列目, 市場・商品区分=3列目
code_col = df.columns[1]  # コード
market_col = df.columns[3]  # 市場・商品区分

# コード→市場名のマッピング作成
market_map = {}
for _, row in df.iterrows():
    c = str(row[code_col]).strip()
    m = str(row[market_col]).strip()
    if c and m and m != 'nan':
        market_map[c] = m

print(f"Market map: {len(market_map)} entries")
print("Sample:", list(market_map.items())[:5])

# screening_result.json読み込み
result = json.load(open("public/screening_result.json", "r", encoding="utf-8"))
stocks = result.get("stocks", result)

# 市場名を追加
updated = 0
for s in stocks:
    code = str(s.get("code", "")).strip()
    if code in market_map:
        s["market"] = market_map[code]
        updated += 1
    else:
        print(f"  NOT FOUND: {code} {s.get('name','?')}")

print(f"Updated {updated}/{len(stocks)} stocks")

# updated_atも更新
JST = timezone(timedelta(hours=9))
result["updated_at"] = datetime.now(JST).strftime("%Y-%m-%dT%H:%M:%S+09:00")
result["stocks"] = stocks

# 保存
with open("public/screening_result.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print("DONE!")
print("First stock market:", stocks[0].get("market", "?"))
