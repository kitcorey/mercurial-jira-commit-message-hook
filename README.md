Mercurial hook for jira
==================================

A Mercurial hook that checks if commit messages contain JIRA keys.

The expected JIRA project is based on the name of the repository, and is configured in `~/.config/jirakeycheck.json`
See example_jirakeycheck.json for an example

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

3. Copy example_jirakeycheck.json to ~/.config/jirakeycheck.json
4. Set your JIRA projects and repo names in ~/.config/jirakeycheck.json

Configuration
-------------
This plugin is configuring by defining "projects" in
~/.config/jirakeycheck.json.

"projects" should be a dictionary that maps JIRA board names to a list of
regular expressions.  During a commit, the commit hook tries to match each of
the regular expressions in order.  If there is a match, then the script
verifies that a JIRA issue id for the associated board is included in the
commit message.

See example_jirakeycheck.json for an example.
