import regex
import logging

chapters = ["Nil",  # 0
            "Employment and earnings",  # 1
            "(a) Support linked to an MP",  # SHORTENED TO AVOID PAGE SPLIT (but received by a local party organisation or indirectly via a central party organisation",)  # 2
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
    # logging.debug(f"Section {chapter_num}")
    # if chapter_num == 0:  # Nil
    # if chapter_num == 1:  # Employment & Earnings
    # json = chapter_1(text)
    # # recieved £... from ...
    # # recieved a monthly allowance of £
    # # payment of £... from ...
    # # £800 (previously £600) a month for
    # # payments from ...:
    # # Fees for ...:
    # # 	recieved £...
    # # Employed as XXX for .... ... I will receive drawings of £500 a month
    # # a monthly payment of £...
    # # recieve £150 for each fortnightly column
    # # look for £, then look for monthly, weekly, fortnightly, a year, yearly, a month, a week, a fortnight, a quarter. Find the first of these and run with that
    # pass
    if chapter_num == 4:  # Visits outside the UK
        last_char = 0
        results = []
        for i in regex.finditer(r"\(Registered \d\d \w+ \d\d\d\d\)", text):
            item = text[last_char:i.end()]
            last_char = int(i.end())

            # Estimated value
            value_text = item[item.find("Estimate of the probable value (or amount of any donation):")+59:item.find("Destination of visit:")].strip().lower()  # saves memory and processing from having to continually search
            if "total" in value_text:
                # Total price. Take last number found (number between total and end of line)
                estimate_value = float(regex.search(r"total [\p{L} ]*(£[\d,.]+)", value_text).group(1).replace("£", "").replace(",", ""))
            else:
                # sum all pound signs together
                estimate_value = 0
                for i in regex.findall(r"£[\d,.]+", value_text):
                    estimate_value += float(i.replace("£", "").replace(",", ""))

            results.append(
                {
                    "Name of donor":    item[item.find("Name of donor:")+14:item.find("Address of donor:")].strip(),
                    "Address of donor": item[item.find("Address of donor:")+17:item.find("Estimate of the probable value (or amount of any donation):")].strip(),
                    "Estimated value": estimate_value,
                    "Destination of visit": item[item.find("Destination of visit:")+21:item.find("Dates of visit:")].strip(),
                    "Dates of visit":   item[item.find("Dates of visit:")+15:item.find("Purpose of visit:")].strip(),
                    "Purpose of visit": item[item.find("Purpose of visit:")+17:i.start()].strip(),
                    "Date registered":  item[i.start():i.end()].strip()
                }
            )
        # when all is said and done
        return "Visits outside the UK", results
    else:
        return f"Chapter {chapter_num} (Not yet coded)", "TBD"


class MP:
    def __init__(self, firstname, lastname):
        # validification
        self.firstname = firstname
        self.lastname = lastname
        self.data = dict()
        logging.debug("MP Initialized: ", firstname, lastname)

    def export_data(self):
        # eventually self.data will be exported in the json format shown in format.json. For now however...
        print(f"{self.firstname} {self.lastname} {self.constituency}:")
        print(self.data)
        pass

    def load_raw(self, raw_text: str):
        logging.debug(f"Raw text for {self.firstname} recieved.")
        raw_text = raw_text.strip().splitlines()
        self.constituency = raw_text[0].replace("(", "").replace(")", "").strip()
        del raw_text[0]
        # print(raw_text)
        # print(self.constituency)
        section = last_section = None
        buffer = ""
        for line in raw_text:
            if line == " " or line.isnumeric():  # remove page ending artifacts
                continue

            # Set section var
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

            # section now set
            if section != last_section:  # section has changed
                # print("Parsing chapter")
                if last_section is not None:
                    chapter_name, chapter_results = parse_chapter(last_section, buffer)
                    self.data[chapter_name] = chapter_results
                buffer = ""  # clear buffer
                last_section = section  # update last_section
            else:
                # print("adding to buffer")
                buffer += line

        # Funnily enough, once the last line has been parsed we still need to send the buffer off!
        chapter_name, chapter_results = parse_chapter(last_section, buffer)
        self.data[chapter_name] = chapter_results
        # Runs when MP is finished parsing. Means that we can export
        self.export_data()  # !!!! TODO

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
        pattern = regex.compile(r"([1-9]|10)\. (E|G|V|L|M|F|\(i\)|\(a\)|\(ii\)|\(b\))((.|\n)*?)(?=([1-9]|10)\. (E|G|V|L|M|F|\(i\)|\(a\)|\(ii\)|\(b\)))", regex.M)
        result = pattern.findall(raw_text)
        final_results = []
        for i in result:
            final_results.append("".join(i))
        print(final_results)

# Now make him load it into a dataframe
