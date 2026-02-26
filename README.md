# NeriPing
A tool for getting notifications from Nerimity with ntfy.

## Note
This tool is very basic. It uses a polling technique that may be inaccurate, and you have to manually input the server/DM channel IDs you want to watch. Once Nerimity's API is more solidified, I might be able to make things more automatic.

## Usage

### As a container (Docker/Podman)
The most optimal way to use the script is with Docker/Podman.

Copy example-compose.yml to a folder and rename it to compose.yml. You'll also need to copy example-config.yml to a folder in that folder called config and rename the file to config.yml.

The folder structure should look like this:
```
[root]
| compose.yml
|-config
  | config.yml
```

### Standalone
The script itself (`neriping.py`) can be run on its own. You'll have to install dependencies using pip and possibly a virtual environment.

The config file will go in `[your home folder]/.littlebitstudios/neriping`.

## Configuration

Here's the structure of the config file.

```yaml
ntfy-base-url: https://ntfy.sh # ntfy.sh is the public instance, you can use your own
ntfy-topic: CHANGE_THIS # use a random ID, or something specific to this use

neri-usr-token: "EXAMPLE_25f976ee-593e-404d-a0c6-b3742801d9cf" # Your Nerimity user token (see README to know where to find this)

your-uid: 1741936300505874432 # copy your UID from your profile page under the 3-dot menu
# the script will ignore messages from this UID and raise the priority of messages containing it

watched-channels:
  - id: 1289157729608441857 # Right click a channel and "Copy ID" to get this number
    title: "Nerimity #General" # Notifications will say "Someone in {title}"

```

### Getting your User Token

This script needs a User Token to function. You can get this from your browser's DevTools (usually found by pressing F12 or Ctrl/Cmd+Shift+I).

In Firefox: Open the DevTools and go to the Storage tab. Look under `Local Storage / https://nerimity.com` and look for the userToken variable. Copy this and paste it as `neri-usr-token` in the configuration.

In Chromium forks (Chrome, Brave, Edge, Opera, Vivaldi...): Open the DevTools and go to the "Application" tab. Look under "Local storage" then "https://nerimity.com" and look for the userToken variable. Copy this and paste it as `neri-usr-token` in the configuration.

**DANGER**: KEEP YOUR USER TOKEN SECRET! Anyone with your User Token can impersonate you!

## Credits/License

Nerimity is open-source software released under the GNU GPLv3. See Nerimity's projects in their [GitHub organization](https://github.com/Nerimity). This project uses Nerimity's API to gather messages.

ntfy is open-source software licensed under the Apache 2.0 and GPLv2 licenses. See their repository: [binwiederhier/ntfy](https://github.com/binwiederhier/ntfy). This project uses ntfy's API to send notifications.

This project is released under the MIT license. See the LICENSE file.