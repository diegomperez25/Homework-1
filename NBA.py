### YOUR IMPORTS HERE ###
import pandas as pd

def read_NBA_stats(url: str) -> pd.DataFrame:
    df = pd.read_csv(url)
    df = df[['year', 'PLAYER', 'TEAM', 'GP', 'PTS', 'REB', 'AST', 'STL', 'BLK']]
    return df

def convert_to_averages(df: pd.DataFrame) -> pd.DataFrame:
    output = df.copy()
    output["PTS"] = (output["PTS"]/output["GP"]).round(1)
    output["REB"] = (output["REB"]/output["GP"]).round(1)
    output["AST"] = (output["AST"]/output["GP"]).round(1)
    output["STL"] = (output["STL"]/output["GP"]).round(1)
    output["BLK"] = (output["BLK"]/output["GP"]).round(1)
    return output

def player_stat(df: pd.DataFrame, player: str, season: str, stat: str) -> pd.DataFrame:
    output = df[(df["year"]==season) & (df["PLAYER"]==player)].copy()
    output['stat'] = stat
    output = output[['year', 'PLAYER', 'TEAM', 'stat', str(stat)]].reset_index()
    output = output.rename(columns = {str(stat): 'value'})
    output.drop('index', axis=1, inplace=True)
    return output

def leader(df: pd.DataFrame, season: str) -> pd.DataFrame:
    sample = df[df["year"]==season].copy()
    gp_leader = player_stat(sample, ((sample[sample["GP"]==sample["GP"].max()].iloc[0,:])["PLAYER"]), season, "GP")
    pts_leader = player_stat(sample,((sample[sample["PTS"]==sample["PTS"].max()].iloc[0,:])["PLAYER"]), season, "PTS")
    reb_leader = player_stat(sample, ((sample[sample["REB"]==sample["REB"].max()].iloc[0,:])["PLAYER"]), season, "REB")
    ast_leader = player_stat(sample, ((sample[sample["AST"]==sample["AST"].max()].iloc[0,:])["PLAYER"]), season, "AST")
    stl_leader = player_stat(sample, ((sample[sample["STL"]==sample["STL"].max()].iloc[0,:])["PLAYER"]), season, "STL")
    blk_leader = player_stat(sample, ((sample[sample["BLK"]==sample["BLK"].max()].iloc[0,:])["PLAYER"]), season, "BLK")
    output = pd.concat([gp_leader, pts_leader, reb_leader, ast_leader, stl_leader, blk_leader]).reset_index()
    output.drop('index', axis=1, inplace=True)
    return output

