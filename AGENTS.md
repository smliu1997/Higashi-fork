# AGENTS.md

## Formatting rules

- Keep at least one trailing newline at end of file.
- Do not normalize files to a single trailing newline.
- If a file already ends with multiple trailing newlines, preserve that unless explicitly instructed otherwise.

## Communication rules

- Replies should be concise, efficient, and direct.
- Prefer short, high-signal answers over long explanations.
- Avoid unnecessary background unless the user asks for it.
- When giving options or next steps, keep them brief and actionable.

## SLURM supervision rules

- If the user asks Codex to submit a job and supervise it, supervise for at most 5 minutes by default.
- Start the 5-minute timer immediately after `sbatch`, not when the job starts running.
- Use real wall-clock waits between checks.
- Concretely: record the time right after `sbatch`, repeatedly check the job output, compute remaining supervision time before each wait, and sleep for `min(30 seconds, time remaining)` so polls occur at most every 30 seconds and total supervision never exceeds the requested wall-clock duration.
- If an error appears in the output file, report it immediately.
- After 5 minutes, stop supervising even if the job is still pending or running.

## Code review rules

- When the user asks to "check code" or requests a review, also evaluate whether code documentation, including docstrings and comments starting with `#`, is clear, correct, and consistent with the implementation.
- Prioritize avoiding confusion and misleading names/comments over polishing wording.
- Flag docstrings or `#` comments that are outdated, ambiguous, incomplete, or contradicted by the code.
- Point out variable names that are materially misleading, especially when they obscure data semantics, shape conventions, units, or control flow.
