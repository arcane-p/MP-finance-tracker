import re

# chapters = {"Nil",
#             "Employment and Earnings",
#             ["(a) Support linked to an MP but received by a local party organisation or indirectly via a central party organisation",
#              "(b) Any other support not included in Category 2(a)"],
#             "Gifts, benefits and hospitality from UK sources",
#             "Visits outside the UK",
#             "Gifts and benefits from sources outside the UK",
#             "Land and property portfolio: (i) value over £100,000 and/or (ii) giving rental income of over £10,000 a year",
#             ["(i) Shareholdings: over 15% of issued share capital",
#              "(ii) Other shareholdings, valued at more than £70,000"],
#             "Miscellaneous",
#             "Family members employed and paid from parliamentary expenses",
#             "Family members engaged in lobbying the public sector on behalf of a third party or client"
# }


class MP:
    def __init__(self, firstname, lastname):
        self.firstname = firstname
        self.lastname = lastname
        print("MP Initialized: ", firstname, lastname)

    def load_raw(self, raw_text: str):
        print(f"Raw text for {self.firstname} recieved.")
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


class Company:
    pass
