from pass_keeper import PassKeeper

def main():
    p = str(input("Type db password: "))
    keeper = PassKeeper('db')
    keeper.db_test(p)


if __name__ == '__main__':
    main()