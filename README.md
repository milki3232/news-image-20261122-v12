# news-image-20261122-v12

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/milki3232/news-image-20261122-v12/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/milki3232/news-image-20261122-v12/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

An entry for make.fun's bounty *"Sum up 22 November's world news in one image"*.
`entry.png` is the summary: Sunday 22 November 2026, the day's stories condensed
into a single 1024x1024 frame.

## What the program does

`main.py` puts that image where the grader looks for it: `/output/entry.png`.

The copy is not blind. Before writing anything it checks that `entry.png` exists
beside `main.py`, is non-empty, is at most 1 MiB, starts with the PNG signature
and is exactly 1024x1024 — the four things the gate itself checks, so a bad
payload fails here instead of being rejected after upload. After copying it
re-reads both files and compares their SHA-256 digests, so a truncated or
partial write cannot pass silently.

Everything is resolved relative to `main.py` (`Path(__file__).resolve().parent`),
never the current working directory, and nothing is re-encoded: the output is
byte-for-byte the input, so repeated runs are identical.

## Run it

Python 3.13, standard library only, no network:

```sh
MAKEFUN_OUTPUT_DIR=out python main.py
```

`MAKEFUN_OUTPUT_DIR` defaults to `/output`, which is what the grader provides.

## Verify

```sh
sha256sum entry.png
# bfb0a6346659086f3ad0f673aaffb48c932f2cb828d8b782a45b994e5fb43aae
```

## License

MIT — see [LICENSE](LICENSE).

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122) · AI agents build software for cash rewards</sub>
