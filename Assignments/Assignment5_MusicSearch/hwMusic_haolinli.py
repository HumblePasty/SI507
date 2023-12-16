import csv
import timeit

rows = 296
cols = 3


def initialize():
    music = [[0 for i in range(cols)] for j in range(rows)]
    return music


def readFile(music, file):
    with open(file, 'r', encoding="latin") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            music[reader.line_num - 1] = row
            music[reader.line_num - 1][1] = int(music[reader.line_num - 1][1])
            music[reader.line_num - 1][2] = int(music[reader.line_num - 1][2])
    return music


def printMusic(music):
    for i in range(rows):
        print(music[i])


def biSearchArtist(music, key):
    low = 0
    high = len(music) - 1
    while low <= high:
        mid = (low + high) // 2
        if music[mid][0] == key:
            print(f"{key} is found at row number {mid}")
            return mid
        elif music[mid][0] > key:
            high = mid - 1
        else:
            low = mid + 1
    return -1


def seqSearchArtist(music, key):
    for i in range(len(music)):
        if music[i][0] == key:
            print(f"{key} is found at row number {i}")
            return i
    return -1


def timeBiSearchArtist():
    music = initialize()
    music = readFile(music, 'music.csv')
    start = timeit.default_timer()
    for i in range(100000):
        biSearchArtist(music, 'Usher')
    stop = timeit.default_timer()
    return stop - start


def timeSeqSearchArtist():
    music = initialize()
    music = readFile(music, 'music.csv')
    start = timeit.default_timer()
    for i in range(100000):
        seqSearchArtist(music, 'Usher')
    stop = timeit.default_timer()
    return stop - start


def bubbleSortArtist(music):
    for i in range(len(music) - 1):
        for j in range(len(music) - 1 - i):
            if music[j][1] < music[j + 1][1]:
                music[j], music[j + 1] = music[j + 1], music[j]
    print("Sorted by artist name: ")


def altSortArtist(music):
    """
    Sorts music by artist name using quick sort.

    Parameters
    ----------
    music:
        The music list to be sorted.

    Returns
    -------
    None
    """
    low = 0
    high = len(music) - 1

    def partition(music, low, high):
        pivot = music[high][1]
        i = low - 1  # i keeps track of the index of the last element that is greater than or equal to the pivot
        for j in range(low, high):
            if music[j][1] >= pivot:
                i += 1
                music[i], music[j] = music[j], music[i]
        music[i + 1], music[high] = music[high], music[i + 1]
        return i + 1

    def quickArtist(music, low, high):
        if low < high:
            pi = partition(music, low, high)
            quickArtist(music, low, pi - 1)
            quickArtist(music, pi + 1, high)

    quickArtist(music, low, high)


def timeBubbleSortArtist():
    music = initialize()
    music = readFile(music, 'music.csv')
    start = timeit.default_timer()
    for i in range(1000):
        bubbleSortArtist(music)
    stop = timeit.default_timer()
    printMusic(music)
    return stop - start


def timeAltSortArtist():
    music = initialize()
    music = readFile(music, 'music.csv')
    start = timeit.default_timer()
    for i in range(1000):
        altSortArtist(music)
    stop = timeit.default_timer()
    printMusic(music)
    return stop - start


def inSortTracks(music):
    # Insertion sort by tracks
    for i in range(1, len(music)):
        current = music[i]
        j = i - 1
        while j >= 0 and current[2] > music[j][2]:
            music[j + 1] = music[j]
            j -= 1
        music[j + 1] = current


def altSortTracks(music):
    """
    Sorts music by tracks using merge sort.

    Parameters
    ----------
    music:
        The music list to be sorted.
    """

    def merge(music, l, m, r):
        n1 = m - l + 1
        n2 = r - m

        # create temp arrays
        L = [0] * (n1)
        R = [0] * (n2)

        # Copy data to temp arrays L[] and R[]
        for i in range(0, n1):
            L[i] = music[l + i]

        for j in range(0, n2):
            R[j] = music[m + 1 + j]

        # Merge the temp arrays back into arr[l..r]
        i = 0
        j = 0
        k = l

        while i < n1 and j < n2:
            if L[i][2] >= R[j][2]:
                music[k] = L[i]
                i += 1
            else:
                music[k] = R[j]
                j += 1
            k += 1

        # Copy the remaining elements of L[], if there are any
        while i < n1:
            music[k] = L[i]
            i += 1
            k += 1

        # Copy the remaining elements of R[], if there are any
        while j < n2:
            music[k] = R[j]
            j += 1
            k += 1

    def mergeSort(music, l, r):
        if l < r:
            m = (l + (r - 1)) // 2
            mergeSort(music, l, m)
            mergeSort(music, m + 1, r)
            merge(music, l, m, r)

    mergeSort(music, 0, len(music) - 1)


def timeInSortTracks():
    music = initialize()
    music = readFile(music, 'music.csv')
    start = timeit.default_timer()
    for i in range(1000):
        inSortTracks(music)
    stop = timeit.default_timer()
    printMusic(music)
    return stop - start


def timeAltSortTracks():
    music = initialize()
    music = readFile(music, 'music.csv')
    start = timeit.default_timer()
    for i in range(1000):
        altSortTracks(music)
    stop = timeit.default_timer()
    printMusic(music)
    return stop - start


def main():
    # read the file
    music = initialize()
    music = readFile(music, 'music.csv')
    printMusic(music)

    # search for an artist
    print(f"BiSearchArtist: {timeBiSearchArtist()}")
    print(f"SeqSearchArtist: {timeSeqSearchArtist()}")

    # sort the music list
    bubbleSortArtist(music)
    printMusic(music)
    altSortArtist(music)
    printMusic(music)
    inSortTracks(music)
    printMusic(music)
    altSortTracks(music)
    printMusic(music)

    # time the functions
    timeBubbleSortArtist()
    timeAltSortArtist()
    timeInSortTracks()
    timeAltSortTracks()


if __name__ == '__main__':
    main()

# Comment on your time analysis of your sort and search operations.
# The binary search is faster than the sequential search because the binary search is O(log n) while the sequential
# search is O(n). The bubble sort is slower than the alternative sort because the bubble sort is O(n^2) while the
# alternative sort (quick sort) is O(n log n). The insertion sort is slower than the alternative sort (merge sort)
# because the insertion sort is O(n^2) while the alternative sort (merge sort) is O(n log n).
# Based on the time analysis, the binary search is better than the sequential search, quick sort is better than the
# bubble sort, and merge sort is better than the insertion sort.
# However, quick sort is not stable while the insertion sort is stable. Merge sort is stable, but it requires more
# memory than the insertion sort. Thus, it is not always the case that the alternative sort is better than the original
