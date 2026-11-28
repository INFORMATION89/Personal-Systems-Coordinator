# How Others Sync Notes with GitHub (Obsidian and Konode)

**Research date:** 2026-11-28
**Status:** desk research for the GitHub route, the first online route in the first viable product (`DECISIONS.md`, D5).
**Prepared with:** Claude Code, tier O (research only); not yet reviewed by the owner.
**Method:** user documentation, READMEs, changelogs and plugin listings only; no source code was read (`CLEAN_ROOM.md`). Licenses noted because they decide what may be learned from and how.

## 1. The two approaches

| Approach | Who | How it works | Result |
|---|---|---|---|
| **Real Git on the device** | Obsidian Git (community plugin, MIT) | Desktop runs the installed `git` program; mobile uses isomorphic-git, a JavaScript re-implementation, because native Git can't run inside Obsidian on Android or iOS [Plugin docs] | Works well on desktop for people who know Git. The author calls mobile "**very unstable**": crashes on clone or pull, memory limits on repository size, no SSH, no rebase. Conflicts are Git merge conflicts with `<<<<<<<` markers inside notes [Plugin docs] |
| **GitHub's web API, no Git on the device** | GitHub Gitless Sync (Obsidian community plugin, **AGPLv3**), several similar plugins, and Konode (MPL-2.0) | Files are read and written through GitHub's REST API with a fine-grained token limited to one repository and Contents read/write [READMEs] | The same logic on desktop and mobile. No Git features locally (no branches or merges). GitHub only |

**PSC's design already uses the second approach** (`ARCHITECTURE.md` §6–§7). The Obsidian Git experience confirms it: putting a Git engine on phones is fragile, and Git's conflict markers are not for average users.

## 2. What each project's documentation teaches

### GitHub Gitless Sync (Obsidian plugin; AGPLv3, so documentation only)
- **No `git` needed;** desktop and mobile share identical logic, through GitHub's REST API.
- **A sync metadata file** in the vault, updated on every sync. Because of it, the author says the plugin must not be combined with other sync tools or with commits made outside the plugin, or data may be lost.
- **The first sync only works if one side is empty.** If both the repository and the vault have files, it fails.
- **Conflicts** open a diff view (split on desktop, unified on mobile), or can be set to always prefer the remote or the local side.
- **Fine-grained token,** Contents read/write, limited to the sync repository.

### Other REST-API Obsidian plugins (listings only)
- Some upload through the **Git Data API in batches** (blobs, tree, commit) instead of one commit per file.
- Some use a **three-way merge with a common baseline**, and flag overlapping edits, binary conflicts and delete-versus-edit conflicts without writing markers into notes.
- Several warn against running two sync tools on the same vault.
- One listing states a **30 MB per-file limit** through the API. That differs from the 100 MB contents-API limit in GitHub's changelog, so it is unverified (A4 tests it).

### Konode (MPL-2.0; user docs, roadmap and changelog only)
- **Fine-grained token, one private repository, Contents read/write.** Public repositories are refused. It writes into its own folder on a branch the user chooses.
- **Per-device files** (one file per data type per device) in its folder, so devices rarely write the same file.
- **SHA-256 integrity** of every payload, verified after download.
- **Pull on a schedule,** because GitHub can't notify devices of changes.
- **Lessons from its changelog and roadmap:**
  - **Stale reads caused conflicts:** responses served from a cache made updates fail with HTTP 409; fixed by disabling caching for those requests.
  - **Idle syncs re-committed** unchanged data; fixed by uploading only when content changed.
  - **Setting up an empty repository** could half-finish silently: the first commit wasn't checked, a token without write access failed without a clear message, and that first commit always went to `main` regardless of the chosen branch.
  - **Branch typos passed the connection test,** then failed later; the branch must be checked during connection.
  - Gitea and Forgejo reuse the same code with a configurable API address, because their contents API mirrors GitHub's.
- Konode orders device payloads by timestamp and uses last-write-wins as a baseline. **PSC does not**: PSC never decides by clock time (`ARCHITECTURE.md` §5.1).

### Obsidian Git (MIT; documentation)
- Conflict resolution keeps "ours", "theirs" or "both" inside the note, then requires marking files resolved and committing. This is a power-user workflow.
- It recommends other apps for mobile Git sync.

## 3. What PSC takes from this

| Lesson | PSC design response |
|---|---|
| A Git engine on phones is fragile | Use GitHub's REST API only; no Git engine in PSC (already decided) |
| Stale cached responses cause false conflicts | Send no-cache headers on every read that feeds a conditional write; treat a 409 as "re-read and re-classify", never as an overwrite |
| Idle syncs must not create commits | Commit only when the cycle has changes; one commit per cycle |
| Empty repositories and branches break setup | At connection: check the repository is private, the token can write, and the branch exists; bootstrap an empty repository with a verified first commit on the chosen branch |
| First sync with both sides non-empty | PSC handles it: an empty base means identical files simply match and different ones become conflict copies, so nothing is refused and nothing is lost. Add a fixture |
| A private metadata file makes outside edits dangerous | PSC's base state lives on the device, and its shared metadata is per-device files in `PSC/`. Commits made outside PSC are simply remote changes; no hidden file must stay in step |
| Multiple sync tools on one folder lose data | The integration guide tells apps and users to use only one sync tool per folder; PSC reports unexpected changes as external edits, not errors |
| Conflict views are what users understand | PSC keeps conflict copies (never markers in notes); Commonplace can show a diff view on top |
| Per-file size limits through the API are unclear (30 MB versus 100 MB) | A4 tests uploads of 10, 30 and 60 MB; the PSC default cap is set from the result |

## 4. Additions to experiment A4

A4 (`IMPLEMENTATION_PLAN.md`) now also checks:
1. Bootstrapping an **empty repository** on a non-`main` branch, and the error when the token lacks write access.
2. Whether reads used for conditional writes need **no-cache headers** to avoid stale 409 responses.
3. Upload limits at **10, 30 and 60 MB** through the Git Data API.
4. Change detection by **comparing commits,** and its limit on how many changed files it reports; tree comparison as the fallback.
5. **One commit per cycle:** create blobs, a tree on top of the base tree, a commit, and a branch update that fails if the branch moved.

## Sources

- [Obsidian Git: README](https://github.com/Vinzent03/obsidian-git) and [documentation](https://publish.obsidian.md/git-doc) (MIT; docs read: Getting Started, Conflict resolution, Features, Authentication, Common issues)
- [GitHub Gitless Sync: README](https://github.com/silvanocerza/github-gitless-sync) and [plugin listing](https://community.obsidian.md/plugins/github-gitless-sync) (AGPLv3; README only)
- Obsidian community listings: [Vault Sync REST](https://community.obsidian.md/plugins/vault-sync-rest), [Octosync](https://community.obsidian.md/plugins/octosync), [GitHub Sync - Zev](https://community.obsidian.md/plugins/github-sync-zev), [Ray Vault Sync](https://community.obsidian.md/plugins/ray-vault-sync), [Simple Git Sync](https://community.obsidian.md/plugins/simple-git-sync)
- [Konode README](https://github.com/konabe-studio/konode/blob/main/README.md), [Getting started](https://github.com/konabe-studio/konode/blob/main/GETTING_STARTED.md), [Roadmap](https://github.com/konabe-studio/konode/blob/main/ROADMAP.md), [Changelog](https://github.com/konabe-studio/konode/blob/main/CHANGELOG.md) (MPL-2.0; documentation only)
- [GitHub changelog: 100 MB contents limit](https://github.blog/changelog/2022-05-03-increased-file-size-limit-when-retrieving-file-contents-via-rest-api)
