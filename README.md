# Toasty Deployer Odoo Companion

An Odoo module that mirrors [Toasty Deployer](https://github.com/All-Things-Toasty-Software-Ltd/toasty-deployer)'s build
history into Odoo, so deployment status, commit SHAs, exit codes, and full terminal logs are all browsable next to the
rest of the business's data, with GitHub owner/repo profile info (avatars, bios, descriptions) mirrored in alongside it.

---

## Features

- **Automatic Deployment Sync:** A cron job polls the Toasty Deployer REST API every 5 minutes, discovering owners,
  repositories, and runs, and creating or updating the matching Odoo records.
- **GitHub Profile Mirroring:** Owner and repository records are enriched from the public GitHub API. Avatar image, bio,
  GitHub URL for owners; description and GitHub URL for repositories, all synced automatically the first time each is
  discovered.
- **Live Status at a Glance:** Repositories show their most recent run's status as a coloured badge
  (success/failure/running) directly on the list and form views, computed from their latest deployment run.
- **Terminal-Style Log Viewer:** A custom OWL widget on the Repository form lists every run for that repo with an
  expandable, monospaced log panel. No need to open each run individually to check what happened.
- **Manual Sync on Demand:** Two wizard actions. **GitHub Sync** and **Toasty Deployer Sync**, let you trigger either
  sync immediately from the UI instead of waiting for the next cron tick.
- **Configurable Server URL:** The Toasty Deployer instance's base URL is a standard Odoo setting under **Settings →
  Toasty Deployer**, not hardcoded.

---

## Installation & Deployment

### 1. Requirements

- An Odoo installation with the **Base** and **Web** apps (no other Toasty Software modules are required. This is a
  standalone companion)
- The `requests` Python package available to Odoo's environment (used for both the Toasty Deployer and GitHub API calls)
- A running [Toasty Deployer](https://github.com/All-Things-Toasty-Software-Ltd/toasty-deployer) instance to sync from

### 2. Install as a Custom Addon

```
git clone https://github.com/All-Things-Toasty-Software-Ltd/toasty-deployer-odoo-companion.git /path/to/odoo/addons/toasty-deployer-odoo-companion
```

Restart Odoo so it picks up the new addons path, then update the apps list, remove the "Apps" filter, search for
**Toasty Deployer**, and click **Activate**.

### 3. Configure the Server URL

Go to **Settings → Toasty Deployer** and set the **Toasty Deployer Server URL** to your instance (defaults to
`https://deploy.toastysoftware.co.uk`).

### 4. Run an Initial Sync

The scheduled cron (`Toasty Deployer: Sync Deployments`) runs every 5 minutes automatically, but you can trigger both
syncs immediately the first time:

- **Toasty Deployer → Configuration → Sync → GitHub Sync** - pulls avatar/bio/description data for every owner and repo
  already known to Odoo
- **Toasty Deployer → Configuration → Sync → Toasty Deployer Sync** - discovers owners/repos/runs from the Toasty
  Deployer API and creates the matching records (new owners/repos are automatically GitHub-synced the moment they're
  first discovered)

---

## Licensing & Copyright

Copyright © All Things Toasty Software Ltd. All rights reserved.

Licensed under
the [LGPLv3](https://github.com/All-Things-Toasty-Software-Ltd/toasty-deployer-odoo-companion/blob/main/LICENSE)
License.