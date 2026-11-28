# Storage Provider Candidates (from Konode's list)

**Research date:** 2026-11-28
**Status:** desk research; no experiment has run. No provider is approved beyond the owner's agreed minimum.
**Prepared with:** Claude Code, tier O (research only); not yet reviewed by the owner.
**Owner direction (2026-11-28):** Google Drive and GitHub are the accepted minimum. Self-hosted storage always stays available.

Evidence labels follow `RULES.md` §6: **[Official]**, **[Community]**, **[Inference]**, **[Untested]**. Konode was studied only through its user documentation and roadmap, not its code (`CLEAN_ROOM.md`). Several provider help pages were seen only through search extracts.

## 1. What Konode supports

| Status in Konode | Services |
|---|---|
| Shipped | Google Drive (`drive.file`), GitHub (fine-grained token, one private repository), WebDAV with presets for Nextcloud/ownCloud, pCloud (EU or US), Koofr, Fastmail and Nutstore; generic WebDAV for Synology, kDrive and others |
| Built for its next version | Dropbox (app folder, OAuth with PKCE), Gitea and Forgejo (through its GitHub backend with a configurable API address) |
| Requested or planned | OneDrive (Graph), S3-compatible storage and Backblaze B2, GitHub Gist |
| Parked or rejected | MEGA (needs MEGA's own crypto SDK; parked), Filen (its SDK is AGPLv3; blocked on licensing), iCloud (no public API or WebDAV; the only third-party "WebDAV" routes relay files through someone else's server), Syncthing (a browser extension can't reach a local folder) |

**Important difference:** Konode is a browser extension, so it cannot use local folders or operating-system file providers. PSC is embedded in native apps, so it can. That adds two routes Konode doesn't have:
- **a user-selected folder,** which covers Syncthing, Nextcloud's desktop client, Synology Drive, Dropbox and OneDrive desktop apps, and similar tools;
- **iCloud through Apple's own container APIs** on Apple devices (`PROVIDER_AUTHORIZATION.md` §9).

## 2. What "sufficient" means for PSC

Derived from `DECISIONS.md`, `RULES.md` §5 and the Commonplace sync review:

| # | Requirement | Why |
|---|---|---|
| R1 | Works from native Android, iOS, Windows and macOS apps without the user running extra software | Phone → cloud → PC |
| R2 | Least-privilege sign-in suitable for native apps (OAuth with PKCE, scoped tokens or app passwords; never the main account password) | Security; `RULES.md` §7 |
| R3 | Files stay user-visible and readable (Markdown, images, JSON) | Portability; Commonplace's plain-file model |
| R4 | Efficient change detection (change feed, cursor, or folder version tags) | No wasteful polling; quotas |
| R5 | Conditional writes ("only if unchanged": ETag/If-Match, revision or SHA) | Never overwrite a newer edit (`RULES.md` §5) |
| R6 | Handles image-sized files (tens of MB) | Commonplace images |
| R7 | Rate limits comfortable for a few devices per person | Opportunistic sync without hitting ceilings |
| R8 | Terms and SDK licenses compatible with a possibly paid Commonplace | `CLEAN_ROOM.md` |
| R9 | No PSC-operated server or third-party relay in the path | `PRINCIPLES.md` §8 |

## 3. Assessment

| Service | Route | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| **Google Drive** | API, `drive.file` | ✓ | ✓ OAuth PKCE | Partly: only app-created files are visible to the app | ✓ change feed | Partly: revisions exist; conditional-update semantics untested | ✓ | ✓ | ✓ | **Minimum.** Blocked on experiments E1/E2 for sharing across apps and platforms |
| **GitHub** | API, GitHub App or fine-grained token | ✓ | ✓ | ✓ | ✓ commits | ✓ SHA required on update [Official] | ✓ up to 100 MB [Official] | ✓ 5,000 requests/hour [Official] | ✓ | **Minimum.** Caveats: deletions stay in history; images grow the repository |
| **Dropbox** | API, app folder | ✓ | ✓ OAuth PKCE [Official] | ✓ | ✓ cursor [Official] | ✓ `rev` [Official] | ✓ upload sessions [Official] | Untested | Check terms | **Strong next candidate.** Plan production approval before 50 linked users [Official] |
| **OneDrive** | API, app folder | ✓ | ✓ OAuth PKCE [Official] | ✓ visible `/Apps/{name}` [Official] | ✓ delta [Official] | ✓ eTag/If-Match [Official] | Caution: app folder not intended for large files [Official] | Throttling with Retry-After [Official] | Check terms | **Strong next candidate.** Common among Windows users |
| **Nextcloud / ownCloud** | WebDAV | ✓ | ✓ app passwords [Official] | ✓ | Probably via folder ETags; RFC 6578 sync-collection for files not confirmed [Untested] | ✓ If-Match, 412 on mismatch [Official/Community] | ✓ (chunked upload for large files) | Server-dependent | ✓ | **Best self-hosted option.** The reference WebDAV target |
| **Synology** | WebDAV Server package, or a folder via Synology Drive | ✓ | User account or app-specific credentials [Untested] | ✓ | Untested | Untested | ✓ | Home server | ✓ | **Self-host via generic WebDAV or the folder route.** Needs a capability probe |
| **Koofr** | WebDAV | ✓ | ✓ app-specific password required [Official] | ✓ | Untested | Untested | Untested | Not published | Check terms | **Acceptable WebDAV preset** if the probe passes. EU-hosted |
| **pCloud** | WebDAV (EU or US host) | ✓ | ✗ main account password; no separate WebDAV password [Community] | ✓ | Untested | Untested | Untested | Not published | Check terms | **Weak:** violates R2 until app passwords exist |
| **kDrive (Infomaniak)** | WebDAV | ✓ | ✓ app password when 2FA is on [Official] | ✓ | Untested | Untested | Untested | Not published | Check terms | **Acceptable** for paid kDrive plans only (WebDAV requires a paid plan [Official]) |
| **Fastmail Files** | WebDAV | ✓ | App passwords likely [Untested] | ✓ | Untested | Untested | Plan quota [Official] | Daily transfer limits per plan [Community] | Check terms | **Niche:** only for existing Fastmail users |
| **Nutstore (坚果云)** | WebDAV | ✓ | App password [Community] | ✓ | Untested | Untested | Untested | ✗ tight: about 600 requests per 30 minutes on free accounts, per Konode | Check terms | **Only if friends in mainland China need it** (Google Drive is unreachable there, per Konode) |
| **Gitea / Forgejo** | API, like GitHub | ✓ | ✓ scoped tokens, can be limited to specific repositories [Official] | ✓ | ✓ commits | ✓ SHA required on update [Official; older Forgejo versions did not enforce it on one endpoint] | Server-dependent | Server-dependent | ✓ | **Self-hosted Git:** a cheap extension of the GitHub adapter |
| **S3-compatible / B2** | Object storage API | ✓ | Access keys: powerful and hard for non-technical users [Inference] | Not a folder users browse easily | No change feed; list and compare [Inference] | AWS S3 supports If-Match and If-None-Match since 2024 [Official]; other S3-compatible services untested | ✓ | ✓ | ✓ | **Later, for technical self-hosters** (for example MinIO or RustFS) |
| **iCloud** | Apple container APIs (Apple devices only) | Apple only | ✓ system account | ✓ if exposed as a visible folder [Untested] | ✓ system-managed | System file coordination | ✓ | ✓ | ✓ | **Apple-only add-on,** not a phone-to-PC route for Android |
| **User-selected folder** | OS file access | ✓ | n/a | ✓ | Weak: scans and watchers | Weak: depends on the sync tool | ✓ | n/a | ✓ | **Always available** (self-hosting guarantee). Quality depends on the tool syncing the folder |
| **GitHub Gist** | API | ✓ | ✓ | Secret gists are unlisted, not private [Konode] | — | — | Small | ✓ | ✓ | **Not suitable** for personal notes |
| **MEGA** | Own SDK | ✓ | Email and password (master-key material) [Konode] | Encrypted; not readable elsewhere | — | No in-place overwrite [Konode] | ✓ | — | Check the SDK license | **Not suitable now** |
| **Filen** | Own SDK | ✓ | — | Encrypted | — | — | — | — | ✗ AGPLv3 SDK [Konode] | **Not suitable** with a possibly paid Commonplace |

## 4. Conclusions

1. **The minimum is enough to start.** Google Drive and GitHub between them cover non-technical users (Drive) and users who want plain files with history (GitHub). Both have least-privilege, native-friendly sign-in. Google's shared-workspace question (E1/E2) is the only blocker.
2. **The self-hosting guarantee is met** by the user-selected folder (always) plus WebDAV, with Nextcloud as the reference server. Gitea and Forgejo come almost free once the GitHub adapter exists.
3. **Best next providers:** Dropbox and OneDrive. Both offer app folders, OAuth with PKCE, change cursors and conditional writes, and both fit the family-registration decision.
4. **WebDAV presets are cheap but uneven.** Each server needs a capability probe (conditional writes, change detection, limits) before it gets a preset. pCloud fails the sign-in requirement today, and Nutstore's rate limit makes it a special case.
5. **Not suitable now:** Gist, MEGA and Filen. Filen is excluded specifically because its AGPL SDK conflicts with a possibly paid Commonplace.
6. **Commercial terms are unchecked for every provider.** Before release, review each provider's developer terms for a paid app (R8).

## 5. Suggested provider order

**Update 2026-11-28:** the owner limited the first release to Google Drive, GitHub and self-hosted (WebDAV and the folder). The rows below after "Self-hosting" are deferred. See [Architecture](../ARCHITECTURE.md) §11 for certainty and [Implementation plan](../IMPLEMENTATION_PLAN.md) for the steps.

| Stage | Providers |
|---|---|
| Minimum (agreed) | Google Drive, GitHub, user-selected folder |
| Self-hosting | WebDAV with Nextcloud as reference; Gitea and Forgejo with the GitHub adapter |
| Next managed providers | Dropbox, OneDrive |
| Apple add-on | iCloud containers on Apple devices |
| WebDAV presets after probing | Koofr, kDrive, Synology, Fastmail; Nutstore only if needed |
| Later | S3-compatible storage for technical self-hosters |
| Not planned | Gist, MEGA, Filen; pCloud until it offers app passwords |

## 6. To verify

- A WebDAV capability probe: conditional PUT (If-Match → 412), folder ETag propagation, RFC 6578 support, ETag stability across renames, and behaviour on 429/503. Run it against Nextcloud, Synology and Koofr first.
- Whether Nextcloud's files endpoint supports RFC 6578 sync-collection.
- Conditional-write support on S3-compatible services other than AWS.
- Developer terms for commercial use: Google, GitHub, Dropbox, Microsoft and each WebDAV service.
- Current rate limits for Koofr, pCloud, kDrive and Fastmail (none were published in the sources found).

## Sources

Konode (user documentation and roadmap only):
- [Konode README](https://github.com/konabe-studio/konode/blob/main/README.md), [Roadmap](https://github.com/konabe-studio/konode/blob/main/ROADMAP.md), [Compatibility](https://github.com/konabe-studio/konode/blob/main/COMPATIBILITY.md)

Providers (via search extracts; official unless marked):
- [Nextcloud: WebDAV basic APIs](https://docs.nextcloud.com/server/stable/developer_manual/client_apis/WebDAV/basic.html)
- [pCloud: WebDAV access](https://help.pcloud.com/article/webdav); [Zotero forum: WebDAV services](https://forums.zotero.org/discussion/comment/417454) (community)
- [Koofr: WebDAV help](https://app.koofr.net/help/webdav) and [connecting through WebDAV](https://koofr.eu/help/koofr_with_webdav/how-do-i-connect-a-service-to-koofr-through-webdav/)
- [Infomaniak: Connecting to kDrive via WebDAV](https://www.infomaniak.com/en/support/faq/2409/connecting-to-kdrive-via-webdav)
- [Fastmail: About file storage](https://www.fastmail.help/hc/en-us/articles/1500000280121); [DEVONthink forum on Fastmail WebDAV limits](https://discourse.devontechnologies.com/t/extremely-slow-webdav-sync-on-ipad-while-fine-on-iphone/70928) (community)
- [Remotely Save: Nutstore WebDAV notes](https://gitea.astro-vps.duckdns.org/bruno/remotely-save/raw/branch/master/docs/remote_services/webdav_jianguoyun/README.md) (community)
- [AWS: S3 conditional writes](https://docs.aws.amazon.com/AmazonS3/latest/userguide/conditional-writes.html) and [If-Match announcement](https://aws.amazon.com/about-aws/whats-new/2024/11/amazon-s3-functionality-conditional-writes)
- [Forgejo: Access token scope](https://forgejo.org/docs/next/user/authentication/token-scope/); [Codeberg Git content API](https://apis.io/apis/codeberg/codeberg-git-content-api/) (third-party listing)
- [RFC 4918: WebDAV](https://www.rfc-editor.org/rfc/rfc4918)
- Google Drive, GitHub, Dropbox and Microsoft sources: see [Provider authorization](PROVIDER_AUTHORIZATION.md#sources)
