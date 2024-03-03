# YOUTUBE 4 ME
# Thomas Fortoul - 3 Mar 2024

from pytube import YouTube, Search, Playlist, Channel

#searches the database for a particular video, can expand results.
def search_video():
    try:
        search_title = input(f"Enter the title of the video you want to search: ")
        s = Search(search_title)

        while True:
            # Display search results
            print("Search Results:")
            for i, result in enumerate(s.results, 1):
                print(f"{i}. {result.title} - {result.watch_url}")

            # Ask the user to choose a video
            while True:
                choice = input(f"Enter the number corresponding to the video you want to download, or 0 if not shown (or 'exit' to cancel): ")
                if choice.lower() == 'exit':
                    print("Search cancelled.")
                    return None
                elif choice.isdigit():
                    choice_index = int(choice) - 1
                    if 0 <= choice_index < len(s.results):
                        chosen_video_url = s.results[choice_index].watch_url
                        return chosen_video_url
                    elif choice_index == -1:
                        more_results = input("Would you like to see more or exit? (more/exit) ")
                        if more_results.lower() == 'more':
                            while True:
                                if more_results.lower() == 'more':
                                    s.get_next_results()
                                    for i, result in enumerate(s.results, 1):
                                        print(f"{i}. {result.title} - {result.watch_url}")
                                    more_results = input("Would you like to see more or exit? (more/exit) ")

                                elif more_results.lower() == 'exit':
                                    print("Search cancelled.")
                                    return
                                
                                else:
                                    more_results = input("Invalid input. Please enter 'more' or 'exit'.")

                        elif more_results.lower() == 'exit':
                            print("Search cancelled.")
                            return

                        else:
                            print("Invalid input. Please enter 'more' or 'exit'.")
                    else:
                        print("Invalid input. Please enter a valid number or 'exit' to cancel.")
                else:
                    print("Invalid input. Please enter a valid number or 'exit' to cancel.")
    except Exception as e:
        print("Error:", e)

def download_playlist():
    url = input('Please enter the playlist url.')
    try:
        playlist = Playlist(url)
    except Exception as e:
        print(f"Error, playlist not found: {e}")
        print("Returning to main menu")
        return
    
    download_multiple_videos(playlist)

def download_channel_videos():
    url = input('Please enter the channel url.')
    try:
        channel = Channel(url)
    except Exception as e:
        print(f"Error, playlist not found: {e}")
        print("Returning to main menu")
        return
    
    download_multiple_videos(channel)


def download_multiple_videos(obj):
    format = input('Would you like to download the video and audio, or just the audio? (both/audio)')
    while True:
        if(format not in ['audio', 'both']):
            format = input("Invalid input. Please type 'both' or 'audio'.")
            continue
        break
    
    for yt in obj.videos:
        print(f'Downloading {yt.title}.')
        try:
            if(format == 'audio'):
                yt.streams.filter(only_audio=True).first().download(f'./{obj.title}/')
            else:
                yt.streams.filter(progressive=True).get_highest_resolution().download(f'./{obj.title}/')

        except Exception as e:
            print(f'Error downloading {yt.title}. {e}. Continuing to next video.')
            continue

        print(f'Finished downlaoding {yt.title}.')
    
    print(f'Finished downloading {obj.title}. Find it at ./{obj.title}/')


# downloads a video / or audio to disk
def download_video():
    url = search_video()
    if(url == None):
        return 

    yt = YouTube(url)
    print("Video Title:", yt.title)

    try:
        yt.check_availability()
    except Exception as e:
        print(f'Encountered an error, cannot download: {e}.')
        return

    format = input('Would you like to download the video and audio, or just the audio? (both/audio)')
    while True:
        if(format == 'audio'):
            stream = yt.streams.filter(only_audio=True).first()
            break
        elif(format == 'both'):
            stream = yt.streams.filter(progressive=True).get_highest_resolution()
            break
        else:
            format = input("Invalid input. Please type 'both' or 'audio'.")
    
    # Download the video
    print("Starting video download.")
    path = stream.download('./downloads/')
    print(f"Video downloaded successfully at {path}.")

def get_channel_details():
    url = input('Please enter the channel url.')
    try:
        channel = Channel(url)
        print("Channel Details:")
        print("-" * 20)

        print(f"Title: {channel.title}")
        print(f"Description: {channel.description}")
        print(f"Subscriber Count: {channel.subscriber_count}")
        print(f"View Count: {channel.view_count}")
        print(f"Video Count: {channel.video_count}")
        print("-" * 20)
    except Exception as e:
        print("Error:", e)

def get_playlist_details():
    url = input('Please enter the playlist url.')
    try:
        playlist = Playlist(url)
        print("Playlist Details:")
        print("-" * 20)
        print(f"Title: {playlist.title}")
        print(f"Author: {playlist.author}")
        print(f"Description: {playlist.description}")
        print(f"Video Count: {len(playlist.video_urls)}")
    except Exception as e:
        print("Error:", e)

def get_video_details():
    url = search_video()
    try:
        yt = YouTube(url)
        print("Video Details:")
        print("-" * 20)
        print(f"Title: {yt.title}")
        print(f"Author: {yt.author}")
        print(f"Length: {yt.length} seconds")
        print(f"Views: {yt.views}")
        print(f"Rating: {yt.rating}")
    except Exception as e:
        print("Error:", e)

def show_menu(menu):
    for key, value in menu.items():
        print(f"{key}: {value}")
    print()

def main():
    overall_menu = {
        "1": {
            "Video": {
                "1": {"Download Video" : "Download Video"}, 
                "2": {"Get Video Details" : "Get Video Details"}
            }
        },

        "2": {
            "Playlist": {
                "1": {"Download Playlist" : "Download Playlist"}, 
                "2": {"Get Playlist Details" : "Get Playlist Details"}
            }
        },

        "3": {
            "Channel": {
                "1": {"Download Channel Videos" : "Download Channel Videos"}, 
                "2": {"Get Channel Details" : "Get Channel Details"}
            }
        }
    }
    current_menu = overall_menu

    while True:
        if(current_menu == overall_menu):
            print("Welcome to Pytube!")
        
        show_menu({k: list(v.keys())[0] for k, v in current_menu.items()})
        choice = input("Choose an option: ")


#Check if choice is within options, and is an integer (try except block)
        try:
            if(int(choice) > len(current_menu)):
                print(f"{choice} is not an option.")
                continue

        except Exception as e:
            print(f"{choice} is not an option.")
            continue

# Check if actionable item or another choice to make
        # Modify current menu
        current_menu = current_menu[choice]  # Get word value for chosen number choice.
        chosen_topic = list(current_menu.keys())[0]
        print(f'You have chosen {chosen_topic}. \n')
        current_menu = current_menu[chosen_topic]  # Go to next dictionary.
        
        if(type(current_menu) == str):
            function_name = current_menu.lower().replace(" ", "_")
            print(f'calling {function_name}')
            globals()[function_name]() # call function.
            print("Returning to main menu.")    
            current_menu = overall_menu # reset to main menu

if __name__ == "__main__":
    main()
