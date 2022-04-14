import re

__author__ = "Jean Laroche"
__version = "1.0.0"

def run(args):
    with open(args.ofxFile) as f:
        data = f.read()

    # A very basic parsing, looking for STMTTRN
    allTrans = re.findall('(?s)<STMTTRN>(.*?)</STMTTRN>',data)

    # We now have the list of transactions
    oldIDs = []
    newIDS = []
    for trans in allTrans:
        # Parse transactions for all the standard fields.
        DTPOSTED = re.findall('(?s)<DTPOSTED>(.*?)[\n<]',trans)
        DTSTART = re.findall('(?s)<DTSTART>(.*?)[\n<]',trans)
        DTEND = re.findall('(?s)<DTEND>(.*?)[\n<]',trans)
        NAME = re.findall('(?s)<NAME>(.*?)[\n<]',trans)
        TRNTYPE = re.findall('(?s)<TRNTYPE>(.*?)[\n<]',trans)
        TRNAMT = re.findall('(?s)<TRNAMT>(.*?)[\n<]',trans)
        FITID = re.findall('(?s)<FITID>(.*?)[\n<]',trans)
        if not len(FITID):
            print(f"Found transaction with no FITID {DTPOSTED=} {NAME=} {TRNAMT=}")
            continue
        # Create a new FITID based on all the transaction info.
        NEWFITID = '-'.join(DTPOSTED+DTSTART+DTEND+NAME+TRNTYPE+TRNAMT)
        if NEWFITID in newIDS:
            print(f"Warning, the same ID will be assigned to two or more transactions {NEWFITID}")
        oldIDs.append(FITID[0])
        newIDS.append(NEWFITID)

    if not len(oldIDs):
        print("No transaction found")
        return

    # Do the replacements.
    for origID,newID in zip(oldIDs,newIDS):
        if args.verbose:
            print(f"Replacing {origID} with {newID}")
        data = data.replace(origID,newID)

    # Write OFX file back
    if args.outputOfxFile is None:
        outputOfxFile = args.ofxFile
        if not args.alwaysYes and input(f"About to overwrite {args.ofxFile}, proceed? -> [y/n]") != 'y':
            return
    else: outputOfxFile = args.outputOfxFile

    with open(outputOfxFile,'w') as f:
        f.write(data)
    print(f"Made {len(oldIDs)} replacements")


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser('fixid', description='Replace the FITID provided by a bank with a unique value derived from the transaction itself.')
    parser.add_argument('ofxFile', help='ofxFile to fix')
    parser.add_argument('-o', dest='outputOfxFile', help='Output ofx file, if not provided, modify in-place', default=None)
    parser.add_argument('-y', dest='alwaysYes', help='Overwrite with no confirmation',action='store_true')
    parser.add_argument('-v', dest='verbose', help='Be verbose',action='store_true')
    args = parser.parse_args()
    run(args)

