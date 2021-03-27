from tqdm import tqdm


def read_file(file_in):
    new_ls = []
    try:
        with open(file_in) as f:
            lines = f.readlines()
            print("Reading file...")
            for l in tqdm(lines):
                _, label, _ = l.split(",")
                if label == "-1":
                    continue
                else:
                    new_ls.append(l)
    except Exception as e:
        print(e)

    return new_ls


def write_file(file_out, new_ls):
    with open(file_out, "w") as f:
        print("Writing file...")
        for item in tqdm(new_ls):
            f.write(item)


def run(file_in, file_out):
    new_ls = read_file(file_in)
    if new_ls:
        write_file(file_out, new_ls)

    # write file
    print("Finished preprocessing")
    print(f"Total items: {len(new_ls)}")


def main():
    file_in = "HSpam14_dataset.txt"
    file_out = "Pre_HSpam14_dataset.txt"
    run(file_in, file_out)


if __name__ == "__main__":
    main()