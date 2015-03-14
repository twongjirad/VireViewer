global mw


def show( mw ):
    f = open( 'bad_channel_list.txt', 'r' )
    l = f.readlines()
    h = []
    for line in l:
        h.append( (line.split()[1], int(line.split()[0])) )
    print h
    mw.vires.setWires( h )


if __name__ == "__main__":
    show( None )
