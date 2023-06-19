import os
import moviepy.editor as mp
import cv2
import tqdm


def save_mp4(paths):
    for path, save_path in paths:

        # Iterate over each folder in the path
        for folder_name in os.listdir(path):
            folder_path = os.path.join(path, folder_name)
            
            # Create a list to store the file paths of the .png files
            png_files = []
            
            # Iterate over each file in the folder
            for file_name in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file_name)
                
                # Check if the file is a .png file
                if file_path.lower().endswith(".png"):
                    png_files.append(file_path)
            
            # Sort the .png files by name
            png_files.sort()
            
            # Create an output .mp4 file name based on the folder name
            output_file = os.path.join(save_path, f"{folder_name}.mp4")
            
            # Create a VideoWriter object
            frame_rate = 30  # Adjust the frame rate as desired
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # Codec for .mp4 file
            video_writer = cv2.VideoWriter(output_file, fourcc, frame_rate, (256, 256))  # Adjust the frame size as desired
            
            # Iterate over the .png files and write them to the video
            for png_file in tqdm.tqdm(png_files):
                frame = cv2.imread(png_file)
                video_writer.write(frame)
            
            # Release the VideoWriter object
            video_writer.release()

    print("Video creation completed.")




def split_videos(paths):
    for path in paths:
        # Iterate over each file in the path
        for file_name in tqdm.tqdm(os.listdir(path)):
            file_path = os.path.join(path, file_name)

            # Check if the file is an mp4 video
            if file_path.lower().endswith(".mp4"):
                # Load the video file
                video = mp.VideoFileClip(file_path)

                # Check if the video duration is greater than 5 seconds
                if video.duration > 5:
                    # Calculate the number of splits required
                    num_splits = int(video.duration / 5)

                    # Split the video into 5-second segments
                    for i in range(num_splits):
                        start_time = i * 5
                        end_time = (i + 1) * 5

                        # Extract the segment
                        segment = video.subclip(start_time, end_time)

                        # Resize the segment to 256x256 resolution
                        segment = segment.resize((256, 256))

                        # Set the frame rate to 30 fps
                        segment = segment.set_fps(30)

                        # Save the segment with a unique filename
                        segment_filename = os.path.join(path, f"{file_name}_{i}.mp4")
                        segment.write_videofile(segment_filename, codec="libx264")

                    # Delete the original long file
                    os.remove(file_path)

        print("Video splitting completed.")


if __name__ == '__main__':
    
    # Provide the folder path as an argument
    #paths = [("./data/sadeghi-modi/train/", "./data/sadeghi-modi-mp4/train"), ("./data/sadeghi-modi/test/", "./data/sadeghi-modi-mp4/test")]
    # save_mp4(paths)
    path = ["data/sadeghi-modi-mp4/train/", 'data/sadeghi-modi-mp4/test/']
    split_videos(path)