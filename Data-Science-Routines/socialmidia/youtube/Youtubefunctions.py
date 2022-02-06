from youtube_transcript_api import  YouTubeTranscriptApi

# Funcao para download de legendas do Youtube
def getSubtitle(id, languages):
    video = YouTubeTranscriptApi.get_transcript(id, ['pt'])
    return video
