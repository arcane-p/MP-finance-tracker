import pdfplumber
from assets.classes import MP
import regex  # regex over re for unicode support
import logging

def load_pdf(file):
    # most horrific regex i've ever seen, all just to allow for one (AND ONLY ONE) space between names. I'm sure I'll come back to this,
    # but it runs surprisingly quickly
    # TODO: REGEX IS SKIPPING LIKE 100 MPS :((
    mp_pattern = regex.compile(r'''(^([\p{L}\-']{3,24}|[\p{L}\-']{3,24} [\p{L}\-']{3,24}), ([\p{L}\-]{3,15}|[\p{L}\-]{2,15} [\p{L}\-]{3,15}))(?=( \([\p{L} ,\-\(\)]+\)))''', regex.M)
    with pdfplumber.open(f"{file}.pdf") as pdf:
        queue_text = ""
        I = 0 ## TEMPORARY
        total_mps = 0  # temp
        for i in pdf.pages:
            # Extract text & detect
            page_text = i.extract_text()
            detections = list(mp_pattern.finditer(page_text))

            # Validification
            # sometimes, despite my best efforts, 'fake' MPs get detected. As much as i've hyper-refined the regex, potential detections\
            # in the future are always possible. Thus, this quickly checks if there are any suspicious MPs and removes the detection. This
            # also has to come before all the logic instead of being validated when initializing MPs as to not mess with logic (which relies
            # on the number of detections to determine if on a full page, etc)
            for match in detections:
                name = match.group().split(",")
                if name[0].strip()[0].islower() or name[1].strip()[0].islower() or "Inc" in name[1].strip() or "Inc." in name[1].strip():
                    detections.remove(match)
                    print(f"Removed {name}!")

            # QUEUE SECTION
            if len(detections) == 0:  # On a full page
                queue_text += page_text  # Add top to bottom of page to queue
                continue  # go to next page w/ added queue
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

            ## TEMPORARY
            I += 1
        # print("Total MPs:", total_mps)
            #if I > 3:
            quit()


def main():
    # url = input("URL: ")
    text = load_pdf("220503")
    print(text)


if __name__ == "__main__":
    main()
