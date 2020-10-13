---
inject: true
to: skupper-didact.md
after: Prerequisites
---
<% cmd = '<%= cmd %>' %>

[Check if the <%= cmd %> command line is available](didact://?commandId=vscode.didact.cliCommandSuccessful&text=<%= cmd %>-requirements-status$$<%= cmd %> "Tests to see if `<%= cmd %>` returns a result"){.didact}

*Status: unknown*{#<%= cmd %>-requirements-status}
