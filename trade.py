import pandas as pd


def make_long(longs, dataframe, row,lots=10,overlap=False):
    # longs is a set of all longs
    # dataframe is a pandas dataframe of asks, used to market exit positions
    # row has our timestamp, entry price at row[0] and row[1] respectively

    # we need to iterate through the dataframe such that when target or stop == open we must close trade

    # check if there is an existing long trade (trade overlap)
    timestamp_of_entry = row[0]

    if overlap:
        for trade in longs:
            try:
                if timestamp_of_entry < trade["timestamp_of_exit"]:
                    return {"timestamp_of_entry": timestamp_of_entry, "type_of_exit": "Overlap"}
            except:
                print("No trades have happened yet, skipping\n")

    # This part of the code will be unreachable if there is a trade overlap
    entry_price = row[1]['close']
    target_price = entry_price + 900  # 9 rupees up for crude
    stop_price = entry_price - 300  # 3 rupees down for crude
    timestamp_of_exit = None
    type_of_exit = None
    pnl = None

    # type of exit and PNL calculation
    for item in dataframe.iterrows():
        if item[0] > timestamp_of_entry:
            current_price = item[1]['open']
            if current_price >= target_price:  # If target is hit
                type_of_exit = "Win"
                pnl = (current_price - entry_price)/100*lots - 76
                timestamp_of_exit = item[0]
                break
            elif current_price <= stop_price:  # If stop is hit
                type_of_exit = "Loss"
                pnl = (current_price - entry_price)/100*lots - 76
                timestamp_of_exit = item[0]
                break

    return {"timestamp_of_entry": timestamp_of_entry,
            "timestamp_of_exit": timestamp_of_exit,
            "entry_price": entry_price,
            "target_price": target_price,
            "stop_price": stop_price,
            "type_of_exit": type_of_exit,
            "pnl": pnl}


def make_short(shorts, dataframe, row,lots=10,overlap=False):
    # longs is a set of all longs
    # dataframe is a pandas dataframe of asks, used to market exit positions
    # row has our timestamp, entry price at row[0] and row[1] respectively

    # we need to iterate through the dataframe such that when target or stop == open we must close trade

    # check if there is an existing long trade (trade overlap)
    timestamp_of_entry = row[0]

    if overlap:
        for trade in shorts:
            try:
                if timestamp_of_entry < trade["timestamp_of_exit"]:
                    return {"timestamp_of_entry": timestamp_of_entry, "type_of_exit": "Overlap"}
            except:
                print("No trades have happened yet, skipping\n")

    # This part of the code will be unreachable if there is a trade overlap
    entry_price = row[1]['close']
    target_price = entry_price + 900  # 9 rupees up for crude
    stop_price = entry_price - 300  # 3 rupees down for crude
    timestamp_of_exit = None
    type_of_exit = None
    pnl = None

    # type of exit and PNL calculation
    for item in dataframe.iterrows():
        if item[0] > timestamp_of_entry:
            current_price = item[1]['open']
            if current_price >= target_price:  # If target is hit
                type_of_exit = "Win"
                pnl = (current_price - entry_price)/100*lots - 76
                timestamp_of_exit = item[0]
                break
            elif current_price <= stop_price:  # If stop is hit
                type_of_exit = "Loss"
                pnl = (current_price - entry_price)/100*lots - 76
                timestamp_of_exit = item[0]
                break

    return {"timestamp_of_entry": timestamp_of_entry,
            "timestamp_of_exit": timestamp_of_exit,
            "entry_price": entry_price,
            "target_price": target_price,
            "stop_price": stop_price,
            "type_of_exit": type_of_exit,
            "pnl": pnl}
