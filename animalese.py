import wave, os, math, sys, random, string, re
from pydub import AudioSegment
from pydub.playback import play

TEMP_FILE_NAME = "temp.wav"
letter_graphs = [
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k",
    "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v",
    "w", "x", "y", "z", "0", "1", "2", "3", "4", "5", "6",
    "7", "8", "9"
]

digraphs = [
    "ch", "sh", "ph", "th", "wh"
]

bebebese = "bebebese_slow"

def build_sentence(sentence):
    sentence_wav = AudioSegment.empty()
    sentence = sentence.lower()
    sentence = replace_swear_words(sentence)
    sentence = replace_parentheses(sentence)
    i = 0
    while (i < len(sentence)):
        char = None
        if (i < len(sentence)-1) and ((sentence[i] + sentence[i+1]) in digraphs):
            char = sentence[i] + sentence[i+1]
            i+=1
        elif sentence[i] in letter_graphs:
            char = sentence[i]
        elif sentence[i] in string.punctuation:
            char = bebebese
        i+=1

        if char != None:
            new_segment = AudioSegment.from_wav("letters/{}.wav".format(char))
            sentence_wav += new_segment

    return sentence_wav

def replace_swear_words(sentence):
    swear_words = ["fuck", "shit", "piss", "crap", "bugger"]
    for word in swear_words:
        sentence = sentence.replace(word, "*"*len(word))
    return sentence
    

def replace_parentheses(sentence):
    while "(" in sentence or ")" in sentence:
        start = sentence.index("(")
        end = sentence.index(")")
        sentence = sentence[:start] + "*"*(end-start) + sentence[end+1:]

    return sentence

def change_playback_speed(sound, speed_change):
    sound_with_altered_frame_rate = sound._spawn(sound.raw_data, overrides={
        "frame_rate": int(sound.frame_rate * speed_change)
    })
    return sound_with_altered_frame_rate.set_frame_rate(sound.frame_rate)

def build_and_say_sentence(sentence):
    sound = build_sentence(sentence)
    sound = change_playback_speed(sound, random.uniform(1.75,2.5))
    play(sound)
    return sound

def build_and_say_sentence_with_voice(sentence, voice):
    sound = build_sentence(sentence)
    sound = change_playback_speed(sound, voice)
    play(sound)
    return sound

if len(sys.argv) > 1:
    sentence = sys.argv[1]
else:
    sentence = "Gib me ur FEETS!"
pitch_shift = 2
sound = build_and_say_sentence_with_voice(sentence, pitch_shift)
sound.export("output.wav", format="wav")