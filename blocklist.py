#tHis file contain block list of jwt token.It is imported by the app and the logout resource so that the token can be added to blocked list
#when the user logout
#token will be treated as terminated as request will not go through
BLOCKLIST=set()

#note
#we are not using database to store blocklist,but recommend to use database to store blocklist