#!/bin/bash
heroku git:remote -a voughzera
git subtree split --prefix vough_backend -b voughtree
git push -f heroku voughtree:master