import pandas as pd
import xgboost as xgb

class Learn:

    def decision(api):
        res = {}
        for n in [2,3]:
            df = api.log.copy()
            for col in df.columns:
                if not col == "response":
                    for i in range(1,3):
                        df[col+" lag_{}".format(i)] = df[col].shift(i)

            df["response_rolling_{}".format(n)] = df["response"].rolling(n).mean()
            df = df.dropna()
            rolling = df["response_rolling_{}".format(n)].copy()
            train_y = rolling
            train_X = df[df.columns[1:-1]].astype(int)

            model = xgb.XGBRegressor(objective='reg:squarederror')
            model.fit(train_X, train_y)

            newrow = pd.DataFrame(columns = train_X.columns)
            newrow.loc[0]= [0 for _ in range(len(train_X.columns))]

            item = list(train_X.columns)[:6]
            for col in item:
                for i in range(1,3):
                    newrow.loc[0][col+" lag_{}".format(i)] = train_X.loc[len(train_X)-i+2][col]

            newrow = newrow.astype(int)
            pred = {}
            '''
            avoid = ""
            if len(api.last_actions) == 3:
                if api.last_actions[0] == api.last_actions[1] \
                   and api.last_actions[0] == api.last_actions[2]:
                    avoid = api.last_actions[0]

                elif api.last_actions[0] == api.last_actions[2]:
                    avoid = api.last_actions[1]
            '''        
            for feat in ["turn right",
                         "turn left",
                         "forward",
                         "backward"]:
                tmp = newrow.copy()
                tmp.loc[0][feat] = 1
                pred[feat] = model.predict(tmp)[0]

            tmp = newrow.copy()
            tmp.loc[0]["check"] = 1
            tmp.loc[0]["touch_sensor"] = -1

            pred["check"] = model.predict(tmp)[0]
            res[n] = pred
        #Choix des predictions

        #Choose if there is something to avoid in case of too much repeat
        avoid = ""
        if len(api.last_actions) == 3:
            if api.last_actions[0] == api.last_actions[1] \
                and api.last_actions[0] == api.last_actions[2]:
                    avoid = api.last_actions[0]
        tmp = -10
        for i in res:
            for c in res[i]:
                if res[i][c] > tmp and not c == avoid:
                    api.action = c
                    tmp = res[i][c]
           
        print("-"*42)
        print(api.action)
        print(pred)
        print(api.last_actions)
        print("-"*42)
        if len(api.last_actions) < 3:
            api.last_actions.append(api.action)
        else:
            api.last_actions = api.last_actions[1:]+[api.action]
