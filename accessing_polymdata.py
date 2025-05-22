import csv
import json
from py_clob_client.client import ClobClient
from py_clob_client.clob_types import OpenOrderParams
from keys import api_key  # Your API key should be safely stored in keys.py

# ----------- Configuration -----------
host = "https://clob.polymarket.com"
chain_id = 137  # Polygon Mainnet

# ----------- Initialize Polymarket CLOB Client -----------
client = ClobClient(
    host=host,
    key=api_key,
    chain_id=chain_id
)

# ----------- Market Fetching with Pagination -----------
markets_list = []
next_cursor = None

while True:
    try:
        print(f"Fetching markets with next_cursor: {next_cursor}")

        if next_cursor is None:
            response = client.get_markets()
        else:
            response = client.get_markets(next_cursor=next_cursor)

        # Check for valid data
        if 'data' not in response:
            print("No data found in response.")
            break

        markets_list.extend(response['data'])
        next_cursor = response.get("next_cursor")

        if not next_cursor:
            break

    except Exception as e:
        print(f"Exception occurred: {e}")
        break

print(f"Total markets fetched: {len(markets_list)}")

# ----------- Filter for SPX and Bitcoin-related Markets -----------
keywords = ["spx", "bitcoin", "btc", "s&p", "s&p 500"]
filtered_markets = [
    market for market in markets_list
    if any(keyword in market.get("question", "").lower() for keyword in keywords)
]

print(f"Filtered to {len(filtered_markets)} markets related to SPX/Bitcoin.")

# ----------- Extract All CSV Headers from Flat and Nested Keys -----------
csv_columns = set()
for market in filtered_markets:
    csv_columns.update(market.keys())
    if 'tokens' in market:
        for token in market['tokens']:
            csv_columns.update({f"token_{key}" for key in token.keys()})

csv_columns = sorted(csv_columns)  # Alphabetically sorted for readability

# ----------- Write Filtered Markets to CSV -----------
csv_file = "spx_btc_markets.csv"
try:
    with open(csv_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for market in filtered_markets:
            row = {}
            for key in csv_columns:
                if key.startswith("token_"):
                    token_key = key[len("token_"):]
                    row[key] = ', '.join([str(token.get(token_key, 'N/A')) for token in market.get('tokens', [])])
                else:
                    row[key] = market.get(key, 'N/A')
            writer.writerow(row)

    print(f"Filtered data written to '{csv_file}' successfully.")

except IOError as e:
    print(f"Error writing to CSV: {e}")
