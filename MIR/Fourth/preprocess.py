import json
import re
from pathlib import Path


def remove_multi_line_comments(string: str) -> str:

    # ruby comments
    multi_line_ruby_regex = re.compile(
        r'''(
        (?<=\n=begin).*?(?=\n=end\s*\n) |
        (?<=^=begin).*?(?=\n=end\s*\n) |
        (?<=\n=begin).*?(?=\n=end$) |
        (?<=^=begin).*?(?=\n=end$)
        )''',
        flags=re.DOTALL | re.VERBOSE | re.MULTILINE
    )
    string = multi_line_ruby_regex.sub('\n', string)

    # Python comments
    multi_line_python_regex1 = re.compile(
        r'''(
            (?<=\n)\'{3}.*?\'{3}(?=\s*\n) |
            (?<=^)\'{3}.*?\'{3}(?=\s*\n) |
            (?<=\n)\'{3}.*?\'{3}(?=$) |
            (?<=^)\'{3}.*?\'{3}(?=$)
        )''',
        flags=re.DOTALL | re.VERBOSE | re.MULTILINE
    )
    multi_line_python_regex2 = re.compile(
        r'''(
            (?<=\n)\"{3}.*?\"{3}(?=\s*\n) |
            (?<=^)\"{3}.*?\"{3}(?=\s*\n) |
            (?<=\n)\"{3}.*?\"{3}(?=$) |
            (?<=^)\"{3}.*?\"{3}(?=$)
        )''',
        flags=re.DOTALL | re.VERBOSE | re.MULTILINE
    )
    string = multi_line_python_regex1.sub('\''*6, string)
    string = multi_line_python_regex2.sub('\"'*6, string)

    multi_line_comment_regex = re.compile(
        r'''(
        (?<=\n/\*).*?(?=\*/\s*\n) |
        (?<=^/\*).*?(?=\*/\s*\n) |
        (?<=\n/\*).*?(?=\*/$) |
        (?<=^/\*).*?(?=\*/$)
        )''',
        flags=re.DOTALL | re.VERBOSE | re.MULTILINE
    )
    string = multi_line_comment_regex.sub('', string)

    return string


def remove_inline_comments(string: str) -> str:
    inline_regex = re.compile(
        r'''(
            (?<=//).+ | # comments like: // This is a comment
            (?<=\#).+ # comments like: # This is a comment
        )''',
        flags=re.VERBOSE
    )
    return inline_regex.sub('', string)


def replace_numbers(string: str) -> str:
    num_regex = re.compile(
        r'''(
            (?<!\w)\d+(\.\d*)?
        )''',
        flags=re.VERBOSE
    )
    return num_regex.sub('NUM', string)


def remove_indents(string: str) -> str:
    regex = re.compile(
        r'''(
            (?<=\n)\s+ |
            (?<=^)\s+
        )''',
        flags=re.VERBOSE
    )
    return regex.sub('', string)


def remove_strings(string: str) -> str:

    str_qoute_text_regex = re.compile(
        r'''(
            \'.*?\'
        )''',
        flags=re.VERBOSE | re.DOTALL
    )
    string = str_qoute_text_regex.sub("\'\'", string)

    str_double_qoute_text_regex = re.compile(
        r'''(
            \".*?\"
        )''',
        flags=re.VERBOSE | re.DOTALL
    )
    string = str_double_qoute_text_regex.sub('\"\"', string)

    str_multi_qoute_text_regex = re.compile(
        r'''(
            \'{3}.*?\'{3}
        )''',
        flags=re.VERBOSE | re.DOTALL
    )
    string = str_multi_qoute_text_regex.sub("\'\'\'\'\'\'", string)

    str_multi_double_qoute_text_regex = re.compile(
        r'''(
            \"{3}.*?\"{3}
        )''',
        flags=re.VERBOSE | re.DOTALL
    )
    string = str_multi_double_qoute_text_regex.sub('\"\"\"\"\"\"', string)

    return string


