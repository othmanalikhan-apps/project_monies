import unittest


if __name__ == '__main__':
    suite = unittest.TestSuite()
    unitLoader = unittest.TestLoader()
    systemLoader = unittest.TestLoader()

    suite.addTests(unitLoader.discover("unit"))
    suite.addTests(systemLoader.discover("system"))

    runner = unittest.TextTestRunner(verbosity=3)
    result = runner.run(suite)


