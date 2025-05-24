# import csv
# from datetime import datetime, timedelta
# from py_clob_client.client import ClobClient
# from keys import api_key
#
# # ----------- Configuration -----------
# host = "https://clob.polymarket.com"
# chain_id = 137  # Polygon Mainnet
# client = ClobClient(host=host, key=api_key, chain_id=chain_id)
#
# # ----------- Time Cutoff -----------
# cutoff_time = datetime.utcnow() - timedelta(days=7)
#
# # ----------- Market Fetching with Early Stop -----------
# markets_list = []
# next_cursor = None
# fetching = True
#
# while fetching:
#     try:
#         print(f"Fetching markets with next_cursor: {next_cursor}")
#         response = client.get_markets(next_cursor=next_cursor) if next_cursor else client.get_markets()
#
#         if 'data' not in response:
#             print("No data found.")
#             break
#
#         for market in response['data']:
#             ts = market.get("updated_at") or market.get("created_at")
#             if ts:
#                 market_time = datetime.fromisoformat(ts.replace("Z", "+00:00"))
#                 if market_time >= cutoff_time:
#                     markets_list.append(market)
#
#         next_cursor = response.get("next_cursor")
#         if not next_cursor:
#             break
#
#     except Exception as e:
#         print(f"Exception occurred: {e}")
#         break
#
# for market in response['data']:
#     question = market.get("question", "")
#     print(f"MARKET: {question}")
#
# # print(f"Total markets from the last 7 days: {len(markets_list)}")
# # print(markets_list)
# # # ----------- Optional: Filter by Keyword and Save to CSV -----------
# # keywords = ["spx", "bitcoin", "btc", "s&p", "s&p 500"]
# # filtered = [
# #     m for m in markets_list if any(k in m.get("question", "").lower() for k in keywords)
# # ]
# #
# # csv_columns = set()
# # for m in filtered:
# #     csv_columns.update(m.keys())
# #     if 'tokens' in m:
# #         for token in m['tokens']:
# #             csv_columns.update({f"token_{k}" for k in token.keys()})
# #
# # csv_columns = sorted(csv_columns)
# # with open("spx_btc_markets.csv", "w", newline="") as f:
# #     writer = csv.DictWriter(f, fieldnames=csv_columns)
# #     writer.writeheader()
# #     for m in filtered:
# #         row = {k: m.get(k, 'N/A') for k in csv_columns if not k.startswith("token_")}
# #         for token in m.get("tokens", []):
# #             for tk in token:
# #                 row[f"token_{tk}"] = token.get(tk, 'N/A')
# #         writer.writerow(row)
# #
# # print("Done writing to CSV.")
import csv
from py_clob_client.client import ClobClient
from keys import api_key

# ----------- Configuration -----------
host = "https://clob.polymarket.com"
chain_id = 137  # Polygon Mainnet
client = ClobClient(host=host, key=api_key, chain_id=chain_id)

# ----------- Market Fetching -----------
all_markets = []
next_cursor = None
fetching = True

while fetching:
    try:
        print(f"Fetching markets with next_cursor: {next_cursor}")
        response = client.get_markets(next_cursor=next_cursor) if next_cursor else client.get_markets()

        if 'data' not in response:
            print("No data found.")
            break

        for market in response['data']:
            all_markets.append(market)
            print(f"MARKET: {market.get('question', '')}")

        next_cursor = response.get("next_cursor")
        if not next_cursor:
            break

    except Exception as e:
        print(f"Exception occurred: {e}")
        break

print(f"\n✅ Total markets fetched: {len(all_markets)}")

# ----------- Save to CSV -----------
csv_columns = set()
for m in all_markets:
    csv_columns.update(m.keys())
    if 'tokens' in m:
        for token in m['tokens']:
            csv_columns.update({f"token_{k}" for k in token.keys()})

csv_columns = sorted(csv_columns)
with open("all_markets.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=csv_columns)
    writer.writeheader()
    for m in all_markets:
        row = {k: m.get(k, 'N/A') for k in csv_columns if not k.startswith("token_")}
        for token in m.get("tokens", []):
            for tk in token:
                row[f"token_{tk}"] = token.get(tk, 'N/A')
        writer.writerow(row)

print("\n✅ Done writing to CSV.")
