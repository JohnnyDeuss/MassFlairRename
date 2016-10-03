"""
	Removes all comments under a given threshold after replying to them.

	Fix requested by /u/Dark_Saint.
	https://www.reddit.com/r/RequestABot/comments/54sd3i/fix_comment_bot/
	https://www.reddit.com/r/redditdev/comments/54syiw/question_deleted_comments/
"""
import praw
import OAuth2Util
from time import sleep

#
# Configuration
#
SUBREDDIT = "BitwiseShiftTest"		# Subreddit name, without the /r/ part.
# Reply given to deleted comments. Set to an empty string '' to not reply at all.
REMOVE_MESSAGE = "Wow, your score is low!"
THRESHOLD = -2
TIME_BETWEEN_RUNS = 30		# In number of seconds, the minimum is 30 seconds

#
# Actual bot
#
r = praw.Reddit('Python:DownvotedCommentRemover')
o = OAuth2Util.OAuth2Util(r)
o.refresh(force=True)

print("Grabbing subreddit...")
subreddit = r.get_subreddit(SUBREDDIT)

def run_bot():
	print("Start bot run")
	print("Grabbing comments...")
	comments = list(subreddit.get_comments(limit=100))
	for comment in comments:
		if comment.score < THRESHOLD and comment.banned_by == None:
			print("Match found! Comment ID: " + comment.id)
			comment.reply(REPLY_MESSAGE)
			print("Reply to deleted comment succesful!")
			comment.remove()
			print("Comment has been deleted")
	print("End bot run")

while True:
	run_bot()
	sleep(max(30, TIME_BETWEEN_RUNS))
