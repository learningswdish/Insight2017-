## Using Python 3.6

Libraries: os   sys


## Repo directory structure

The directory structure for your repo should look like this:

    ├── README.md 
    ├── run.sh
    ├── src
    │   └── find_political_donors.py
    ├── input
    │   └── itcont.txt
    ├── output
    |   └── medianvals_by_zip.txt
    |   └── medianvals_by_date.txt
    ├── insight_testsuite
        └── run_tests.sh
        └── results.txt
        └── tests
        |    └── test_1
        |        ├── input
        |        │   └── itcont.txt
        |        |__ output
        |        │   └── medianvals_by_zip.txt
        |        |   └── medianvals_by_date.txt
        |        |── src
        |            └── find_political_donors.py
        |── temp
                 ├── input
                 │   └── your-own-input.txt
                 |── output
                 |   └── medianvals_by_zip.txt
                 |   └── medianvals_by_date.txt
                 |── src
                     └── find_political_donors.py


## Overview
The overall algorithm is simple.
1. process with the original records, filter out invalid records such as reocrd with non-empty OTHER_ID
2. use the processed records and filter in a more precise way, checking TRANSACTION_DT and ZIP_CODE field
3. build a hashmap, use string(CMTE_ID+ZIP_CODE/TRANSACTION_DT) as key, value is the sorted list of TRANSACTION_AMT in ascending order.For medianvals_by_zip, for each reocrd we insert the TRANSACTION_AMT into the list and get the middle element(s) of the list. For medianvals_by_date, after processing all records, we get the middle element(s) of the list
4. write the results to output files 





