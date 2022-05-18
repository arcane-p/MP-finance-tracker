import pdfplumber
from assets.classes import MP
import regex  # had to use regex for unicode category support


def load_pdf(file):
    # most horrific regex i've ever seen, all just to allow for one (AND ONLY ONE) space between names. I'm sure I'll come back to this, 
    # but it runs surprisingly quickly
    mp_pattern = regex.compile(r'''(([\p{L}\-']{3,24}|[\p{L}\-']{3,24} [\p{L}\-']{3,24}), ([\p{L}\-]{3,15}|[\p{L}\-]{3,15} [\p{L}\-]{3,15}))(?=( \([\p{L} ,\-\(\)]+\)))''', regex.M)
    with pdfplumber.open(f"{file}.pdf") as pdf:
        queue_text = ""
        for i in pdf.pages:
            # Extract text & detect
            page_text = i.extract_text()
            detections = list(mp_pattern.finditer(page_text))

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

            if i == pdf.pages[-1]:  # last page
                break  # Finished! no need to continue or create more queues

            # from last mp to page end
            name = detections[len(detections)-1].group().split(",")
            queue_text = page_text[detections[len(detections)-1].end():len(page_text)]


def main():
    # url = input("URL: ")
    text = load_pdf("220503")
    print(text)


if __name__ == "__main__":
    main()
