from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

required = [
    "id:'builtin-tdg-middle-school'",
    "id:'builtin-tdg-high-school'",
    "id:'builtin-tdg-university'",
    "id:'builtin-tdg-world-champion'",
]
missing = [course_id for course_id in required if course_id not in s]
if missing:
    raise SystemExit(f"Required TDG school courses are missing from index.html: {missing}")

# The course definitions and the correct persistent order now live directly in
# index.html. Do not rewrite a stale save-order expression during deployment.
print('All four TDG school courses are installed; course order is handled by index.html.')
