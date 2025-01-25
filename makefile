.PHONY: diff-prompt

diff-prompt:
	@echo "Generating diff prompt..."
	@bash utils/generate_diff_prompt.sh
	@echo "Done. Review diff_prompt.txt and provide it to the AI"