# mycroft-skill-jupiter-broadcasting
My 2nd attempt at creating a mycroft skill

This is a 3rd party skill that can either reside in `~/.mycroft/third_party_skills/` or `/opt/mycroft/third_party` .

# Intents
| Intent         | Example Keyphrase                                         | Function                                                    | Output                                                                                                            |
|----------------|-----------------------------------------------------------|-------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------|
| JbLiveIntent   | Mycroft, jblive.tv                                        | Opens jblive.tv in the default browser                      | Opening J.B. Live.tv                                                                                              |
| JbLiveAm       | Mycroft, jblive.am                                        | Opens jblive.am in the default browser                      | Opening J.B. Live.am                                                                                              |
| JbLiveFm       | Mycroft, jblive.fm                                        | Opens jblive.fm in the default browser                      | Opening J.B. Live.fm                                                                                              |
| JbLatestIntent | Mycroft, latest `show name` episode                       | Parses the appropriate rss feed and gets the first episode. | Opening latest `show name`url.                                                                     |
| JbListenIntent | Mycroft, listen to the latest `show name` episode         | Parses the appropriate rss feed and gets the first episode. | Opening latest `show name`                                                                      |

# Shows
| Show |
|------|
| BSD Now! |
| Beer is Tasty |
| Coder Radio |
| Computer Action Show |
| Fauxshow |
| Howto Linux |
| In Depth Look |
| Joint Failures |
| Jupiter Broadcasting |
| Jupiter@Nite |
| Legend of the Stoned Owl |
| Linux Unplugged |
| MMOrgue |
| Plan B |
| Podcast Networks |
| Rover Log |
| Scibyte |
| Stoked |
| Tech Talk Today |
| Techsnap |
| The Linux Action Show! |
| Torked |
| Unfilter |
| Women's Tech Radio |

## Install
```
mkdir -p ~/.mycroft/third_party_skills/
cd ~/.mycroft/third_party_skills/
git clone https://github.com/the7erm/mycroft-skill-jupiter-broadcasting.git jupiter_broadcasting
source ~/.virtualenvs/mycroft/bin/activate
# if that doesn't work try `source <path to virtualenv/bin/activate>`
pip install -r requirements.txt
# restart mycroft
./mycroft.sh restart
```

## Configuring `mycroft.ini`
By default the `JBSkill` uses `xdg-open` to open media & webpages.
Everyone has their favorite media player feel free to set it to `vlc` please
note `vlc --flag` will not work.  You'll need to write a wrapper script that
calls `vlc` with the command line arguments you'd like.

`mycroft.ini` can be changed in either `/etc/mycroft/mycroft.ini` for system wide configuration or `$HOME/.mycroft/mycroft.ini` for a specific user.

```ini
[JbSkill]
webpage_command = xdg-open
media_command = xdg-open
```

## feedcache
The JbSkill will only fetch a podcast once per hour.
`~/.mycroft/skills/JbSkill/feedcache` is the location of the cache file.


In the event that the device you want your media to play/view isn't the same box as you run mycroft on you'll want to read [ssh how to](https://github.com/the7erm/mycroft-skill-jupiter-broadcasting/blob/master/how-to/how-to-ssh.md).
