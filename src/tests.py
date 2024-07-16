import unittest
import requests
from app import create_app, db

class TestBlogAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Users\\fengj\\Downloads\\sqlite-tools-win-x64-3460000\\blog.db'
        cls.app.config['TESTING'] = True
        cls.client = cls.app.test_client()

        with cls.app.app_context():
            db.create_all()

        cls.base_url = 'http://localhost:5000'
        cls.token = None
        cls.post_id = None

    @classmethod
    def tearDownClass(cls):
        with cls.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_01_create_user(self):
        url = self.base_url + '/signup'
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = requests.post(url, json=data)
        self.assertEqual(201, response.status_code)

    def test_02_login(self):
        url = self.base_url + '/login'
        response = requests.get(url, auth=('testuser', 'testpassword'))

        if response.status_code == 200:
            self.token = response.json().get('token')
            self.assertIsNotNone(self.token)
            self.assertEqual(200, response.status_code)
        else:
            self.fail(f"Failed to login: {response.status_code}")

    def test_03_create_post(self):
        self.test_02_login()

        url = self.base_url + '/blog'
        data = {'title': 'Test Post', 'content': 'This is a test post content.'}
        headers = {'Authorization': 'Bearer ' + self.token}

        response = requests.post(url, json=data, headers=headers)

        self.assertEqual(200, response.status_code, f"Failed to create post: {response.json()}")
        print(response.json())
        self.post_id = response.json().get('post', {}).get('id')
    def test_04_get_all_posts(self):
        url = self.base_url + '/blog'
        response = requests.get(url)

        self.assertEqual(200, response.status_code)
        self.assertTrue('posts' in response.json())

    def test_05_create_and_get_post(self):
        self.test_03_create_post()

        # Retrieve the created post
        created_post_id = self.get_created_post_id()
        url_get = f'{self.base_url}/blog/{created_post_id}'
        headers = {'Authorization': 'Bearer ' + self.token}
        response_get = requests.get(url_get, headers=headers)

        self.assertEqual(200, response_get.status_code)
        self.assertTrue('post' in response_get.json())
        post_data = response_get.json()['post']

        # Verify post data fields
        self.assertEqual(created_post_id, post_data['id'])
        self.assertEqual('Test Post', post_data['title'])
        self.assertEqual('This is a test post content.', post_data['content'])
        self.assertEqual('testuser', post_data['author'])

    def get_created_post_id(self):
        url = self.base_url + '/blog'
        response = requests.get(url)

        self.assertEqual(200, response.status_code)
        posts = response.json().get('posts', [])
        for post in posts:
            if post['title'] == 'Test Post' and post['content'] == 'This is a test post content.':
                return post['id']

        return None

    def test_06_update_post(self):
        self.test_03_create_post()

        # Update the created post
        url_update = f'{self.base_url}/blog/{self.post_id}'
        data_update = {'title': 'Updated Post Title', 'content': 'This is an updated post content.'}
        headers = {'Authorization': 'Bearer ' + self.token}

        response_update = requests.put(url_update, json=data_update, headers=headers)

        self.assertEqual(200, response_update.status_code, f"Failed to update post: {response_update.json()}")

        # Verify the updated post details
        url_get = f'{self.base_url}/blog/{self.post_id}'
        response_get = requests.get(url_get, headers=headers)
        self.assertEqual(200, response_get.status_code)

    def test_07_delete_post(self):
        self.test_03_create_post()

        # Delete the created post
        url_delete = f'{self.base_url}/blog/{self.post_id}'
        headers = {'Authorization': 'Bearer ' + self.token}

        response_delete = requests.delete(url_delete, headers=headers)

        self.assertEqual(200, response_delete.status_code, f"Failed to delete post: {response_delete.json()}")

        # Verify if the post has been deleted
        url_get = f'{self.base_url}/blog/{self.post_id}'
        response_get = requests.get(url_get)

        self.assertEqual(200, response_get.status_code)
        self.assertEqual('Post not found!', response_get.json().get('message'))

if __name__ == '__main__':
    unittest.main()

