# diff

import sys

def run(repo):
    sys.stdout = open('./log/diff.log',"w+", encoding="utf_8_sig") # 標準出力をdiff.logに変更

    commits_size = repo.git.rev_list('--count', 'HEAD') # コミットの総数
    commit_count = 0
    truee_commit_count = 0 #検索で該当するコミット数カウントのため
    hexsha = "HEAD"
    for commit in repo.iter_commits():
        commit_no =  int(commits_size) - commit_count
        if (commit_count != 0):

            s = repo.git.diff(hexsha + ".." + commit.hexsha)        #diffログを入れる
            lines = s.splitlines()                                  #行ごと(改行判定(split)もして）リスト化


            deep_search = "GET"
            search_flag = "False"                                   #検索結果に該当する差分かどうか判別するための変数
            search = []
            for line in lines:                                      #行ごとにまわす
                if line.startswith("+") or line.startswith("-"):    #もしも行の先頭が"+"or"-""の時...
                    if "@" in line:                                 #もしも"@"が含まれていた時...
                        if deep_search in line:
                         search.append(line)
                         search_flag = "TRUEE"                      #検索結果に該当する行があるならTRUEEにする

            if search_flag == "TRUEE":                              #TRUEEなら該当するコミット内の該当コード内容を表示
                truee_commit_count += 1                             #該当するコミット数カウント（まだどこでもprintしてない）
                print("\n--- " + str(commit_no+1) + " commit .. " + str(commit_no) + " commit ---\n") #何コミット目から何コミット目を検索しているか表示
                for list in search:                                 #ログで見やすく改行するためのfor文
                    print(list)

        hexsha = commit.hexsha
        commit_count += 1

    print("\n--- 1 commit .. 0 commit ---\n")
    print(repo.git.diff(hexsha + "..4b825dc642cb6eb9a060e54bf8d69288fbee4904")) # ファイルの差分を取得

    sys.stdout = sys.__stdout__ # 標準出力をコンソールにもどす
    print("diff.log に出力しました")

    print("##############################################################")
    print("検索に該当するコミット数(deep_search = " + str(deep_search) + ") : "+ str(truee_commit_count))
    print("##############################################################")