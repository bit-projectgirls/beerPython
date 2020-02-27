import os
import cv2
import Oracle
# searchimg = cv2.imread('C:/image_test/wahoo_test.jpg', cv2.IMREAD_COLOR)
# findlist_x = {}
import cx_Oracle
import os
# Connection
def create_connection():
    dsn = cx_Oracle.makedsn("localhost", 1521, "orcl")
    db = cx_Oracle.connect("BGirls", "BGirls", dsn)
    return db

def connection_test():
    conn = create_connection()
    cursor = conn.cursor()
    print("CONN:", conn)
    sql = "SELECT * FROM searchDB"
    cursor.execute("SELECT * FROM searchDB")
    beer_row_list = []

    for row in cursor:
        beer_row_list.append(row)
    conn.close()

    return beer_row_list




def histogram(search_image_array):
    searchHLS = cv2.cvtColor(search_image_array, cv2.COLOR_BGR2HLS)
    searchhistogram = cv2.calcHist([searchHLS], [0], None, [256], [0, 256])
    findlist = {}

    beer_row_list = connection_test()

    for row in beer_row_list:
        IMAGE_DIR = "C:\image"
        full_fname =os.path.join(IMAGE_DIR, row[-1])
        beerNo = row[1]
        print(full_fname)
        imgNames = cv2.imread(full_fname)
        imgsHLS = cv2.cvtColor(imgNames, cv2.COLOR_BGR2HLS)
        # cv2.imshow('', imgsHLS)
        # cv2.waitKey(0)

        histogram = cv2.calcHist([imgsHLS], [0], None, [256], [0, 256])
        # print(histogram)

        matching_score = cv2.compareHist(histogram, searchhistogram, cv2.HISTCMP_CORREL)
        if (matching_score > 0.2):
            findlist[full_fname] = matching_score
            # print(findlist)
    findlist_x = sorted(findlist.items(), key=(lambda x: x[1]), reverse=True)
        # for k in findlist_x:
        #     print(k)
    return findlist_x


def matching(searchimg, findlist_x, beerNo):

    sift = cv2.xfeatures2d.SIFT_create()

    findlist = {}

    for fname in findlist_x:
        # print(fname)
        imgNames = cv2.imread(fname[0])

        kp1, des1 = sift.detectAndCompute(searchimg, None)
        kp2, des2 = sift.detectAndCompute(imgNames, None)

        bf = cv2.BFMatcher()
        matches = bf.knnMatch(des1, des2, k=2)
        good = []
        for m, n in matches:
            if m.distance < 0.75 * n.distance:
                good.append([m])

        img3 = cv2.drawMatchesKnn(searchimg, kp1, imgNames, kp2, good, None, flags=2)
        count = len(good)

        if (count > 0):
            findlist[fname] = count
            # print(count)
        findlist_x = sorted(findlist.items(), key=(lambda x: x[1]), reverse=True)
    print(findlist_x)
    return findlist_x
def make_list(findlist_x):
    beer_row_list = connection_test()
    for row in beer_row_list:
        beerNo = row[1]
        for beers in findlist_x:
            if (beerNo > 0):
                findlist_x[beers] = beerNo
    print(findlist_x)
    return findlist_x
    # for k in findlist_x:
    #     print(k)


# if __name__ == '__main__':
#     findlist_x = histogram(searchimg)
#     matching(searchimg, findlist_x)