# Conduit Real Wolrd Example
- Base repo:
    - https://github.com/gothinkster/django-realworld-example-app


## Project models
- User
    - Sex: Optional
- Article
    - title: maximum length is 100
    - description: maximum 100
    - tags: unlimited number of Tag class can be added
    - can be liked
    - can be shared
    - can be commented
    - can be updated
    - can save the article into archive
- Tag
    - ManyToMany field with Article model
    - title: maximum length is 50
- Comment
    - ManyToOne(ForeignKey) filed with User
    - can be liked
    - can be commented by everyone
    - authenticaiton is required
    - can be updated
    - can be deleted
- Profile
    - OneToOne field with user class
    - Automatically created at the User registration
    - Automatically deleted when a user delete his/her account
    - can be followed
    - can be unfollowed

## Authentication
- JWT is used