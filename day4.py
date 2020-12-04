from typing import List, Dict, Set, Callable

REQUIRED: Set[str] = {'byr',
'iyr',
'eyr',
'hgt',
'hcl',
'ecl',
'pid'}

OPTIONAL: Set[str] = {'cid'}


def data_reader(path: str) -> List[Dict[str, str]]:
    passports: List[Dict[str, str]] = []
    passport: Dict[str, str] = {}
    with open(path, 'r') as f:
        for line in f:
            if line == '\n':
                passports.append(passport)
                passport: Dict[str, str] = {}
            else:
                for key_val in line.strip().split():
                    key, val = key_val.split(':')
                    passport[key] = val
        passports.append(passport)
    return passports


passports: List[Dict[str, str]] = data_reader('data/day4_data')


def check_valid(passport: Dict[str, str]) -> bool:
    required_times = 0
    for key in passport.keys():
        if key in OPTIONAL:
            continue
        if key not in REQUIRED:
            return False
        else:
            required_times += 1
    if len(REQUIRED) == required_times:
        return True
    return False


def count_valid_passports(passports_input: List[Dict[str, str]]) -> int:
    valid_passports: int = 0
    for passport in passports_input:
        valid_passports += int(check_valid(passport))
    return valid_passports

# print(count_valid_passports(passports))
# assert count_valid_passports(passports) == 2
# print(count_valid_passports(passports))

# Part 2 #
DIGITS: str = '0123456789'

def check_all_digits(s: str) -> bool:
    return all(x in set(DIGITS) for x in s)


def is_valid_byr(byr: str) -> bool:
    if len(byr) != 4:
        return False
    if not check_all_digits(byr):
        return False
    if not ((int(byr) >= 1920) and (int(byr) <= 2002)):
        return False
    return True


def is_valid_iyr(iyr: str) -> bool:
    if len(iyr) != 4:
        return False
    if not check_all_digits(iyr):
        return False
    if not ((int(iyr) >= 2010) and (int(iyr) <= 2020)):
        return False
    return True


def is_valid_eyr(eyr: str) -> bool:
    if len(eyr) != 4:
        return False
    if not check_all_digits(eyr):
        return False
    if not ((int(eyr) >= 2020) and (int(eyr) <= 2030)):
        return False
    return True


def is_valid_hgt(hgt: str) -> bool:
    if not (hgt.endswith('cm') or hgt.endswith('in')):
        return False
    if not check_all_digits(hgt[:-2]):
        return False
    if hgt.endswith('cm'):
        if not ((int(hgt[:-2]) >= 150) and (int(hgt[:-2]) <= 193)):
            return False
    elif hgt.endswith('in'):
        if not ((int(hgt[:-2]) >= 59) and (int(hgt[:-2]) <= 76)):
            return False
    else:
        return False
    return True


def is_valid_hcl(hcl: str) -> bool:
    if len(hcl) != 7:
        return False
    if not hcl.startswith('#'):
        return False
    valid_set: Set[str] = set('abcdef0123456789')
    if not all(c in valid_set for c in hcl[1:]):
        return False
    return True


def is_valid_ecl(ecl: str) -> bool:
    valid_ecl: Set[str] = {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}
    if ecl not in valid_ecl:
        return False
    return True


def is_valid_pid(pid: str) -> bool:
    if len(pid) != 9:
        return False
    if not check_all_digits(pid):
        return False
    return True


validity_functions: Dict[str, Callable] = {'byr': is_valid_byr,
'iyr': is_valid_iyr,
'eyr': is_valid_eyr,
'hgt': is_valid_hgt,
'hcl': is_valid_hcl,
'ecl': is_valid_ecl,
'pid': is_valid_pid}


def check_fields(passport: Dict[str, str]) -> bool:
    for key, val in passport.items():
        if key in OPTIONAL:
            continue
        if not validity_functions[key](val):
            return False
    return True


def check_valid2(passport: Dict[str, str]) -> bool:
    if not check_valid(passport):
        return False
    if not check_fields(passport):
        return False
    return True


def count_valid_passports2(passports_input: List[Dict[str, str]]) -> int:
    valid_passports: int = 0
    for passport in passports_input:
        valid_passports += int(check_valid2(passport))
    return valid_passports


# for invalid
# assert count_valid_passports2(passports) == 0
# for valid
# assert count_valid_passports2(passports) == 4
print(count_valid_passports2(passports))
