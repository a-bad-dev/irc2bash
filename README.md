# irc2bash
A bridge between an IRC channel and the bash interpreter.
Ensure you run this in a sandboxed VM unless you want random people messing with your PC remotely.
This also works with sh, zsh, csh, and (probably) fish.

# Installing
## Linux
Clone the repository.
`git clone --depth=1 https://github.com/a-bad-dev/irc2bash.git`
`cd irc2bash/`

Set up the config file (`skel_config.py`) with the editor of your choice.
The important settings are:
`realname`: Set this to the real name of your bot, use `rce` if unsure.
`nickname`: Set this to the nickname of your bot, this is the name you probably want to change. Use `rce-bot` or something similar if unsure.
`channels`: Sdd channels to this list for your bot to join.
`ip`: Set this to the IP or domain name of the IRC server
`port`: Set this to the port of the IRC server. Use `6667` if unsure.
`ssl`: Enable this to use SSL. Set to `False` if unsure.
`command_prefix`: The prefix used before commands sent to the bash interpreter. Set this to `$` if unsure.
`bot_prefix`: The prefix used before commands that control the bot itself. Set this to `#` if unsure.
`opper_nicknames`: List of nicknames allowed to control the bot. Set this to your own nick if unsure.

Rename the config file so the script can detect it.
`mv skel_config.py config.py`

Run the bot.
`python3 main.py`
or
`chmod +x main.py`
`./main.py`

A systemd service is included if you want the bot to start on boot. For non-systemd systems, use a cron job running at reboot or something similar.

## Windows
go get a real OS
