A simple python chat program
============================
----
# Quick Summary
  1. This program is created to help teach Python to new programmers.
  1. This is not designed for security, but for teachability with the idea that it will evolve over time.
  1. Yes, we could use a declarative API spec (OpenAPI), but that doesn't teach Python, see above.

# Objectives
  1. Create quick Flask API
  1. API should support user registration (CRUD)
  1. API should support message passing (CRUD) between users
  1. API should use local file system storage only.
  1. API should run in a container.

# API Specification
## Registration API (`POST`: `/api/v1/register`)
### Purpose
  Allows a user to register their handle and get a UserId to post chat messages.
### Inputs
  ```json
    {
      "secret":<string>,
      "userHandle":<string>
    }
  ```
### Response
  * Success (`HTTP/200 OK`): 
    ```json
        {
          "userId": <int>,
          "authToken": "<string>"
        }
    ```
    Integer (userId, authToken).
  * Failure (`HTTP/400 BAD REQUEST`): your request is malformed.
  * Failure (`HTTP/401 UNAUTHORIZED`): no secret was found in the request
  * Failure (`HTTP/403 FORBIDDEN`): an invalid secret.
  * Failure (`HTTP/500 INTERNAL SERVER ERROR`): Unhandled exception.

### Operation:
  1. Parse request and sanitize the inputs.
     1. Is request body parsable JSON? No: return `HTTP/400`.
     1. Does `secret` exist? No: return `HTTP/401`.
     1. Is `secret` a non-empty string of 12-64 characters?  No: return `HTTP/401`.
     1. Does `userHandle` exist? No: Return `HTTP/400`.
     1. Is `userHandle` a non-empty string of 3-64 characters?  No: return `HTTP/400`.
  1. Open `<root>/users/secret.dat`
     1. Error: Return `HTTP/500`
  1. Read `<root>/users/secret.dat` contents.  Do contents match `secret` string?  No: Return `HTTP/403`
  1. Generate random string (`authToken`)
  1. Generate unique integer (`myId`) for the new user.
  1. Create file `<root>/users/<myId>.dat` and write `authToken` to the file.
  1. Generate sha256 hash of `userHandle` as `hashUserHandle`
  1. Create `<root>/users/<hashUserHandle>` and write `myId` to the file.
  1. Return `HTTP/200` and the JSON response:
     ```json
         {
          "userId": <int>,
          "authToken": "<string>"
         }
     ```

## Registration API (`GET`: `/api/v1/register`)
### Purpose
  Look up and return a user's id given their handle.

### Inputs
  ```json
      {
        "myId":<int>,
        "myAuth":"<string>",
        "userHandle":"<string>"
      }
  ```

### Response:
  * Success (`HTTP/200 OK`): Return JSON containing the other user's ID.
    ```json
        {
          "userId": <int>,
        }
    ```
  * Failure (`HTTP/400 BAD REQUEST`): your request is malformed.
  * Failure (`HTTP/401 UNAUTHORIZED`): no `myAuth` or `myId` was found in the request
  * Failure (`HTTP/403 FORBIDDEN`): an invalid `myId` and/or `myAuth` or you don't have permissions.
  * Failure (`HTTP/404 NOT FOUND`): empty (indicates user does not exist).
  * Failure (`HTTP/500 INTERNAL SERVER ERROR`): Unhandled exception.

### Operation:
  1. Parse request and sanitize the inputs.
     1. Is request body parsable JSON? No: return `HTTP/400`.
     1. Does `myId` exist? No: return `HTTP/400`.
     1. Is `myId` an integer? No: return `HTTP/400`.
     1. Does `myAuth` exist? No: return `HTTP/400`.
     1. Is `myAuth` a non-empty string of 12-64 characters?  No: return `HTTP/400`.
     1. Does `userHandle` exist? No: Return `HTTP/400`.
     1. Is `userHandle` a non-empty string of 3-64 characters?  No: return `HTTP/400`.
  1. Open `<root>/users/<myId>.dat`
     1. File not found error: Return `HTTP/401`.
     1. Other Error: return `HTTP/500`.
  1. Read `<myId>.dat` to obtain the user's authentication secret.
     1. Does `myAuth` match what is in the file?  No: return `HTTP/403`
  1. Generate a sha256 hash of `userHandle` as `hashUserHandle`
  1. Open `<root>/users/<hashUserHandle>.dat`
     1. File not found error: Return `HTTP/404` (user not found.)
     1. Other Error: return `HTTP/500`
  1. Read the file contents and return `HTTP/200` and the JSON body:
    ```json
        {
          "userId": <int>,
        }
    ```

