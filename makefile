decks:
	poetry run python utils/anki-generators/decks.py
	git add public/decks/*

diff:
	@echo "Generating diff prompt..."
	@bash utils/generate_diff_prompt.sh
	@echo "Done. Review diff_prompt.txt and provide it to the AI"