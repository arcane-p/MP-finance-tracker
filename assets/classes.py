import re
import logging

chapters = ["Nil",  # 0
            "Employment and earnings",  # 1
            "(a) Support linked to an MP", # SHORTENED TO AVOID PAGE SPLIT (but received by a local party organisation or indirectly via a central party organisation",)  # 2
            "(b) Any other support not included in Category 2(a)",  # 3 -> 2
            "Gifts, benefits and hospitality from UK sources",  # 4 -> 3
            "Visits outside the UK",  # 5 -> 4
            "Gifts and benefits from sources outside the UK",  # 6 -> 5
            "Land and property portfolio:",  # SHORTENED TO AVOID PAGE SPLIT ((i) value over £100,000 and/or (ii) giving rental income of over £10,000 a year",)  # 7 -> 6
            "(i) Shareholdings: over 15% of issued share capital",  # 8 -> 7
            "(ii) Other shareholdings, valued at more than £70,000",  # 9 -> 7
            "Miscellaneous",  # 10 -> 8
            "Family members employed and paid from parliamentary expenses",  # 11 -> 9
            "Family members engaged in lobbying the public sector"  # SHORTENED TO AVOID PAGE SPLIT on behalf of a third party or client",  # 12 -> 10
            ]

def parse_chapter(chapter_num: int, text: str):
    if chapter_num == 1:
        # recieved £... from ...
        # recieved a monthly allowance of £
        # payment of £... from ...
        # £800 (previously £600) a month for
        # payments from ...:
        # Fees for ...:
        # 	recieved £...
        # Employed as XXX for .... ... I will receive drawings of £500 a month
        # a monthly payment of £...
        # recieve £150 for each fortnightly column
        # look for £, then look for monthly, weekly, fortnightly, a year, yearly, a month, a week, a fortnight, a quarter. Find the first of these and run with that
        pass

class MP:
    def __init__(self, firstname, lastname):
        # validification
        self.firstname = firstname
        self.lastname = lastname
        logging.debug("MP Initialized: ", firstname, lastname)

    def load_raw(self, raw_text: str):
        print(f"Raw text for {self.firstname} recieved.")
        raw_text = raw_text.strip().splitlines()
        self.constituency = raw_text[0].replace("(", "").replace(")", "")
        del raw_text[0]
        print(raw_text)
        # print(self.constituency)
        section = None
        for line in raw_text:
            # remove page ending artifacts
            if line == " ":
                continue
            if len(line) == 1 and line.isnumeric():
                # print(f"Debug! Skipping {line}")
                continue
            for possible_match in chapters:
                if possible_match in line:
                    if chapters.index(possible_match) >= 9:
                        section = chapters.index(possible_match) - 2
                    elif chapters.index(possible_match) >= 3:
                        section = chapters.index(possible_match) - 1
                    else:
                        section = chapters.index(possible_match)
            else:
                if section is None:
                    print(f"ERROR: {line}")
            # section will already be set
            print(section, line)

        return
        # Check for NIL
        # 1. Employment and Earnings
        # 2. (a) Support linked to an MP but received by a local party organisation or indirectly via a central party organisation (b) Any other support not included in Category 2(a)
        # 3. Gifts, benefits and hospitality from UK sources
        # 4. Visits outside the UK
        # 5. Gifts and benefits from sources outside the UK
        # 6. Land and property portfolio: (i) value over £100,000 and/or (ii) giving rental income of over £10,000 a year
        # 7. (i) Shareholdings: over 15% of issued share capital (ii) Other shareholdings, valued at more than £70,000
        # 8. Miscellaneous
        # 9. Family members employed and paid from parliamentary expenses
        # 10. Family members engaged in lobbying the public sector on behalf of a third party or client
        if "Nil" in raw_text:
            final_results = None
        pattern = re.compile(r"([1-9]|10)\. (E|G|V|L|M|F|\(i\)|\(a\)|\(ii\)|\(b\))((.|\n)*?)(?=([1-9]|10)\. (E|G|V|L|M|F|\(i\)|\(a\)|\(ii\)|\(b\)))", re.M)
        result = pattern.findall(raw_text)
        final_results = []
        for i in result:
            final_results.append("".join(i))
        print(final_results)

# Now make him load it into a dataframe
