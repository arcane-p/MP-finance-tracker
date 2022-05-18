import pdfplumber
from assets.classes import MP
import re


def load_pdf(file):
    # TODO regex catches "Asylum and Migration Policy Project Refugee", "care of Embassy of Ukraine Ukraine", "owned by Manor Mews Medway", \
    # "Christine Jardine Communications Trader", "Director of Eviivo Ltd notice", "from Analogue Electrics Ltd month", "Asylum and Migration Policy Refugee" \
    # "as a secretary Coffey", "via JJC Holdings Ltd AF". Possibly limit it to 3 words?
    mp_pattern = re.compile(r"([a-zA-Z]+?, [a-z A-Z]*?)(?=( \([a-z A-Z]*\)))", re.M)
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
