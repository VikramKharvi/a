import subprocess
import re

def get_git_log():
    command = [
        'git', 'log', '--graph', '--oneline', '--decorate', '--all',
        '--format=format:%h %d %s'
    ]
    result = subprocess.run(command, stdout=subprocess.PIPE, text=True)
    return result.stdout.splitlines()

def parse_git_log(log_lines):
    mermaid_lines = ['gitGraph']
    branch_stack = ['main']
    current_branch = 'main'

    for line in log_lines:
        if '*' in line:  # This is a commit
            commit_match = re.search(r'\* (\w+) (\(([^)]+)\))? (.*)', line)
            if commit_match:
                commit_hash = commit_match.group(1)
                branches = commit_match.group(3)
                message = commit_match.group(4)

                if branches:
                    if 'tag:' in branches:
                        mermaid_lines.append(f'    commit id: "{commit_hash}" tag: "{branches.split("tag: ")[1]}"')
                    elif 'HEAD ->' in branches:
                        new_branch = branches.split('HEAD -> ')[1].split(',')[0].strip()
                        if new_branch != current_branch:
                            mermaid_lines.append(f'    branch {new_branch}')
                            mermaid_lines.append(f'    checkout {new_branch}')
                            current_branch = new_branch
                        mermaid_lines.append(f'    commit id: "{commit_hash}"')
                    else:
                        mermaid_lines.append(f'    commit id: "{commit_hash}"')
                else:
                    mermaid_lines.append(f'    commit id: "{commit_hash}"')

        elif '/' in line:  # This is a merge
            merge_match = re.search(r'\s*(/|\|\\)\s*', line)
            if merge_match:
                mermaid_lines.append(f'    merge {current_branch}')

    return '\n'.join(mermaid_lines)

def main():
    log_lines = get_git_log()
    mermaid_diagram = parse_git_log(log_lines)
    print(mermaid_diagram)

if __name__ == "__main__":
    main()