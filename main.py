import pdfplumber
from assets.classes import MP
import regex  # regex over re for unicode support
import logging
# import tempfile
import progressbar
progressbar.streams.wrap_stderr()
logging.basicConfig()

# import pandas as pd
# data = pd.read_csv("https://www.theyworkforyou.com/mps/?f=csv")
# #clean data
# data = data.drop("Person ID", axis=1).drop("Party", axis=1).drop("URI", axis=1)
# data["Full name"] = data["Last name"] + ", " + data["First name"]
# constituencies = data["Constituency"].tolist()


def load_pdf(file):
    # Convoluted regex, which despite appearences runs quickly and accurately
    mp_pattern = regex.compile(r'''(([\p{L}\-']{3,24}|[\p{L}\-']{2,24} [\p{L}\-']{2,24}), ([\p{L}\-]{2,15}|[\p{L}\-]{2,15} [\p{L}\ -]{1,25}))(?=( \(\p{Lu}[\p{L} ,\-]+\)))''', regex.M)
    with pdfplumber.open(f"{file}.pdf") as pdf:
        queue_text = ""
        total_mps = 0  # temp
        for i in progressbar.progressbar(pdf.pages):
            # Extract text & detect
            page_text = i.extract_text()
            detections = list(mp_pattern.finditer(page_text))

            # QUEUE SECTION
            # This skips the page if there is a full page with no detections
            if len(detections) == 0:  # On a full page
                queue_text += page_text  # Add top to bottom of page to queue
                continue  # go to next page w/ added queue

            # if there are detections on the page:
            elif i != pdf.pages[0]:
                queue_text += page_text[0:detections[0].start()]  # add page top to previous_mp's queue
                mp = MP(firstname=name[1].strip(), lastname=name[0].strip())  # noqa: F821, name will always be set by previous iteration when page != 1
                mp.load_raw(queue_text)  # load previous_mp

            # all but last MP
            for i in range(0, len(detections)-1):
                name = detections[i].group().split(",")
                mp = MP(firstname=name[1].strip(), lastname=name[0].strip())
                mp.load_raw(page_text[detections[i].end():detections[i+1].start()])
                total_mps += 1

            if i == pdf.pages[-1]:  # last page
                break  # Finished! no need to continue or create more queues

            # from last mp to page end
            name = detections[len(detections)-1].group().split(",")
            queue_text = page_text[detections[len(detections)-1].end():len(page_text)]

            # TEMPORARY
            if total_mps > 0:
                quit()


# def checker(line):
#     results = [ele in line for ele in constituencies]
#     return any(results)
#     print(line, ",", constituencies[results.index(True)])


# def main():
#     # Convert PDF to Text
#     with tempfile.TemporaryFile(mode="w+", encoding="utf-8") as outfile:
#         with pdfplumber.open(f'{input("PDF filename: ")}.pdf') as infile:
#             for page in progressbar.progressbar(infile.pages):
#                 outfile.write(page.extract_text())
#         outfile.seek(0)

#         with open("temp_text.txt", "w", encoding="utf-8") as f:
#             f.write(outfile.read())

#         # print("start")
#         # for line in outfile:
#         #     if checker(line) is True:
#         #         print(line, end="")
#         # print("end")
#     exit()
#     text = load_pdf("220503")
#     print(text)


if __name__ == "__main__":
    load_pdf("220503")
