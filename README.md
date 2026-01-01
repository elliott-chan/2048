# 2048

1. Generate an initial board with a random number of '2's at random cells, e.g.:

    [ 2  ,null,  2 ,null],
    [null, 2  ,null, 2  ],
    [ 2  ,null,  2 ,null],
    [null, 2  ,null, 2  ]

2. Support *Move Left* on the board. E.g.:
Before:                                         After Move Left:
    [null, 8  , 2  , 2  ],                          [ 8  , 4  ,null,null],
    [ 4  , 2  ,null, 2  ],                          [ 4  ,null,null,null],
    [null,null,null,null],                          [null,null,null,null],
    [null,null,null, 2  ]                           [ 2  ,null,null,null]

3. Support *Move Right*. E.g.:
Before:                                         After Move Right:
    [null, 8  , 2  , 2  ],                          [null,null, 8  , 4  ],
    [ 4  , 2  ,null, 2  ],                          [null,null, 4  , 4  ],
    [null,null,null,null],                          [null,null,null,null],
    [null,null,null, 2  ]                           [null,null,null, 2  ]

4. Support *Move Up* and *Move Down*. E.g.:
Before:                                         After Merge Up:
    [null, 8  , 2  , 2  ],                          [ 4  , 8  , 2  , 4  ],
    [ 4  , 2  ,null, 2  ],                          [null, 2  ,null, 2  ],
    [null,null,null,null],                          [null,null,null,null],
    [null,null,null, 2  ]                           [null,null,null,null]

5. Generate a '2' or '4' at a random empty space after each valid move that changes the board. E.g:
Before:                                        After Move Up and adding a new 2 or 4:
    [null, 8  , 2  , 2  ],                          [ 4  , 8  , 2  , 4  ],
    [ 4  , 2  ,null, 2  ],                          [null, 2  ,null, 2  ],
    [null,null,null,null],                          [null,null,null,null],
    [null,null,null, 2  ]                           [ 2  ,null,null,null]

6. Determine endgame condition (Lose or Win). E.g.:
No more moves (Lose):                          Or, we've reached the goal of 2048 (Win):
    [ 2  , 4  , 2  , 4  ]                           [ 4  ,null,null, 2  ],
    [ 2  , 4  , 2  , 4  ],                          [2048,null,null,null],
    [ 4  , 2  , 4  , 2  ],                          [ 4  , 2  ,null,null],
    [ 2  , 4  , 2  , 4  ],                          [ 4  ,null,null,null]

7. AI Suggestion. During a gameplay, allow players to ask for the best possible move from an AI model to avoid gameover and 
   maximize the chance of winning the game. You can use an offline AI model or connect with a remote AI service. Please do not submit
   with any credentials.

Remarks:
- Any programming language is welcome.
- You may make reasonable assumptions and clearly state them if not explicitly mentioned.
- The goal is to create a well-structured, maintainable codebase. Don't overthink the task or worry about performance.
- A very basic user inferface would be appreciated. However, adding extra features will not earn additional credit.
- The requirements may deviate from the original 2048 game. Priority to given requirements.
