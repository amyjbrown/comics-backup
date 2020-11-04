import os
import shutil

def atomicWrite(file: str, data, text: bool=True, overwrite: bool=True):
    """
    Closest one can get to an atomic write on windows
    write `data` to `file` atomically (e.g. using fsync) 
    uses a tmp_file "tmp_$file" for the atomic rewrite

    if `text` is true, then use 'wb' mode instead of 'w' mode
    if `overwrite` is false, then the temp file is kept around (using this for metadata)
    WILL CLOBER TMP_FILE IF IT ALREADY EXISTS!!!
    """
    temp_file = f"temp_{file}"
    with open(temp_file, "w+" if text else "wb+") as f:
        f.write()
        # ensure all data is on disk
        f.flush()
        os.fsync(f.fileno)

        os.replace(temp_file, file)
        # finally, delete tmp_file
        if overwrite:
            os.remove(temp_file)



if __name__ == "__main__":
    with open("example.txt", "w+") as f:
        f.write("whoop whoop fuck the police!\n")
    atomicWrite("example.txt", "[SUCCESS] i'm in yer file replacing ya\n")

    with open("example2.txt", "w+") as f: f.write("this is an examplefile\n")
    with open("temp_example2.txt", "w+") as f: f.write("this is an existing stub!!\n") 
    atomicWrite("example2.txt", "[SUCCESS] repleced existing stub and example2.txt\n")

    with open("temp_example3.txt", "w+") as f: f.write("stub with no other file to overwrite\n")
    atomicWrite("example3.txt", "[SUCCESS] checking to see if all's well\n")