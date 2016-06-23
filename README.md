# mycroft-skill-jupiter-broadcasting
My 2nd attempt at creating a mycroft skill

This is a 3rd party skill that can either reside in `~/.mycroft/third_party_skills/` or `/opt/mycroft/third_party` .


# Intents
| Intent         | Example Keyphrase                                         | Function                                                    | Output                                                                                                            |
|----------------|-----------------------------------------------------------|-------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------|
| JbLiveIntent   | Mycroft, jblive.tv                                        | Opens jblive.tv in the default browser                      | Opening J.B. Live.tv                                                                                              |
| JbLiveAm       | Mycroft, jblive.am                                        | Opens jblive.am in the default browser                      | Opening J.B. Live.am                                                                                              |
| JbLiveFm       | Mycroft, jblive.fm                                        | Opens jblive.fm in the default browser                      | Opening J.B. Live.fm                                                                                              |
| JbLatestIntent | Mycroft, latest `show name` episode                       | Parses the appropriate rss feed and gets the first episode. | Opening latest `show name` episode media url.                                                                     |
| JbListenIntent | Mycroft, listen to the latest `show name` episode         | Parses the appropriate rss feed and gets the first episode. | Opening latest `show name` page.                                                                     |

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
# restart the skills service
```

