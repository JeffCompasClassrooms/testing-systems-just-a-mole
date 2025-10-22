import requests
import subprocess
import os
import pytest

server = subprocess.Popen(["python", "squirrel_server.py"])

def describe_test_squirrel_server():
    @pytest.fixture(autouse=True)
    def clear_database():
        os.system("cp empty_squirrel_db.db squirrel_db.db")
        yield
        os.system("cp empty_squirrel_db.db squirrel_db.db")

    def describe_get():
        def test_get_gets_empty_list_on_fresh_database():
            response = requests.get("http://127.0.0.1:8080/squirrels")
            assert(response.text == "[]")
        
        def test_get_gets_populated_list():
            squirrel = {
                "name": "Fluffy",
                "size": "large"
            }
            requests.post("http://127.0.0.1:8080/squirrels", data = squirrel)

            response = requests.get("http://127.0.0.1:8080/squirrels")
            assert(response.status_code == 200)
            assert(response.text == '[{"id": 1, "name": "Fluffy", "size": "large"}]')
        
        def test_get_returns_404_on_wrong_url():
            response = requests.get("http://127.0.0.1:8080/notsquirrel")
            assert(response.status_code == 404)

    def describe_retrieve():
        def test_retrieve_gets_squirrel():
            squirrel = {
                "name": "Fluffy",
                "size": "large"
            }
            requests.post("http://127.0.0.1:8080/squirrels", data = squirrel)

            response = requests.get("http://127.0.0.1:8080/squirrels/1")
            assert(response.status_code == 200)
            assert(response.text == '{"id": 1, "name": "Fluffy", "size": "large"}')
        
        def test_retrieve_gets_squirrel_from_multiple():
            squirrel1 = {
                "name": "Fluffy",
                "size": "large"
            }
            squirrel2 = {
                "name": "Fatty",
                "size": "small"
            }
            squirrel3 = {
                "name": "Stuffy",
                "size": "large"
            }
            requests.post("http://127.0.0.1:8080/squirrels", data = squirrel1)
            requests.post("http://127.0.0.1:8080/squirrels", data = squirrel2)
            requests.post("http://127.0.0.1:8080/squirrels", data = squirrel3)
            get = requests.get("http://127.0.0.1:8080/squirrels/2")

            assert(get.text == '{"id": 2, "name": "Fatty", "size": "small"}')

        def test_retrieve_returns_404_on_invalid_id():
            squirrel = {
                "name": "Fluffy",
                "size": "large"
            }
            requests.post("http://127.0.0.1:8080/squirrels", data = squirrel)

            response = requests.get("http://127.0.0.1:8080/squirrels/2")
            assert(response.status_code == 404)

    def describe_post():
        def test_post_creates_squirrel_on_empty_database():
            squirrel = {
                "name": "Fluffy",
                "size": "large"
            }
            response = requests.post("http://127.0.0.1:8080/squirrels", data = squirrel)
            get = requests.get("http://127.0.0.1:8080/squirrels")

            assert(response.status_code == 201)
            assert(get.text == '[{"id": 1, "name": "Fluffy", "size": "large"}]')
        
        def test_post_creates_squirrel_on_populated_database():
            squirrel1 = {
                "name": "Fluffy",
                "size": "large"
            }
            squirrel2 = {
                "name": "Fatty",
                "size": "small"
            }
            squirrel3 = {
                "name": "Stuffy",
                "size": "large"
            }
            requests.post("http://127.0.0.1:8080/squirrels", data = squirrel1)
            requests.post("http://127.0.0.1:8080/squirrels", data = squirrel2)
            requests.post("http://127.0.0.1:8080/squirrels", data = squirrel3)
            get = requests.get("http://127.0.0.1:8080/squirrels")

            assert(get.text == '[{"id": 1, "name": "Fluffy", "size": "large"}, {"id": 2, "name": "Fatty", "size": "small"}, {"id": 3, "name": "Stuffy", "size": "large"}]')

        def test_post_returns_404_on_bad_request():
            squirrel = {
                "name": "Fluffy",
                "size": "large"
            }
            response = requests.post("http://127.0.0.1:8080/badsquirrel", data = squirrel)

            assert(response.status_code == 404)

        def test_post_returns_404_on_bad_data():
            squirrel = {
                "notname": "Fluffy",
                "notsize": "medium"
            }
            response = requests.post("http://127.0.0.1:8080/squirrel", data = squirrel)
            assert(response.status_code == 404)
    
    def describe_replace():
        def test_replace_updates_squirrel():
            squirrel1 = {
                "name": "Fluffy",
                "size": "large"
            }
            squirrel2 = {
                "name": "Fatty",
                "size": "super large"
            }
            requests.post("http://127.0.0.1:8080/squirrels", data = squirrel1)
            response = requests.get("http://127.0.0.1:8080/squirrels/1")
            assert(response.text == '{"id": 1, "name": "Fluffy", "size": "large"}')

            requests.put("http://127.0.0.1:8080/squirrels/1", data = squirrel2)
            response = requests.get("http://127.0.0.1:8080/squirrels/1")

            assert(response.text == '{"id": 1, "name": "Fatty", "size": "super large"}')
        
        def test_replace_updates_squirrel_on_populated_database():
            squirrel1 = {
                "name": "Fluffy",
                "size": "large"
            }
            squirrel2 = {
                "name": "Fatty",
                "size": "small"
            }
            squirrel3 = {
                "name": "Stuffy",
                "size": "large"
            }
            requests.post("http://127.0.0.1:8080/squirrels", data = squirrel1)
            requests.post("http://127.0.0.1:8080/squirrels", data = squirrel2)
            requests.post("http://127.0.0.1:8080/squirrels", data = squirrel3)

            requests.put("http://127.0.0.1:8080/squirrels/1", data = squirrel2)
            requests.put("http://127.0.0.1:8080/squirrels/3", data = squirrel1)
            response = requests.get("http://127.0.0.1:8080/squirrels")

            assert(response.text == '[{"id": 1, "name": "Fatty", "size": "small"}, {"id": 2, "name": "Fatty", "size": "small"}, {"id": 3, "name": "Fluffy", "size": "large"}]')

        def test_replace_returns_404_on_bad_request():
            squirrel1 = {
                "name": "Fluffy",
                "size": "large"
            }
            squirrel2 = {
                "name": "Fatty",
                "size": "super large"
            }
            requests.post("http://127.0.0.1:8080/squirrels", data = squirrel1)
            response = requests.get("http://127.0.0.1:8080/squirrels/1")
            assert(response.text == '{"id": 1, "name": "Fluffy", "size": "large"}')

            requests.put("http://127.0.0.1:8080/squirrels/1", data = squirrel2)
            response = requests.get("http://127.0.0.1:8080/squirrels/5")

            assert(response.status_code == 404)
        
    def describe_delete():
        def test_delete_makes_an_empty_database():
            squirrel = {
            "name": "Fluffy",
            "size": "large"
            }
            requests.post("http://127.0.0.1:8080/squirrels", data = squirrel)
            response = requests.get("http://127.0.0.1:8080/squirrels")
            assert(response.text == '[{"id": 1, "name": "Fluffy", "size": "large"}]')

            requests.delete("http://127.0.0.1:8080/squirrels/1")
            response = requests.get("http://127.0.0.1:8080/squirrels")
            assert(response.text == '[]')

        def test_delete_removes_just_one_squirrel():
            squirrel1 = {
                "name": "Fluffy",
                "size": "large"
            }
            squirrel2 = {
                "name": "Fatty",
                "size": "super large"
            }

            requests.post("http://127.0.0.1:8080/squirrels", data = squirrel1)
            requests.post("http://127.0.0.1:8080/squirrels", data = squirrel2)
            response = requests.get("http://127.0.0.1:8080/squirrels")
            assert(response.text == '[{"id": 1, "name": "Fluffy", "size": "large"}, {"id": 2, "name": "Fatty", "size": "super large"}]')

            requests.delete("http://127.0.0.1:8080/squirrels/1")
            response = requests.get("http://127.0.0.1:8080/squirrels")
            assert(response.text == '[{"id": 2, "name": "Fatty", "size": "super large"}]')

            def test_delete_returns_404_on_bad_request():
                squirrel = {
                    "name": "Fluffy",
                    "size": "large"
                }
                requests.post("http://127.0.0.1:8080/squirrels", data = squirrel)

                response = requests.delete("http://127.0.0.1:8080/squirrels/10")
                assert(response.status_code == 404)
server.terminate()