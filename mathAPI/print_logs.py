# print_logs.py
import sqlite3
import json

def main():
    conn = sqlite3.connect("test.db")
    cursor = conn.execute(
        "SELECT id, operation, input_data, result, timestamp "
        "FROM request_log ORDER BY id DESC LIMIT 20"
    )
    print("Last 20 requests")
    print("-" * 60)
    for _id, op, inp, res, ts in cursor:
        # parse input_data (should be a JSON string)
        try:
            inp_parsed = json.loads(inp)
        except Exception:
            inp_parsed = inp

        # result may already be an int/float
        res_parsed = res
        if isinstance(res, str):
            try:
                res_parsed = json.loads(res)
            except Exception:
                pass

        print(f"{_id:>3} | {op:<10} | in={inp_parsed} → {res_parsed} | at {ts}")
    conn.close()

if __name__ == "__main__":
    main()
