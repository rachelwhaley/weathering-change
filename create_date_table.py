# datetime.py   
# Creates a csv 
daypermonth = [31,29,31,30,31,30,31,31,30,31,30,31]
hours = [7,8,9,10,11,12,13,14,15,16,17,18,19]
for m in range(1,12):
    for d in range(1,daypermonth[m]):
        for h in hours:
            print ('D{0:02d}{1:02d}{2:d},{0:d}/{1:d}/2021 {2:d}:00'.format(m, d, h))
