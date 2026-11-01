"""The local course catalog.

Only the Git Essentials track is exposed by the one-page lesson
workspace.
"""

from __future__ import annotations

COURSES = [
    {
        "slug": "git-essentials",
        "title": "Git Essentials",
        "tagline": "Track your work without guessing what changed.",
        "description": "Learn Git by making real commits in a disposable repository. You "
        "will stage changes, read history, build a branch, and merge it "
        "back—without risking anything you care about.",
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
                        "summary": "Turn a folder into a Git repository and read "
                        "its status.",
                        "duration_minutes": 20,
                        "is_mandatory": True,
                        "initial_files": {
                            "README.md": "# Launch checklist\n"
                            "\n"
                            "- [ ] Write the first "
                            "draft\n"
                            "- [ ] Review it\n"
                            "- [ ] Ship it\n",
                            "src/app.py": "def main():\n"
                            '    print("Hello from the '
                            'app")\n'
                            "\n"
                            "\n"
                            "if __name__ == "
                            '"__main__":\n'
                            "    main()\n",
                        },
                        "content": [
                            {
                                "type": "heading",
                                "eyebrow": "Step 01",
                                "text": "Create the repository",
                            },
                            {
                                "type": "paragraph",
                                "text": "`git init` turns the current "
                                "directory into a repository by "
                                "creating a hidden `.git` folder. The "
                                "folder is local; nothing is "
                                "uploaded.",
                            },
                            {
                                "type": "command",
                                "label": "Initialize Git",
                                "command": "git init",
                            },
                            {
                                "type": "output",
                                "label": "Command output",
                                "text": "Initialized empty Git repository in "
                                "/home/learner/.git/",
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
                                "text": "`git status` is the command you will "
                                "run most often. Untracked files are "
                                "visible to Git but not part of the "
                                "next commit yet.",
                            },
                            {
                                "type": "command",
                                "label": "Check the status",
                                "command": "git status",
                            },
                            {
                                "type": "output",
                                "label": "Command output",
                                "text": "On branch main\n"
                                "\n"
                                "No commits yet\n"
                                "\n"
                                "Untracked files:\n"
                                '  (use "git add <file>..." to '
                                "include in what will be committed)\n"
                                "\tREADME.md\n"
                                "\tsrc/\n"
                                "\n"
                                "nothing added to commit but "
                                "untracked files present",
                            },
                            {
                                "type": "callout",
                                "tone": "note",
                                "title": "The three places",
                                "text": "Your working tree is the folder you "
                                "edit. The staging area is what the "
                                "next commit will include. The "
                                "repository is the history of "
                                "commits.",
                            },
                            {
                                "type": "checkpoint",
                                "title": "Your turn",
                                "text": "Run `git status --short`. The `??` "
                                "marks untracked files. Keep that "
                                "status open while you move to the "
                                "next lesson.",
                            },
                        ],
                    },
                    {
                        "slug": "staging-and-committing",
                        "title": "Staging & Committing",
                        "summary": "Turn a working-tree change into a clear, "
                        "permanent commit.",
                        "duration_minutes": 25,
                        "is_mandatory": True,
                        "initial_files": {
                            "README.md": "# Launch checklist\n\nA tiny project.\n",
                            "src/app.py": "def main():\n"
                            '    print("Hello from the '
                            'app")\n'
                            "\n"
                            "\n"
                            "if __name__ == "
                            '"__main__":\n'
                            "    main()\n",
                        },
                        "content": [
                            {
                                "type": "heading",
                                "eyebrow": "Setup",
                                "text": "Start a repository",
                            },
                            {
                                "type": "paragraph",
                                "text": "This sandbox begins as a plain "
                                "folder. Create a repository and make "
                                "the starter files the first commit "
                                "before you change anything.",
                            },
                            {
                                "type": "command",
                                "label": "Initialize and make the first commit",
                                "command": "git init -b main && git add . && "
                                'git commit -m "Initial project '
                                'setup"',
                            },
                            {
                                "type": "output",
                                "label": "Command output",
                                "text": "[main (root-commit) 4c1a9e2] Initial "
                                "project setup\n"
                                " 2 files changed, 14 insertions(+)\n"
                                " create mode 100644 README.md\n"
                                " create mode 100644 src/app.py",
                            },
                            {
                                "type": "heading",
                                "eyebrow": "Step 01",
                                "text": "Make a focused change",
                            },
                            {
                                "type": "paragraph",
                                "text": "Append a line to the README. Then "
                                "ask Git what changed with `git "
                                "diff`.",
                            },
                            {
                                "type": "command",
                                "label": "Edit the README",
                                "command": "printf '\\n## Next up\\nShip the "
                                "first version.\\n' >> README.md "
                                "&& git diff",
                            },
                            {
                                "type": "output",
                                "label": "Command output",
                                "text": "diff --git a/README.md b/README.md\n"
                                "index 4f2a1c3..8d9e0f1 100644\n"
                                "--- a/README.md\n"
                                "+++ b/README.md\n"
                                "@@ -1,3 +1,6 @@\n"
                                " # Launch checklist\n"
                                " \n"
                                " A tiny project.\n"
                                "+\n"
                                "+## Next up\n"
                                "+Ship the first version.",
                            },
                            {
                                "type": "heading",
                                "eyebrow": "Step 02",
                                "text": "Stage only what belongs together",
                            },
                            {
                                "type": "paragraph",
                                "text": "`git add` moves changes into the "
                                "staging area. Use `git add -p` for "
                                "very large changes, but a specific "
                                "path is perfect here.",
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
                                "text": "A commit is a labelled snapshot. "
                                "Write the subject in the imperative "
                                "mood: “Add launch plan,” not “Added "
                                "stuff.”",
                            },
                            {
                                "type": "command",
                                "label": "Commit the staged change",
                                "command": 'git commit -m "Add launch plan to '
                                'README" && git log --oneline',
                            },
                            {
                                "type": "output",
                                "label": "Command output",
                                "text": "[main 9b7c2d4] Add launch plan to "
                                "README\n"
                                " 1 file changed, 3 insertions(+)\n"
                                "9b7c2d4 Add launch plan to README\n"
                                "4c1a9e2 Initial project setup",
                            },
                            {
                                "type": "checkpoint",
                                "title": "Your turn",
                                "text": "Run `git show --stat HEAD` to "
                                "inspect the commit you just made. "
                                "Notice that `HEAD` is a moving "
                                "pointer to the latest commit.",
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
                        "summary": "Create a branch, make a change, and merge it "
                        "into main.",
                        "duration_minutes": 30,
                        "is_mandatory": True,
                        "initial_files": {
                            "README.md": "# Launch checklist\n\nA tiny project.\n",
                            "src/app.py": "def main():\n"
                            '    print("Hello from the '
                            'app")\n'
                            "\n"
                            "\n"
                            "if __name__ == "
                            '"__main__":\n'
                            "    main()\n",
                        },
                        "content": [
                            {
                                "type": "heading",
                                "eyebrow": "Setup",
                                "text": "Create a base commit",
                            },
                            {
                                "type": "paragraph",
                                "text": "A branch needs at least one commit. "
                                "Initialize the repository and "
                                "snapshot the starter project.",
                            },
                            {
                                "type": "command",
                                "label": "Create the starting point",
                                "command": "git init -b main && git add . && "
                                'git commit -m "Initial project '
                                'setup"',
                            },
                            {
                                "type": "heading",
                                "eyebrow": "Step 01",
                                "text": "Branch away from main",
                            },
                            {
                                "type": "paragraph",
                                "text": "A branch is a movable pointer to a "
                                "commit. `git switch -c` creates a "
                                "new branch and moves you onto it.",
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
                                "command": "printf '\\nprint(\"Have a nice "
                                "day\")\\n' >> src/app.py && git "
                                "add src/app.py && git commit -m "
                                '"Add a friendly greeting"',
                            },
                            {
                                "type": "output",
                                "label": "Command output",
                                "text": "[feature/greeting 71d3c9a] Add a "
                                "friendly greeting\n"
                                " 1 file changed, 2 insertions(+)",
                            },
                            {
                                "type": "heading",
                                "eyebrow": "Step 03",
                                "text": "Merge back into main",
                            },
                            {
                                "type": "paragraph",
                                "text": "Switch to `main` and merge the "
                                "branch. Because `main` has not moved "
                                "since you branched, Git can "
                                "fast-forward.",
                            },
                            {
                                "type": "command",
                                "label": "Switch, merge, and inspect history",
                                "command": "git switch main && git merge "
                                "feature/greeting && git log "
                                "--oneline --graph --all",
                            },
                            {
                                "type": "output",
                                "label": "Command output",
                                "text": "Switched to branch 'main'\n"
                                "Updating 4c1a9e2..71d3c9a\n"
                                "Fast-forward\n"
                                " src/app.py | 2 ++\n"
                                " 1 file changed, 2 insertions(+)\n"
                                "* 71d3c9a Add a friendly greeting\n"
                                "* 4c1a9e2 Initial project setup",
                            },
                            {
                                "type": "callout",
                                "tone": "tip",
                                "title": "Branch early",
                                "text": "Branches are cheap. Create one "
                                "before an experiment and `main` "
                                "stays a clean, known-good starting "
                                "point.",
                            },
                            {
                                "type": "checkpoint",
                                "title": "Your turn",
                                "text": "Run `git branch --show-current` and "
                                "`git status`. You should be back on "
                                "`main` with a clean working "
                                "tree.",
                            },
                        ],
                    }
                ],
            },
        ],
    }
]
