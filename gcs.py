import os
import git
import sys
import shutil

def clone_repository(repo_url, clone_dir):
    """Clone the repository from the given URL."""
    try:
        # Check if the clone directory exists
        if os.path.exists(clone_dir):
            print(f"[+] Deleting existing directory: {clone_dir}\n")
            # Remove the existing directory
            shutil.rmtree(clone_dir)
        
        # Clone the repository
        repo = git.Repo.clone_from(repo_url, clone_dir)
        return repo
    except git.exc.GitCommandError as e:
        print("Error:", e)
        return None

def create_commit_list(repo):
    """Create a list of dictionaries containing commit information."""
    commit_list = []
    try:
        # Iterate over all commits in the repository
        for commit in repo.iter_commits('--all'):
            # Extract commit metadata
            commit_data = {
                'hash': commit.hexsha,
                'author': str(commit.author),
                'email': commit.author.email,
                'date': str(commit.authored_datetime),
                'message': commit.message
            }
            # Add commit data to the list
            commit_list.append(commit_data)
    except git.exc.GitCommandError as e:
        print("Error:", e)
    return commit_list


def extract_unique_emails(commit_list):
    """Extract unique email addresses from the commit list."""
    unique_emails = set()
    for commit_data in commit_list:
        # Split the author field to extract the name and email address
        #print(commit_data['author'])
        if commit_data['email'] and 'users.noreply.github.com' not in commit_data['email']:
            email = commit_data['email']
            # Add the email address to the set

            unique_emails.add(email)
    # Convert the set to a list and return
    return list(unique_emails)


def main(repo_url,keywords):
    # Specify the directory to clone the repository into
    clone_dir = "/tmp/repo_clone"
    
    # Clone the repository
    repo = clone_repository(repo_url, clone_dir)
    
    if repo:
        # Create a list of dictionaries containing commit information
        commit_list = create_commit_list(repo)

        unique_emails = extract_unique_emails(commit_list)
        with open("./email_address.txt", "w") as f:
            for email in unique_emails:
                f.write(email + "\n")
            print(f"\033[92m[+] Unique email addresses written to email_address.txt\033[0m\n")
        
        # print("Unique Email Addresses:")
        # for email in unique_emails:
        #     print(email)
        
        #Searching for keyword in commits
        check_keyword_in_messages(commit_list, keywords)
    else:
        print("Failed to clone the repository.")

def check_keyword_in_messages(commit_list, keywords):
    """Check for a specific keywords in commit messages and print matching messages with their hashes."""
    print("\033[92m[+] Searching for specific keword, use (cd /tmp/repo_clone && git show commit_hash) to display related change\033[0m")
    keyword_list= keywords.split(",")
    for commit_data in commit_list:
        message = commit_data['message']
        for keyword in keyword_list:
            if keyword.lower() in message.lower():
                print(f"Commit Hash: {commit_data['hash']}")
                print(f"Message: {message}\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <repository_url> [keywords]")
        sys.exit(1)
    repository_url = sys.argv[1]
    keywords = sys.argv[2] if len(sys.argv) > 2 else "password,secur"
    main(repository_url, keywords)

