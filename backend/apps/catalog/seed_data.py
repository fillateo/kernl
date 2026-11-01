"""The local course catalog.

Keeping the content in Python makes the seed idempotent and reviewable. Each
lesson carries its own sandbox starter files, so every terminal session begins
in exactly the right state.
"""

from __future__ import annotations

COURSES = [
    {
        "slug": "linux-foundations",
        "title": "Linux Foundations",
        "tagline": "Get comfortable in the shell—one command at a time.",
        "description": (
            "Start with the commands you will use every day. You will explore "
            "the filesystem, shape output, and make sense of permissions, all "
            "inside a real Linux terminal that resets when you leave."
        ),
        "level": "beginner",
        "duration_minutes": 95,
        "accent": "lime",
        "icon": "terminal",
        "outcomes": [
            "Move around the filesystem without guessing",
            "Create, copy, move, and remove files with confidence",
            "Read command output and chain commands together",
            "Understand Linux file permissions and chmod",
        ],
        "tools": ["bash", "ls", "pwd", "grep", "chmod", "pipes"],
        "modules": [
            {
                "title": "The command line",
                "summary": "Build the reflexes that make a terminal feel familiar.",
                "lessons": [
                    {
                        "slug": "working-with-linux-commands",
                        "title": "Working With Linux Commands",
                        "summary": (
                            "Run your first commands and learn what successful "
                            "output looks like."
                        ),
                        "duration_minutes": 12,
                        "is_mandatory": True,
                        "initial_files": {
                            "welcome.txt": (
                                "Welcome to your Kernl sandbox.\n"
                                "This folder is yours. Break things—it resets.\n"
                            ),
                            "projects/hello.txt": (
                                "Hello from a real Linux filesystem.\n"
                            ),
                            "README.md": (
                                "# Sandbox notes\n\n"
                                "Use this space to try every command in the lesson.\n"
                            ),
                        },
                        "content": [
                            {
                                "type": "heading",
                                "eyebrow": "Step 01",
                                "text": "Directory listing",
                            },
                            {
                                "type": "paragraph",
                                "text": (
                                    "`ls` is the Linux command for listing files and "
                                    "directories. Run it with no arguments and it "
                                    "shows what is in your current directory."
                                ),
                            },
                            {
                                "type": "command",
                                "label": "List the current directory",
                                "command": "ls",
                            },
                            {
                                "type": "output",
                                "label": "Command output",
                                "text": "README.md  projects  welcome.txt",
                            },
                            {
                                "type": "paragraph",
                                "text": (
                                    "No error message? That is a successful command. "
                                    "In the shell, silence is usually a good sign."
                                ),
                            },
                            {
                                "type": "heading",
                                "eyebrow": "Step 02",
                                "text": "Ask for more detail",
                            },
                            {
                                "type": "paragraph",
                                "text": (
                                    "Options—also called flags—change how a command "
                                    "behaves. The `-l` option tells `ls` to use its "
                                    "long listing format."
                                ),
                            },
                            {
                                "type": "command",
                                "label": "Display one file per line with details",
                                "command": "ls -l",
                            },
                            {
                                "type": "output",
                                "label": "Command output",
                                "text": (
                                    "total 12\n"
                                    "-rw-rw-r-- 1 learner learner 103 Nov  1 09:00 README.md\n"
                                    "drwxrwxr-x 2 learner learner  40 Nov  1 09:00 projects\n"
                                    "-rw-rw-r-- 1 learner learner  71 Nov  1 09:00 welcome.txt"
                                ),
                            },
                            {
                                "type": "callout",
                                "tone": "note",
                                "title": "Command anatomy",
                                "text": (
                                    "In `ls -l`, `ls` is the command and `-l` is an "
                                    "option. If you add a path after it, that path is "
                                    "an argument."
                                ),
                            },
                            {
                                "type": "heading",
                                "eyebrow": "Step 03",
                                "text": "Make the shell talk back",
                            },
                            {
                                "type": "paragraph",
                                "text": (
                                    "`echo` prints its arguments to standard output. "
                                    "It is a tiny command, but it becomes useful when "
                                    "you start composing commands together."
                                ),
                            },
                            {
                                "type": "command",
                                "label": "Print a greeting",
                                "command": 'echo "Hello world"',
                            },
                            {
                                "type": "output",
                                "label": "Command output",
                                "text": "Hello world",
                            },
                            {
                                "type": "list",
                                "style": "bullet",
                                "items": [
                                    "Commands usually return no text when they succeed.",
                                    "Error messages tell you what the shell could not do.",
                                    "Options begin with a hyphen; arguments come after.",
                                ],
                            },
                            {
                                "type": "checkpoint",
                                "title": "Your turn",
                                "text": (
                                    "Run `pwd` in the terminal. What directory are you "
                                    "standing in? Then run `ls -a` and notice the files "
                                    "that start with a dot."
                                ),
                            },
                        ],
                    },
                    {
                        "slug": "working-with-files-and-directories",
                        "title": "Working With Files and Directories",
                        "summary": (
                            "Create, copy, move, and remove files without leaving "
                            "the terminal."
                        ),
                        "duration_minutes": 18,
                        "is_mandatory": True,
                        "initial_files": {
                            "welcome.txt": "A small file is a good place to start.\n",
                            "notes/todo.txt": (
                                "Read the first chapter\n"
                                "Practice five commands\n"
                                "Clean up the sandbox\n"
                            ),
                        },
                        "content": [
                            {
                                "type": "heading",
                                "eyebrow": "Step 01",
                                "text": "Find your footing",
                            },
                            {
                                "type": "paragraph",
                                "text": (
                                    "`pwd` prints the working directory—the folder "
                                    "your shell is currently inside. Every relative "
                                    "path is resolved from here."
                                ),
                            },
                            {
                                "type": "command",
                                "label": "Print the working directory",
                                "command": "pwd",
                            },
                            {
                                "type": "output",
                                "label": "Command output",
                                "text": "/home/learner",
                            },
                            {
                                "type": "heading",
                                "eyebrow": "Step 02",
                                "text": "Make a place for practice",
                            },
                            {
                                "type": "paragraph",
                                "text": (
                                    "`mkdir` creates a directory. Run `ls` before and "
                                    "after so you can see the change."
                                ),
                            },
                            {
                                "type": "command",
                                "label": "Create a practice directory",
                                "command": "mkdir practice && ls",
                            },
                            {
                                "type": "output",
                                "label": "Command output",
                                "text": "notes  practice  welcome.txt",
                            },
                            {
                                "type": "paragraph",
                                "text": (
                                    "`cd` changes the working directory. The `&&` "
                                    "operator runs the next command only if the first "
                                    "one succeeds."
                                ),
                            },
                            {
                                "type": "command",
                                "label": "Enter the directory and create a file",
                                "command": "cd practice && touch first.txt && pwd",
                            },
                            {
                                "type": "output",
                                "label": "Command output",
                                "text": "/home/learner/practice",
                            },
                            {
                                "type": "callout",
                                "tone": "tip",
                                "title": "Tab completion is your friend",
                                "text": (
                                    "Start typing a path and press Tab. Bash will "
                                    "complete it for you, which is faster and less "
                                    "error-prone than typing every character."
                                ),
                            },
                            {
                                "type": "heading",
                                "eyebrow": "Step 03",
                                "text": "Copy, move, remove",
                            },
                            {
                                "type": "paragraph",
                                "text": (
                                    "`cp` copies, `mv` moves (and renames), and `rm` "
                                    "removes. These commands act immediately: there is "
                                    "no recycle bin on the command line."
                                ),
                            },
                            {
                                "type": "command",
                                "label": "Copy a file, then rename it",
                                "command": (
                                    "cd /home/learner && cp welcome.txt practice/copy.txt "
                                    "&& mv practice/copy.txt practice/renamed.txt "
                                    "&& ls practice"
                                ),
                            },
                            {
                                "type": "output",
                                "label": "Command output",
                                "text": "first.txt  renamed.txt",
                            },
                            {
                                "type": "command",
                                "label": "Remove a file",
                                "command": "rm practice/renamed.txt && ls practice",
                            },
                            {
                                "type": "output",
                                "label": "Command output",
                                "text": "first.txt",
                            },
                            {
                                "type": "checkpoint",
                                "title": "Your turn",
                                "text": (
                                    "Create a folder called `archive`, move "
                                    "`welcome.txt` into it, and list the folder to "
                                    "confirm the move."
                                ),
                            },
                        ],
                    },
                ],
            },
            {
                "title": "Output, pipes & permissions",
                "summary": "Make commands work together and understand who can do what.",
                "lessons": [
                    {
                        "slug": "reading-command-output",
                        "title": "Reading Command Output",
                        "summary": (
                            "Search, count, and redirect the text that commands "
                            "produce."
                        ),
                        "duration_minutes": 15,
                        "is_mandatory": True,
                        "initial_files": {
                            "logs/app.log": (
                                "INFO  server started on port 8080\n"
                                "INFO  health check passed\n"
                                "WARN  slow query took 820ms\n"
                                "ERROR database connection timed out\n"
                                "INFO  retrying connection\n"
                                "INFO  connection restored\n"
                                "ERROR cache miss for session 42\n"
                                "INFO  request completed in 34ms\n"
                            ),
                            "data/servers.csv": (
                                "name,region,status\n"
                                "api-1,eu-west,healthy\n"
                                "api-2,us-east,healthy\n"
                                "api-3,ap-south,degraded\n"
                            ),
                        },
                        "content": [
                            {
                                "type": "heading",
                                "eyebrow": "Step 01",
                                "text": "Read a slice of a file",
                            },
                            {
                                "type": "paragraph",
                                "text": (
                                    "`head` prints the beginning of a file. The `-n` "
                                    "option controls how many lines you see."
                                ),
                            },
                            {
                                "type": "command",
                                "label": "Show the first three lines",
                                "command": "head -n 3 logs/app.log",
                            },
                            {
                                "type": "output",
                                "label": "Command output",
                                "text": (
                                    "INFO  server started on port 8080\n"
                                    "INFO  health check passed\n"
                                    "WARN  slow query took 820ms"
                                ),
                            },
                            {
                                "type": "heading",
                                "eyebrow": "Step 02",
                                "text": "Find the signal",
                            },
                            {
                                "type": "paragraph",
                                "text": (
                                    "`grep` searches text line by line. Pipe the output "
                                    "of one command into another with `|`."
                                ),
                            },
                            {
                                "type": "command",
                                "label": "Find errors in the log",
                                "command": "grep ERROR logs/app.log",
                            },
                            {
                                "type": "output",
                                "label": "Command output",
                                "text": (
                                    "ERROR database connection timed out\n"
                                    "ERROR cache miss for session 42"
                                ),
                            },
                            {
                                "type": "paragraph",
                                "text": (
                                    "Count matching lines with `-c`, or make the "
                                    "search case-insensitive with `-i`."
                                ),
                            },
                            {
                                "type": "command",
                                "label": "Count the errors",
                                "command": "grep -c ERROR logs/app.log",
                            },
                            {
                                "type": "output",
                                "label": "Command output",
                                "text": "2",
                            },
                            {
                                "type": "heading",
                                "eyebrow": "Step 03",
                                "text": "Redirect the stream",
                            },
                            {
                                "type": "paragraph",
                                "text": (
                                    "`>` sends output into a file and replaces its "
                                    "contents. `>>` appends instead of replacing."
                                ),
                            },
                            {
                                "type": "command",
                                "label": "Write matching lines to a report",
                                "command": (
                                    "grep ERROR logs/app.log > errors.txt && "
                                    "cat errors.txt"
                                ),
                            },
                            {
                                "type": "output",
                                "label": "Command output",
                                "text": (
                                    "ERROR database connection timed out\n"
                                    "ERROR cache miss for session 42"
                                ),
                            },
                            {
                                "type": "callout",
                                "tone": "warning",
                                "title": "Overwrite happens instantly",
                                "text": (
                                    "A single `>` replaces a file immediately. Use "
                                    "`>>` when you mean to add to the end."
                                ),
                            },
                            {
                                "type": "checkpoint",
                                "title": "Your turn",
                                "text": (
                                    "Count the lines in `data/servers.csv` with "
                                    "`wc -l`, then find only the degraded server with "
                                    "`grep degraded`."
                                ),
                            },
                        ],
                    },
                    {
                        "slug": "file-permissions-demystified",
                        "title": "File Permissions, Demystified",
                        "summary": (
                            "Read Linux permission strings and change them with chmod."
                        ),
                        "duration_minutes": 20,
                        "is_mandatory": True,
                        "initial_files": {
                            "deploy.sh": (
                                "#!/usr/bin/env bash\n"
                                "echo 'Deploying the sandbox...'\n"
                                "echo 'Done.'\n"
                            ),
                            "secrets.env": "API_TOKEN=not-a-real-token\n",
                            "shared.txt": "This note is safe to share.\n",
                        },
                        "content": [
                            {
                                "type": "heading",
                                "eyebrow": "Step 01",
                                "text": "Decode the permission string",
                            },
                            {
                                "type": "paragraph",
                                "text": (
                                    "Run `ls -l` and look at the first ten characters. "
                                    "The first character is the file type; the next "
                                    "nine are permissions for the owner, group, and "
                                    "everyone else."
                                ),
                            },
                            {
                                "type": "command",
                                "label": "Inspect three files",
                                "command": "ls -l deploy.sh secrets.env shared.txt",
                            },
                            {
                                "type": "output",
                                "label": "Command output",
                                "text": (
                                    "-rw-r--r-- 1 learner learner  89 Nov  1 09:10 deploy.sh\n"
                                    "-rw-r--r-- 1 learner learner  30 Nov  1 09:10 secrets.env\n"
                                    "-rw-r--r-- 1 learner learner  35 Nov  1 09:10 shared.txt"
                                ),
                            },
                            {
                                "type": "list",
                                "style": "bullet",
                                "items": [
                                    "`r` means read, `w` means write, `x` means execute.",
                                    "The first triplet belongs to the owner.",
                                    "The second belongs to the group; the third to everyone else.",
                                ],
                            },
                            {
                                "type": "heading",
                                "eyebrow": "Step 02",
                                "text": "Make a script executable",
                            },
                            {
                                "type": "paragraph",
                                "text": (
                                    "A script needs execute permission before you can "
                                    "run it with `./`. `chmod +x` adds that permission "
                                    "for everyone."
                                ),
                            },
                            {
                                "type": "command",
                                "label": "Add execute permission",
                                "command": "chmod +x deploy.sh && ls -l deploy.sh",
                            },
                            {
                                "type": "output",
                                "label": "Command output",
                                "text": (
                                    "-rwxr-xr-x 1 learner learner 89 Nov  1 09:10 deploy.sh"
                                ),
                            },
                            {
                                "type": "command",
                                "label": "Run the script",
                                "command": "./deploy.sh",
                            },
                            {
                                "type": "output",
                                "label": "Command output",
                                "text": "Deploying the sandbox...\nDone.",
                            },
                            {
                                "type": "heading",
                                "eyebrow": "Step 03",
                                "text": "Use numbers for precision",
                            },
                            {
                                "type": "paragraph",
                                "text": (
                                    "Octal notation is a compact way to set all three "
                                    "triplets at once: read is 4, write is 2, and "
                                    "execute is 1. `600` means read and write for the "
                                    "owner only."
                                ),
                            },
                            {
                                "type": "command",
                                "label": "Lock down a secret",
                                "command": "chmod 600 secrets.env && ls -l secrets.env",
                            },
                            {
                                "type": "output",
                                "label": "Command output",
                                "text": "-rw------- 1 learner learner 30 Nov  1 09:10 secrets.env",
                            },
                            {
                                "type": "callout",
                                "tone": "warning",
                                "title": "Permissions are not encryption",
                                "text": (
                                    "If someone can read the file as root, permissions "
                                    "will not protect it. Never put real credentials in "
                                    "a learning sandbox."
                                ),
                            },
                            {
                                "type": "checkpoint",
                                "title": "Your turn",
                                "text": (
                                    "Set `shared.txt` to `644` and confirm the result. "
                                    "Then run `stat shared.txt` to see the same "
                                    "permissions in a different format."
                                ),
                            },
                        ],
                    },
                ],
            },
        ],
    },
    {
        "slug": "git-essentials",
        "title": "Git Essentials",
        "tagline": "Track your work without guessing what changed.",
        "description": (
            "Learn Git by making real commits in a disposable repository. "
            "You will stage changes, read history, build a branch, and merge it "
            "back—without risking anything you care about."
        ),
        "level": "beginner",
        "duration_minutes": 75,
        "accent": "violet",
        "icon": "branch",
        "outcomes": [
            "Initialize a repository and read its status",
            "Stage and commit changes with clear messages",
            "Inspect history with git log and git diff",
            "Create a branch and merge it safely",
        ],
        "tools": ["git init", "git status", "git add", "git commit", "git switch"],
        "modules": [
            {
                "title": "Repositories",
                "summary": "The three places a Git change can live.",
                "lessons": [
                    {
                        "slug": "your-first-repository",
                        "title": "Your First Repository",
                        "summary": (
                            "Turn a folder into a Git repository and read its status."
                        ),
                        "duration_minutes": 20,
                        "is_mandatory": True,
                        "initial_files": {
                            "README.md": (
                                "# Launch checklist\n\n"
                                "- [ ] Write the first draft\n"
                                "- [ ] Review it\n"
                                "- [ ] Ship it\n"
                            ),
                            "src/app.py": (
                                'def main():\n    print("Hello from the app")\n\n\n'
                                'if __name__ == "__main__":\n    main()\n'
                            ),
                        },
                        "content": [
                            {
                                "type": "heading",
                                "eyebrow": "Step 01",
                                "text": "Create the repository",
                            },
                            {
                                "type": "paragraph",
                                "text": (
                                    "`git init` turns the current directory into a "
                                    "repository by creating a hidden `.git` folder. "
                                    "The folder is local; nothing is uploaded."
                                ),
                            },
                            {
                                "type": "command",
                                "label": "Initialize Git",
                                "command": "git init",
                            },
                            {
                                "type": "output",
                                "label": "Command output",
                                "text": "Initialized empty Git repository in /home/learner/.git/",
                            },
                            {
                                "type": "command",
                                "label": "See the hidden folder",
                                "command": "ls -a",
                            },
                            {
                                "type": "output",
                                "label": "Command output",
                                "text": ".  ..  .git  README.md  src",
                            },
                            {
                                "type": "heading",
                                "eyebrow": "Step 02",
                                "text": "Ask Git what it sees",
                            },
                            {
                                "type": "paragraph",
                                "text": (
                                    "`git status` is the command you will run most "
                                    "often. Untracked files are visible to Git but not "
                                    "part of the next commit yet."
                                ),
                            },
                            {
                                "type": "command",
                                "label": "Check the status",
                                "command": "git status",
                            },
                            {
                                "type": "output",
                                "label": "Command output",
                                "text": (
                                    "On branch main\n\n"
                                    "No commits yet\n\n"
                                    "Untracked files:\n"
                                    '  (use "git add <file>..." to include in what will be committed)\n'
                                    "\tREADME.md\n\tsrc/\n\n"
                                    "nothing added to commit but untracked files present"
                                ),
                            },
                            {
                                "type": "callout",
                                "tone": "note",
                                "title": "The three places",
                                "text": (
                                    "Your working tree is the folder you edit. The "
                                    "staging area is what the next commit will include. "
                                    "The repository is the history of commits."
                                ),
                            },
                            {
                                "type": "checkpoint",
                                "title": "Your turn",
                                "text": (
                                    "Run `git status --short`. The `??` marks untracked "
                                    "files. Keep that status open while you move to the "
                                    "next lesson."
                                ),
                            },
                        ],
                    },
                    {
                        "slug": "staging-and-committing",
                        "title": "Staging & Committing",
                        "summary": (
                            "Turn a working-tree change into a clear, permanent commit."
                        ),
                        "duration_minutes": 25,
                        "is_mandatory": True,
                        "initial_files": {
                            "README.md": "# Launch checklist\n\nA tiny project.\n",
                            "src/app.py": (
                                'def main():\n    print("Hello from the app")\n\n\n'
                                'if __name__ == "__main__":\n    main()\n'
                            ),
                        },
                        "content": [
                            {
                                "type": "heading",
                                "eyebrow": "Setup",
                                "text": "Start a repository",
                            },
                            {
                                "type": "paragraph",
                                "text": (
                                    "This sandbox begins as a plain folder. Create a "
                                    "repository and make the starter files the first "
                                    "commit before you change anything."
                                ),
                            },
                            {
                                "type": "command",
                                "label": "Initialize and make the first commit",
                                "command": (
                                    "git init -b main && git add . && "
                                    'git commit -m "Initial project setup"'
                                ),
                            },
                            {
                                "type": "output",
                                "label": "Command output",
                                "text": (
                                    "[main (root-commit) 4c1a9e2] Initial project setup\n"
                                    " 2 files changed, 14 insertions(+)\n"
                                    " create mode 100644 README.md\n"
                                    " create mode 100644 src/app.py"
                                ),
                            },
                            {
                                "type": "heading",
                                "eyebrow": "Step 01",
                                "text": "Make a focused change",
                            },
                            {
                                "type": "paragraph",
                                "text": (
                                    "Append a line to the README. Then ask Git what "
                                    "changed with `git diff`."
                                ),
                            },
                            {
                                "type": "command",
                                "label": "Edit the README",
                                "command": (
                                    "printf '\\n## Next up\\nShip the first version.\\n' "
                                    ">> README.md && git diff"
                                ),
                            },
                            {
                                "type": "output",
                                "label": "Command output",
                                "text": (
                                    "diff --git a/README.md b/README.md\n"
                                    "index 4f2a1c3..8d9e0f1 100644\n"
                                    "--- a/README.md\n+++ b/README.md\n"
                                    "@@ -1,3 +1,6 @@\n"
                                    " # Launch checklist\n \n"
                                    " A tiny project.\n"
                                    "+\n"
                                    "+## Next up\n"
                                    "+Ship the first version."
                                ),
                            },
                            {
                                "type": "heading",
                                "eyebrow": "Step 02",
                                "text": "Stage only what belongs together",
                            },
                            {
                                "type": "paragraph",
                                "text": (
                                    "`git add` moves changes into the staging area. "
                                    "Use `git add -p` for very large changes, but a "
                                    "specific path is perfect here."
                                ),
                            },
                            {
                                "type": "command",
                                "label": "Stage the README",
                                "command": "git add README.md && git status --short",
                            },
                            {
                                "type": "output",
                                "label": "Command output",
                                "text": "M  README.md",
                            },
                            {
                                "type": "heading",
                                "eyebrow": "Step 03",
                                "text": "Commit the snapshot",
                            },
                            {
                                "type": "paragraph",
                                "text": (
                                    "A commit is a labelled snapshot. Write the subject "
                                    "in the imperative mood: “Add launch plan,” not "
                                    "“Added stuff.”"
                                ),
                            },
                            {
                                "type": "command",
                                "label": "Commit the staged change",
                                "command": (
                                    'git commit -m "Add launch plan to README" && '
                                    "git log --oneline"
                                ),
                            },
                            {
                                "type": "output",
                                "label": "Command output",
                                "text": (
                                    "[main 9b7c2d4] Add launch plan to README\n"
                                    " 1 file changed, 3 insertions(+)\n"
                                    "9b7c2d4 Add launch plan to README\n"
                                    "4c1a9e2 Initial project setup"
                                ),
                            },
                            {
                                "type": "checkpoint",
                                "title": "Your turn",
                                "text": (
                                    "Run `git show --stat HEAD` to inspect the commit "
                                    "you just made. Notice that `HEAD` is a moving "
                                    "pointer to the latest commit."
                                ),
                            },
                        ],
                    },
                ],
            },
            {
                "title": "History & branches",
                "summary": "Make a safe copy of history, then bring the work back.",
                "lessons": [
                    {
                        "slug": "branching-without-fear",
                        "title": "Branching Without Fear",
                        "summary": (
                            "Create a branch, make a change, and merge it into main."
                        ),
                        "duration_minutes": 30,
                        "is_mandatory": True,
                        "initial_files": {
                            "README.md": "# Launch checklist\n\nA tiny project.\n",
                            "src/app.py": (
                                'def main():\n    print("Hello from the app")\n\n\n'
                                'if __name__ == "__main__":\n    main()\n'
                            ),
                        },
                        "content": [
                            {
                                "type": "heading",
                                "eyebrow": "Setup",
                                "text": "Create a base commit",
                            },
                            {
                                "type": "paragraph",
                                "text": (
                                    "A branch needs at least one commit. Initialize "
                                    "the repository and snapshot the starter project."
                                ),
                            },
                            {
                                "type": "command",
                                "label": "Create the starting point",
                                "command": (
                                    "git init -b main && git add . && "
                                    'git commit -m "Initial project setup"'
                                ),
                            },
                            {
                                "type": "heading",
                                "eyebrow": "Step 01",
                                "text": "Branch away from main",
                            },
                            {
                                "type": "paragraph",
                                "text": (
                                    "A branch is a movable pointer to a commit. "
                                    "`git switch -c` creates a new branch and moves "
                                    "you onto it."
                                ),
                            },
                            {
                                "type": "command",
                                "label": "Create a feature branch",
                                "command": "git switch -c feature/greeting",
                            },
                            {
                                "type": "output",
                                "label": "Command output",
                                "text": "Switched to a new branch 'feature/greeting'",
                            },
                            {
                                "type": "heading",
                                "eyebrow": "Step 02",
                                "text": "Commit on the branch",
                            },
                            {
                                "type": "command",
                                "label": "Add a greeting and commit it",
                                "command": (
                                    "printf '\\nprint(\"Have a nice day\")\\n' >> src/app.py "
                                    "&& git add src/app.py && "
                                    'git commit -m "Add a friendly greeting"'
                                ),
                            },
                            {
                                "type": "output",
                                "label": "Command output",
                                "text": (
                                    "[feature/greeting 71d3c9a] Add a friendly greeting\n"
                                    " 1 file changed, 2 insertions(+)"
                                ),
                            },
                            {
                                "type": "heading",
                                "eyebrow": "Step 03",
                                "text": "Merge back into main",
                            },
                            {
                                "type": "paragraph",
                                "text": (
                                    "Switch to `main` and merge the branch. Because "
                                    "`main` has not moved since you branched, Git can "
                                    "fast-forward."
                                ),
                            },
                            {
                                "type": "command",
                                "label": "Switch, merge, and inspect history",
                                "command": (
                                    "git switch main && git merge feature/greeting && "
                                    "git log --oneline --graph --all"
                                ),
                            },
                            {
                                "type": "output",
                                "label": "Command output",
                                "text": (
                                    "Switched to branch 'main'\n"
                                    "Updating 4c1a9e2..71d3c9a\nFast-forward\n"
                                    " src/app.py | 2 ++\n 1 file changed, 2 insertions(+)\n"
                                    "* 71d3c9a Add a friendly greeting\n"
                                    "* 4c1a9e2 Initial project setup"
                                ),
                            },
                            {
                                "type": "callout",
                                "tone": "tip",
                                "title": "Branch early",
                                "text": (
                                    "Branches are cheap. Create one before an "
                                    "experiment and `main` stays a clean, known-good "
                                    "starting point."
                                ),
                            },
                            {
                                "type": "checkpoint",
                                "title": "Your turn",
                                "text": (
                                    "Run `git branch --show-current` and `git status`. "
                                    "You should be back on `main` with a clean working "
                                    "tree."
                                ),
                            },
                        ],
                    },
                ],
            },
        ],
    },
    {
        "slug": "bash-scripting",
        "title": "Bash Scripting",
        "tagline": "Turn one-off commands into tools you can reuse.",
        "description": (
            "Take the commands you already know and give them structure. Write "
            "scripts that accept arguments, make decisions, and repeat work "
            "without another copy-paste."
        ),
        "level": "intermediate",
        "duration_minutes": 110,
        "accent": "coral",
        "icon": "code",
        "outcomes": [
            "Write and run a bash script with a shebang",
            "Use variables and positional arguments",
            "Make scripts respond to success and failure",
            "Loop over files and guard conditions",
        ],
        "tools": ["bash", "chmod", "variables", "if", "for"],
        "modules": [
            {
                "title": "Script fundamentals",
                "summary": "From a text file to a command you can run.",
                "lessons": [
                    {
                        "slug": "your-first-script",
                        "title": "Your First Script",
                        "summary": (
                            "Write a tiny bash script, make it executable, and run it."
                        ),
                        "duration_minutes": 25,
                        "is_mandatory": True,
                        "initial_files": {
                            "hello.sh": (
                                "#!/usr/bin/env bash\n"
                                "echo 'Hello from a script'\n"
                                'echo "Running: $(basename "$0")"\n'
                            ),
                        },
                        "content": [
                            {
                                "type": "heading",
                                "eyebrow": "Step 01",
                                "text": "Read before you run",
                            },
                            {
                                "type": "paragraph",
                                "text": (
                                    "A script is a file of commands. The first line, "
                                    "called a shebang, tells the operating system "
                                    "which interpreter should run the file."
                                ),
                            },
                            {
                                "type": "command",
                                "label": "Inspect the script",
                                "command": "cat hello.sh",
                            },
                            {
                                "type": "output",
                                "label": "Command output",
                                "text": (
                                    "#!/usr/bin/env bash\n"
                                    "echo 'Hello from a script'\n"
                                    'echo "Running: $(basename "$0")"'
                                ),
                            },
                            {
                                "type": "callout",
                                "tone": "note",
                                "title": "The shebang",
                                "text": (
                                    "`#!/usr/bin/env bash` asks the system to find "
                                    "`bash` on PATH and use it as the interpreter."
                                ),
                            },
                            {
                                "type": "heading",
                                "eyebrow": "Step 02",
                                "text": "Give it permission to run",
                            },
                            {
                                "type": "paragraph",
                                "text": (
                                    "Try running `./hello.sh` now. It fails because "
                                    "the file is not executable yet. Add execute "
                                    "permission with `chmod`."
                                ),
                            },
                            {
                                "type": "command",
                                "label": "Make the script executable",
                                "command": "chmod +x hello.sh && ./hello.sh",
                            },
                            {
                                "type": "output",
                                "label": "Command output",
                                "text": "Hello from a script\nRunning: hello.sh",
                            },
                            {
                                "type": "heading",
                                "eyebrow": "Step 03",
                                "text": "Run it without chmod",
                            },
                            {
                                "type": "paragraph",
                                "text": (
                                    "You can also hand the script to bash explicitly. "
                                    "This works even without execute permission and is "
                                    "handy while you are iterating."
                                ),
                            },
                            {
                                "type": "command",
                                "label": "Run the script through bash",
                                "command": "bash hello.sh",
                            },
                            {
                                "type": "output",
                                "label": "Command output",
                                "text": "Hello from a script\nRunning: hello.sh",
                            },
                            {
                                "type": "checkpoint",
                                "title": "Your turn",
                                "text": (
                                    "Add a third `echo` line to `hello.sh` using "
                                    "`printf` or a text editor command, then rerun it. "
                                    'Notice that `$(basename "$0")` is evaluated when '
                                    "the script runs, not when you write it."
                                ),
                            },
                        ],
                    },
                    {
                        "slug": "variables-and-arguments",
                        "title": "Variables & Arguments",
                        "summary": (
                            "Make a script configurable without editing its source."
                        ),
                        "duration_minutes": 35,
                        "is_mandatory": True,
                        "initial_files": {
                            "greet.sh": (
                                "#!/usr/bin/env bash\n"
                                'name="${1:-friend}"\n'
                                'echo "Hello, ${name}!"\n'
                                'echo "You passed ${#} argument(s)."\n'
                            ),
                        },
                        "content": [
                            {
                                "type": "heading",
                                "eyebrow": "Step 01",
                                "text": "Read the argument",
                            },
                            {
                                "type": "paragraph",
                                "text": (
                                    "`$1` is the first positional argument. The "
                                    "`${1:-friend}` form supplies a default when the "
                                    "argument is missing."
                                ),
                            },
                            {
                                "type": "command",
                                "label": "Run with and without an argument",
                                "command": "chmod +x greet.sh && ./greet.sh && ./greet.sh Ada",
                            },
                            {
                                "type": "output",
                                "label": "Command output",
                                "text": (
                                    "Hello, friend!\n"
                                    "You passed 0 argument(s).\n"
                                    "Hello, Ada!\n"
                                    "You passed 1 argument(s)."
                                ),
                            },
                            {
                                "type": "heading",
                                "eyebrow": "Step 02",
                                "text": "Use variables safely",
                            },
                            {
                                "type": "paragraph",
                                "text": (
                                    "Assign with `name=value` — no spaces around the "
                                    "equals sign. Quote expansions, especially when a "
                                    "value might contain spaces."
                                ),
                            },
                            {
                                "type": "command",
                                "label": "Use a variable in the shell",
                                "command": (
                                    'project="Kernl"; echo "Working on ${project}"; '
                                    'echo "The variable is ${#project} characters long."'
                                ),
                            },
                            {
                                "type": "output",
                                "label": "Command output",
                                "text": (
                                    "Working on Kernl\n"
                                    "The variable is 5 characters long."
                                ),
                            },
                            {
                                "type": "callout",
                                "tone": "warning",
                                "title": "Quote your variables",
                                "text": (
                                    'Prefer `"$name"` over `$name`. Unquoted values '
                                    "can split into multiple arguments or expand "
                                    "wildcards unexpectedly."
                                ),
                            },
                            {
                                "type": "heading",
                                "eyebrow": "Step 03",
                                "text": "Capture a result",
                            },
                            {
                                "type": "paragraph",
                                "text": (
                                    "Command substitution with `$(...)` captures the "
                                    "output of a command. The special variable `$?` "
                                    "holds the exit status of the previous command."
                                ),
                            },
                            {
                                "type": "command",
                                "label": "Capture output and check status",
                                "command": (
                                    'greeting="$(printf "hello")"; '
                                    'echo "${greeting}, learner"; true; '
                                    'echo "Status: $?"'
                                ),
                            },
                            {
                                "type": "output",
                                "label": "Command output",
                                "text": "hello, learner\nStatus: 0",
                            },
                            {
                                "type": "checkpoint",
                                "title": "Your turn",
                                "text": (
                                    "Update `greet.sh` to also print the second "
                                    "argument if one is provided. Test the zero-, "
                                    "one-, and two-argument cases."
                                ),
                            },
                        ],
                    },
                ],
            },
            {
                "title": "Control flow",
                "summary": "Let the script decide and repeat.",
                "lessons": [
                    {
                        "slug": "loops-and-conditionals",
                        "title": "Loops & Conditionals",
                        "summary": (
                            "Write a script that checks for files and loops over them."
                        ),
                        "duration_minutes": 50,
                        "is_mandatory": True,
                        "initial_files": {
                            "notes/day-1.txt": "First day notes.\n",
                            "notes/day-2.txt": "Second day notes.\n",
                            "notes/day-3.txt": "Third day notes.\n",
                            "inventory.sh": (
                                "#!/usr/bin/env bash\n"
                                "count=0\n"
                                "for file in notes/*.txt; do\n"
                                '  if [ -f "$file" ]; then\n'
                                '    echo "Found $(basename "$file")"\n'
                                "    count=$((count + 1))\n"
                                "  fi\n"
                                "done\n"
                                'echo "Total files: ${count}"\n'
                            ),
                        },
                        "content": [
                            {
                                "type": "heading",
                                "eyebrow": "Step 01",
                                "text": "Read the control flow",
                            },
                            {
                                "type": "paragraph",
                                "text": (
                                    "The `for` loop walks over a list; the `if` block "
                                    "guards the work inside it. Bash ends blocks with "
                                    "`done` and `fi`—the keyword reversed."
                                ),
                            },
                            {
                                "type": "command",
                                "label": "Inspect the script",
                                "command": "cat inventory.sh",
                            },
                            {
                                "type": "output",
                                "label": "Command output",
                                "text": (
                                    "#!/usr/bin/env bash\ncount=0\n"
                                    "for file in notes/*.txt; do\n"
                                    '  if [ -f "$file" ]; then\n'
                                    '    echo "Found $(basename "$file")"\n'
                                    "    count=$((count + 1))\n"
                                    "  fi\ndone\n"
                                    'echo "Total files: ${count}"'
                                ),
                            },
                            {
                                "type": "heading",
                                "eyebrow": "Step 02",
                                "text": "Run the loop",
                            },
                            {
                                "type": "command",
                                "label": "Run the inventory script",
                                "command": "chmod +x inventory.sh && ./inventory.sh",
                            },
                            {
                                "type": "output",
                                "label": "Command output",
                                "text": (
                                    "Found day-1.txt\n"
                                    "Found day-2.txt\n"
                                    "Found day-3.txt\n"
                                    "Total files: 3"
                                ),
                            },
                            {
                                "type": "callout",
                                "tone": "note",
                                "title": "Arithmetic in bash",
                                "text": (
                                    "`$((...))` evaluates an arithmetic expression. "
                                    "`((count++))` is the shorter form you will see in "
                                    "many scripts."
                                ),
                            },
                            {
                                "type": "heading",
                                "eyebrow": "Step 03",
                                "text": "Add a guard",
                            },
                            {
                                "type": "paragraph",
                                "text": (
                                    "Real scripts should fail clearly. Check for a "
                                    "directory before looping over it and use `exit 1` "
                                    "to signal failure."
                                ),
                            },
                            {
                                "type": "command",
                                "label": "Test a precondition",
                                "command": (
                                    'if [ -d notes ]; then echo "notes/ exists"; '
                                    'else echo "missing"; exit 1; fi'
                                ),
                            },
                            {
                                "type": "output",
                                "label": "Command output",
                                "text": "notes/ exists",
                            },
                            {
                                "type": "checkpoint",
                                "title": "Your turn",
                                "text": (
                                    "Run `./inventory.sh` after deleting one note. "
                                    "Then add a line to the script that reports when "
                                    "no files were found."
                                ),
                            },
                        ],
                    },
                ],
            },
        ],
    },
]
