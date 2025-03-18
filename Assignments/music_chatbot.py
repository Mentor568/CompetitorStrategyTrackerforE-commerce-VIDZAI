import random

music_recommendations = {
    "happy": [
        "🎵 Happy by Pharrell Williams",
        "🎵 Good Vibes by Chris Janson",
        "🎵 Can't Stop the Feeling by Justin Timberlake",
        "🎵 Dynamite by BTS",
        "🎵 Dance Monkey by Tones and I"
    ],
    "sad": [
        "😔 Someone Like You by Adele",
        "😔 Let Her Go by Passenger",
        "😔 Jeene Bhi De by Arijit Singh",
        "😔 Fix You by Coldplay",
        "😔 Arcade by Duncan Laurence"
    ],
    "study": [
        "📚 Weightless by Marconi Union",
        "📚 Lofi Beats Playlist",
        "📚 Rainy Jazz by Various Artists",
        "📚 Chillhop Essentials by Chillhop Music",
        "📚 Soft Piano Melodies by Relaxing Music"
    ],
    "party": [
        "🎉 Uptown Funk by Bruno Mars",
        "🎉 Despacito by Luis Fonsi",
        "🎉 Shape of You by Ed Sheeran",
        "🎉 One Dance by Drake",
        "🎉 Levitating by Dua Lipa"
    ],
    "relax": [
        "🌊 Weightless by Marconi Union",
        "🌊 Ocean Sounds by Nature's Melody",
        "🌊 Meditation Flow by Calm Beats",
        "🌊 Ambient Forest Sounds by Relaxing Nature",
        "🌊 Spa Relaxation Music by Peaceful Sounds"
    ]
}

def get_music_recommendation(user_input):
    user_input = user_input.lower()

    for mood, songs in music_recommendations.items():
        if mood in user_input:
            return f"Here are some {mood}-themed songs you might like:\n\n" + "\n".join(songs)
    
   
    return "I couldn't find specific songs for that. Try asking for 'happy', 'sad', 'party', 'study', or 'relax' music!"
