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
    - Nickname
    - Par
    - Course

Course
    - Name
    - Holes (9 or 18)
    - Tee Time Link
    - Website Link

CoreUser
    - First Name
    - Last Name
    - Email

Game
    - Date Played
    - Course
    - Holes Played

UserGameLink
    - CoreUser
    - Game

HoleScoreLink
    - UserGameLink
    - Hole
    - Score

