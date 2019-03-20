from math import sqrt


def _confidence(ups, downs):
    n = ups + downs
    if n == 0:
        return 0
    z = 1.6  # 1.0 = 85%, 1.6 = 95%
    phat = float(ups) / n
    return (phat + z * z / (2 * n) - z * sqrt((phat * (1 - phat) + z * z / (4 * n)) / n)) / (1 + z * z / n)


def confidence(ups, downs):
    if ups + downs == 0:
        return 0
    else:
        return _confidence(ups, downs)


def ppt(bed, doctors, inpatient, day):
    bed_inday = bed * day
    count_inpatient = inpatient * day

    a = bed_inday // doctors
    b = count_inpatient // doctors
    result = confidence(a, b)

    return result*100


if __name__ == "__main__":
    result1 = ppt(1200, 200, 4000, 7)
    result2 = ppt(3000, 100, 4000, 7)
    print(result1)
    print(result2)
