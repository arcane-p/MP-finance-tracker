# MP-Finance-Tracker
## Info

UK's MP's are given a basic annual salary paid by the government, to the tune of £84k yearly. For some, this is enough. For others, this is apparently not. MPs who earn additional money must report it, and this is published monthly.

It interested me to figure out which MPs undertake lucrative secondary jobs, and just how much they're getting paid. Additionally to reporting income, various other things are reported - such as gifts, hospitality, visits, shareholdings (above £70k), and family members lobbying or being paid by the public sector.

Thus, this program aims to scrape and then quantize these monthly reports. The data will then be able to be displayed in a variety of ways.

### Roadmap
 - [x] Scrape information from PDF reliably
 - [ ] Detect MPs successfully
	 - This has been done mostly but still has false negatives. I'll need to re-address - maybe using a master list of all MPs found elsewhere.
 - [ ] Clean and quantize data received
 - [ ] Export
 - [ ] Display
 - [ ] Make it a recursive standalone script so that it can execute each month automatically

## Usage
### Installation

    pip install -r "requirements.txt"
    (you'll also have to download the PDF yourself at (https://www.parliament.uk/mps-lords-and-offices/standards-and-financial-interests/parliamentary-commissioner-for-standards/registers-of-interests/register-of-members-financial-interests/)
    python3 main.py
