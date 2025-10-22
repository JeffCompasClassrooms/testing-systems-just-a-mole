from mydb import MyDB
import pytest
import pickle
import os

def describe_test_mydb():

    @pytest.fixture(autouse=True, scope="session")
    def create_and_delete_database():
        if os.path.isfile("tedster.db"):
                os.remove("tedster.db")
        with open("tedster.db", 'wb') as f:
                pass

    def describe_init():
        def test_init_creates_empty_db():
              if os.path.isfile("tedster.db"):
                os.remove("tedster.db")

                assert(not os.path.isfile("tedster.db"))

                a_db = MyDB("tedster.db")
                
                assert(os.path.isfile("tedster.db"))

        def test_init_does_not_create_db():
            start_db = MyDB("tedster.db")
            start_db.saveString("test")

            a_db = MyDB("tedster.db")

            b_list = a_db.loadStrings()
    
            assert(os.path.isfile("tedster.db"))
            assert(["test"] == b_list)
            
            os.remove("tedster.db")

    def describe_load_strings():
        def test_loadstrings_returns_empty_array_when_empty():
              a_db = MyDB("tedster.db")
              assert(a_db.loadStrings() == [])

        def test_loadstrings_returns_saved_array():
            a_db = MyDB("tedster.db")
            a_db.saveString("Test")
            assert(a_db.loadStrings() == ["Test"])
            os.remove("tedster.db")
         
    def describe_save_strings():
        def test_savestrings_works_where_there_was_no_file():
        # setup
        # ensure that there is no tedster.db
            if os.path.isfile("tedster.db"):
                os.remove("tedster.db")

            a_db = MyDB("tedster.db")
            a_list = ['hi', 'test']

            # exercise
            a_db.saveStrings(a_list)

            # verify
            os.path.isfile("tedster.db")
            b_list = a_db.loadStrings()

            assert(a_list == b_list)

            # teardown
            os.remove("tedster.db")
        
        def test_savestrings_works_where_there_was_a_file():            
            os.path.isfile("tedster.db")

            a_db = MyDB("tedster.db")
            a_list = ['hi', 'test']

            a_db.saveStrings(a_list)
            
            os.path.isfile("tedster.db")
            b_list = a_db.loadStrings()

            assert(a_list == b_list)
            os.remove("tedster.db")

    def describe_save_string():
        def test_savestring_works_when_there_is_no_file():
            if os.path.isfile("tedster.db"):
                os.remove("tedster.db")

            a_db = MyDB("tedster.db")

            a_db.saveString("test")

            os.path.isfile("tedster.db")
            b_list = a_db.loadStrings()

            assert(["test"] == b_list)
            os.remove("tedster.db")

        def test_savestring_works_when_there_was_a_file():
            os.path.isfile("tedster.db")

            a_db = MyDB("tedster.db")
            

            a_db.saveString("test")
            
            os.path.isfile("tedster.db")
            b_list = a_db.loadStrings()

            assert(["test"] == b_list)
            os.remove("tedster.db")