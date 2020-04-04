# distribute-impulse-responses

Recursively distribute IRs from a given directory to the bank/preset directories of the AMT Pangaea IR Convolution Player CP-100

## Examples

Connect device as USB drive.

### Build directory structure and exit

    python3 distribute_irs.py --build --drive dst

### Copy directory containing IRs to device

    python3 distribute_irs.py --collection src --drive dst

### Copy directory but keep banks 1, 4 and 8 untouched

    python3 distribute_irs.py --collection src --drive dst -skip 1 4 8
