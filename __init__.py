# Copyright 2016 Eugene R. Miller
#
# Mycroft Jupiter Broadcasting skill is free software: you can redistribute
# it and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 2 of the License,
#  or (at your option) any later version.
#
# Mycroft Jupiter Broadcasting skill is distributed in the hope that it will
#  be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Mycroft Jupiter Broadcasting skill.
# If not, see <http://www.gnu.org/licenses/>.

from os.path import dirname, join, expanduser
from adapt.intent import IntentBuilder
from adapt.tools.text.tokenizer import EnglishTokenizer
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger

from feedcache import cache
from pprint import pprint

import subprocess
import shelve

__author__ = 'the7erm'

LOGGER = getLogger(__name__)

SHOWS = {
    "BSD Now!": {
        "alt": [
            "B.S.D. Now"
        ],
        "href": "http://www.jupiterbroadcasting.com/show/bsdnow/",
        "rss": {
            "HD Torrent RSS": ("http://bitlove.org/jupiterbroadcasting"
                               "/bsdnowhd/feed"),
            "HD Video RSS": "http://feeds.feedburner.com/BsdNowHd",
            "MP3 Audio RSS": "http://feeds.feedburner.com/BsdNowMp3",
            "Mobile Video RSS": "http://feeds.feedburner.com/BsdNowMobile",
            "OGG Audio RSS": "http://feeds.feedburner.com/BsdNowOgg"
        },
        "title": "BSD Now!"
    },
    "Beer is Tasty": {
        "href": "http://www.jupiterbroadcasting.com/show/beeristasty/"
    },
    "Coder Radio": {
        "rss": {
            "MP3 Audio RSS": "http://feeds.feedburner.com/coderradiomp3",
            "OGG Audio RSS": ("http://www.jupiterbroadcasting.com/feeds"
                              "/coderradioogg.xml"),
            "Video RSS": "http://feeds.feedburner.com/coderradiovideo",
            "iTunes MP3": ("http://itunes.apple.com/us/podcast"
                           "/coder-radio-mp3/id534941512"),
            "iTunes Video": ("http://itunes.apple.com/us/podcast"
                             "/coder-radio-video/id534941251")
        },
        "title": "Coder Radio"
    },
    "Computer Action Show": {
        "href": "http://www.jupiterbroadcasting.com/show/cas/"
    },
    "Cooder Radio": {
        "href": "http://www.jupiterbroadcasting.com/show/coderradio/"
    },
    "Fauxshow": {
        "alt": [
            "Faux show",
            "Foe Show"
        ],
        "href": "http://www.jupiterbroadcasting.com/show/fauxshow/",
        "rss": {
            "FauxShow HD RSS": "http://www.jupiterbroadcasting.com"
                               "/feeds/FauxShowHD.xml",
            "FauxShow MP3 RSS": "http://www.jupiterbroadcasting.com/feeds"
                                "/FauxShowMP3.xml",
            "FauxShow Mobile RSS": "http://www.jupiterbroadcasting.com"
                                   "/feeds/FauxShowMobile.xml",
            "FauxShow iTunes": "http://itunes.apple.com/us/podcast"
                               "/fauxshow-hd/id522616872"
        },
        "title": "Fauxshow"
    },
    "Howto Linux": {
        "alt": [
            "How to Linux"
        ],
        "href": "http://www.jupiterbroadcasting.com/show/h2l/",
        "rss": {
            "HD Torrent": "http://bitlove.org/jupiterbroadcasting/h2lhd/feed",
            "HD Video": "http://feeds.feedburner.com/HowtoLinuxHd",
            "mp3 Audio": "http://feeds.feedburner.com/HowToLinuxMp3",
            "ogg Audio": "http://feeds.feedburner.com/HowtoLinuxOgg"
        },
        "title": "Howto Linux"
    },
    "In Depth Look": {
        "href": "http://www.jupiterbroadcasting.com/show/indepthlook/",
        "title": "In Depth Look"
    },
    "Joint Failures": {
        "href": "http://www.jupiterbroadcasting.com/show/jointfailures/",
        "title": "Joint Failures"
    },
    "Jupiter Broadcasting": {
        "href": "http://jupiterbroadcasting.com/",
        "rss": {
            "Large Video RSS": "http://feeds2.feedburner.com"
                               "/AllJupiterVideos",
            "MP3 Audio RSS": "http://feeds2.feedburner.com"
                             "/JupiterBroadcasting",
            "OGG Audio RSS": "http://feeds2.feedburner.com"
                             "/AllJupiterBroadcastingShowsOgg",
            "iTunes Large Video": "http://itunes.apple.com/WebObjects"
                                  "/MZStore.woa/wa/viewPodcast?id=286971585",
            "iTunes MP3": "http://itunes.apple.com/WebObjects/MZStore.woa/wa"
                          "/viewPodcast?id=280019325"
        },
        "title": "Jupiter Broadcasting",
        "alt": ["J.B."],
    },
    "Jupiter@Nite": {
        "alt": [
            "jupiter at night",
            "jupiter at knight",
            "jupiter @ night"
        ],
        "href": "http://www.jupiterbroadcasting.com/show/nite/",
        "title": "Jupiter@Nite"
    },
    "Legend of the Stoned Owl": {
        "href": "http://www.jupiterbroadcasting.com/show"
                "/legend-of-the-stoned-owl/",
        "title": "Legend of the Stoned Owl"
    },
    "Linux Unplugged": {
        "href": "http://www.jupiterbroadcasting.com/show/linuxun/",
        "rss": {
            "MP3 Audio RSS": "http://feeds.feedburner.com/linuxunplugged",
            "Ogg Audio RSS": "http://feeds.feedburner.com/linuxunogg",
            "Torrent RSS": "http://bitlove.org/jupiterbroadcasting"
                           "/linuxunvid/feed",
            "Video RSS": "http://feeds.feedburner.com/linuxunvid",
            "WebM Torrent RSS": "http://bitlove.org/jupiterbroadcasting"
                                "/linuxunwebm/downloads.rss",
            "iTunes Audio": "https://itunes.apple.com/us/podcast"
                            "/linux-unplugged-podcast/id687598126"
        },
        "title": "Linux Unplugged"
    },
    "MMOrgue": {
        "alt": [
            "m.m. org"
        ],
        "href": "http://www.jupiterbroadcasting.com/show/mmorgue/",
        "title": "MMOrgue"
    },
    "Plan B": {
        "href": "http://www.jupiterbroadcasting.com/show/planb/",
        "rss": {
            "MP3 Audio RSS": "http://feeds.feedburner.com/planbmp3",
            "Ogg Audio RSS": "http://feeds.feedburner.com/planbogg",
            "Torrent RSS": "http://bitlove.org/jupiterbroadcasting"
                           "/planbvid/feed",
            "Video RSS": "http://feeds.feedburner.com/PlanBVideo",
            "iTunes Audio": "https://itunes.apple.com/us/podcast/plan-b"
                            "/id634760977"
        },
        "title": "Plan B"
    },
    "Podcast Networks": {
        "rss": {
            "Miro": "http://subscribe.getmiro.com/"
                    "?url1=http%3A//feeds2.feedburner.com/"
                    "JupiterBroadcastingVideos&trackback1="
                    "http%3A//www.miroguide.com/feeds/9506"
                    "/subscribe-hit&section1=video",
            "Stitcher": "http://landing.stitcher.com/?srcid=515",
            "Zune": ("http://social.zune.net/redirect?type=podcastseries"
                     "&id=66a6dec9-5ff2-45c6-99cd-0d74d4d02f5e&target=client"),
            "iTunes": ("http://itunes.apple.com/WebObjects/MZStore.woa/wa"
                       "/viewPodcast?id=286971585")
        },
        "title": "Podcast Networks"
    },
    "Rover Log": {
        "href": "http://www.jupiterbroadcasting.com/show/rover-log/"
    },
    "Sci Byte": {
        "alt": [
            "psy bite",
            "sci bite"
        ],
        "href": "http://www.jupiterbroadcasting.com/show/scibyte/"
    },
    "Scibyte": {
        "rss": {
            "HD Video RSS": "http://feeds.feedburner.com/scibytehd",
            "Large Video RSS": "http://feeds.feedburner.com/scibytelarge",
            "MP3 Audio RSS": "http://feeds.feedburner.com/scibyteaudio",
            "iPod Video RSS": "http://feeds.feedburner.com/scibytemobile"
        },
        "title": "Scibyte"
    },
    "Stoked": {
        "href": "http://www.jupiterbroadcasting.com/show/stoked/",
        "title": "Stoked"
    },
    "Tech Talk Today": {
        "href": "http://www.jupiterbroadcasting.com/show/today/",
        "rss": {
            "Ogg Audio": "http://feedpress.me/t3ogg",
            "Torrent": "http://bitlove.org/jupiterbroadcasting/t3mob/feed",
            "Video": "http://feedpress.me/t3mob",
            "iTunes mp3": ("https://itunes.apple.com/us/podcast"
                           "/tech-talk-today-mp3/id885658551"),
            "mp3 Audio": "http://feedpress.me/t3mp3"
        },
        "title": "Tech Talk Today"
    },
    "Techsnap": {
        "alt": [
            "tech snap",
            "tech snapped",
            "techsnap",
            "texas map",
            "text app",
            "text nap",
            "text now",
            "text snapped",
            "texts snapped",
        ],
        "rss": {
            "TechSNAP HD RSS": "http://feeds.feedburner.com/techsnaphd",
            "TechSNAP Large RSS": "http://feeds.feedburner.com/techsnaplarge",
            "TechSNAP MP3 RSS": "http://feeds.feedburner.com/techsnapmp3",
            "TechSNAP Mobile RSS": "http://feeds.feedburner.com"
                                   "/techsnapmobile",
            "TechSNAP OGG RSS": "http://feeds.feedburner.com/techsnapogg",
            "TechSNAP iTunes HD": "http://itunes.apple.com/us/podcast"
                                  "/techsnap-in-hd/id433058842",
            "TechSNAP iTunes Large": "http://itunes.apple.com/us/podcast"
                                     "/techsnap-large-video/id433058851",
            "TechSNAP iTunes MP3": "http://itunes.apple.com/us/podcast"
                                   "/techsnap-mp3/id433059024",
            "TechSNAP iTunes Mobile": "http://itunes.apple.com/us/podcast"
                                      "/techsnap-mobile-video/id433058959"
        },
        "title": "Techsnap",
        "href": "http://www.jupiterbroadcasting.com/show/techsnap/",

    },
    "The Linux Action Show!": {
        "href": "http://www.jupiterbroadcasting.com/show/linuxactionshow/",
        "rss": {
            "Large Video RSS": "http://feeds.feedburner.com"
                               "/computeractionshowvideo",
            "MP3 Audio RSS": "http://feeds2.feedburner.com"
                             "/TheLinuxActionShow",
            "Ogg Audio RSS": "http://feeds2.feedburner.com"
                             "/TheLinuxActionShowOGG",
            "iPod Video RSS": "http://feeds.feedburner.com"
                              "/linuxactionshowipodvid",
            "iTunes Large Video": "http://itunes.apple.com/WebObjects"
                                  "/MZStore.woa/wa/viewPodcast?id=337466330",
            "iTunes MP3": "http://itunes.apple.com/WebObjects/MZStore.woa"
                          "/wa/viewPodcast?id=160075139",
            "iTunes iPod Video": "http://itunes.apple.com/us/podcast"
                                 "/the-linux-action-show-ipod/id373583809"
        },
        "title": "The Linux Action Show!",
        "alt": ['linux action show', "las", "l.a.s.", "lass"]
    },
    "Torked": {
        "href:": "http://www.jupiterbroadcasting.com/show/torked/",
        "title": "Torked"
    },
    "Unfilter": {
        "href": "http://www.jupiterbroadcasting.com/show/unfilter/",
        "rss": {
            "HD Video RSS": "http://www.jupiterbroadcasting.com/feeds"
                            "/unfilterHD.xml",
            "MP3 Audio RSS": "http://www.jupiterbroadcasting.com/feeds"
                             "/unfilterMP3.xml",
            "Mobile Video RSS": "http://www.jupiterbroadcasting.com/feeds"
                                "/unfilterMob.xml",
            "OGG Audio RSS": "http://www.jupiterbroadcasting.com/feeds"
                             "/unfilterogg.xml",
            "unfilter on iTunes": "http://ax.search.itunes.apple.com"
                                  "/WebObjects/MZSearch.woa/wa"
                                  "/search?entity=podcast&media=all"
                                  "&page=1&restrict=true&startIndex=0"
                                  "&term=Unfilter"
        },
        "title": "Unfilter"
    },
    "Women's Tech Radio": {
        "href": "http://www.jupiterbroadcasting.com/show/wtr/"
    }
}


