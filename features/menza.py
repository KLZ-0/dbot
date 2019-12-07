import re
import datetime
import aiohttp
from bs4 import BeautifulSoup

all_regex = re.compile("\d*g|\d?\d\.\d?\d\.\d\d\d\d")
date_regex = re.compile("\d?\d\.\d?\d\.\d\d\d\d")
stripnumber_regex = re.compile("^\d\.\s")
stripnumber_regex_v2 = re.compile("^\d\.\s?\d+g")

"""
Download and parse the page into memory when:
    The bot starts
    The weekly fetch occurs
    The user request a fetch
"""

def normalizeDate(date):
    """Strips leading zeroes from dates and checks if their components are integers"""
    try:
        return ".".join([str(int(d)) for d in date.split(".")])
    except ValueError:
        return None

class Day:
    date = ""
    menu = []

    def __init__(self, date, menu=[]):
        self.date = date
        self.menu = []

    def dump(self, ret=False):
        """Object dump"""
        if ret:
            return str({self.date: self.menu})
        else:
            print(self.dump(True))

    def __str__(self):
        nl = "\n\t"
        return f"{self.date}{nl}{nl.join(self.menu)}"


class Menza:
    days = []
    timestamp = None

    def dump(self, ret=False):
        """Object dump"""
        if ret:
            return str([str(day) for day in self.days])
        else:
            print(self.dump(True))

    def __str__(self):
        return self.dump(ret=True)

    async def fetch(self):
        content = ""
        async with aiohttp.ClientSession() as session:
            async with session.get("http://www.kam.vutbr.cz/?p=tydn&provoz=10") as r:
                if r.status != 200:
                    return False

                content = await r.text()

        self.days = []
        content = content[content.find("týdenní"):]
        soup = BeautifulSoup(content, 'html.parser')

        for child in soup.findAll(string=all_regex):
            if date_regex.match(child):
                self.days.append(Day(str(child)))
                continue

            text = child.replace("\n", " ").replace("\xa0", " ").replace("\r", "")

            # Strip the beginning of lines starting with "n. meal" or "n.meal"
            # Who the fuck made that page, seriously?
            if stripnumber_regex.search(text):
                text = text[3:]
            elif stripnumber_regex_v2.search(text):
                text = text[2:]

            try:
                self.days[-1].menu.append(str(text))
            except IndexError:
                pass

        self.timestamp = datetime.datetime.today()
        return True

    def getByDate(self, date):
        """Returns the day corresponding to the date string argument"""
        for day in self.days:
            if day.date == date:
                return day
            elif normalizeDate(day.date) == normalizeDate(date) and normalizeDate(date):
                return day

        return None

    def get(self, date):
        """Returns the day corresponding to the argument"""
        try:
            return self.days[int(date)-1]
        except IndexError:
            return None
        except ValueError:
            return self.getByDate(date)

    def dumpDates(self):
        # TODO: move date normalization to parsing and generate an error message if a days date can't be normalized
        return [normalizeDate(d.date) for d in self.days]

    def listDates(self):
        nl = "\n\t"
        return f"Available days are:{nl}{nl.join(self.dumpDates())}"

    def isLoaded(self, date):
        return normalizeDate(date) in self.dumpDates()
