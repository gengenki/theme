# diff

import sys
from tqdm import tqdm

# 変更行から文字を検索し、その行を抜き出す
def search_lines(repo, hexsha_after, hexsha_before, commit_no, search_word, true_commit_count, true_line_count):
    s = repo.git.diff(hexsha_after + ".." + hexsha_before)  # diffログを"s"に入れる
    lines = s.splitlines()                                  # 行ごと(改行判定(split)もして）リスト化
    
    search_flag = "False"                                   # 検索結果に該当する差分かどうか判別するための変数
    search_path_flag = "False"                              # 検索結果に該当する差分のパスかどうか判別するための変数
    true_plus_count = 0
    true_minus_count = 0
    commit_log_no = 0

    search = []
    rest_search = []
    for line in lines:                                      # 行ごとにまわす
        #if "public class AccountsRest" in line:  
            if line.startswith("+++") or line.startswith("---"): #+++, ---の内容を一時的に保存するため
                if "Rest" in line:                          # "Rest"のパス変更のみ適用
                    if "Accounts" in line:                    # パスをさらに調べたいとき(何Restかまで調べたくないときはコメントアウト)
                        rest_search.append(line)
                        search_path_flag = "True"  
            if line.startswith("+  ") or line.startswith("-  "):# +++ ---を排除した場合
             if "@" in line:                                # もしも"@"が含まれていた時...
                if search_word in line:
                    if "Account" in line: 
                        search.append(line)
                        search_flag = "True"                    # 検索結果に該当する行があるならtrueにする
                        true_line_count += 1                   # 検索結果に該当する行をカウント
                        if line.startswith("+  "):
                            true_plus_count += 1
                        if line.startswith("-  "):
                            true_minus_count += 1

    if search_flag == "True" and search_path_flag == "True":  # trueなら該当するコミット内の該当コード内容を表示
        true_commit_count += 1                               # 該当するコミット数カウント
        print("\n--- " + str(commit_no+1) + " commit .. " + str(commit_no) + " commit ---")

        for commit in repo.iter_commits():
            if(commit_log_no == commit_no):
                print([
                  commit_no,
                  #commit.author,
                  commit.committed_datetime.strftime('%Y-%m-%d %H:%M:%S'),
                  #commit.message,
                  commit.hexsha
                  ]) 
            commit_log_no+=1

        for list_rest in rest_search:                                 # ログで見やすく改行するためのfor文
            print(list_rest)
        print("+ の数 : "+str(true_plus_count))
        print("- の数 : "+str(true_minus_count))
     #   print("time : "+ s.committed_datetime.strftime)
        for list in search:                                 # ログでdiff見やすく改行するためのfor文
            print(list)

    return true_commit_count, true_line_count

def run(repo):
    sys.stdout = open('./log/diff.log',"w+", encoding="utf_8_sig") # 標準出力をdiff.logに変更

    search_word = "Param"    #さらに検索するワード
    commits_size = repo.git.rev_list('--count', 'HEAD') # コミットの総数
    commit_count = 0
    true_line_count = 0
    true_commit_count = 0
    hexsha_after = "HEAD" # 差分取得用のハッシュ値（親）

    with tqdm(total=int(commits_size), desc='diff.log') as pbar: # プログレスバーの設定
        for commit in repo.iter_commits():
            commit_no =  int(commits_size) - commit_count

            if (commit_count != 0):
                true_commit_count, true_line_count = search_lines(repo, hexsha_after, commit.hexsha, commit_no, search_word, true_commit_count, true_line_count)

            hexsha_after = commit.hexsha
            commit_count += 1
            pbar.update(1) # プログレスバーの進捗率を更新

    true_commit_count, true_line_count  = search_lines(repo, hexsha_after, "4b825dc642cb6eb9a060e54bf8d69288fbee4904", 0, search_word, true_commit_count, true_line_count) # 最初のコミットの差分

    sys.stdout = sys.__stdout__ # 標準出力をコンソールにもどす

    print("##############################################################")
    print("検索に該当するコミット数 : "+ str(true_commit_count))
    print("検索に該当する行数 : "+ str(true_line_count))
  #  print("検索に該当するコミット数(deep_search = " + str(search_word) + ") : "+ str(true_commit_count))
  #  print("検索に該当する行数(deep_search = " + str(search_word) + ") : "+ str(true_line_count))
    print("##############################################################")