class JbSkill(MycroftSkill):

    def __init__(self):
        super(JbSkill, self).__init__(name="JbSkill")
        self.showmap = {}

    def initialize(self):
        self.load_data_files(dirname(__file__))
        self.load_regex_files(join(dirname(__file__), 'regex', self.lang))

        jb_live_intent = IntentBuilder("JbLiveIntent").\
            require("JbLiveKeyword").build()
        self.register_intent(jb_live_intent, self.handle_jb_live_intent)

        jb_live_am_intent = IntentBuilder("JbLiveAmIntent").\
            require("JbLiveAm").build()
        self.register_intent(jb_live_am_intent, self.handle_jb_live_am_intent)

        jb_live_fm_intent = IntentBuilder("JbLiveFmIntent").\
            require("JbLiveFm").build()
        self.register_intent(jb_live_fm_intent, self.handle_jb_live_fm_intent)

        tokenizer = EnglishTokenizer()
        self.tokenize_shows(tokenizer)

        listen_intent = IntentBuilder(
            "JbListenIntent").require("JbPlayKeyword").require(
                "LatestKeyword").require("Show").build()

        self.register_intent(listen_intent, self.handle_jb_listen_intent)

        latest_intent = IntentBuilder(
            "JbLatestIntent").require("LatestKeyword").require(
                "Show").build()

        self.register_intent(latest_intent, self.handle_jb_latest_intent)

        open_intent = IntentBuilder(
            "JbOpenIntent").require("OpenKeyword").require(
                "Show").build()

        self.register_intent(open_intent, self.handle_jb_open_intent)

    def get_latest_episode(self, url, media=False):
        storage_path = join(self.file_system.path, 'feedcache')
        LOGGER.debug("storage_path:%s" % storage_path)
        storage = shelve.open(storage_path)
        ttl = 60 * 60
        link = ""
        try:
            fc = cache.Cache(storage, timeToLiveSeconds=ttl)
            parsed_data = fc.fetch(url)
            print "parsed_data.feed.title:", parsed_data.feed.title
            for entry in parsed_data.entries:
                pprint(entry)
                if media:
                    media_content = entry.media_content
                    if media_content:
                        link = entry.media_content[0]['url']
                else:
                    link = entry.link
                if link:
                    break
        finally:
            storage.close()
        return link

    def tokenize_show(self, tokenizer, title, entry):
        tokenized_title = tokenizer.tokenize(title)[0]
        self.add_token(title, entry)

        if title != tokenized_title:
            self.add_token(title, entry)

    def add_token(self, token, entry):
        self.register_vocabulary(token, "Show")
        if token in self.showmap:
            self.showmap[token] += entry
        else:
            self.showmap[token] = entry

    def tokenize_shows(self, tokenizer):
        for title in SHOWS:
            show = SHOWS.get(title)

            if not show.get('title'):
                show['title'] = title

            entry = [show]
            self.tokenize_show(tokenizer, title, entry)
            alts = show.get("alt", [])

            for alt in alts:
                self.tokenize_show(tokenizer, alt, entry)

    def get_webpage_command(self):
        open_cmd = "xdg-open"
        if self.config:
            open_cmd = self.config.get("webpage_command", open_cmd)
        return open_cmd

    def get_media_command(self):
        open_cmd = "xdg-open"
        if self.config:
            open_cmd = self.config.get("media_command", open_cmd)
        return open_cmd

    def handle_jb_live_intent(self, message):
        data = {
            "stream": "J.B. Lyve t.v."
        }
        self.speak_dialog("opening", data)
        open_cmd = self.get_webpage_command()
        subprocess.check_output([open_cmd, "http://jblive.tv/"])

    def handle_jb_live_am_intent(self, message):
        data = {
            "stream": "J.B. Lyve a.m."
        }
        self.speak_dialog("opening", data)
        open_cmd = self.get_webpage_command()
        subprocess.check_output([open_cmd, "http://jblive.am/"])

    def handle_jb_live_fm_intent(self, message):
        data = {
            "stream": "J.B. Lyve f.m."
        }
        self.speak_dialog("opening", data)
        open_cmd = self.get_webpage_command()
        subprocess.check_output([open_cmd, "http://jblive.fm/"])

    def should_skip(self, title):
        if not title:
            return True
        skip = ['itunes', 'ipod', "torrent"]
        title_lower = title.lower()
        lower_title = title.lower()
        for s in skip:
            if s in lower_title:
                return True
        return False

    def iterate_shows_to_latest(self, message, media=False):
        show_name = message.metadata.get('Show')
        entries = self.showmap.get(show_name)
        LOGGER.debug("message:%s" % message)
        LOGGER.debug("latest entries:%s" % entries)

        if entries and len(entries) > 0:
            open_cmd = self.get_webpage_command()
            entry = entries[0]
            LOGGER.debug("entry:%s" % entry)
            data = {
                "stream": "latest %s episode" % entry.get("title", "")
            }
            self.speak_dialog("opening", data)
            href = entry.get("href")

            for title, rss_url in entry.get("rss", {}).items():
                # We don't want to parse itunes urls or torrent urls.
                if self.should_skip(title):
                    continue

                if rss_url:
                    episode_link = self.get_latest_episode(rss_url, media)
                    if episode_link:
                        href = episode_link
                        open_cmd = self.get_media_command()
                break

            subprocess.check_output([open_cmd, href])

    def handle_jb_latest_intent(self, message):
        self.iterate_shows_to_latest(message, False)

    def handle_jb_listen_intent(self, message):
        self.iterate_shows_to_latest(message, True)

    def handle_jb_open_intent(self, message):
        show_name = message.metadata.get('Show')
        entries = self.showmap.get(show_name)
        LOGGER.debug("message:%s" % message)

        if entries and len(entries) > 0:
            entry = entries[0]
            LOGGER.debug("entry:%s" % entry)
            data = {
                "stream": "%s website" % entry.get("title", "")
            }
            self.speak_dialog("opening", data)
            open_cmd = self.get_webpage_command()
            subprocess.check_output([open_cmd, entry.get("href")])

    def stop(self):
        pass


def create_skill():
    return JbSkill()
