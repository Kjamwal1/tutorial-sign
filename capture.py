import os
import cv2
import time
import uuid

# Configuration
IMAGE_PATH = 'CollectedImages'
labels = ['Hello', 'Yes', 'No', 'Thanks', 'ILoveYou', 'Please']
number_of_images = 20  # Images per label
capture_delay = 2      # Seconds between captures
warmup_time = 5        # Seconds for camera warmup

def create_folders():
    """Create folders for each label if they don't exist"""
    if not os.path.exists(IMAGE_PATH):
        os.makedirs(IMAGE_PATH)
    
    for label in labels:
        label_path = os.path.join(IMAGE_PATH, label)
        if not os.path.exists(label_path):
            os.makedirs(label_path)

def capture_images():
    """Capture images for each label"""
    create_folders()
    
    for label in labels:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print(f"Error: Could not open camera for {label}")
            continue
            
        print(f'Collecting images for {label}. Get ready...')
        
        # Camera warmup
        for _ in range(5):
            cap.read()
        time.sleep(warmup_time)
        
        print('Start posing... Press "q" to skip this label')
        
        count = 0
        while count < number_of_images:
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame")
                break
                
            # Display the frame with instructions
            display_frame = frame.copy()
            cv2.putText(display_frame, f"Label: {label}", (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(display_frame, f"Image: {count+1}/{number_of_images}", (10, 70), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow('Image Collection', display_frame)
            
            # Save the image
            imagename = os.path.join(IMAGE_PATH, label, f"{label}_{uuid.uuid1()}.jpg")
            cv2.imwrite(imagename, frame)
            print(f"Saved: {imagename}")
            count += 1
            
            # Wait for specified delay or quit
            start_time = time.time()
            while (time.time() - start_time) < capture_delay:
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    cap.release()
                    cv2.destroyAllWindows()
                    return
                
        cap.release()
        print(f"Completed collection for {label}\n")
        
        # Brief pause between labels
        if label != labels[-1]:
            print("Prepare for the next label in 5 seconds...")
            time.sleep(5)
    
    cv2.destroyAllWindows()
    print("Image collection completed for all labels!")

if __name__ == "__main__":
    capture_images()