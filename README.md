# Golf Tracker App

## Features
- Ability to add a game and track scores for the group
- Course listing with contact info and tee time links
- Weather Info?


## Models
Tee
    - Name
    - Distance
    - Hole

Hole
    - Hole Number
    - Course

Course
    - Name
    - Holes
    - Tee Time Link
    - Website Link

CoreUser
    - First Name
    - Last Name

Game
    - Date Played
    - Course

UserGameLink
    - CoreUser
    - Game

HoleScoreLink
    - UserGameLink
    - Hole
    - Score

