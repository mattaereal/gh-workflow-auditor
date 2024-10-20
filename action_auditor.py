from pathlib import Path
import re
import os

def read_actions_file():
    array_of_usernames = []
    actions_path = os.path.join(os.path.dirname(__file__), 'actions.txt')
    with open(actions_path, 'r') as lines:
        for line in lines:
            username = line.split('/')[0]
            username_regex = re.compile("[A-Za-z0-9-]*")
            if username_regex.fullmatch(username):
                if username not in array_of_usernames:
                    array_of_usernames.append(username)
    return array_of_usernames

class ActionAuditor:
    def __init__(self, gh_wrapper, logger):
        self.gh = gh_wrapper
        self.logger = logger

    def check_usernames(self, username_list):
        for username in username_list:
            renamed_or_not = self.gh.stale_checker(username=username)
            if not renamed_or_not:
                self.logger.warning(f"Security Issue: Supply chain. {username} was renamed but used in workflows. Signup the username at https://github.com to make sure.")

    def action_audit(self):
        actions_path = Path(os.path.join(os.path.dirname(__file__), 'actions.txt'))
        if actions_path.exists():
            usernames = read_actions_file()
            self.check_usernames(usernames)
            actions_path.unlink()
        else:
            self.logger.info("No actions.txt file to scan. Supply chain scan complete.")

