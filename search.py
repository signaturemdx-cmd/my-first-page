import pandas as pd
import os
import sys

# Look right here on the main page — no subfolder!
FOLDER = "."

def search_id(target_id):
    found = []
    for fname in os.listdir(FOLDER):
        if fname in [".git"]:
            continue
        fpath = os.path.join(FOLDER, fname)
        if not os.path.isfile(fpath):
            continue
        try:
            if fname.endswith((".xlsx", ".xls")):
                df = pd.read_excel(fpath)
            elif fname.endswith(".csv"):
                df = pd.read_csv(fpath)
            else:
                continue
            matches = df[df.apply(
                lambda r: r.astype(str).str.contains(target_id, case=False, na=False).any(),
                axis=1
            )]
            if not matches.empty:
                found.append({"file": fname, "results": matches.to_dict("records")})
        except Exception as e:
            print(f"⚠️ Could not read {fname}: {e}")
    return found

if __name__ == "__main__":
    target = sys.argv[1].strip() if len(sys.argv) > 1 else ""
    if not target:
        print("❌ Please enter an ID to search for")
    else:
        print(f"🔍 Searching for: {target}")
        results = search_id(target)
        if not results:
            print(f"❌ No matches found for: {target}")
        else:
            print(f"✅ Found {len(results)} matching file(s):")
            for item in results:
                print(f"\n📂 File: {item['file']}")
                for row in item["results"]:
                    print(f"   {row}")
