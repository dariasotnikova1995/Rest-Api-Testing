import requests
import json
import os
import pytest
import uuid

BASE_URL = "https://gorest.co.in/public/v2"
TOKEN = os.getenv("97868afed478b03b757ab4abd0024158060c4b905b6b0bb8e5fe6c8b7d940ca0")

if TOKEN is None:
    raise ValueError("97868afed478b03b757ab4abd0024158060c4b905b6b0bb8e5fe6c8b7d940ca0 environment variable not set")

print(f"Using token: {TOKEN}")

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

def create_user():
    unique_email = f"testuser{uuid.uuid4()}@example.com"
    user_data = {
        "name": "Test User",
        "gender": "male",
        "email": unique_email,
        "status": "active"
    }
    response = requests.post(f"{BASE_URL}/users", headers=HEADERS, data=json.dumps(user_data))
    if response.status_code != 201:
        print(f"Failed to create user: {response.json()}")
    return response.json()

def create_post(user_id, title, body):
    post_data = {
        "user_id": user_id,
        "title": title,
        "body": body
    }
    response = requests.post(f"{BASE_URL}/posts", headers=HEADERS, data=json.dumps(post_data))
    if response.status_code != 201:
        print(f"Failed to create post: {response.json()}")
    return response.json()

def delete_user(user_id):
    response = requests.delete(f"{BASE_URL}/users/{user_id}", headers=HEADERS)
    return response.status_code

def delete_post(post_id):
    response = requests.delete(f"{BASE_URL}/posts/{post_id}", headers=HEADERS)
    return response.status_code

def test_create_post():
    # Step 1: Create a user
    user = create_user()
    assert user.get("id") is not None, f"User creation failed: {user}"
    user_id = user["id"]
    print(f"User created with ID: {user_id}")

    # Step 2: Create a post
    post_title = "Test Post Title"
    post_body = "This is the body of the test post."
    post = create_post(user_id, post_title, post_body)
    assert post.get("id") is not None, f"Post creation failed: {post}"
    post_id = post["id"]
    print(f"Post created with ID: {post_id}")

    # Step 3: Verify the post was created
    assert post["title"] == post_title, "Post title does not match"
    assert post["body"] == post_body, "Post body does not match"
    assert post["user_id"] == user_id, "Post user ID does not match"
    print("Post creation verified")

    # Step 4: Clean up - Delete the created post and user
    post_deletion_status = delete_post(post_id)
    assert post_deletion_status == 204, "Post deletion failed"
    print(f"Post with ID {post_id} deleted")

    user_deletion_status = delete_user(user_id)
    assert user_deletion_status == 204, "User deletion failed"
    print(f"User with ID {user_id} deleted")

if __name__ == "__main__":
    pytest.main(["-s", __file__])
