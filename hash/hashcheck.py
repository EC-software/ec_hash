
import os

str_workdir = r"./"
str_workdir = r"C:\Users\22016\Martin\opg\HASH"
str_infile1 = "hash.txt"
str_infile2 = "re-hash.txt"

def read_hash_file(str_ffn):
    """ Read file
    Read a file in the format produced by: 7z.exe h -scrcCRC64
    :param str_ffn: Full file name
    :return: list of relevant lines from file
    """
    str_sep = "----------------"
    with open(str_ffn) as fil_in:
        lst_lines = fil_in.readlines()
    # Find the overall separators in the file
    lst_seperators = [n for n in range(len(lst_lines))
                      if lst_lines[n][:len(str_sep)] == str_sep
                      and len(set(lst_lines[n].strip()).symmetric_difference({'-', ' '})) == 0]
    # -- print(f"seprs: {lst_seperators}")
    # find the fixed-length segments of the lines
    str_samp_sep = lst_lines[lst_seperators[0]]
    num_fix1 = str_samp_sep.find(' ') + 1
    num_fix2 = str_samp_sep[num_fix1+1:].find(' ') + num_fix1 + 1
    # -- print(f"fixes: {num_fix1}, {num_fix2}")
    # build the list of tokens
    lst_hash_lines = lst_lines[lst_seperators[0]+1:lst_seperators[1]]  # for the relevant part of the file
    dic_ret = dict()  # Initialise the return object
    for lin in lst_hash_lines:
        t1 = lin[:num_fix1]
        t2 = lin[num_fix1:num_fix2].strip()
        t3 = lin[num_fix2:].strip()
        if t2 != '':  # it's not a directory
            if not t3 in dic_ret.keys():
                dic_ret[t3] = (t1.strip(), t2.strip())
            else:
                print(f"Same key repeated, this is not okay: {t3}")
    return dic_ret


def main(str_workdir, str_infile1, str_infile2):
    """

    :param str_workdir:
    :param str_infile1:
    :param str_infile2:
    :return:
    """
    dic_1 = read_hash_file(os.path.join(str_workdir, str_infile1))
    dic_2 = read_hash_file(os.path.join(str_workdir, str_infile2))
    for k1 in dic_1.keys():
        # -- print(f"l1: {k1}: {dic_1[k1]}")
        if k1 in dic_2.keys():
            # -- print(f"l2: {k1}: {dic_1[k1]}")
            tup1 = dic_1[k1]
            tup2 = dic_2[k1]
            if tup1[0] != tup2[0]:
                print(f"Files have different HASH ({tup1[0]} != {tup2[0]}) for {k1}")
            if tup1[1] != tup2[1]:
                print(f"Files have different size ({tup1[1]} != {tup2[1]}) for {k1}")
        else:
            print(f"File from hash-1 is missing in hash-2: {k1}")

if __name__ == "__main__":
    main(str_workdir, str_infile1, str_infile2)