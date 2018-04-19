from finalproj import *
import unittest



class GetDataTests(unittest.TestCase):
    def testYelpGetData(self):
        table()
        g_id = getgoogledata("48104")
        y_data = getyelpdata(g_id)
        self.assertEqual(type(y_data), list)
        self.assertEqual(type(y_data[8]), dict)
        self.assertTrue("price" in y_data[5])
        self.assertTrue("name" in y_data[67])
        self.assertTrue(len(y_data) > 90)

    def testGoogleGetData(self):
        table()
        g_id = getgoogledata("48104")
        self.assertTrue(type(g_id), int)
        statement1 = "SELECT lat,lng FROM Google WHERE zipcode = ?"
        cur.execute(statement1, ("48104",))
        lat,lng = cur.fetchone()
        self.assertTrue(type(lat), float)
        self.assertTrue(type(lng), float)

class StoreDataTests(unittest.TestCase):
    def testyelpdb(self):
        table()
        g_id = getgoogledata("48104")
        y_data = getyelpdata(g_id)
        statement = "SELECT * FROM Yelp"
        cur.execute(statement)
        results = cur.fetchall()
        self.assertEqual(len(results), 100)
        self.assertTrue(type(results), list)
        self.assertEqual(type(results[0][0]), str)
        self.assertEqual(type(results[0][1]), float)
        self.assertEqual(type(results[0][2]), float)
        self.assertTrue(results[0][1] > 0 and results[0][1] <= 5)

    def testgoogledb(self):
        table()
        g_id = getgoogledata("48104")
        statement = "SELECT * FROM Google"
        cur.execute(statement)
        results = cur.fetchall()
        self.assertTrue(type(results), list)
        self.assertEqual(len(results[0]), 6)
        self.assertTrue(results[0][0].isnumeric())


class ProcessDataTests(unittest.TestCase):
    def testvisualization1(self):
        table()
        g_id = getgoogledata("48104")
        y_data = getyelpdata(g_id)
        results = getdistance(g_id, showViz = False)
        self.assertTrue(type(results), list)
        for x in results:
            self.assertEqual(type(x), float)
        self.assertTrue(len(results) > 10)


    def testvisualization2(self):
        table()
        g_id = getgoogledata("48104")
        y_data = getyelpdata(g_id)
        results = getprice(g_id, showViz = False)
        self.assertTrue(type(results), list)
        for x in results:
            self.assertTrue(x <= 4)


    def testvisualization3(self):
        table()
        g_id = getgoogledata("48104")
        y_data = getyelpdata(g_id)
        results =  category(g_id, showViz = False)
        self.assertTrue(type(results), dict)
        self.assertTrue(len(results.keys()) > 10)
        self.assertTrue("Sandwiches" in results)


    def testvisualization4(self):
        table()
        g_id = getgoogledata("48104")
        y_data = getyelpdata(g_id)
        results =  groupedbar(g_id, showViz = False)
        self.assertTrue(type(results), list)
        for sublist in results:
            self.assertTrue(type(sublist), list)







unittest.main()
