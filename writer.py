import os
import shutil

def atomicWrite(file: str, data, text: bool=True):
    """
    Closest one can get to an atomic write on windows
    write `data` to `file` atomically (e.g. using fsync) 
    uses a tmp_file "tmp_$file" for the atomic rewrite

    if `text` is true, then use 'wb' mode instead of 'w' mode
    WILL CLOBER TMP_FILE IF IT ALREADY EXISTS!!!
    """
    temp_file = f"temp_{file}"
    with open(temp_file, "w+" if text else "wb+") as f:
        f.write(data)
        # ensure all data is on disk
        f.flush()
        os.fsync(f.fileno())

    # replace real file with temp file now that it's been closed
    os.replace(temp_file, file)



if __name__ == "__main__":
    with open("example.txt", "w+") as f:
        f.write("[FAILURE]Example 1 text\n")
    atomicWrite("example.txt", 
        "[SUCCESS] Example 1 Text successfuly rewritten\n"
        )

    with open("example2.txt", "w+") as f: f.write("[FAILURE]Example 2 text\n")
    with open("temp_example2.txt", "w+") as f: 
        f.write("[tempfile]This is the pre-made example 2 tempfile\n")
    atomicWrite("example2.txt", 
        "[SUCCESS] repleced existing stub and example2.txt\n"
        )

    with open("temp_example3.txt", "w+") as f: 
        f.write("[tempfile] Example 3 tempfile with no existing main file\n")
    atomicWrite("example3.txt", 
        "[SUCCESS] checking to see if all's well\n"
        )