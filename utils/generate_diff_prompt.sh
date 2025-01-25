#!/bin/bash

# Generate diff prompt script

PROMPT_FILE="utils/diff_prompt.txt"

cat << EOF > "$PROMPT_FILE"
I want you to summarize the following code changes. 
Please provide a clear, concise description of the modifications grouped by their functionality.
Focus on the purpose and implications of the changes rather than just listing line differences.

Include these sections:
1. Overview of changes
2. Specific modifications grouped by functionality
3. Any notable patterns or code quality considerations

Here are the code diffs:

$(git diff --color=never)
EOF

echo "Diff prompt generated at $PROMPT_FILE"