# Network Web Development

![Python](https://img.shields.io/badge/Python-3.9-blue)
![Django](https://img.shields.io/badge/Django-3.2-green)

Network Web Development is a server-side web application that allows users to create, view, and interact with posts. It provides features such as creating new posts, viewing all posts, viewing user profiles, following users, and liking posts.

## Features

- **New Post:** Users who are signed in can create new text-based posts by filling in a text area and submitting the post.
- **All Posts:** The "All Posts" link displays all posts from all users, sorted by most recent. Each post includes the username of the poster, post content, post timestamp, and number of likes.
- **Profile Page:** Clicking on a username displays that user's profile page, showing the number of followers, number of people followed, and all posts in reverse chronological order. For other users, a "Follow" or "Unfollow" button is provided to toggle following.
- **Following:** The "Following" link displays posts made by users that the current user follows, similar to the "All Posts" page but with a limited set of posts.
- **Pagination:** Posts are paginated with 10 posts per page, with "Next" and "Previous" buttons for navigation.
- **Edit Post:** Users can edit their own posts by clicking an "Edit" button. The content of the post is replaced with a textarea for editing, and changes can be saved without reloading the entire page.
- **Like and Unlike:** Users can like or unlike posts with asynchronous updating of the like count on the page.

## Instructions

1. Clone the repository:

   ```bash
   git clone https://github.com/NohaGad/Network-Web-development.git

2. Navigate to the project directory:

   ```bash
   cd Network-Django

3. Run migrations:

   ```bash
   python manage.py migrate

4. Start the development server:

   ```bash
   python manage.py runserver

5. Access the application at `http://127.0.0.1:8000/`.


## Contributing
Contributions are welcome! If you find any issues or have suggestions for improvements, feel free to open an issue or submit a pull request.



