Mercurial hook for jira
==================================

A Mercurial hook that checks if commit messages contain JIRA keys.

The expected JIRA project is based on the name of the repository, and is configured in `~/.config/jirakeycheck.yaml`
See example_jirakeycheck.yaml for an example

Installation
------------
1. Copy `jirakeycheck.py` and `commitwrapper.py` to ~/.hg (or any dir you like)
2. Add the following lines to $HOME/.hgrc:

    ```
    [extensions]
       # wrapper so that only manual commits will use the manualpre(txn)commit hooks
       manualcommithook = ~/.hg/commitwrapper.py
    [hooks]
       #check all manual outgoing commits
       manualpretxncommit = python:~/.hg/jirakeycheck.py:checkCommitMessage
    ```

3. Copy example_jirakeycheck.yaml to ~/.config/jirakeycheck.yaml
4. Set your JIRA projects and repo names in ~/.config/jirakeycheck.yaml
