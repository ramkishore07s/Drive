# ITWS Project: Drive

## Team members:
* Ramkishore S
* Antony Martin

## Contents:
1. Implementation
2. Features

        1. Console Operations
        2. API
        3. Blogs (inspired from `<username>.github.io`)
        4. Shared files
3. Security
4. Installation and Running

## Implementation
* The backend is implemented as a State machine.
* We followed the MVC model.
* File system is used to store User files.

### Controllers
* Auth
* Main
* Shared

### Models
* User

### Views
* main
* login
* signup
* shared_files
* shared_folders
* blog

### Controllers
* forms used in controllers can be found in the `forms` folder, one file corresponding to each controller

#### Auth
* Used for user authentication(login, signup and logout).
* `Flask-Login` is used to manage all authentication tasks.
* `Flask-WTF` is used to manage forms.

#### Main
* Used for managing user files in the backend File System
* Provides wrappers for all user operations, so no user command(look at Console Operations under Features) is executed directly, but they are scrutenized and executed only if they are OK.
* Requires user authentication

#### Shared
* Used for accessing public files

### Models
#### User
* Used to store user data `id, email, username, password-hash`

### Views
#### Main
* For accessing User's data(files and folders),and provides functionalities like `create folder`, `change-folder`, `delete file/folder`, `upload file` etc.

#### Login
* For user login

#### Signup
* For user signup

#### Shared_files
* For displaying public files of particular user

#### Shared folders
* Displaying public component of every user

#### Blog
* Each user can upload a file `blog.html` to the root directory which will be served at `/blog/<user id>`
* Inspired by `<username>.github.io` feature in <a href='https://www.github.com'>GitHub</a>.
* Currently blogs only support inline styling and scripting, (cannot attach files)

## Features
### Console Operations
#### `cd()`
* `cd("<folder name>")` to change folders. Does not support paths, the folder must be in the current directory
* `cd(".")` to go to root directory of user
* `cd("..")` to go back, if performed from root folder, no change

#### `ls()`
* To list out files, filesizes and folders in the current directory

#### `delete_file("<filename>")`
* Deletes the given file/folder is it is present in the current directory
* Does not accept paths, wildcard expressions etc.

