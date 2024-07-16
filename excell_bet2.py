import gspread
from sklearn.linear_model import LinearRegression
import numpy as np

TEAMS = {"c": "Catalyst",
         "v": "Vortex",
         "x": "Xenon",
         "r": "Raze",
         "p": "Phantom",
         "h": "Havoc",
         "q": "Quartz",
         }


def add_note(sh, sheet_name, team1, result, team2):
    try:
        worksheet = sh.worksheet(sheet_name)
        worksheet.append_row([TEAMS[team1], result, TEAMS[team2]])
        print("Запись успешно добавлена.")

    except Exception as e:
        print("Ошибка при добавлении записи:", e)


def start_sheet(sh, sheet_name):
    try:
        worksheet = sh.worksheet(sheet_name)
        worksheet.append_row(["ТИМА1", "РЕЗУЛЬТАТ", "ТИМА2"])
        print("Заголовок успешно создан.")

    except Exception as e:
        print("Ошибка при создании заголовка:", e)


def clear_sheet(sh, sheet_name):
    try:
        worksheet = sh.worksheet(sheet_name)
        worksheet.clear()
        print("Лист очищен")

    except Exception as e:
        print("Ошибка при очистке листа:", e)


def clear_node():
    pass


def history_matches(sh, sheet_name, team1, team2):
    try:
        worksheet = sh.worksheet(sheet_name)
        data = worksheet.get_all_values()[1::]

        # Список всех результатов между командами
        scores = []
        team1_name = TEAMS[team1]
        team2_name = TEAMS[team2]

        # Проход по данным и фильтрация счета для каждой команды
        for row in data:
            current_team1, score, current_team2 = row
            left_score, right_score = map(str, score.split(":"))
            if current_team1 == team1_name and current_team2 == team2_name:
                scores.append(left_score + ":" + right_score)
            elif current_team1 == team2_name and current_team2 == team1_name:
                scores.append(right_score + ":" + left_score)
        print(f"Статистика матчей между командами: {team1_name} и {team2_name} на карте {sheet_name}")
        for _ in scores:
            print(_)

    except Exception as e:
        print("Ошибка при вычислении статистики:", e)


def stat_winner(sh, sheet_name, team1, team2):
    try:
        worksheet = sh.worksheet(sheet_name)
        data = worksheet.get_all_values()[1::]

        # Список всех результатов между командами
        scores = [0, 0]
        rounds_win1 = 0
        rounds_win2 = 0
        amount_games = 0
        team1_name = TEAMS[team1]
        team2_name = TEAMS[team2]

        # Проход по данным и фильтрация счета для каждой команды
        for row in data:
            current_team1, score, current_team2 = row
            left_score, right_score = map(int, score.split(":"))

            if current_team1 == team1_name and current_team2 == team2_name:
                if left_score > right_score:
                    scores[0] += 1
                else:
                    scores[1] += 1

                rounds_win1 += left_score
                rounds_win2 += right_score
                amount_games += 1

            elif current_team1 == team2_name and current_team2 == team1_name:
                if left_score > right_score:
                    scores[1] += 1
                else:
                    scores[0] += 1

                rounds_win1 += right_score
                rounds_win2 += left_score
                amount_games += 1

        print(
            f"Винрейт команды {team1_name} против {team2_name} на карте {sheet_name}: {round((scores[0] / (scores[0] + scores[1])) * 100)}%")
        print(f"Среднее число раундов от {team1_name}: {round(rounds_win1 / amount_games, 2)}")
        print(f"Среднее число раундов от {team2_name}: {round(rounds_win2 / amount_games, 2)}")

    except Exception as e:
        print("Ошибка при вычислении винрейта:", e)


# def predict(sh, sheet_name, team1, team2):
#     try:
#         worksheet = sh.worksheet(sheet_name)
#         data = worksheet.get_all_values()[1::]
#         team1_name = TEAMS[team1]
#         team2_name = TEAMS[team2]
#
#         scores_team_1 = np.array([]).reshape((-1, 1))
#         scores_team_2 = np.array([])
#         model = LinearRegression()
#
#         # Проход по данным и фильтрация счета для каждой команды
#         for row in data:
#             current_team1, score, current_team2 = row
#             left_score, right_score = map(int, score.split(":"))
#
#             if current_team1 == team1_name and current_team2 == team2_name:
#                 if left_score > right_score:
#                     scores_team_1.__add__(left_score)
#                 else:
#                     scores_team_2.__add__(right_score)
#
#             elif current_team1 == team2_name and current_team2 == team1_name:
#                 if left_score > right_score:
#                     scores_team_1.__add__(right_score)
#                 else:
#                     scores_team_2.__add__(left_score)
#
#         model.fit(scores_team_1, scores_team_2)
#
#     except Exception as e:
#         print("Ошибка при вычислении винрейта:", e)


def main():
    # Указываем путь к JSON
    gc = gspread.service_account(filename='python-duels-81a43312f644.json')
    sh = gc.open("DuelsStats")
    worksheet_list = sh.worksheets()
    print("MAPS:", ", ".join([worksheet.title for worksheet in worksheet_list]))
    print("ALL COMMANDS: add, stat_win, start_sheet, clear_sheet, history, end")

    while True:
        print("Enter request: ")
        request = str(input()).split()

        if request[0] == "add":
            add_note(sh, request[1], request[2], request[3], request[4])

        elif request[0] == "stat_win":
            stat_winner(sh, request[1], request[2], request[3])

        elif request[0] == "start_sheet":
            start_sheet(sh, request[1])

        elif request[0] == "clear_sheet":
            clear_sheet(sh, request[1])

        elif request[0] == "history":
            history_matches(sh, request[1], request[2], request[3])

        elif request[0] == "end":
            break


if __name__ == "__main__":
    main()