## Message Passing (Chat) API (`POST`: `/api/v1/chat`)
### Purpose
 Publish a message to a recipient user's queue.

### Inputs
  ```json
      {
        "myId":<int>,
        "myAuth":"<string>",
        "userHandle":"<string>"
      }
  ```

### Response:
* Success (`HTTP/200 OK`): Return JSON containing the other user's ID.
  ```json
      {
        "userId": <int>,
      }
  ```
* Failure (`HTTP/400 BAD REQUEST`): your request is malformed.
* Failure (`HTTP/401 UNAUTHORIZED`): no `myAuth` or `myId` was found in the request
* Failure (`HTTP/403 FORBIDDEN`): an invalid `myId` and/or `myAuth` or you don't have permissions.
* Failure (`HTTP/404 NOT FOUND`): empty (indicates user does not exist).
* Failure (`HTTP/500 INTERNAL SERVER ERROR`): Unhandled exception.

### Operation:
1. Parse request and sanitize the inputs.
   1. Is request body parsable JSON? No: return `HTTP/400`.
   1. Does `myId` exist? No: return `HTTP/400`.
   1. Is `myId` an integer? No: return `HTTP/400`.
   1. Does `myAuth` exist? No: return `HTTP/400`.
   1. Is `myAuth` a non-empty string of 12-64 characters?  No: return `HTTP/400`.
   1. Does `userHandle` exist? No: Return `HTTP/400`.
   1. Is `userHandle` a non-empty string of 3-64 characters?  No: return `HTTP/400`.
1. Open `<root>/users/<myId>.dat`
   1. File not found error: Return `HTTP/401`.
   1. Other Error: return `HTTP/500`.
1. Read `<myId>.dat` to obtain the user's authentication secret.
   1. Does `myAuth` match what is in the file?  No: return `HTTP/403`
1. Generate a sha256 hash of `userHandle` as `hashUserHandle`
1. Open `<root>/users/<hashUserHandle>.dat`
   1. File not found error: Return `HTTP/404` (user not found.)
   1. Other Error: return `HTTP/500`
1. Read the file contents and return `HTTP/200` and the JSON body:
   ```json
   {
   "userId": <int>,
   }
   ```

## Message Passing (Chat) API (`GET`: `/api/v1/chat`)
### Purpose
  Fetch the messages in a given user's queue

### Inputs
  ```json
      {
        "myId":<int>,
        "myAuth":"<string>"
      }
  ```

### Response:
* Success (`HTTP/200 OK`): Return JSON containing the other user's ID.
  ```json
      {
        "myId": <int>,
        
      }
  ```
* Failure (`HTTP/400 BAD REQUEST`): your request is malformed.
* Failure (`HTTP/401 UNAUTHORIZED`): no `myAuth` or `myId` was found in the request
* Failure (`HTTP/403 FORBIDDEN`): an invalid `myId` and/or `myAuth` or you don't have permissions.
* Failure (`HTTP/404 NOT FOUND`): empty (indicates user does not exist).
* Failure (`HTTP/500 INTERNAL SERVER ERROR`): Unhandled exception.

### Operation:
1. Parse request and sanitize the inputs.
    1. Is request body parsable JSON? No: return `HTTP/400`.
    1. Does `myId` exist? No: return `HTTP/400`.
    1. Is `myId` an integer? No: return `HTTP/400`.
    1. Does `myAuth` exist? No: return `HTTP/400`.
    1. Is `myAuth` a non-empty string of 12-64 characters?  No: return `HTTP/400`.
    1. Does `userHandle` exist? No: Return `HTTP/400`.
    1. Is `userHandle` a non-empty string of 3-64 characters?  No: return `HTTP/400`.
1. Open `<root>/users/<myId>.dat`
    1. File not found error: Return `HTTP/401`.
    1. Other Error: return `HTTP/500`.
1. Read `<myId>.dat` to obtain the user's authentication secret.
    1. Does `myAuth` match what is in the file?  No: return `HTTP/403`
1. Generate a sha256 hash of `userHandle` as `hashUserHandle`
1. Open `<root>/users/<hashUserHandle>.dat`
    1. File not found error: Return `HTTP/404` (user not found.)
    1. Other Error: return `HTTP/500`
1. Read the file contents and return `HTTP/200` and the JSON body:
   ```json
   {
   "userId": <int>,
   }
   ```



# Setup, Build and Deploy
* TBD