def extract_tokens(string: str) -> str:
    # num_id_regex = re.compile(
    #     r'''(
    #         (?<=\W) |
    #         (?=\W)
    #     )''',
    #     flags=re.VERBOSE
    # )
    between_tokens_regex = re.compile(
        r'''(
            (?<=[\(\)\[\]\{\}\.;,]) |
            (?=[\(\)\[\]\{\}\.;,]) |
            (?<=\") (?=[^\"]) |
            (?<=[^\"]) (?=\") |
            (?<=\') (?=[^\']) |
            (?<=[^\']) (?=\') |
            (?<=[=\+\-\*%&/!\|:<>]) (?=[^=\+\-\*%&/!\|:<>]) |
            (?<=[^=\+\-\*%&/!\|:<>]) (?=[=\+\-\*%&/!\|:<>])
        )''',
        flags=re.VERBOSE
    )
    string = between_tokens_regex.sub(' ', string)

    return string


def remove_non_ascii_characters(string: str) -> str:
    non_ascii_regex = re.compile(
        r'''(
            [^\x00-\x7f]
        )''',
        flags=re.VERBOSE
    )
    return non_ascii_regex.sub('', string)


def preprocess(string: str):
    string = remove_non_ascii_characters(string)
    string = remove_indents(string)
    string = remove_strings(string)
    string = replace_numbers(string)
    string = remove_inline_comments(string)
    string = remove_multi_line_comments(string)
    string = extract_tokens(string)
    string = re.sub('\s+', ' ', string)
    return string


def preprocess_repos():
    repos_dict = json.loads(Path('repos_dict.json').read_text())

    preprocessed_data_path = Path('preprocessed_data')
    preprocessed_data_path.mkdir()

    for repo in repos_dict:

        last_repo_path = Path('data') / repo["dir_name"]
        repo_path = Path(str(preprocessed_data_path)) / repo["dir_name"]
        print(repo_path)
        repo_path.mkdir()

        for file in repo["files_url"]:
            # print(file)
            preprocess_file(last_repo_path, repo_path, file)
            # break
        # break


def preprocess_file(last_repo_path, repo_path, file):

    language_path = Path(str(repo_path)) / file["language"]
    if not language_path.exists():
        language_path.mkdir()

    code_path = Path(
        str(language_path)) / f'{file["name"]}.txt'
    # print(code_path)
    last_code_path = Path(str(last_repo_path)) / \
        file["language"] / f'{file["name"]}.txt'
    if not last_code_path.exists():
        return
    # print(last_code_path)
    code = last_code_path.read_text()
    preprocessed_code = preprocess(code)
    code_path.write_text(preprocessed_code)


string = '''/* first
second
third */
ali ajsjnajsn
/* first C comment
second C comment
third C comment */
\'\'\'first quote comment
second quote comment
third quote comment
\'\'\'
a = ali
\'\'\'first quote comment
second quote comment
third quote comment
\'\'\'

\"\"\"
first double quote line of the comment
second double quote line of the commet
\"\"\"
/* first C comment
second C comment
third C comment */
=begin
jsjdisjdij =begin
skndksdknsd =end
skndksndk
=end

'''


inline_str = '''
jsjansj = ajnsjan #habsajsasa
# hbshabshb aknsjnas
//ksjnjasjna
nkans = asajsn
'''

if __name__ == '__main__':
    path = Path('preprocessed_data')
    preprocess_repos()

    # t = Path(
    #     'cmd.kubectx.fzf.go.txt')
    # path = Path(
    #     '/Users/amireza/Desktop/term 6/MIR/Assignments/4/4/data/ahmetb_kubectx/Go') / t

    # string = '''API = {
    # 'events': 'https://api.github.com/users/{username}/received_events'.format(username=ACCOUNT['username'])
    # }'''
    # print(preprocess(string))

    # t = Path(
    #     'script.github_bot.github_bot.py.txt')
    # path = Path('koft1.txt')
    # string = path.read_text()
    # x = preprocess(string)
    # Path('koft.txt').write_text(x)
