# FixFITID

A small python script to fix poorly defined FITID strings in ofx files.
Some banks are pretty bad at creating FITID strings that are unique for each transaction and remain the same no matter when/how often you download your data. This can cause problems with software like Gnucash for example, which expects the FITID to be unique to each transaction and to never change.
This tiny script replaces the bank-created FITID with one created based on the transaction data (date, amount, note etc). This ID is therefore constant for a transaction (as long as the note, amount, date do not change, which they shouldn't). It's also fairly unique, except in corner cases (consecutive identical transactions on the same day). 
